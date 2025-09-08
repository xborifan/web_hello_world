from pydantic import BaseModel, EmailStr, field_validator as fv
from pydantic_extra_types.phone_numbers import PhoneNumber
from typing import Optional
from datetime import datetime, date


class RussianPhoneNumber(PhoneNumber):
    supported_regions=["RU"]
    default_region_code="+7"
    
    
class User(BaseModel):
    #id: int
    name: str
    surname: str
    patronymic: Optional[str]
    login: str
    dateOfReg: Optional[datetime]
    dateOfBirth: date
    email: Optional[EmailStr]
    phone: Optional[RussianPhoneNumber]
    
    @fv("dateOfBirth")
    def validate_age(cls, value: date):
        today = date.today()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        if age < 18:
            raise ValueError(f"Вам должно быть больше 18 лет! ({age} - это недостаточно)")
        if age > 99:
            raise ValueError(f"Старикам здесь не место! ({age} - это многовато)")
        return value
    
    @fv("name", "surname", "patronymic")
    def validate_fio(cls, value: str):
        return value.strip().capitalize() if value else value
    
    @fv("phone", mode="before")
    def validate_phone(cls, value: str):
        if value:
            if value.startswith("8"):
                value = value.replace("8", "+7", 1)
        return value
    
    @fv("dateOfReg")
    def validate_registration_date(cls, value: datetime):
        return value if value else datetime.now()
    
    @fv("login")
    def validate_login(cls, value: str):
        if value.strip() == "":
            raise ValueError(f"Логин не может быть пустым!")
        return value.lower()
    
    @fv("email", mode="after")
    def validate_email(cls, value: EmailStr):
        return value.lower() if value else value     