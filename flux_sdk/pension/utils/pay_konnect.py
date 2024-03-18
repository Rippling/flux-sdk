import contextlib
import csv
import datetime
import logging
from decimal import Decimal
from io import StringIO, IOBase
from typing import Optional, Union, Any

from flux_sdk.flux_core.data_models import (
    ContributionType,
    DeductionType,
    Employee,
    EmployeeState,
    File,
    Gender,
)
from flux_sdk.pension.capabilities.report_payroll_contributions.data_models import (
    EmployeePayrollRecord,
    LeaveInfo,
    PayrollRunContribution,
    PayrollUploadSettings,
)
from flux_sdk.pension.capabilities.update_deduction_elections.data_models import (
    EmployeeDeductionSetting,
)

logger = logging.getLogger(__name__)

columns_180 = [
    "Plan_Number",
    "Plan_Name",
    "EIN",
    "Company_ID",
    "Division",
    "Payroll_Date",
    "Payroll_Start_Date",
    "Ending_Payroll_date",
    "Payroll_Run_Type",
    "Pay_Cycle",
    "SSN",
    "Employee_ID",
    "First_Name",
    "Middle_Name",
    "Last_Name",
    "Name_Suffix",
    "Birth_Date",
    "Gender",
    "Marital_Status",
    "Address_Line_1",
    "Address_Line_2",
    "City",
    "State",
    "Zip_Code",
    "Country_Code",
    "Home_Phone_Number",
    "Work_Phone_Number",
    "Work_Phone_Ext",
    "Email_Address",
    "Work_Email_Address",
    "Hire_Date",
    "Termination_Date",
    "ReHire_Date",
    "Pay_Group",
    "Employee_Category",
    "Employee_Pay_Type",
    "Employee_WorkStatus_Code",
    "Employee_Status_Code",
    "Employee_Type",
    "Employee_Department",
    "Employee_Location_Code",
    "Pay_Period_Hours",
    "Pay_Period_Gross_Wages",
    "Pay_Period_Plan_Wages",
    "Pay_Period_Excluded_Wages",
    "YTD_Hours_Worked",
    "YTD_Total_Compensation",
    "YTD_Plan_Compensation",
    "YTD_Excluded_Compensation",
    "Officer_Type",
    "Ownership_Percentage",
    "Highly_Comp_Code",
    "Participation_Date",
    "Eligibility_Code",
    "Salary_Amount",
    "Termination_Reason_Code",
    "Sarbanes_Oxley_Reporting_Indicator",
    "Federal_Exemptions",
    "Projected Start Date",
    "Adjusted_Service_Date",
    "Match_Eligibility_Date",
    "Annual_Salary",
    "Hourly_Rate",
    "Earnings",
    "Earnings_YTD",
    "CONT_401K",
    "CONT_YTD_401K",
    "CONT_Contribution_%_401K",
    "CONT_Contribution_$_401K",
    "CONT_ROTH_401K",
    "CONT_YTD_ROTH_401K",
    "CONT_Contribution_%_ROTH_401K",
    "CONT_Contribution_$_ROTH_401K",
    "CONT_401K_CATCHUP",
    "CONT_YTD_401K_CATCHUP",
    "CONT_Contribution_%_401K_CATCHUP",
    "CONT_Contribution_$_401K_CATCHUP",
    "CONT_ROTH_401K_CATCHUP",
    "CONT_YTD_ROTH_401K_CATCHUP",
    "CONT_Contribution_%_ROTH_401K_CATCHUP",
    "CONT_Contribution_$_ROTH_401K_CATCHUP",
    "CONT_Company_Match",
    "CONT_YTD_Company_Match",
    "CONT_Contribution_%_Company_Match",
    "CONT_Contribution_$_Company_Match",
    "LOAN_Ref_Number",
    "LOAN_Amount",
]

columns_360 = [
    "Record Type",
    "Plan Number",
    "SSN",
    "Effective Date",
    "Eligibility Date",
    "Transaction Date",
    "Transaction Type",
    "Code",
    "Value Type",
    "Value",
    "Loan Reference Number",
    "Loan Goal",
]

STANDARD_DATE_FORMAT = "%m/%d/%Y"


class ReportPayrollContributionsPayKonnectUtil:
    """
    This class embodies the functionality to "report payroll contributions" for vendors utilizing
    the PayKonnect formatted file.
    Developers are required to implement the format_contributions_for_pay_konnect_vendor method in their code.
    To obtain the Plan_Number and Plan_Name from the admin during installation, include the following code in
    spoke/config/manifest/variable in your app's manifest file:
    "variables": [
            {
              "name": "plan_id",
              "type": "TEXT",
              "title": "Plan Number",
              "required": true,
              "page": "account-setup",
              "required_in_install_flow": true
            },
            {
              "name": "plan_name",
              "type": "TEXT",
              "title": "Plan Name",
              "required": true,
              "page": "account-setup",
              "required_in_install_flow": true
            }
        ],
    For further details regarding their implementation details, check their documentation.
    """

    @staticmethod
    def _get_formatted_ssn(ssn: str) -> str:
        return ssn[:3] + "-" + ssn[3:5] + "-" + ssn[5:9]

    @staticmethod
    def _get_gender(gender: Gender) -> str:
        if gender.name == "MALE":
            return "Male"
        if gender.name == "FEMALE":
            return "Female"
        else:
            return "Not Specified"

    @staticmethod
    def _get_employee_status(employee_status: EmployeeState, ytd_leave_infos: list[LeaveInfo]):
        if employee_status.name == "ACTIVE":
            return "Active"
        if employee_status.name == "TERMINATED":
            return "Terminated"
        for leave_info in ytd_leave_infos:
            if leave_info.start_date <= datetime.datetime.now().date() <= leave_info.return_date:
                return "Leave"
        return ""

    @staticmethod
    def _get_pay_frequency(pay_frequency: str) -> str:
        if pay_frequency == "WEEKLY":
            return "Weekly"
        if pay_frequency == "BI_WEEKLY":
            return "Bi-Weekly"
        if pay_frequency == "SEMI_MONTHLY":
            return "Semi-Monthly"
        if pay_frequency == "MONTHLY":
            return "Monthly"
        if pay_frequency == "QUARTERLY":
            return "Quarterly"
        else:
            return "Annually"

    @staticmethod
    def _get_employee_category(employee: Employee) -> str:
        employee_category = ""
        if employee.is_full_time:
            employee_category = "Full-Time"
        elif employee.is_part_time:
            employee_category = "Part-Time"
        elif employee.is_contractor:
            employee_category = "Contractor"
        return employee_category

    @staticmethod
    def _get_employee_pay_type(employee: Employee) -> str:
        employee_pay_type = ""
        if employee.is_salaried:
            employee_pay_type = "Salaried"
        elif employee.is_hourly:
            employee_pay_type = "Hourly"
        return employee_pay_type

    @staticmethod
    def _get_loa_info(leave_infos: list[LeaveInfo]) -> str:
        leave_type = ""
        for leave_info in leave_infos:
            if leave_info.start_date <= datetime.datetime.now().date() <= leave_info.return_date:
                leave_type = ReportPayrollContributionsPayKonnectUtil._convert_to_sentence_case(
                    leave_info.leave_type.name
                )

        return leave_type

    @staticmethod
    def to_bytes(content: Union[str, bytes]) -> bytes:
        data = content.encode() if isinstance(content, str) else content
        return data

    @staticmethod
    def _get_today_date():
        today = datetime.datetime.now()
        return today.strftime("%d%m%Y")

    @staticmethod
    def _pst_now():
        from zoneinfo import ZoneInfo

        tz = ZoneInfo("US/Pacific")
        dt = datetime.datetime.now(tz=tz)
        # Stripping off microseconds here but not miliseconds because mongo ignores the microseconds part.
        return dt.replace(microsecond=int(dt.microsecond / 1000) * 1000)

    @staticmethod
    def _convert_to_sentence_case(text: Optional[str]) -> str:
        return text.capitalize() if text else ""

    @staticmethod
    def get_file_name(payroll_upload_settings: PayrollUploadSettings) -> str:
        """
        This method receives a PayrollUploadSettings from which the developer
        is expected to return file name based on payroll_upload_settings
        :param payroll_upload_settings:
        :return: str
        """

        plan_name = str(payroll_upload_settings.customer_partner_settings.get("plan_id"))
        transmission_date = ReportPayrollContributionsPayKonnectUtil._get_today_date()
        report_time = ReportPayrollContributionsPayKonnectUtil._pst_now().strftime("%H%M%S%f")[:-3]
        return "{}_{}_{}.csv".format(plan_name, transmission_date, report_time)

    @staticmethod
    def format_contributions_for_pay_konnect_vendor(
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
        customer_partner_settings = payroll_upload_settings.customer_partner_settings
        plan_id = str(customer_partner_settings.get("plan_id"))
        plan_name = str(customer_partner_settings.get("plan_name"))
        division = customer_partner_settings.get("division", "")
        pay_group = customer_partner_settings.get("pay_group", "")

        with contextlib.closing(StringIO()) as output:
            writer = csv.DictWriter(output, fieldnames=columns_180, quoting=csv.QUOTE_ALL)
            writer.writeheader()

            for employee_payroll_record in employee_payroll_records:
                payroll_contributions: list[PayrollRunContribution] = employee_payroll_record.payroll_contributions
                payroll_contribution_map = {pc.deduction_type.name: pc for pc in payroll_contributions}
                employee: Employee = employee_payroll_record.employee
                ssn: str = ReportPayrollContributionsPayKonnectUtil._get_formatted_ssn(employee.ssn)
                ein: str = payroll_upload_settings.ein
                company_id: str = payroll_upload_settings.payrun_info.payroll_run_id
                employee_id: str = getattr(employee, "employee_id", "")
                try:
                    payroll_employee_contribution_401k: Optional[PayrollRunContribution] = payroll_contribution_map.get(
                        ContributionType._401K.name, None
                    )
                    payroll_company_match_contribution: Optional[PayrollRunContribution] = payroll_contribution_map.get(
                        ContributionType.COMPANY_MATCH.name, None
                    )
                    payroll_employee_loan_repayment: Optional[PayrollRunContribution] = payroll_contribution_map.get(
                        ContributionType.LOAN.name, None
                    )
                    payroll_date_absolute = getattr(payroll_upload_settings.payrun_info, "check_date", None)
                    payroll_date = payroll_date_absolute.strftime(STANDARD_DATE_FORMAT) if payroll_date_absolute else ""
                    payroll_start_date = getattr(
                        payroll_upload_settings.payrun_info,
                        "pay_period_start_date",
                        None,
                    )
                    payroll_start_date = payroll_start_date.strftime(STANDARD_DATE_FORMAT) if payroll_start_date else ""
                    payroll_end_date = getattr(payroll_upload_settings.payrun_info, "pay_period_end_date", None)
                    payroll_end_date = payroll_end_date.strftime(STANDARD_DATE_FORMAT) if payroll_end_date else ""
                    payroll_run_type: str = getattr(payroll_upload_settings.payrun_info, "run_type", "")
                    pay_frequency: Optional[str] = getattr(payroll_upload_settings.payrun_info, "pay_frequency", None)
                    pay_frequency = (
                        ReportPayrollContributionsPayKonnectUtil._get_pay_frequency(pay_frequency)
                        if pay_frequency
                        else ""
                    )
                    employee_401k: Decimal = (
                        payroll_employee_contribution_401k.amount if payroll_employee_contribution_401k else Decimal(0)
                    )
                    employee_catchup: Decimal = (
                        payroll_contribution_map[ContributionType._401K_CATCHUP.name].amount
                        if payroll_contribution_map.get(ContributionType._401K_CATCHUP.name, None)
                        else Decimal(0)
                    )
                    employee_roth: Decimal = (
                        payroll_contribution_map[ContributionType.ROTH.name].amount
                        if payroll_contribution_map.get(ContributionType.ROTH.name, None)
                        else Decimal(0)
                    )
                    employee_roth_catchup: Decimal = (
                        payroll_contribution_map[ContributionType.ROTH_401K_CATCHUP.name].amount
                        if payroll_contribution_map.get(ContributionType.ROTH_401K_CATCHUP.name, None)
                        else Decimal(0)
                    )
                    company_match_contribution = (
                        payroll_company_match_contribution.amount if payroll_company_match_contribution else Decimal(0)
                    )
                    employee_loan_repayment = (
                        payroll_employee_loan_repayment.amount if payroll_employee_loan_repayment else Decimal(0)
                    )
                    employee_first_name = employee.first_name
                    employee_middle_name = employee.middle_name
                    employee_last_name = employee.last_name
                    address_line_1 = (
                        employee.address.address_line_1 if employee.address and employee.address.address_line_1 else ""
                    )
                    address_line_2 = (
                        employee.address.address_line_2 if employee.address and employee.address.address_line_2 else ""
                    )
                    city = employee.address.city if employee.address and employee.address.city else ""
                    state = employee.address.state if employee.address and employee.address.state else ""
                    zip_code = employee.address.zip_code if employee.address and employee.address.zip_code else ""
                    country = (
                        ReportPayrollContributionsPayKonnectUtil._convert_to_sentence_case(employee.address.country)
                        if employee.address and employee.address.country
                        else ""
                    )
                    personal_email = employee.personal_email
                    work_email = employee.business_email
                    employee_category = ReportPayrollContributionsPayKonnectUtil._get_employee_category(employee)
                    pay_type = ReportPayrollContributionsPayKonnectUtil._get_employee_pay_type(employee)
                    termination_date = getattr(employee, "termination_date", None)
                    termination_date = termination_date.strftime(STANDARD_DATE_FORMAT) if termination_date else ""
                    birth_day = employee.dob.strftime(STANDARD_DATE_FORMAT)
                    phone_number = employee.phone_number if employee.phone_number else ""
                    rehire_date = employee.start_date.strftime(STANDARD_DATE_FORMAT)
                    hire_date = employee.original_hire_date.strftime(STANDARD_DATE_FORMAT)
                    hours_worked = (
                        employee_payroll_record.hours_worked if employee_payroll_record.hours_worked else Decimal(0)
                    )
                    gross_pay = getattr(employee_payroll_record, "gross_pay", 0)
                    eoy_info = getattr(employee_payroll_record, "eoy_info", None)
                    employee_year_to_date_hours_worked = Decimal(0)
                    employee_year_to_date_gross_pay = Decimal(0)
                    ytd_employee_401k = Decimal(0)
                    ytd_employee_roth = Decimal(0)
                    ytd_employee_catchup = Decimal(0)
                    ytd_employee_roth_catchup = Decimal(0)
                    ytd_company_match_contribution = Decimal(0)
                    ytd_plan_compensation = Decimal(0)
                    if eoy_info:
                        employee_year_to_date_hours_worked = eoy_info.year_to_date_hours
                        employee_year_to_date_gross_pay = eoy_info.year_to_date_gross_pay
                        ytd_employee_401k = eoy_info.year_to_date_pretax_deferral
                        ytd_employee_roth = eoy_info.year_to_date_roth_deferral
                        ytd_employee_catchup = eoy_info.year_to_date_pretax_catchup
                        ytd_employee_roth_catchup = eoy_info.year_to_date_roth_catchup
                        ytd_company_match_contribution = eoy_info.year_to_date_employer_match
                        ytd_plan_compensation = eoy_info.year_to_date_gross_pay
                    if rehire_date == hire_date:
                        rehire_date = ""
                    employee_work_status_code = (
                        (ReportPayrollContributionsPayKonnectUtil._get_loa_info(employee_payroll_record.leave_infos))
                        if hasattr(employee_payroll_record, "leave_infos")
                        else ""
                    )
                    ytd_leave_infos: list[LeaveInfo] = getattr(employee_payroll_record, "ytd_leave_infos", [])
                    employee_status = ReportPayrollContributionsPayKonnectUtil._get_employee_status(
                        employee.status, ytd_leave_infos
                    )
                    employee_type = getattr(employee, "employment_type", "")
                    employee_department = getattr(employee, "department", "")
                    gender = ReportPayrollContributionsPayKonnectUtil._get_gender(employee.gender)
                    marital_status = getattr(employee, "marital_status", None)
                    marital_status = (
                        ReportPayrollContributionsPayKonnectUtil._convert_to_sentence_case(marital_status.name)
                        if marital_status
                        else ""
                    )
                    salary = getattr(employee_payroll_record, "salary", Decimal(0))
                    termination_reason = getattr(employee, "termination_reason", "")
                    annual_salary = getattr(employee_payroll_record, "annual_salary", Decimal(0))

                    mapping_from_column_name_to_value = {
                        "Plan_Number": plan_id,
                        "Plan_Name": plan_name,
                        "EIN": ein,
                        "Company_ID": company_id,
                        "Division": division,
                        "Payroll_Date": payroll_date,
                        "Payroll_Start_Date": payroll_start_date,
                        "Ending_Payroll_date": payroll_end_date,
                        "Payroll_Run_Type": payroll_run_type,
                        "Pay_Cycle": pay_frequency,
                        "SSN": ssn,
                        "Employee_ID": employee_id,
                        "First_Name": employee_first_name,
                        "Middle_Name": employee_middle_name,
                        "Last_Name": employee_last_name,
                        "Name_Suffix": "",
                        "Birth_Date": birth_day,
                        "Gender": gender,
                        "Marital_Status": marital_status,
                        "Address_Line_1": address_line_1,
                        "Address_Line_2": address_line_2,
                        "City": city,
                        "State": state,
                        "Zip_Code": zip_code,
                        "Country_Code": country,
                        "Home_Phone_Number": phone_number,
                        "Work_Phone_Number": phone_number,
                        "Work_Phone_Ext": "",
                        "Email_Address": personal_email,
                        "Work_Email_Address": work_email,
                        "Hire_Date": hire_date,
                        "Termination_Date": termination_date,
                        "ReHire_Date": rehire_date,
                        "Pay_Group": pay_group,
                        "Employee_Category": employee_category,
                        "Employee_Pay_Type": pay_type,
                        "Employee_WorkStatus_Code": employee_work_status_code,
                        "Employee_Status_Code": employee_status,
                        "Employee_Type": employee_type,
                        "Employee_Department": employee_department,
                        "Employee_Location_Code": "",
                        "Pay_Period_Hours": hours_worked,
                        "Pay_Period_Gross_Wages": gross_pay,
                        "Pay_Period_Plan_Wages": "",
                        "Pay_Period_Excluded_Wages": "",
                        "YTD_Hours_Worked": employee_year_to_date_hours_worked,
                        "YTD_Total_Compensation": employee_year_to_date_gross_pay,
                        "YTD_Plan_Compensation": ytd_plan_compensation,
                        "YTD_Excluded_Compensation": "",
                        "Officer_Type": "",
                        "Ownership_Percentage": "",
                        "Highly_Comp_Code": "",
                        "Participation_Date": "",
                        "Eligibility_Code": "",
                        "Salary_Amount": salary,
                        "Termination_Reason_Code": termination_reason,
                        "Sarbanes_Oxley_Reporting_Indicator": "",
                        "Federal_Exemptions": "",
                        "Projected Start Date": "",
                        "Adjusted_Service_Date": "",
                        "Match_Eligibility_Date": "",
                        "Annual_Salary": annual_salary,
                        "Hourly_Rate": "",
                        "Earnings": "",
                        "Earnings_YTD": "",
                        "CONT_401K": employee_401k,
                        "CONT_YTD_401K": ytd_employee_401k,
                        "CONT_Contribution_%_401K": "",
                        "CONT_Contribution_$_401K": "",
                        "CONT_ROTH_401K": employee_roth,
                        "CONT_YTD_ROTH_401K": ytd_employee_roth,
                        "CONT_Contribution_%_ROTH_401K":"",
                        "CONT_Contribution_$_ROTH_401K":"",
                        "CONT_401K_CATCHUP": employee_catchup,
                        "CONT_YTD_401K_CATCHUP": ytd_employee_catchup,
                        "CONT_Contribution_%_401K_CATCHUP":"",
                        "CONT_Contribution_$_401K_CATCHUP":"",
                        "CONT_ROTH_401K_CATCHUP": employee_roth_catchup,
                        "CONT_YTD_ROTH_401K_CATCHUP": ytd_employee_roth_catchup,
                        "CONT_Contribution_%_ROTH_401K_CATCHUP":"",
                        "CONT_Contribution_$_ROTH_401K_CATCHUP":"",
                        "CONT_Company_Match": company_match_contribution,
                        "CONT_YTD_Company_Match": ytd_company_match_contribution,
                        "CONT_Contribution_%_Company_Match": "",
                        "CONT_Contribution_$_Company_Match": "",
                        "LOAN_Ref_Number": 1,
                        "LOAN_Amount": employee_loan_repayment,
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
            file.name = ReportPayrollContributionsPayKonnectUtil.get_file_name(payroll_upload_settings)
            file.content = ReportPayrollContributionsPayKonnectUtil.to_bytes(output.getvalue())
            return file

class UpdateDeductionElectionsPayKonnectUtil:
    """
    This class represents the "update deduction elections" capability for vendors utilizing
    the Ascensus. The developer is supposed to implement
    parse_deductions_for_ascensus method in their implementation. For further details regarding their
    implementation details, check their documentation.
    """

    @staticmethod
    def get_deduction_type(given_ded_type) -> Optional[DeductionType]:
        # Need to update based on PayKonnects response.
        # https://rippling.atlassian.net/browse/BENPNP-5
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
    def _parse_loan_rows(row: dict[str, Any], ssn_to_loan_sum_map: dict[str, Decimal]) -> dict[str, Decimal]:
        ssn = row["SSN"]
        # For now, I have assumed that loans are always amount based. asked the same to paykonnect.
        # will update this according to response.
        if UpdateDeductionElectionsPayKonnectUtil._is_valid_amount(row["Value"]):
            loan_value = Decimal(row["Value"])
            if ssn in ssn_to_loan_sum_map:
                ssn_to_loan_sum_map[ssn] += loan_value
            else:
                ssn_to_loan_sum_map[ssn] = loan_value

        return ssn_to_loan_sum_map

    @staticmethod
    def _create_eds_for_value(
            deduction_type: DeductionType,
            value: Union[str, Decimal],
            percentage: bool,
            ssn: str,
            effective_date: datetime.datetime,
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
    def _parse_deduction_rows(
            row: dict[str, Any], result: list[EmployeeDeductionSetting]
    ) -> list[EmployeeDeductionSetting]:
        ssn = row["SSN"]
        deduction_type = UpdateDeductionElectionsPayKonnectUtil.get_deduction_type(row["Code"])
        eligibility_date = (
            datetime.datetime.strptime(row["Eligibility Date"], "%m%d%Y")
            if row["Eligibility Date"]
            else datetime.datetime.now()
        )

        if (
                UpdateDeductionElectionsPayKonnectUtil._is_valid_amount(row["Value"])
                and deduction_type
        ):
            result.append(
                UpdateDeductionElectionsPayKonnectUtil._create_eds_for_value(
                    deduction_type=deduction_type,
                    value=row["Value"],
                    percentage=True if row["Value Type"] == "Percent" else False,
                    ssn=ssn,
                    effective_date=eligibility_date,
                )
            )

        return result

    @staticmethod
    def parse_deductions_for_pay_konnect(uri: str, stream: IOBase) -> list[EmployeeDeductionSetting]:
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
                ssn = row["SSN"]
                record_type = row["Record Type"]

                if record_type == "D":
                    UpdateDeductionElectionsPayKonnectUtil._parse_deduction_rows(row, result)
                elif record_type == "L":
                    UpdateDeductionElectionsPayKonnectUtil._parse_loan_rows(row, ssn_to_loan_sum_map)
                else:
                    logger.error(f"Unknown transaction type in row: {row}")

            except Exception as e:
                logger.error(f"[UpdateDeductionElectionsImpl.parse_deductions] Parse row failed due to error {e}")

        for ssn in ssn_to_loan_sum_map:
            loan_sum = ssn_to_loan_sum_map[ssn]
            result.append(
                UpdateDeductionElectionsPayKonnectUtil._create_eds_for_value(
                    deduction_type=DeductionType._401K_LOAN_PAYMENT,
                    value=Decimal(loan_sum),
                    percentage=False,
                    ssn=ssn,
                    effective_date=datetime.datetime.now(),
                )
            )

        return result

