import os
import unittest
from datetime import date, datetime
from decimal import Decimal
from unittest.mock import patch

from flux_sdk.flux_core.data_models import (
    Address,
    ContributionType,
    Employee,
    EmployeeState,
    File,
    Gender,
    LeaveType,
    MaritalStatus,
)
from flux_sdk.pension.capabilities.report_payroll_contributions.data_models import (
    EmployeePayrollRecord,
    LeaveInfo,
    PayrollRunContribution,
    PayrollUploadSettings,
    PayrunInfo,
)
from flux_sdk.pension.utils.pay_konnect_report_payroll_contributions import ReportPayrollContributionsPayKonnectUtil


class TestReportPayrollContributionsPayKonnectUtil(unittest.TestCase):
    """
    Tests for functions for the UpdatePayrollContributions capability.
    """

    def setUp(self) -> None:
        self.payroll_upload_settings: PayrollUploadSettings = PayrollUploadSettings()
        self.payrunInfo = PayrunInfo()
        self.payrunInfo.payroll_run_id = "54321"
        self.payrunInfo.pay_period_start_date = datetime(2021, 1, 1)
        self.payrunInfo.pay_period_end_date = datetime(2021, 2, 1)
        self.payrunInfo.check_date = date(2021, 4, 1)
        self.payrunInfo.paid_at_date = datetime(2021, 1, 1)
        self.payrunInfo.pay_frequency = "WEEKLY"
        self.customer_partner_settings: dict = {
            "plan_id": "HISS001",
            "plan_name": "Hiss",
            "division": "Division",
            "pay_group": "pay group",
            "plan_year_end_date": datetime(2021, 4, 30),
        }
        self.payroll_upload_settings.customer_partner_settings = self.customer_partner_settings
        self.payroll_upload_settings.payrun_info = self.payrunInfo
        self.payroll_upload_settings.company_legal_name = "RIPPLING TEST"
        self.payroll_upload_settings.company_name = "RIPPLING"
        self.payroll_upload_settings.ein = "123456789"

        self.employee_payroll_records: list[EmployeePayrollRecord] = []
        employeePayrollRecord = EmployeePayrollRecord()

        employee: Employee = Employee()
        employee.first_name = "Rand"
        employee.middle_name = "D"
        employee.ssn = "523546780"
        employee.last_name = "Doe"
        employee.address = Address()
        employee.address.address_line_1 = "123 Main St"
        employee.address.address_line_2 = "Apt 1"
        employee.address.city = "San Francisco"
        employee.address.state = "CA"
        employee.address.zip_code = "94105"
        employee.address.country = "US"
        employee.business_email = "abcd@website.com"
        employee.dob = datetime(1990, 1, 1)
        employee.start_date = datetime(2020, 1, 1)
        employee.original_hire_date = datetime(2020, 1, 1)
        employee.termination_date = date(2020, 6, 1)
        employee.start_date = datetime(2021, 1, 1)
        employee.gender = Gender.FEMALE
        employee.is_full_time = True
        employee.is_contractor = False
        employee.employment_type = "Hourly"
        employee.department = "department"
        employee.phone_number = "1234543212"
        employee.personal_email = "test1@email.com"
        employee.is_salaried = True
        employee.status = EmployeeState.ACTIVE
        employee.is_international_employee = False
        employee.marital_status = MaritalStatus.SINGLE

        payrollRunContribution1 = PayrollRunContribution()
        payrollRunContribution1.deduction_type = ContributionType._401K
        payrollRunContribution1.amount = Decimal(1000)

        payrollRunContribution2 = PayrollRunContribution()
        payrollRunContribution2.deduction_type = ContributionType.LOAN
        payrollRunContribution2.amount = Decimal(3000)

        payroll_contributions = [payrollRunContribution1, payrollRunContribution2]
        employeePayrollRecord.payroll_contributions = payroll_contributions
        employeePayrollRecord.employee = employee

        employeePayrollRecord.gross_pay = Decimal(10000)
        employeePayrollRecord.hours_worked = Decimal(2400)
        employeePayrollRecord.annual_salary = Decimal(100000)

        self.seed_loa(employeePayrollRecord)

        self.employee_payroll_records = [employeePayrollRecord]
        terminated_employee_payroll_records: list[
            EmployeePayrollRecord
        ] = self._get_terminated_employee_payroll_records()
        self.employee_payroll_records.extend(terminated_employee_payroll_records)
        self.employee_payroll_records.extend(self._get_terminated_employee_payroll_records(date(2020, 3, 1)))

    def get_terminated_employee(self, end_date: date = date(2020, 5, 1), name: str = "NotAppear") -> Employee:
        employee: Employee = Employee()
        employee.first_name = "John"
        employee.middle_name = "D"
        employee.ssn = "523546780"
        employee.role_id = "12345"
        employee.last_name = "Doe"
        employee.address = Address()
        employee.address.address_line_1 = "123 Main St"
        employee.address.address_line_2 = "Apt 1"
        employee.address.city = "San Francisco"
        employee.address.state = "CA"
        employee.address.zip_code = "94105"
        employee.address.country = "US"
        employee.business_email = "abc@website.com"
        employee.employment_type = "Hourly"
        employee.department = "department"
        employee.termination_reason = "terminated"
        employee.personal_email = "test2@email.com"
        employee.is_salaried = True
        employee.dob = datetime(1990, 1, 1)
        employee.start_date = datetime(2020, 1, 1)
        employee.original_hire_date = datetime(2020, 1, 1)
        employee.gender = Gender.FEMALE
        employee.is_full_time = True
        employee.is_contractor = False
        employee.phone_number = "1234543212"
        employee.status = EmployeeState.TERMINATED
        employee.termination_date = end_date
        employee.is_international_employee = False
        employee.marital_status = MaritalStatus.SINGLE
        return employee

    def _get_terminated_employee_payroll_records(
        self, end_date: date = date(2020, 5, 1)
    ) -> list[EmployeePayrollRecord]:
        employee_payroll_records = []
        for i in range(1, 5):
            employee_payroll_record = EmployeePayrollRecord()
            employee_payroll_record.employee = self.get_terminated_employee(name="John")
            employee_payroll_record.hours_worked = Decimal(2400)
            employee_payroll_record.annual_salary = Decimal(100000)
            employee_payroll_records.append(employee_payroll_record)
        return employee_payroll_records

    def get_nested_attributes(self, obj, attribute):
        nested_list = attribute.split(".")
        curr_obj = obj
        for attribute in nested_list:
            if getattr(curr_obj, attribute, None) is None:
                return None
            curr_obj = getattr(curr_obj, attribute, None)
        return curr_obj

    def set_nested_attribute(self, obj, attribute, value) -> None:
        nested_list = attribute.split(".")
        curr_obj = obj
        for index, attribute in enumerate(nested_list):
            if getattr(curr_obj, attribute, None) is None:
                return None
            if index + 1 == len(nested_list):
                setattr(curr_obj, attribute, value)
            curr_obj = getattr(curr_obj, attribute, None)

    def test_format_contributions_for_payKonnect_vendor_failure(self) -> None:
        required_employee_payroll_records_information = [
            "employee.ssn",
            "payroll_contributions",
            "employee.first_name",
            "employee.middle_name",
            "employee.last_name",
            "employee.address",
            "employee.dob",
            "employee.start_date",
            "employee.original_hire_date",
            "employee.gender",
            "employee.marital_status",
        ]
        incomplete_employee_payroll_records = self.employee_payroll_records
        for required_field in required_employee_payroll_records_information:
            for index, incomplete_employee_payroll_record in enumerate(incomplete_employee_payroll_records):
                self.set_nested_attribute(incomplete_employee_payroll_record, required_field, None)
            with self.assertRaises(Exception):
                ReportPayrollContributionsPayKonnectUtil.format_contributions_for_pay_konnect_vendor(
                    incomplete_employee_payroll_records, self.payroll_upload_settings
                )

            for index, incomplete_employee_payroll_record in enumerate(incomplete_employee_payroll_records):
                original_attr_value = self.get_nested_attributes(self.employee_payroll_records[index], required_field)
                self.set_nested_attribute(
                    incomplete_employee_payroll_record,
                    required_field,
                    original_attr_value,
                )

    @patch(
        "flux_sdk.pension.utils.pay_konnect_report_payroll_contributions.ReportPayrollContributionsPayKonnectUtil._pst_now",
        return_value=datetime(2021, 1, 1),
    )
    def test_format_contributions_for_pay_konnect_vendor(self, mock_pst_now) -> None:
        contributions_file: File = ReportPayrollContributionsPayKonnectUtil.format_contributions_for_pay_konnect_vendor(
            self.employee_payroll_records, self.payroll_upload_settings
        )
        file_content = contributions_file.content.decode()
        with open(os.path.join(os.path.dirname(__file__), "contributions.csv")) as contribution_file:
            contribution_file_contents = contribution_file.read()
            self.assertEqual(file_content.replace("\r\n", "\n"), contribution_file_contents)

    def test_get_file_name(self) -> None:
        file_name = ReportPayrollContributionsPayKonnectUtil.get_file_name(self.payroll_upload_settings)
        transmission_date = ReportPayrollContributionsPayKonnectUtil._get_today_date()
        self.assertEqual(file_name.split("_")[0], "HISS001")
        self.assertEqual(file_name.split("_")[1], transmission_date)
        report_time_without_extension = file_name.split("_")[2].split(".")[0]
        self.assertTrue(report_time_without_extension.isdigit())

    def seed_loa(self, employeePayrollRecord) -> None:
        leave_info = LeaveInfo()
        leave_info.leave_type = LeaveType.MEDICAL
        leave_info.start_date = datetime(2021, 1, 1).date()
        leave_info.return_date = datetime(2021, 1, 10).date()
        leave_info.is_paid = True
        employeePayrollRecord.leave_infos = [leave_info]
        employeePayrollRecord.ytd_leave_infos = [leave_info]
