from flux_sdk.flux_core.data_models import Employee, Name

class AppConfig:
    '''
    This contains the application data gathered durring installation which is necesary to prepare employee data or process deductions
    '''
    auto_enroll: bool
    group_id: str
    

class EmployeeData(Employee):
    '''
    This extends the core definition of an employee to include insurance eligibiliity data
    '''
    insurance_eligible: bool
    
    
