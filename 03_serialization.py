"""
シリアライズ・デシリアライズに関する比較
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import json
import typing
import uuid

import pytest
import attr
import cattr
import cerberus
import marshmallow as ma
import marshmallow.validate as ma_v
import pydantic as pd


class E(Enum):
    A = 'X'
    B = 'Y'


class PydanticSubModel(pd.BaseModel):
    s: str


class PydanticModel(pd.BaseModel):
    i: int
    d: datetime
    e: E
    m: PydanticSubModel


@dataclass()
class MarshmallowSubModel:
    s: str


class MarshmallowSubSchema(ma.Schema):
    s = ma.fields.Str()

    @ma.post_load
    def make(self, data, **kwargs):
        return MarshmallowSubModel(**data)


@dataclass()
class MarshmallowModel:
    i: int
    d: datetime
    m: MarshmallowSubModel


class MarshmallowSchema(ma.Schema):
    i = ma.fields.Int()
    d = ma.fields.DateTime()
    m = ma.fields.Nested(MarshmallowSubSchema)

    @ma.post_load
    def make(self, data, **kwargs):
        return MarshmallowModel(**data)

    class Meta:
        unknown = ma.EXCLUDE


@attr.s
class AttrsSubModel:
    s: str = attr.ib()


@attr.s
class AttrsModel:
    i: int = attr.ib()
    d: datetime = attr.ib()
    e: E = attr.ib()


class TestSerializeDeserialize:
    base_data = dict(
        i=1,
        d=datetime.fromisoformat('2021-01-11T14:27:42.758260'),
        e=E.B,
    )

    expected_json = json.dumps(dict(
        i=1,
        d='2021-01-11T14:27:42.758260',
        e='Y',
        m=dict(s="hoge")
    ))

    exclude_fields = {'d', 'e', 'm'}

    def test_pydantic(self):
        data = dict(m=PydanticSubModel(s="hoge")) | self.base_data
        m = PydanticModel(**data)
        assert m.dict() == data
        j = m.json()
        assert j == self.expected_json
        assert PydanticModel.parse_raw(j) == m

        assert m.dict(exclude=self.exclude_fields) == {'i': 1}

    def test_marshmallow(self):
        data = dict(m=MarshmallowSubModel(s="hoge")) | self.base_data
        del data["e"]
        # m = MarshmallowSchema().load(data)
        # assert MarshmallowSchema().dump(m) == data
        m = MarshmallowModel(**data)
        j = MarshmallowSchema().dumps(m)
        # assert j == self.expected_json
        assert MarshmallowSchema().load(json.loads(j)) == m

        assert MarshmallowSchema(only={'i',}).dump(m) == {'i': 1}

    def test_attrs(self):
        data = dict(m=AttrsSubModel(s="hoge")) | self.base_data
        del data["m"]
        m = AttrsModel(**data)
        assert attr.asdict(m) == data
        cattr.unstructure
