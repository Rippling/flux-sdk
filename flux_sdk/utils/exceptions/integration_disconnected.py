class IntegrationDisconnectedException(Exception):
    def __init__(self, disconnect_reason: str):
        self.message = 'Integration disconnected'
        self.status_code = 500
        self.disconnect_reason = disconnect_reason
