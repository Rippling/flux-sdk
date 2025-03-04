from abc import ABC

from flux_sdk.pension.capabilities.update_deduction_elections.interface import UpdateDeductionElections


class UpdateDeductionElection(UpdateDeductionElections, ABC):
    """Report payroll contributions for employees in your application via data in Rippling.
    This class represents the "report payroll contribution" capability. The developer is supposed to implement
    format_contributions method in their implementation. For further details regarding their
    implementation details, check their documentation.
    """