import csv
import datetime
import logging
from decimal import Decimal
from io import IOBase
from typing import Any, Union

from flux_sdk.flux_core.data_models import DeductionType
from flux_sdk.pension.capabilities.update_deduction_elections.data_models import (
    EmployeeDeductionSetting,
)
from flux_sdk.pension.utils.common import (
    RecordTypeKeys,
    get_deduction_type,
)

logger = logging.getLogger(__name__)

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


class UpdateDeductionElectionsPayKonnectUtil:
    """
    This class represents the "update deduction elections" capability for vendors utilizing
    the PayKonnect. The app developer is supposed to implement
    parse_deductions_for_pay_konnect method in their implementation. For further details regarding their
    implementation details, check their documentation.
    """

    @staticmethod
    def _parse_loan_rows(row: dict[str, Any], ssn_to_loan_sum_map: dict[str, Decimal]) -> None:
        ssn = row["SSN"]
        if UpdateDeductionElectionsPayKonnectUtil._is_valid_amount(row["Value"]):
            loan_value = Decimal(row["Value"])
            if ssn in ssn_to_loan_sum_map:
                ssn_to_loan_sum_map[ssn] += loan_value
            else:
                ssn_to_loan_sum_map[ssn] = loan_value

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
    def _parse_deduction_rows(row: dict[str, Any], result: list[EmployeeDeductionSetting]) -> None:
        ssn = row["SSN"]
        deduction_type = get_deduction_type(row["Code"])
        eligibility_date = (
            datetime.datetime.strptime(row["Eligibility Date"], "%m%d%Y")
            if row["Eligibility Date"]
            else datetime.datetime.now()
        )

        if UpdateDeductionElectionsPayKonnectUtil._is_valid_amount(row["Value"]) and deduction_type:
            result.append(
                UpdateDeductionElectionsPayKonnectUtil._create_eds_for_value(
                    deduction_type=deduction_type,
                    value=row["Value"],
                    percentage=True if row["Value Type"] == "Percent" else False,
                    ssn=ssn,
                    effective_date=eligibility_date,
                )
            )

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

                if record_type == RecordTypeKeys.DeductionType.value:
                    UpdateDeductionElectionsPayKonnectUtil._parse_deduction_rows(row, result)
                elif record_type == RecordTypeKeys.LoanType.value:
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
