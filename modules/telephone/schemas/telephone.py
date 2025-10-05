# Libs
from pydantic import constr, BaseModel


class TelephoneSchema(BaseModel):
    number: constr(
        min_length=4,
        max_length=17,
    )
