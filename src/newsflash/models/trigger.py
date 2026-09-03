from pydantic import BaseModel


class Trigger(BaseModel):
    element_id: str
    element_name: str
    trigger: str

    def to_path(self) -> str:
        return f"/{self.element_name}/{self.element_id}/{self.trigger}"
