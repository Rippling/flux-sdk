import csv
import logging
from datetime import datetime
from decimal import Decimal
from io import IOBase
from typing import Any, Union

from flux_sdk.flux_core.data_models import (
    DeductionType,
)
from flux_sdk.pension.capabilities.update_deduction_elections.data_models import (
    EmployeeDeductionSetting,
)
from flux_sdk.pension.utils.common import (
    RecordTypeKeys,
    get_deduction_type,
)

logger = logging.getLogger(__name__)

COLUMNS_360 = [
    "RecordType",  ## 'D' represents Contribution Change, 'L' represents Loan
    "PlanId",  ## Plan ID or Contract number
    "EmployeeLastName",
    "EmployeeFirstName",
    "EmployeeMiddleInitial",
    "EmployeeSSN",
    "EffectiveDate",  ## The date that the change is effective
    "ContributionCode",
    "DeferralPercent",
    "DeferralAmount",
    "EmployeeEligibilityDate",  ## The date the employee became eligible
    "LoanNumber",
    "LoanPaymentAmount",
    "TotalLoanAmount",
]


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
        is_percentage: bool,
        ssn: str,
        effective_date: datetime,
    ) -> EmployeeDeductionSetting:
        eds = EmployeeDeductionSetting()
        eds.ssn = ssn
        eds.effective_date = effective_date
        eds.deduction_type = deduction_type
        eds.value = Decimal(value)  # type: ignore
        eds.is_percentage = is_percentage
        return eds

    @staticmethod
    def _is_valid_amount(value) -> bool:
        try:
            Decimal(value)
            return True
        except Exception:
            return False

    @staticmethod
    def _parse_deduction_rows(row: dict[str, Any], result: list[EmployeeDeductionSetting]) -> None:
        ssn = row["EmployeeSSN"]
        deduction_type = get_deduction_type(row["ContributionCode"])
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
                    is_percentage=row["DeferralPercent"] > row["DeferralAmount"],
                    ssn=ssn,
                    effective_date=eligibility_date,
                )
            )

    @staticmethod
    def _parse_loan_rows(row: dict[str, Any], ssn_to_loan_sum_map: dict[str, Decimal]) -> None:
        ssn = row["EmployeeSSN"]
        if UpdateDeductionElectionsAscensusUtil._is_valid_amount(row["LoanPaymentAmount"]):
            loan_value = Decimal(row["LoanPaymentAmount"])
            if ssn in ssn_to_loan_sum_map:
                ssn_to_loan_sum_map[ssn] += loan_value
            else:
                ssn_to_loan_sum_map[ssn] = loan_value

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

                if record_type == RecordTypeKeys.DeductionType.value:
                    UpdateDeductionElectionsAscensusUtil._parse_deduction_rows(row, result)
                elif record_type == RecordTypeKeys.LoanType.value:
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
                    is_percentage=False,
                    ssn=ssn,
                    effective_date=datetime.now(),
                )
            )

        return result
