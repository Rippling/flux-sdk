import base64
import importlib
import io

import jsonpickle

from flux_kit_references.pension.capabilities.update_payroll_contributions.data_models import (
    EmployeePayrollRecord,
    PayrollUploadSettings,
)

def invoke(app: str, event: dict[str, any]):
    hook = event['hook']

    if hook == 'parse_deductions':
        impl = import_implementation(app, "pension", "update_deduction_elections")
        uri = event['uri']
        file_content: bytes = base64.b85decode(jsonpickle.decode(event['content']))
        stream: io.IOBase = io.StringIO(file_content.decode())
        return jsonpickle.encode(impl.UpdateDeductionElectionsImpl.parse_deductions(uri, stream))
    elif hook == 'get_file_name':
        impl = import_implementation(app, "pension", "update_payroll_contributions")
        payroll_upload_settings: PayrollUploadSettings = jsonpickle.decode(event['payroll_upload_settings'])
        result = impl.UpdatePayrollContributionsImpl.get_file_name(payroll_upload_settings)
        return result
    elif hook == 'format_deductions':
        impl = import_implementation(app, "pension", "update_payroll_contributions")
        employee_payroll_records: list[EmployeePayrollRecord] = jsonpickle.decode(event['employee_payroll_records'])
        payroll_upload_settings: PayrollUploadSettings = jsonpickle.decode(event['payroll_upload_settings'])
        return jsonpickle.encode(base64.b85encode(impl.UpdatePayrollContributionsImpl.format_deductions(employee_payroll_records, payroll_upload_settings)))


def import_implementation(root, kit, capability):
    return importlib.import_module(f".{kit}_kit.capabilities.{capability}.implementation", root)