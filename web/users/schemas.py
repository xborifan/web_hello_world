from pydantic import BaseModel, EmailStr, field_validator
from pydantic_extra_types.phone_numbers import PhoneNumber
from typing import Optional
from datetime import datetime, timedelta


class RussianPhoneNumber(PhoneNumber):
    supported_regions=["RU"]
    default_region_code="+7"
    
    
class User(BaseModel):
    #id: int
    name: str
    surname: str
    patronymic: Optional[str]
    login: str
    date_reg: datetime
    date_birth: datetime
    email: Optional[EmailStr]
    phone: Optional[RussianPhoneNumber]
    
    @field_validator("date_birth")
    def validate_age(cls, value: datetime):
        currentDate = datetime.now().today()
        naive = value.replace(tzinfo=None)
        age = currentDate.year - naive.year
        print(age)
        if age < 18:
            raise ValueError(f"Вам должно быть больше 18 лет!")
        if age > 99:
            raise ValueError(f"Вы староваты для этого!")
        return value
    
    @field_validator("name", "surname", "patronymic")
    def validate_fio(cls, value: str):
        if value:
            value = value.capitalize()
        return value
    
    @field_validator("phone", mode="before")
    def validate_phone(cls, value: str):
        if value:
            if value.startswith("8"):
                value = value.replace("8", "+7", 1)
        return value