from flux_sdk.flex.capabilities.update_contributions.data_models import EmployeeContribution
from flux_sdk.flex.capabilities.update_enrollments.data_models import EmployeeEnrollment


class EmployeeJoinedEnrollmentContribution(EmployeeContribution):
    joined_enrollment: EmployeeEnrollment
