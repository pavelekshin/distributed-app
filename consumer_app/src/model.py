from pydantic import BaseModel


class UserData(BaseModel):
    acc_id: str
    unsubscribe: bool
    msg_id: str
