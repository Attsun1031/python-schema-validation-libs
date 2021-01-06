"""
スキーマ定義に関する比較
"""

import typing
import pydantic as pd
import marshmallow as ma
import attr, cattr
import jsonschema
import cerberus


# テスト対象データ
data = {"i": "1", "j": None}

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

print(PydanticModel(**data))


################################################################################
# marshmallow
################################################################################
print("=== marshmallow")


class MarshmallowModel(ma.Schema):
    # Required
    i = ma.fields.Int(required=True, allow_none=False)
    # Nullable & Required
    j = ma.fields.Int(required=True, allow_none=True)
    # Optional
    k = ma.fields.Int(missing=3)


print(MarshmallowModel().load(data))


################################################################################
# attr
################################################################################
print("=== attr")


@attr.s
class AttrsModel:
    # Required
    i = attr.ib(validator=attr.validators.instance_of(int), converter=int)
    # Nullable & Required
    j = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(int)), converter=lambda i: int(i) if i is not None else None)
    # Optional
    k = attr.ib(default=3, validator=attr.validators.instance_of(int), converter=int)


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
    # Optional
    'k': {'type': 'integer', 'default': 3, 'coerce': int},
}
cerberus_validator = cerberus.Validator(cerberus_schema)
print(cerberus_validator.validated(data))

