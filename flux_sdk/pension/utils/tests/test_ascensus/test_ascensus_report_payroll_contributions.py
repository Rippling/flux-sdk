import os
import unittest
from datetime import date, datetime
from decimal import Decimal

from flux_sdk.flux_core.data_models import (
    Address,
    ContributionType,
    Employee,
    EmployeeState,
    File,
    MaritalStatus,
)
from flux_sdk.pension.capabilities.report_payroll_contributions.data_models import (
    EmployeePayrollRecord,
    PayrollRunContribution,
    PayrollUploadSettings,
    PayrunInfo,
)
from flux_sdk.pension.utils.ascensus_report_payroll_contributions import ReportPayrollContributionsAscensusUtil


class TestReportPayrollContributionsAscensusUtil(unittest.TestCase):
    """
    Tests for functions for the UpdatePayrollContributions capability.
    """

    def setUp(self) -> None:
        self.payroll_upload_settings: PayrollUploadSettings = PayrollUploadSettings()
        self.payrunInfo = PayrunInfo()
        self.payrunInfo.payroll_run_id = "54321"
        self.payrunInfo.original_pay_date = datetime(2021, 1, 1)
        self.payrunInfo.check_date = datetime(2021, 7, 1)
        self.payrunInfo.pay_frequency = "WEEKLY"
        self.dummyPayRunInfo = PayrunInfo()
        self.dummyPayRunInfo.payroll_run_id = "12345"
        self.dummyPayRunInfo.check_date = datetime(2021, 7, 1)
        self.customer_partner_settings: dict = {
            "client_id": "HISS00",
            "site_code_frequency": "E",
            "company_contribution_column": "MATCH",
            "EXCLUDE_SEVERANCE": False,
            "EXCLUDE_IMPUTED_INCOME": False,
            "EXCLUDE_BONUS": True,
            "frequency_or_pay_type": "FREQUENCY",
            "site_code_mapping_for_weekly": "C",
            "feins": {
                "123456789": {
                    "fein_site_code": "B",
                    "fein_site_code_mapping_for_weekly": "D",
                }
            },
            "env": "TS",
        }
        self.payroll_upload_settings.customer_partner_settings = (
            self.customer_partner_settings
        )
        self.payroll_upload_settings.current_month_payruns = [self.payrunInfo, self.dummyPayRunInfo]
        self.payroll_upload_settings.payrun_info = self.payrunInfo
        self.payroll_upload_settings.company_legal_name = "RIPPLING TEST"
        self.payroll_upload_settings.company_name = "RIPPLING"
        self.payroll_upload_settings.ein = "123456789"
        self.payroll_upload_settings.environment = "TS"

        self.employee_payroll_records: list[EmployeePayrollRecord] = []
        employeePayrollRecord = EmployeePayrollRecord()

        employee: Employee = Employee()
        employee.first_name = "John"
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
        employee.business_email = "abc@website.com"
        employee.dob = datetime(1990, 1, 1)
        employee.start_date = datetime(2020, 1, 1)
        employee.original_hire_date = datetime(2020, 1, 1)
        employee.termination_date = date(2020, 6, 1)
        employee.start_date = datetime(2021, 1, 1)
        employee.status = EmployeeState.ACTIVE
        employee.is_international_employee = False
        employee.marital_status = MaritalStatus.SINGLE
        employee.is_salaried = True

        payrollRunContribution1 = PayrollRunContribution()
        payrollRunContribution1.deduction_type = ContributionType._401K
        payrollRunContribution1.amount = Decimal(1000.001)

        payrollRunContribution2 = PayrollRunContribution()
        payrollRunContribution2.deduction_type = ContributionType.LOAN
        payrollRunContribution2.amount = Decimal(3000.20)

        payroll_contributions = [payrollRunContribution1, payrollRunContribution2]
        employeePayrollRecord.payroll_contributions = payroll_contributions
        employeePayrollRecord.employee = employee

        employeePayrollRecord.gross_pay = Decimal(10000)
        employeePayrollRecord.bonus = Decimal(1000)
        employeePayrollRecord.hours_worked = Decimal(2400)
        employeePayrollRecord.annual_salary = Decimal(100000)

        self.employee_payroll_records = [employeePayrollRecord]

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

    def test_format_contributions_for_ascensus_vendor_failure(self) -> None:
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
            for index, incomplete_employee_payroll_record in enumerate(
                incomplete_employee_payroll_records
            ):
                self.set_nested_attribute(
                    incomplete_employee_payroll_record, required_field, None
                )
            with self.assertRaises(Exception):
                ReportPayrollContributionsAscensusUtil.format_contributions_for_ascensus_vendor(
                    incomplete_employee_payroll_records, self.payroll_upload_settings
                )

            for index, incomplete_employee_payroll_record in enumerate(
                incomplete_employee_payroll_records
            ):
                original_attr_value = self.get_nested_attributes(
                    self.employee_payroll_records[index], required_field
                )
                self.set_nested_attribute(
                    incomplete_employee_payroll_record,
                    required_field,
                    original_attr_value,
                )

    def test_format_contributions_for_ascensus_vendor(self) -> None:
        contributions_file: File = ReportPayrollContributionsAscensusUtil.format_contributions_for_ascensus_vendor(
            self.employee_payroll_records, self.payroll_upload_settings
        )
        file_content = contributions_file.content.decode()
        with open(
            os.path.join(os.path.dirname(__file__), "contributions_report_payroll_contributions.csv")
        ) as contribution_file:
            contribution_file_contents = contribution_file.read()
            self.assertEqual(
                file_content.replace("\r\n", "\n"), contribution_file_contents
            )

    def test_get_file_name(self) -> None:
        timestamp = datetime.now()
        format_timestamp = timestamp.strftime("%m%d%Y.%H%M%S")
        test_file_name = "{}_{}_{}_{}.csv".format(
            "TS", "HISS00","54321", format_timestamp,
        )

        file_name = ReportPayrollContributionsAscensusUtil.get_file_name(
            self.payroll_upload_settings
        )
        self.assertEqual(file_name, test_file_name)
