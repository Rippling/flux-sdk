import contextlib
import csv
import logging
from datetime import datetime
from decimal import ROUND_HALF_UP, Decimal
from io import StringIO
from typing import Optional, Union

from flux_sdk.flux_core.data_models import (
    ContributionType,
    Employee,
    EmployeeState,
    File,
)
from flux_sdk.pension.capabilities.report_payroll_contributions.data_models import (
    EmployeePayrollRecord,
    PayrollRunContribution,
    PayrollUploadSettings,
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

STANDARD_DATE_FORMAT = "%m/%d/%Y"
TWO_PLACES = Decimal(".01")


class ReportPayrollContributionsAscensusUtil:
    """
    This class embodies the functionality to "report payroll contributions" for vendors utilizing
    the Ascensus formatted file.
    Developers are required to implement the format_contributions_for_ascensus_vendor method in their code.
    To obtain the Plan_Number and Plan_Name from the admin during installation, include the following code in
    spoke/config/manifest/variable in your app's manifest file:
    "variables": [
            {
              "name": "client_id",
              "type": "TEXT",
              "title": "Plan ID",
              "required": true,
            }
        ],
    For further details regarding their implementation details, check their documentation.
    """

    @staticmethod
    def _get_formatted_ssn(ssn: str) -> str:
        return ssn[:3] + "-" + ssn[3:5] + "-" + ssn[5:9]

    @staticmethod
    def to_bytes(content: Union[str, bytes]) -> bytes:
        data = content.encode() if isinstance(content, str) else content
        return data

    @staticmethod
    def _get_amount_from_payroll_contribution(
        payroll_contribution: Optional[PayrollRunContribution],
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
        environment = payroll_upload_settings.environment
        client_id = str(payroll_upload_settings.customer_partner_settings["client_id"])
        payroll_run_id = payroll_upload_settings.payrun_info.payroll_run_id

        if not environment or not client_id:
            raise RuntimeError(
                "Environment and client_id must be present to upload Vanguard file"
            )
        timestamp = datetime.now()
        format_timestamp = timestamp.strftime("%m%d%Y.%H%M%S")
        return "{}_{}_{}_{}.csv".format(
            environment, client_id, payroll_run_id, format_timestamp
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
        with contextlib.closing(StringIO()) as output:
            writer = csv.DictWriter(output, fieldnames=COLUMNS_180)
            writer.writeheader()

            for employee_payroll_record in employee_payroll_records:
                employee: Employee = employee_payroll_record.employee
                ssn = ReportPayrollContributionsAscensusUtil._get_formatted_ssn(
                    employee.ssn
                )
                payroll_contributions: list[
                    PayrollRunContribution
                ] = employee_payroll_record.payroll_contributions
                payroll_contribution_map = {
                    pc.deduction_type.name: pc for pc in payroll_contributions
                }

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

                    current_date_of_hire = employee.start_date.strftime(
                        STANDARD_DATE_FORMAT
                    )
                    current_date_of_term = getattr(employee, "termination_date", None)
                    if (
                        current_date_of_term
                        and employee.status == EmployeeState.TERMINATED
                    ):
                        current_date_of_term = current_date_of_term.strftime(
                            STANDARD_DATE_FORMAT
                        )
                    else:
                        current_date_of_term = ""
                    prior_hire_date = employee.original_hire_date.strftime(
                        STANDARD_DATE_FORMAT
                    )
                    prior_term_date = ""
                    if (
                        hasattr(employee, "termination_date")
                        and employee.termination_date
                    ):
                        prior_term_date = employee.termination_date.strftime(
                            STANDARD_DATE_FORMAT
                        )

                    payroll_employee_contribution_401k: Decimal = ReportPayrollContributionsAscensusUtil.\
                        _get_amount_from_payroll_contribution(
                        payroll_contribution_map.get(ContributionType._401K.name, None)
                    )
                    payroll_company_match_contribution: Decimal = ReportPayrollContributionsAscensusUtil.\
                        _get_amount_from_payroll_contribution(
                        payroll_contribution_map.get(
                            ContributionType.COMPANY_MATCH.name, None
                        )
                    )
                    payroll_employee_loan_repayment: Decimal = ReportPayrollContributionsAscensusUtil.\
                        _get_amount_from_payroll_contribution(
                        payroll_contribution_map.get(ContributionType.LOAN.name, None)
                    )
                    payroll_employee_roth_401k: Decimal = ReportPayrollContributionsAscensusUtil.\
                        _get_amount_from_payroll_contribution(
                        payroll_contribution_map.get(ContributionType.ROTH.name, None)
                    )

                    gross_pay = getattr(
                        employee_payroll_record, "gross_pay", Decimal(0)
                    )
                    annual_salary = getattr(
                        employee_payroll_record, "annual_salary", Decimal(0)
                    )
                    hours_worked = getattr(
                        employee_payroll_record, "hours_worked", Decimal(0)
                    )

                    mapping_from_column_name_to_value = {
                        "SOCIAL SECURITY": ssn,
                        "LAST NAME": employee_last_name,
                        "FIRST NAME": employee_first_name,
                        "MI": "",
                        "DIVISIONAL CODE": "",
                        "TOTAL COMPENSATION": gross_pay,
                        "EMPLOYEE 401(K)": payroll_employee_contribution_401k,
                        "ROTH 401(K)": payroll_employee_roth_401k,
                        "LOAN PAYMENT AMOUNT": payroll_employee_loan_repayment,
                        "MATCH": payroll_company_match_contribution,
                        "PROFIT SHARING": "",
                        "SAFE HARBOR MATCH": "",
                        "SAFE HARBOR NEC": "",
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
                        "PRIOR DATE OF HIRE": prior_hire_date,
                        "PRIOR DATE OF TERM": prior_term_date,
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
                        "[ReportPayrollContribution] Not able to write the row for employee: {}".format(
                            ssn
                        )
                    )
            file = File()
            file.name = ReportPayrollContributionsAscensusUtil.get_file_name(
                payroll_upload_settings
            )
            file.content = ReportPayrollContributionsAscensusUtil.to_bytes(
                output.getvalue()
            )
            return file
