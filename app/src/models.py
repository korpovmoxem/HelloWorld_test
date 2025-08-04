from pydantic import BaseModel, field_validator


class AddHeroRequest(BaseModel):
    name: str

    @field_validator('name')
    def 