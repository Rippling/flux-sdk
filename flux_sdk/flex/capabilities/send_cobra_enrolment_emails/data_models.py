from typing import (
    Any,
    Dict,
    List,
    Optional,
)

from pydantic import BaseModel


# This class models an email with various options for recipients, attachments, and sending configurations.
class Email(BaseModel):
    template_name: str
    recipients_data: List[Dict[str, Any]]
    global_data: dict
    attachments: Optional[List[Dict[str, Any]]] = None
    cc_everyone: Optional[bool] = False
    sendSecurely: Optional[bool] = False
    name_space: Optional[str] = None
    unique_key: Optional[str] = None
    reply_to: Optional[str] = None