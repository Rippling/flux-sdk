import io
import unittest
from decimal import Decimal

from flux_sdk.pension.utils.ascensus_update_deduction_elections import UpdateDeductionElectionsAscensusUtil


class TestUpdateDeductionElections(unittest.TestCase):
    """
    Tests for functions for the UpdateDeductionElections capability.
    """

    def get_file_data_for_test_update_deduction(self, date):
        ssn1 = "523546780"
        ssn2 = "523546781"

        sample_deferral_file = (
            "RecordType,PlanId,EmployeeLastName,EmployeeFirstName,EmployeeMiddleInitial,EmployeeSSN,EffectiveDate,ContributionCode,DeferralPercent,DeferralAmount,EmployeeEligibilityDate,LoanNumber,LoanPaymentAmount,TotalLoanAmount\n"
            "D,222222-00000,DOE,JOHN,,{},03312019,401K,10.00,0.00,5102022,,,,\n"
            "D,222222-00000,DOE,JOHN,,{},03312019,4ROTH,0,2.00,,,,,\n"
            "D,222222-00000,DOE,JOHN,,{},03312019,401K,5.00,0.00,,,,,,\n"
            "D,222222-00000,DOE,JOHN,,{},03312019,4ROTH,0,1.00,,03312019,,,\n"
            "L,222222-00000,DOE,JOHN,,{},04122018,401L,,,03312019,20181031922XXX,00000000101.19 ,00000005524.17,\n"
            "L,222222-00000,DOE,JOHN,,{},04192018,401L,,,,20180817923XXX,00000000061.30 ,00000007171.35,\n"
            "L,222222-00000,DOE,JOHN,,{},04122018,401L,,,,20181031924XXX,00000000100.00 ,00000005524.17,\n"
            "L,222222-00000,DOE,JOHN,,{},04192018,401L,,,,20180817925XXX,00000000100.00 ,00000007171.35,\n"
        ).format(ssn1, ssn1, ssn2, ssn2, ssn1, ssn2, ssn1, ssn2)

        return sample_deferral_file

    def test_parse_deductions(self):
        sample_deferral_file = self.get_file_data_for_test_update_deduction("3/6/2023")

        result = UpdateDeductionElectionsAscensusUtil.parse_deductions_for_ascensus(
            "", io.StringIO(sample_deferral_file)
        )
        ssn1 = "523546780"

        count = 0
        for ed in result:
            count = count+1
            if ed.ssn == ssn1:
                if ed.deduction_type == "_401K":
                    self.assertEqual(ed.value, Decimal("10.00"))
                    self.assertEqual(ed.is_percentage, True)
                if ed.deduction_type == "ROTH_401K":
                    self.assertEqual(ed.value, Decimal("2.00"))
                    self.assertEqual(ed.is_percentage, False)
                if ed.deduction_type == "_401K_LOAN_PAYMENT":
                    self.assertEqual(ed.value, Decimal("201.19"))
                    self.assertEqual(ed.is_percentage, False)
            else:
                if ed.deduction_type == "_401K":
                    self.assertEqual(ed.value, Decimal("5.00"))
                    self.assertEqual(ed.is_percentage, True)
                if ed.deduction_type == "ROTH_401K":
                    self.assertEqual(ed.value, Decimal("1.00"))
                    self.assertEqual(ed.is_percentage, False)
                if ed.deduction_type == "_401K_LOAN_PAYMENT":
                    self.assertEqual(ed.value, Decimal("161.30"))
                    self.assertEqual(ed.is_percentage, False)

        self.assertEqual(count, 6)