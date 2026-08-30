from pydantic import BaseModel


class Trigger(BaseModel):
    element_id: str
    element_name: str
    trigger: str
