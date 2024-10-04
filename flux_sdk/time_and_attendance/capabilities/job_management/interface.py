from abc import ABC, abstractmethod

from flux_sdk.time_and_attendance.capabilities.job_management.data_models import (
    GetEmployeesPayRateOverridesResponse,
    GetJobAttributesRequest,
    GetJobAttributesResponse,
)


class JobManagement(ABC):
    @abstractmethod
    def get_job_attributes(self, request: GetJobAttributesRequest) -> GetJobAttributesResponse:
        """
        A function that gets job attributes from the third-party system.

        Use this hook to fetch job attributes from the third-party system
        so that they can be matched with attributes in Rippling.

        If request.requested_attribute_values is False, only fetch the mapping of the attributes to Rippling.

        If request.requested_attribute_values is True, fetch the mapping and the attribute values.

        Only fetch data for the attributes in request.requested_attributes. If requested_attributes is None, fetch all.
        Note, it is recommended to use the key_in_requested_attributes helper in the requested.

        :param request: The request containing the attributes to fetch and if values are required.
        :return: The response containing the job attributes from the third-party system, mapping to their Rippling
        attributes and possible values.
        """

    @abstractmethod
    def get_employees_pay_rate_overrides(self) -> GetEmployeesPayRateOverridesResponse:
        """
        A function that gets the pay rate override for each employee that requires an override.
        
        Use this hook to fetch the pay rate override for each employee that requires it.

        The pay rate override is tied to the attribute mapped to Rippling.PAY_RATE.

        If a default pay rate is given in the get_job_attributes hook, an employee may get a different one through this.

        :return: The response containing the pay rate override for each employee that requires it.
        """
