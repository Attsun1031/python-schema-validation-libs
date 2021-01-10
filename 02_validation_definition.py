"""
バリデーション定義に関する比較
"""

import typing
import uuid

import pytest
import attr
import cattr
import cerberus
import marshmallow as ma
import marshmallow.validate as ma_v
import pydantic as pd

regex = r'^apple (pie|tart|sandwich)$'


class PydanticModel(pd.BaseModel):
    # standard type & range validation
    i: pd.conint(gt=1, le=3)
    # collection type & length
    j: pd.conlist(int, min_items=1, max_items=5)
    # regex
    k: pd.constr(regex=regex)
    # oneOf
    l: typing.Literal['abc', 'def']
    # Union
    u: typing.Union[uuid.UUID, int]
    # custom validator
    c: int

    @pd.validator('c')
    def custom_field_validator(cls, v):
        if v == 2:
            raise ValueError('err')
        return v

    @pd.root_validator
    def multiple_field_validator(cls, values):
        if values.get('i') == values.get('u'):
            raise ValueError('err')
        return values


class MarshmallowCustomValidator(ma_v.Validator):
    def __init__(self, v):
        self.v = v

    def __call__(self, value):
        if value == self.v:
            raise ma.ValidationError('err')


class MarshmallowModel(ma.Schema):
    # standard type & range validation
    i = ma.fields.Int(validate=ma_v.Range(min=1, max=3, min_inclusive=False))
    # collection type & length
    j = ma.fields.List(ma.fields.Int(), validate=ma_v.Length(min=1, max=5))
    # regex
    k = ma.fields.Str(validate=ma_v.Regexp(regex=regex))
    # oneOf
    l = ma.fields.Str(validate=ma_v.OneOf(['abc', 'def']))
    # Union (not supported)
    u = ma.fields.UUID()
    # custom validation
    c = ma.fields.Int(validate=MarshmallowCustomValidator(2))

    @ma.validates_schema
    def multiple_field_validator(self, data, **kwargs):
        if data.get("i") == data.get("u"):
            raise ma.ValidationError("err")


def attr_custom_validator(instance, attribute, value):
    if value == 2:
        raise ValueError('err')


@attr.s
class AttrsModel:
    # standard type & range validation (not supported)
    i = attr.ib(validator=[attr.validators.instance_of(int)])
    # collection type & length (both not supported)
    j = attr.ib()
    # regex
    k = attr.ib(validator=[attr.validators.matches_re(regex)])
    # oneOf (not supported)
    l = attr.ib()
    # Union (not supported)
    u = attr.ib()
    # custom validation
    c = attr.ib()

    @c.validator
    def _check_c(self, attribute, value):
        if value == 2:
            raise ValueError


class CerberusCustomValidator(cerberus.Validator):
    types_mapping = {
        **cerberus.Validator.types_mapping,
        'UUID': cerberus.TypeDefinition('UUID', (uuid.UUID,), ())
    }

    def _validate_custom(self, custom, field, value):
        if custom and value == 2:
            self._error(field, "err")


cerberus_schema = {
    # standard type & range validation
    'i': {'type': 'integer', 'min': 2, 'max': 3},
    # collection type & length
    'j': {'type': 'list', 'minlength': 1, 'maxlength': 5},
    # regex
    'k': {'type': 'string', 'regex': regex},
    # oneOf
    'l': {'type': 'string', 'allowed': ['abc', 'def']},
    # union
    'u': {'type': ['UUID', 'integer']},
    # custom
    'c': {'type': 'integer', 'custom': True}
}

pytest_params = [
    'data,is_valid',
    [
        (dict(i=3, j=[1, 2, 3], k='apple pie', l='abc', u=uuid.uuid4(), c=1), True),
        (dict(i=1, j=[1, 2, 3], k='apple pie', l='abc', u=uuid.uuid4(), c=1), False),
        (dict(i=3, j=[1, 2, 3, 4, 5, 6], k='apple pie', l='abc', u=uuid.uuid4(), c=1), False),
        (dict(i=3, j=[1, 2, 3], k='apple mac', l='abc', u=uuid.uuid4(), c=1), False),
        (dict(i=3, j=[1, 2, 3], k='apple pie', l='ghi', u=uuid.uuid4(), c=1), False),
        (dict(i=3, j=[1, 2, 3], k='apple pie', l='abc', u=3, c=1), False),
        (dict(i=3, j=[1, 2, 3], k='apple pie', l='abc', u=uuid.uuid4(), c=2), False),
    ]
]


class TestValidation:

    @pytest.mark.parametrize(*pytest_params)
    def test_pydantic(self, data, is_valid):
        try:
            PydanticModel(**data)
            assert is_valid
        except pd.ValidationError:
            assert not is_valid

    @pytest.mark.parametrize(*pytest_params)
    def test_marshmallow(self, data, is_valid):
        try:
            MarshmallowModel().load(data)
            assert is_valid
        except ma.ValidationError:
            assert not is_valid

    @pytest.mark.parametrize(*pytest_params)
    def test_attr(self, data, is_valid):
        try:
            cattr.structure(data, AttrsModel)
            assert is_valid
        except ValueError:
            assert not is_valid

    @pytest.mark.parametrize(*pytest_params)
    def test_cerberus(self, data, is_valid):
        assert CerberusCustomValidator(cerberus_schema).validate(data) == is_valid
