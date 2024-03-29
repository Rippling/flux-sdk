import contextlib
import csv
import logging
from datetime import datetime
from decimal import ROUND_HALF_UP, Decimal
from enum import Enum
from io import IOBase, StringIO
from typing import Any, Optional, Union

from flux_sdk.flux_core.data_models import (
    ContributionType,
    DeductionType,
    Employee,
    File,
)
from flux_sdk.pension.capabilities.report_payroll_contributions.data_models import (
    EmployeePayrollRecord,
    PayrollRunContribution,
    PayrollUploadSettings,
)
from flux_sdk.pension.capabilities.update_deduction_elections.data_models import (
    EmployeeDeductionSetting,
)

logger = logging.getLogger(__name__)

COLUMNS_180 = [
    "SOCIAL SECURITY",
    "LAST NAME",
    "FIRST NAME",
    "MI",
    "DIVISIONAL CODE",
    "TOTAL COMPENSATION",
    "EMPLOYEE 401(K)",
    "ROTH 401(K)",
    "LOAN PAYMENT AMOUNT",
    "MATCH",
    "PROFIT SHARING",
    "SAFE HARBOR MATCH",
    "SAFE HARBOR NEC",
    "CLIENT SPECIFIC",
    "CLIENT SPECIFIC",
    "CLIENT SPECIFIC",
    "HOURS",
    "ADDRESS 1",
    "ADDRESS 2",
    "CITY",
    "STATE",
    "ZIP",
    "DATE OF BIRTH",
    "CURRENT DATE OF HIRE",
    "EMPLOYEE ELIGIBILITY DATE",
    "CURRENT DATE OF TERM",
    "PRIOR DATE OF HIRE",
    "PRIOR DATE OF TERM",
    "ESTIMATED ANNUAL COMPENSATION",
    "EMPLOYMENT STATUS",
    "HCE CODE",
    "KEY EE CODE",
    "ENROLLMENT ELIGIBILITY",
    "UNION STATUS CODE",
    "EMPLOYEE WORK EMAIL",
]

COLUMNS_360 = [
    "RecordType",
    "PlanId",
    "EmployeeLastName",
    "EmployeeFirstName",
    "EmployeeMiddleInitial",
    "EmployeeSSN",
    "EffectiveDate",
    "ContributionCode",
    "DeferralPercent",
    "DeferralAmount",
    "EmployeeEligibilityDate",
    "LoanNumber",
    "LoanPaymentAmount",
    "TotalLoanAmount",
]

STANDARD_DATE_FORMAT = "%m/%d/%Y"
TWO_PLACES = Decimal(".01")


class AscensusSettingsKeys(Enum):
    CLIENT_ID = "client_id"
    COMPANY_CONTRIBUTION_COLUMN = "company_contribution_column"
    FREQUENCY_OR_PAY_TYPE = "frequency_or_pay_type"
    EXCLUDE_SEVERANCE = "EXCLUDE_SEVERANCE"
    EXCLUDE_IMPUTED_INCOME = "EXCLUDE_IMPUTED_INCOME"
    EXCLUDE_BONUS = "EXCLUDE_BONUS"
    SITE_CODE_MAPPING = "site_code_mapping"
    FEIN_SETTINGS = "feins"


class ReportPayrollContributionsAscensusUtil:
    """
    This class embodies the functionality to "report payroll contributions" for vendors utilizing
    the Ascensus formatted file.
    Developers are required to implement the format_contributions_for_ascensus_vendor method in their code.
    For further details regarding their implementation details, check their documentation.
    """

    @staticmethod
    def get_formatted_ssn(ssn: str) -> str:
        return ssn[:3] + "-" + ssn[3:5] + "-" + ssn[5:]

    @staticmethod
    def to_bytes(content: str | bytes) -> bytes:
        return content.encode() if isinstance(content, str) else content

    @staticmethod
    def get_amount_from_payroll_contribution(
        payroll_contribution: PayrollRunContribution | None,
    ):
        if payroll_contribution is None:
            return Decimal("0.00")
        return payroll_contribution.amount.quantize(TWO_PLACES, ROUND_HALF_UP)

    @staticmethod
    def get_file_name(payroll_upload_settings: PayrollUploadSettings) -> str:
        """
        Receives a PayrollUploadSettings from which the developer
        is expected to return file name based on payroll_upload_settings
        :param payroll_upload_settings:
        :return: str
        """
        customer_partner_settings = payroll_upload_settings.customer_partner_settings
        environment = customer_partner_settings.get("env", "TS")
        client_id = str(customer_partner_settings[AscensusSettingsKeys.CLIENT_ID.value])
        payroll_run_id = payroll_upload_settings.payrun_info.payroll_run_id

        if not environment or not client_id:
            missing_attrs: list[str] = []
            missing_attrs.extend("Environment") if not environment else ""
            missing_attrs.extend("Client ID") if not client_id else ""
            raise RuntimeError(f"{', '.join(missing_attrs)} must be present to upload file")
        timestamp = datetime.now()
        format_timestamp = timestamp.strftime("%m%d%Y.%H%M%S")
        return f"{environment}_{client_id}_{payroll_run_id}_{format_timestamp}.csv"

    @staticmethod
    def get_fein_settings(ein: str, customer_update_settings: dict) -> dict:
        fein_peps = customer_update_settings.get("feins", {})
        fein_settings = fein_peps.get(ein, {})
        return fein_settings

    @staticmethod
    def get_total_compensation(
        employee_payroll_record: EmployeePayrollRecord, customer_update_settings: dict
    ) -> Decimal:
        compensation: Decimal = getattr(employee_payroll_record, "gross_pay", Decimal(0))
        exclude_severance = customer_update_settings.get(AscensusSettingsKeys.EXCLUDE_SEVERANCE.value, False)
        exclude_bonus = customer_update_settings.get(AscensusSettingsKeys.EXCLUDE_BONUS.value, False)
        exclude_imputed_income = customer_update_settings.get(AscensusSettingsKeys.EXCLUDE_IMPUTED_INCOME.value, False)

        if exclude_severance is True:
            compensation -= getattr(employee_payroll_record, "severance", Decimal(0))

        if exclude_bonus is True:
            compensation -= getattr(employee_payroll_record, "bonus", Decimal(0))

        if exclude_imputed_income is True:
            compensation -= getattr(employee_payroll_record, "imputed_pay", Decimal(0))

        return round(compensation, 2)

    @staticmethod
    def get_index_of_current_payroll_run(
        payroll_upload_settings: PayrollUploadSettings,
    ) -> int:
        current_month_payroll_runs = getattr(payroll_upload_settings, "current_month_payruns", [])
        check_date = getattr(payroll_upload_settings.payrun_info, "check_date", None)
        current_payroll_run_id = payroll_upload_settings.payrun_info.payroll_run_id
        sorted_payroll_run_ids = sorted(
            [
                payroll_run.payroll_run_id
                for payroll_run in current_month_payroll_runs
                if payroll_run.check_date == check_date
            ]
        )
        return sorted_payroll_run_ids.index(current_payroll_run_id)

    @staticmethod
    def _get_fein_site_code(fein_settings: dict, pay_frequency: str | None, pay_type: str | None) -> str | None:
        fein_site_code_frequency_mapping_key = (
            f"fein_site_code_mapping_for_{pay_frequency.lower()}" if pay_frequency else None
        )
        fein_site_code_pay_type_mapping_key = f"fein_site_code_mapping_for_{pay_type.lower()}" if pay_type else None
        if fein_site_code_frequency_mapping_key and fein_site_code_frequency_mapping_key in fein_settings:
            return fein_settings[fein_site_code_frequency_mapping_key]
        if fein_site_code_pay_type_mapping_key and fein_site_code_pay_type_mapping_key in fein_settings:
            return fein_settings[fein_site_code_pay_type_mapping_key]

        return fein_settings.get("fein_site_code", None)

    @staticmethod
    def _get_default_site_code(
        preference_type: str,
        customer_partner_settings: dict,
        pay_frequency: str | None,
        pay_type: str | None,
    ) -> str:
        site_code_frequency_mapping_key = f"site_code_mapping_for_{pay_frequency.lower()}" if pay_frequency else None
        site_code_pay_type_mapping_key = f"site_code_mapping_for_{pay_type.lower()}" if pay_type else None
        if site_code_frequency_mapping_key and site_code_frequency_mapping_key in customer_partner_settings:
            return customer_partner_settings[site_code_frequency_mapping_key]
        if site_code_pay_type_mapping_key and site_code_pay_type_mapping_key in customer_partner_settings:
            return customer_partner_settings[site_code_pay_type_mapping_key]

        site_code = customer_partner_settings.get(f"site_code_{preference_type.lower()}", "A")
        return site_code

    @staticmethod
    def _get_preference_type_site_code(
        preference_type: str, fein_settings: dict, customer_partner_settings: dict
    ) -> str:
        fein_site_code = fein_settings.get("fein_site_code", None)
        if fein_site_code:
            return fein_site_code
        return customer_partner_settings.get(f"site_code_{preference_type.lower()}", "A")

    @staticmethod
    def get_site_code(
        fein_settings: dict,
        payroll_update_settings: PayrollUploadSettings,
        no_of_salaried_roles: int,
        no_of_hourly_roles: int,
    ) -> str:
        """
        This method is used to get the site code for the given payroll run
        If pay_type and pay_frequency is None tries to fetch site_code from fein_settings
            and fallbacks to default site code if site code not in fein setting not present
        Else tries to fetch it from fein settings for preferable pay/frequency else default fien site code
        Else tries to fetch it from customer_partner_settings for preferable pay/frequency else default site code
        :param fein_settings:
        :param payroll_update_settings:
        :param no_of_salaried_roles:
        :param no_of_hourly_roles:
        :return:
        """
        customer_partner_settings = payroll_update_settings.customer_partner_settings
        preference_type = customer_partner_settings.get(AscensusSettingsKeys.FREQUENCY_OR_PAY_TYPE.value, "FREQUENCY")
        pay_frequency = pay_type = None
        if preference_type == "FREQUENCY":
            pay_frequency = getattr(payroll_update_settings.payrun_info, "pay_frequency", None)
        else:
            pay_type = "SALARIED" if no_of_salaried_roles >= no_of_hourly_roles else "HOURLY"

        if pay_frequency is None and pay_type is None:
            return ReportPayrollContributionsAscensusUtil._get_preference_type_site_code(
                preference_type, fein_settings, customer_partner_settings
            )

        fein_site_code = ReportPayrollContributionsAscensusUtil._get_fein_site_code(
            fein_settings, pay_frequency, pay_type
        )
        if fein_site_code:
            return fein_site_code

        return ReportPayrollContributionsAscensusUtil._get_default_site_code(
            preference_type, customer_partner_settings, pay_frequency, pay_type
        )

    @staticmethod
    def format_contributions_for_ascensus_vendor(
        employee_payroll_records: list[EmployeePayrollRecord],
        payroll_upload_settings: PayrollUploadSettings,
    ) -> File:
        """
        Given a list of EmployeePayrollRecord and the PayrollUploadSettings, prepare a file for upload to the pension
        provider.  The file will be sent verbatim, so any compression or other formatting required by the pension
        provider must be applied within this function.
        :param employee_payroll_records:
        :param payroll_upload_settings:
        :return: File
        """
        no_of_hourly_roles = no_of_salaried_roles = 0
        with contextlib.closing(StringIO()) as output:
            writer = csv.DictWriter(output, fieldnames=COLUMNS_180)
            writer.writeheader()
            for employee_payroll_record in employee_payroll_records:
                employee: Employee = employee_payroll_record.employee
                ssn = ReportPayrollContributionsAscensusUtil.get_formatted_ssn(employee.ssn)
                payroll_contributions: list[PayrollRunContribution] = employee_payroll_record.payroll_contributions
                payroll_contribution_map = {pc.deduction_type.name: pc for pc in payroll_contributions}
                if employee.is_salaried:
                    no_of_salaried_roles = no_of_salaried_roles + 1
                elif employee.is_hourly:
                    no_of_hourly_roles = no_of_hourly_roles + 1

                try:
                    employee_first_name = employee.first_name
                    employee_last_name = employee.last_name
                    address_line_1 = employee.address.address_line_1
                    address_line_2 = employee.address.address_line_2
                    zip_code = employee.address.zip_code
                    city = employee.address.city
                    state = employee.address.state
                    work_email = employee.business_email
                    employee_dob = employee.dob.strftime(STANDARD_DATE_FORMAT)

                    current_date_of_hire = employee.start_date.strftime(STANDARD_DATE_FORMAT)
                    current_date_of_term = getattr(employee, "termination_date", None)
                    current_date_of_term = (
                        current_date_of_term.strftime(STANDARD_DATE_FORMAT) if current_date_of_term else ""
                    )

                    payroll_employee_contribution_401k: Decimal = (
                        ReportPayrollContributionsAscensusUtil.get_amount_from_payroll_contribution(
                            payroll_contribution_map.get(ContributionType._401K.name, None)
                        )
                    )
                    payroll_company_match_contribution: Decimal = (
                        ReportPayrollContributionsAscensusUtil.get_amount_from_payroll_contribution(
                            payroll_contribution_map.get(ContributionType.COMPANY_MATCH.name, None)
                        )
                    )
                    payroll_employee_loan_repayment: Decimal = (
                        ReportPayrollContributionsAscensusUtil.get_amount_from_payroll_contribution(
                            payroll_contribution_map.get(ContributionType.LOAN.name, None)
                        )
                    )
                    payroll_employee_roth_401k: Decimal = (
                        ReportPayrollContributionsAscensusUtil.get_amount_from_payroll_contribution(
                            payroll_contribution_map.get(ContributionType.ROTH.name, None)
                        )
                    )

                    annual_salary = getattr(employee_payroll_record, "annual_salary", Decimal(0))
                    total_compensation = ReportPayrollContributionsAscensusUtil.get_total_compensation(
                        employee_payroll_record,
                        payroll_upload_settings.customer_partner_settings,
                    )
                    hours_worked = getattr(employee_payroll_record, "hours_worked", Decimal(0))
                    company_contribution_column = payroll_upload_settings.customer_partner_settings[
                        AscensusSettingsKeys.COMPANY_CONTRIBUTION_COLUMN.value
                    ]

                    mapping_from_column_name_to_value = {
                        "SOCIAL SECURITY": ssn,
                        "LAST NAME": employee_last_name,
                        "FIRST NAME": employee_first_name,
                        "MI": "",
                        "DIVISIONAL CODE": "",
                        "TOTAL COMPENSATION": total_compensation,
                        "EMPLOYEE 401(K)": payroll_employee_contribution_401k,
                        "ROTH 401(K)": payroll_employee_roth_401k,
                        "LOAN PAYMENT AMOUNT": payroll_employee_loan_repayment,
                        company_contribution_column: payroll_company_match_contribution,
                        "CLIENT SPECIFIC": "",
                        "HOURS": hours_worked,
                        "ADDRESS 1": address_line_1,
                        "ADDRESS 2": address_line_2,
                        "CITY": city,
                        "STATE": state,
                        "ZIP": zip_code,
                        "DATE OF BIRTH": employee_dob,
                        "CURRENT DATE OF HIRE": current_date_of_hire,
                        "EMPLOYEE ELIGIBILITY DATE": "",
                        "CURRENT DATE OF TERM": current_date_of_term,
                        "PRIOR DATE OF HIRE": "",
                        "PRIOR DATE OF TERM": "",
                        "ESTIMATED ANNUAL COMPENSATION": annual_salary,
                        "EMPLOYMENT STATUS": "",
                        "HCE CODE": "",
                        "KEY EE CODE": "",
                        "ENROLLMENT ELIGIBILITY": "",
                        "UNION STATUS CODE": "",
                        "EMPLOYEE WORK EMAIL": work_email,
                    }
                    writer.writerow(mapping_from_column_name_to_value)
                except Exception as e:
                    logger.exception(
                        "[ReportPayrollContribution] Not able to write the row for employee: {} due to error {}".format(
                            ssn, e
                        )
                    )
                    raise Exception(
                        "[ReportPayrollContribution] Not able to write the row for employee: {}".format(ssn)
                    )
            file = File()
            file.name = ReportPayrollContributionsAscensusUtil.get_file_name(payroll_upload_settings)
            client_id = str(payroll_upload_settings.customer_partner_settings[AscensusSettingsKeys.CLIENT_ID.value])
            check_date = getattr(payroll_upload_settings.payrun_info, "check_date", None)
            if check_date:
                check_date = check_date.strftime(STANDARD_DATE_FORMAT)
            fein_settings = ReportPayrollContributionsAscensusUtil.get_fein_settings(
                payroll_upload_settings.ein,
                payroll_upload_settings.customer_partner_settings,
            )
            site_code = ReportPayrollContributionsAscensusUtil.get_site_code(
                fein_settings,
                payroll_upload_settings,
                no_of_salaried_roles,
                no_of_hourly_roles,
            )
            index_of_current_payroll_run = ReportPayrollContributionsAscensusUtil.get_index_of_current_payroll_run(
                payroll_upload_settings
            )
            header = "{},{},{},{}\n".format(client_id, check_date, site_code, index_of_current_payroll_run)

            file.content = ReportPayrollContributionsAscensusUtil.to_bytes(header + output.getvalue())
            return file


class UpdateDeductionElectionsAscensusUtil:
    """
    This class represents the "update deduction elections" capability for vendors utilizing
    the Ascensus. The developer is supposed to implement
    parse_deductions_for_ascensus method in their implementation. For further details regarding their
    implementation details, check their documentation.
    """

    @staticmethod
    def _create_eds_for_value(
        deduction_type: DeductionType,
        value: Union[str, Decimal],
        percentage: bool,
        ssn: str,
        effective_date: datetime,
    ) -> EmployeeDeductionSetting:
        eds = EmployeeDeductionSetting()
        eds.ssn = ssn
        eds.effective_date = effective_date
        eds.deduction_type = deduction_type
        eds.value = Decimal(value)  # type: ignore
        eds.is_percentage = percentage
        return eds

    @staticmethod
    def _is_valid_amount(value) -> bool:
        try:
            Decimal(value)
            return True
        except Exception:
            return False

    @staticmethod
    def get_deduction_type(given_ded_type) -> Optional[DeductionType]:
        ded_match_map = {
            "4ROTH": DeductionType.ROTH_401K,
            "4ROTC": DeductionType.ROTH_401K,
            "401K": DeductionType._401K,
            "401KC": DeductionType._401K,
            "401L": DeductionType._401K_LOAN_PAYMENT,
            "403B": DeductionType._403B,
            "401A": DeductionType.AFTER_TAX_401K,
            "401O": DeductionType._401K,
        }
        return ded_match_map.get(given_ded_type, None)

    @staticmethod
    def _parse_deduction_rows(
        row: dict[str, Any], result: list[EmployeeDeductionSetting]
    ) -> list[EmployeeDeductionSetting]:
        ssn = row["EmployeeSSN"]
        deduction_type = UpdateDeductionElectionsAscensusUtil.get_deduction_type(row["ContributionCode"])
        eligibility_date = (
            datetime.strptime(row["EmployeeEligibilityDate"], "%m%d%Y")
            if row["EmployeeEligibilityDate"]
            else datetime.now()
        )

        if (
            UpdateDeductionElectionsAscensusUtil._is_valid_amount(row["DeferralAmount"])
            and UpdateDeductionElectionsAscensusUtil._is_valid_amount(row["DeferralPercent"])
            and deduction_type
        ):
            result.append(
                UpdateDeductionElectionsAscensusUtil._create_eds_for_value(
                    deduction_type=deduction_type,
                    value=row["DeferralAmount"]
                    if row["DeferralAmount"] > row["DeferralPercent"]
                    else row["DeferralPercent"],
                    percentage=row["DeferralPercent"] > row["DeferralAmount"],
                    ssn=ssn,
                    effective_date=eligibility_date,
                )
            )

        return result

    @staticmethod
    def _parse_loan_rows(row: dict[str, Any], ssn_to_loan_sum_map: dict[str, Decimal]) -> dict[str, Decimal]:
        ssn = row["EmployeeSSN"]
        if UpdateDeductionElectionsAscensusUtil._is_valid_amount(row["LoanPaymentAmount"]):
            loan_value = Decimal(row["LoanPaymentAmount"])
            if ssn in ssn_to_loan_sum_map:
                ssn_to_loan_sum_map[ssn] += loan_value
            else:
                ssn_to_loan_sum_map[ssn] = loan_value

        return ssn_to_loan_sum_map

    @staticmethod
    def parse_deductions_for_ascensus(uri: str, stream: IOBase) -> list[EmployeeDeductionSetting]:
        """
        This method receives a stream from which the developer is expected to return a list of EmployeeDeductionSetting
        for each employee identifier (SSN).
        :param uri: Contains the path of file
        :param stream: Contains the stream
        :return: list[EmployeeDeductionSetting]
        """
        result: list[EmployeeDeductionSetting] = []

        try:
            reader = csv.DictReader(stream)  # type: ignore
        except Exception as e:
            logger.error(f"[UpdateDeductionElectionsImpl.parse_deductions] Parse deductions failed due to message {e}")
            return result

        ssn_to_loan_sum_map: dict[str, Decimal] = {}

        for row in reader:
            try:
                ssn = row["EmployeeSSN"]
                record_type = row["RecordType"]

                if record_type == "D":
                    UpdateDeductionElectionsAscensusUtil._parse_deduction_rows(row, result)
                elif record_type == "L":
                    UpdateDeductionElectionsAscensusUtil._parse_loan_rows(row, ssn_to_loan_sum_map)
                else:
                    logger.error(f"Unknown transaction type in row: {row}")

            except Exception as e:
                logger.error(f"[UpdateDeductionElectionsImpl.parse_deductions] Parse row failed due to error {e}")

        for ssn in ssn_to_loan_sum_map:
            loan_sum = ssn_to_loan_sum_map[ssn]
            result.append(
                UpdateDeductionElectionsAscensusUtil._create_eds_for_value(
                    deduction_type=DeductionType._401K_LOAN_PAYMENT,
                    value=Decimal(loan_sum),
                    percentage=False,
                    ssn=ssn,
                    effective_date=datetime.now(),
                )
            )

        return result
