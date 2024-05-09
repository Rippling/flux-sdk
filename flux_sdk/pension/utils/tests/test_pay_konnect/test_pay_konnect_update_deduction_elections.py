import io
import unittest
from decimal import Decimal

from flux_sdk.pension.utils.pay_konnect_update_deduction_elections import UpdateDeductionElectionsPayKonnectUtil


class TestUpdateDeductionElections(unittest.TestCase):
    """
    Tests for functions for the UpdateDeductionElections capability.
    """

    def get_file_data_for_test_update_deduction(self, date, ssn1, ssn2):

        sample_deferral_file = (
            "Record Type,Plan Number,SSN,Effective Date,Eligibility Date,"
            "Transaction Date,Transaction Type,Code,Value Type,Value,Loan Reference Number,Loan Goal\n"
            "D,222222-00000,{},,03312019,,,401K,Amount,1.0,123,\n"
            "D,222222-00000,{},,03312019,,,4ROTH,Percent,12.0,123,\n"
            "D,222222-00000,{},,03312019,,,401K,Amount,15.00,123,\n"
            "D,222222-00000,{},,03312019,,,4ROTH,Amount,25.00,123,\n"
            "L,222222-00000,{},,04122018,,,401L,Amount,20.00,123,\n"
            "L,222222-00000,{},,04122018,,,401L,Amount,30.00,123,\n"
            "L,222222-00000,{},,04122018,,,401L,Amount,40.00,123,\n"
            "L,222222-00000,{},,04122018,,,401L,Amount,50.00,123,\n"
        ).format(ssn1, ssn1, ssn2, ssn2, ssn1, ssn2, ssn1, ssn2)

        return sample_deferral_file

    def test_parse_deductions(self):
        ssn1 = "523546780"
        ssn2 = "523546781"
        sample_deferral_file = self.get_file_data_for_test_update_deduction("3/6/2023", ssn1, ssn2)

        result = UpdateDeductionElectionsPayKonnectUtil.parse_deductions_for_pay_konnect(
            "", io.StringIO(sample_deferral_file)
        )

        count = 0
        for ed in result:
            count = count + 1
            if ed.ssn == ssn1:
                if ed.deduction_type == "_401K":
                    self.assertEqual(ed.value, Decimal("1.00"))
                    self.assertEqual(ed.is_percentage, True)
                if ed.deduction_type == "ROTH_401K":
                    self.assertEqual(ed.value, Decimal("12.00"))
                    self.assertEqual(ed.is_percentage, True)
                if ed.deduction_type == "_401K_LOAN_PAYMENT":
                    self.assertEqual(ed.value, Decimal("60"))
                    self.assertEqual(ed.is_percentage, False)
            else:
                if ed.deduction_type == "_401K":
                    self.assertEqual(ed.value, Decimal("15.00"))
                    self.assertEqual(ed.is_percentage, False)
                if ed.deduction_type == "ROTH_401K":
                    self.assertEqual(ed.value, Decimal("25.00"))
                    self.assertEqual(ed.is_percentage, False)
                if ed.deduction_type == "_401K_LOAN_PAYMENT":
                    self.assertEqual(ed.value, Decimal("80"))
                    self.assertEqual(ed.is_percentage, False)

        self.assertEqual(count, 6)
