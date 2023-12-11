import contextlib
import csv
import logging
import datetime
from decimal import Decimal
from six import StringIO
from pytz import timezone
from typing import Optional, Union

from flux_sdk.flux_core.data_models import (
    File,
    Employee,
    ContributionType,
    Gender,
    EmployeeState,
)
from flux_sdk.pension.capabilities.report_payroll_contributions.data_models import (
    EmployeePayrollRecord,
    PayrollRunContribution,
    PayrollUploadSettings,
    LeaveInfo,
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
    "CONT_Company_Match",
    "CONT_YTD_Company_Match",
    "CONT_Contribution_%_Company_Match",
    "CONT_Contribution_$_Company_Match",
    "LOAN_Ref_Number",
    "LOAN_Amount",
]


class ReportPayrollContributionsPayKonnectUtil:
    """
    This class embodies the functionality to "report payroll contributions" for vendors utilizing
    the payKonnect formatted file.
    Developers are required to implement the format_contributions_for_payKonnect_vendor method in their code.
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
    def _get_payroll_contributions_map(
        payroll_contributions: list[PayrollRunContribution],
    ) -> dict[str, PayrollRunContribution]:
        payroll_contribution_map = {}
        for payroll_contribution in payroll_contributions:
            payroll_contribution_map[
                payroll_contribution.deduction_type.name
            ] = payroll_contribution

        return payroll_contribution_map

    @staticmethod
    def _get_formatted_ssn(ssn: str) -> str:
        return ssn[:3] + "-" + ssn[3:5] + "-" + ssn[5:9]

    @staticmethod
    def _get_gender(gender: Gender) -> str:
        if gender.name == "MALE":
            gender_code = "Male"
        elif gender.name == "FEMALE":
            gender_code = "Female"
        else:
            gender_code = "Not Specified"

        return gender_code

    @staticmethod
    def _get_employee_status(
        employee_status: EmployeeState, ytd_leave_infos: list[LeaveInfo]
    ):
        status = ""
        if employee_status.name == "ACTIVE":
            status = "Active"
        elif employee_status.name == "TERMINATED":
            status = "Terminated"
        for leave_info in ytd_leave_infos:
            if (
                leave_info.start_date
                <= datetime.datetime.now().date()
                <= leave_info.return_date
            ):
                status = "Leave"
                break
        return status

    @staticmethod
    def _date_formatter(date):
        formatted_date = date.strftime("%m/%d/%Y")
        if len(formatted_date) != 10:
            formatted_date = "0" + formatted_date
        return formatted_date

    @staticmethod
    def _get_rounded_decimal(amount: Decimal, precision: int):
        return round(amount, precision)

    @staticmethod
    def _get_pay_frequency(pay_frequency: str) -> str:
        if pay_frequency == "WEEKLY":
            return "Weekly"
        elif pay_frequency == "BI_WEEKLY":
            return "Bi-Weekly"
        elif pay_frequency == "SEMI_MONTHLY":
            return "Semi-Monthly"
        elif pay_frequency == "MONTHLY":
            return "Monthly"
        elif pay_frequency == "QUARTERLY":
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
            if (
                leave_info.start_date
                <= datetime.datetime.now().date()
                <= leave_info.return_date
            ):
                leave_type = (
                    ReportPayrollContributionsPayKonnectUtil._convert_to_sentence_case(
                        leave_info.leave_type.name
                    )
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
        tz = timezone("US/Pacific")
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

        plan_name = payroll_upload_settings.customer_partner_settings.get(
            "plan_id", "Plan_Number"
        )

        transmission_date = ReportPayrollContributionsPayKonnectUtil._get_today_date()
        report_time = ReportPayrollContributionsPayKonnectUtil._pst_now().strftime(
            "%H%M%S"
        )
        return "{}_{}_{}.csv".format(plan_name, transmission_date, report_time)

    @staticmethod
    def format_contributions_for_payKonnect_vendor(
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
        plan_id: str = customer_partner_settings.get("plan_id")
        plan_name: str = customer_partner_settings.get("plan_name")

        with contextlib.closing(StringIO()) as output:
            writer = csv.DictWriter(output, fieldnames=columns_180)
            writer.writeheader()

            for employee_payroll_record in employee_payroll_records:
                payroll_contributions: list[
                    PayrollRunContribution
                ] = employee_payroll_record.payroll_contributions
                payroll_contribution_map = ReportPayrollContributionsPayKonnectUtil._get_payroll_contributions_map(
                    payroll_contributions
                )
                employee: Employee = employee_payroll_record.employee

                ssn: str = ReportPayrollContributionsPayKonnectUtil._get_formatted_ssn(
                    employee.ssn
                )
                ein: str = payroll_upload_settings.ein
                company_id: str = payroll_upload_settings.payrun_info.payroll_run_id
                employee_id: str = (
                    employee.employee_id
                    if hasattr(employee, "employee_id") and employee.employee_id
                    else ""
                )
                try:
                    payroll_employee_contribution_401k: Optional[
                        PayrollRunContribution
                    ] = payroll_contribution_map.get(ContributionType._401K.name, None)
                    payroll_company_match_contribution: Optional[
                        PayrollRunContribution
                    ] = payroll_contribution_map.get(
                        ContributionType.COMPANY_MATCH.name, None
                    )
                    payroll_employee_loan_repayment: Optional[
                        PayrollRunContribution
                    ] = payroll_contribution_map.get(ContributionType.LOAN.name, None)

                    payroll_date_absolute = (
                        payroll_upload_settings.payrun_info.original_pay_date
                        if hasattr(
                            payroll_upload_settings.payrun_info, "original_pay_date"
                        )
                        and payroll_upload_settings.payrun_info.original_pay_date
                        else None
                    )
                    payroll_date = (
                        payroll_date_absolute.strftime("%m/%d/%Y")
                        if payroll_date_absolute
                        else ""
                    )
                    payroll_start_date = (
                        payroll_upload_settings.payrun_info.pay_period_start_date
                        if hasattr(
                            payroll_upload_settings.payrun_info, "pay_period_start_date"
                        )
                        and payroll_upload_settings.payrun_info.pay_period_start_date
                        else None
                    )
                    payroll_start_date = (
                        payroll_start_date.strftime("%m/%d/%Y")
                        if payroll_start_date
                        else ""
                    )

                    payroll_end_date = (
                        payroll_upload_settings.payrun_info.pay_period_end_date
                        if hasattr(
                            payroll_upload_settings.payrun_info, "pay_period_end_date"
                        )
                        and payroll_upload_settings.payrun_info.pay_period_end_date
                        else None
                    )
                    payroll_end_date = (
                        payroll_end_date.strftime("%m/%d/%Y")
                        if payroll_end_date
                        else ""
                    )
                    payroll_run_type: str = (
                        ReportPayrollContributionsPayKonnectUtil._convert_to_sentence_case(
                            payroll_upload_settings.payrun_info.run_type.name
                        )
                        if hasattr(payroll_upload_settings.payrun_info, "run_type")
                        else ""
                    )

                    pay_frequency: str = (
                        ReportPayrollContributionsPayKonnectUtil._get_pay_frequency(
                            payroll_upload_settings.payrun_info.pay_frequency
                        )
                        if hasattr(payroll_upload_settings.payrun_info, "pay_frequency")
                        and payroll_upload_settings.payrun_info.pay_frequency
                        else ""
                    )

                    employee_401k: Decimal = (
                        payroll_employee_contribution_401k.amount
                        if payroll_employee_contribution_401k
                        else Decimal(0)
                    )
                    company_match_contribution = (
                        payroll_company_match_contribution.amount
                        if payroll_company_match_contribution
                        else Decimal(0)
                    )
                    employee_loan_repayment = (
                        payroll_employee_loan_repayment.amount
                        if payroll_employee_loan_repayment
                        else Decimal(0)
                    )
                    employee_first_name = employee.first_name
                    employee_middle_name = employee.middle_name
                    employee_last_name = employee.last_name
                    address_line_1 = (
                        employee.address.address_line_1
                        if employee.address and employee.address.address_line_1
                        else ""
                    )
                    address_line_2 = (
                        employee.address.address_line_2
                        if employee.address and employee.address.address_line_2
                        else ""
                    )
                    city = (
                        employee.address.city
                        if employee.address and employee.address.city
                        else ""
                    )
                    state = (
                        employee.address.state
                        if employee.address and employee.address.state
                        else ""
                    )
                    zip_code = (
                        employee.address.zip_code
                        if employee.address and employee.address.zip_code
                        else ""
                    )
                    country = (
                        ReportPayrollContributionsPayKonnectUtil._convert_to_sentence_case(
                            employee.address.country
                        )
                        if employee.address and employee.address.country
                        else ""
                    )
                    personal_email = employee.personal_email
                    work_email = employee.business_email
                    employee_category = (
                        ReportPayrollContributionsPayKonnectUtil._get_employee_category(
                            employee
                        )
                    )
                    pay_type = (
                        ReportPayrollContributionsPayKonnectUtil._get_employee_pay_type(
                            employee
                        )
                    )
                    termination_date = ""
                    if (
                        hasattr(employee, "termination_date")
                        and employee.termination_date
                    ):
                        termination_date = employee.termination_date.strftime("%m%d%Y")
                    birth_day = (
                        ReportPayrollContributionsPayKonnectUtil._date_formatter(
                            employee.dob
                        )
                    )
                    phone_number = (
                        employee.phone_number if employee.phone_number else ""
                    )
                    rehire_date = (
                        ReportPayrollContributionsPayKonnectUtil._date_formatter(
                            employee.start_date
                        )
                    )
                    hire_date = (
                        ReportPayrollContributionsPayKonnectUtil._date_formatter(
                            employee.original_hire_date
                        )
                    )
                    hours_worked = (
                        employee_payroll_record.hours_worked
                        if employee_payroll_record.hours_worked
                        else Decimal(0)
                    )
                    gross_pay = (
                        employee_payroll_record.gross_pay
                        if hasattr(employee_payroll_record, "gross_pay")
                        else Decimal(0)
                    )
                    employee_year_to_date_hours_worked = (
                        employee_payroll_record.eoy_info.year_to_date_hours
                        if hasattr(employee_payroll_record, "eoy_info")
                        else Decimal(0)
                    )
                    employee_year_to_date_gross_pay = (
                        employee_payroll_record.eoy_info.year_to_date_gross_pay
                        if hasattr(employee_payroll_record, "eoy_info")
                        else Decimal(0)
                    )
                    if rehire_date == hire_date:
                        rehire_date = ""
                    employee_work_status_code = (
                        (
                            ReportPayrollContributionsPayKonnectUtil._get_loa_info(
                                employee_payroll_record.leave_infos
                            )
                        )
                        if hasattr(employee_payroll_record, "leave_infos")
                        else ""
                    )

                    ytd_leave_infos = []
                    if hasattr(employee_payroll_record, "ytd_leave_infos"):
                        ytd_leave_infos: list[
                            LeaveInfo
                        ] = employee_payroll_record.ytd_leave_infos
                    employee_status = (
                        ReportPayrollContributionsPayKonnectUtil._get_employee_status(
                            employee.status, ytd_leave_infos
                        )
                    )
                    gender = ReportPayrollContributionsPayKonnectUtil._get_gender(
                        employee.gender
                    )
                    marital_status = (
                        ReportPayrollContributionsPayKonnectUtil._convert_to_sentence_case(
                            employee.marital_status.name
                        )
                        if hasattr(employee, "marital_status")
                        else ""
                    )
                    salary = (
                        employee_payroll_record.salary
                        if hasattr(employee_payroll_record, "salary")
                        and employee_payroll_record.salary
                        else Decimal(0)
                    )
                    annual_salary = (
                        employee_payroll_record.annual_salary
                        if hasattr(employee_payroll_record, "annual_salary")
                        and employee_payroll_record.annual_salary
                        else Decimal(0)
                    )

                    mapping_from_column_name_to_value = {
                        "Plan_Number": plan_id,
                        "Plan_Name": plan_name,
                        "EIN": ein,
                        "Company_ID": company_id,
                        "Division": "CLARIFY",
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
                        "Pay_Group": "CLARIFY",
                        "Employee_Category": employee_category,
                        "Employee_Pay_Type": pay_type,
                        "Employee_WorkStatus_Code": employee_work_status_code,
                        "Employee_Status_Code": employee_status,
                        "Employee_Type": "",
                        "Employee_Department": "",
                        "Employee_Location_Code": "",
                        "Pay_Period_Hours": hours_worked,
                        "Pay_Period_Gross_Wages": gross_pay,
                        "Pay_Period_Plan_Wages": "CLARIFY",
                        "Pay_Period_Excluded_Wages": "",
                        "YTD_Hours_Worked": employee_year_to_date_hours_worked,
                        "YTD_Total_Compensation": employee_year_to_date_gross_pay,
                        "YTD_Plan_Compensation": "CLARIFY",
                        "YTD_Excluded_Compensation": "",
                        "Officer_Type": "",
                        "Ownership_Percentage": "",
                        "Highly_Comp_Code": "",
                        "Participation_Date": "",
                        "Eligibility_Code": "CLARIFY",
                        "Salary_Amount": salary,
                        "Termination_Reason_Code": "NEED TO ADD",
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
                        "CONT_YTD_401K": "",
                        "CONT_Contribution_%_401K": "",
                        "CONT_Contribution_$_401K": "",
                        "CONT_Company_Match": "",
                        "CONT_YTD_Company_Match": company_match_contribution,
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
                        "[ReportPayrollContribution] Not able to write the row for employee: {}".format(
                            ssn
                        )
                    )

            file = File()
            file.name = ReportPayrollContributionsPayKonnectUtil.get_file_name(
                payroll_upload_settings
            )
            file.content = ReportPayrollContributionsPayKonnectUtil.to_bytes(
                output.getvalue()
            )
            return file
