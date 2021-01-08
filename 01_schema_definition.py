"""
スキーマ定義に関する比較
"""

import typing
from datetime import date

import attr
import cattr
import cerberus
import marshmallow as ma
import pydantic as pd

# テスト対象データ
data = {"i": "1", "j": None}
data_extended = {"a": 3} | data

################################################################################
# pydantic
################################################################################
print("=== pydantic")


class PydanticModel(pd.BaseModel):
    # Required
    i: int
    # Nullable & Required
    j: typing.Optional[int] = pd.Field(...)
    # Optional
    k: int = 3
    # Default value
    d: date = pd.Field(default_factory=date.today)

    class Config:
        arbitrary_types_allowed = True


class ExtendedPydanticModel(PydanticModel):
    a: int


print(PydanticModel(**data))
print(ExtendedPydanticModel(**data_extended))

################################################################################
# marshmallow
################################################################################
print("=== marshmallow")


class MarshmallowModel(ma.Schema):
    # Required
    i = ma.fields.Int(required=True, allow_none=False)
    # Nullable & Required
    j = ma.fields.Int(required=True, allow_none=True)
    # Default value
    k = ma.fields.Int(missing=3)
    # Default factory
    d = ma.fields.Date(missing=date.today)


class ExtendedMarshmallowModel(MarshmallowModel):
    a = ma.fields.Int(required=True)

m = MarshmallowModel().load(data)
print(MarshmallowModel().load(data))
print(ExtendedMarshmallowModel().load(data_extended))

################################################################################
# attr
################################################################################
print("=== attr")


@attr.s
class AttrsModel:
    # Required
    i = attr.ib(validator=attr.validators.instance_of(int), converter=int)
    # Nullable & Required
    j = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(int)),
                converter=lambda i: int(i) if i is not None else None)
    # Default value
    k = attr.ib(default=3, validator=attr.validators.instance_of(int), converter=int)
    # Default factory
    d = attr.ib(factory=date.today)


print(cattr.structure(data, AttrsModel))

################################################################################
# cerberus
################################################################################
print("=== cerberus")

cerberus_schema = {
    # Required
    'i': {'type': 'integer', 'required': True, 'coerce': int},
    # Nullable & Required
    'j': {'type': 'integer', 'required': True, 'nullable': True, 'coerce': int},
    # Default value
    'k': {'type': 'integer', 'default': 3, 'coerce': int},
    # Default factory
    'd': {'type': 'date', 'default_setter': lambda _: date.today()},
}
extended_cerberus_schema = {"a": {'type': 'integer', 'required': True, 'coerce': int}} | cerberus_schema

print(cerberus.Validator(cerberus_schema).validated(data))
print(cerberus.Validator(extended_cerberus_schema).validated(data_extended))
