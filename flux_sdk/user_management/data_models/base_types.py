class User:
    id: str
    first_name: str
    last_name: str
    primary_email: str

    def __init__(self, id: str, first_name: str, last_name: str, primary_email: str) -> None:
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.primary_email = primary_email