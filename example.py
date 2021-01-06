ython 3.9.0 (default, Jan  6 2021, 13:30:45)
[Clang 12.0.0 (clang-1200.0.32.28)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import pydantic as pd
>>> class M(pd.BaseModel):
...
KeyboardInterrupt
>>> import typing
>>> class M(pd.BaseModel):
...   i: int
...   j: typing.Optional[int]
...   k: int = 0
...
>>> M()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/atsumitatsuya/Library/Caches/pypoetry/virtualenvs/python-datavalidation-frameworks-X7pON5WL-py3.9/lib/python3.9/site-packages/pydantic/main.py", line 362, in __init__
    raise validation_error
pydantic.error_wrappers.ValidationError: 1 validation error for M
i
  field required (type=value_error.missing)
>>> M(i=1)
M(i=1, j=None, k=0)
>>> M(i=None)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/atsumitatsuya/Library/Caches/pypoetry/virtualenvs/python-datavalidation-frameworks-X7pON5WL-py3.9/lib/python3.9/site-packages/pydantic/main.py", line 362, in __init__
    raise validation_error
pydantic.error_wrappers.ValidationError: 1 validation error for M
i
  none is not an allowed value (type=type_error.none.not_allowed)
>>> class M(pd.BaseModel):
...   k: int = 0
...   j: typing.Optional[int] = pd.Field(...)
...   i: int
...
>>> M(i=None)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/atsumitatsuya/Library/Caches/pypoetry/virtualenvs/python-datavalidation-frameworks-X7pON5WL-py3.9/lib/python3.9/site-packages/pydantic/main.py", line 362, in __init__
    raise validation_error
pydantic.error_wrappers.ValidationError: 2 validation errors for M
j
  field required (type=value_error.missing)
i
  none is not an allowed value (type=type_error.none.not_allowed)
>>> M(i=1)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/atsumitatsuya/Library/Caches/pypoetry/virtualenvs/python-datavalidation-frameworks-X7pON5WL-py3.9/lib/python3.9/site-packages/pydantic/main.py", line 362, in __init__
    raise validation_error
pydantic.error_wrappers.ValidationError: 1 validation error for M
j
  field required (type=value_error.missing)
>>> M(i=1, j=3)
M(k=0, j=3, i=1)
>>> M(i=1, j=3, k=5)
M(k=5, j=3, i=1)
>>> M(i=1, j=None, k=5)
M(k=5, j=None, i=1)
>>> import marshmallow as ma
>>> class M(ma.Schema):
...   s: ma.fields.Str()
...   t: ma.fields.Str(allow_none=False)
...   u: ma.fields.Str(required=True)
...
>>> M()
<M(many=False)>
>>> M().validate()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: validate() missing 1 required positional argument: 'data'
>>> M().validate()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: validate() missing 1 required positional argument: 'data'
>>> M().validate()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: validate() missing 1 required positional argument: 'data'
>>> M().load({})
{}
>>> M().load({"s": "hoge"})
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/atsumitatsuya/Library/Caches/pypoetry/virtualenvs/python-datavalidation-frameworks-X7pON5WL-py3.9/lib/python3.9/site-packages/marshmallow/schema.py", line 727, in load
    return self._do_load(
  File "/Users/atsumitatsuya/Library/Caches/pypoetry/virtualenvs/python-datavalidation-frameworks-X7pON5WL-py3.9/lib/python3.9/site-packages/marshmallow/schema.py", line 909, in _do_load
    raise exc
marshmallow.exceptions.ValidationError: {'s': ['Unknown field.']}
>>> class M(ma.Schema):
...   s = ma.fields.Str()
...   t = ma.fields.Str(allow_none=False)
...   u = ma.fields.Str(required=True)
...
>>> M().load({})
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/atsumitatsuya/Library/Caches/pypoetry/virtualenvs/python-datavalidation-frameworks-X7pON5WL-py3.9/lib/python3.9/site-packages/marshmallow/schema.py", line 727, in load
    return self._do_load(
  File "/Users/atsumitatsuya/Library/Caches/pypoetry/virtualenvs/python-datavalidation-frameworks-X7pON5WL-py3.9/lib/python3.9/site-packages/marshmallow/schema.py", line 909, in _do_load
    raise exc
marshmallow.exceptions.ValidationError: {'u': ['Missing data for required field.']}
>>> M().load({"u": "hoge"})
{'u': 'hoge'}
>>> M().load({"u": "hoge", "t": None})
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/atsumitatsuya/Library/Caches/pypoetry/virtualenvs/python-datavalidation-frameworks-X7pON5WL-py3.9/lib/python3.9/site-packages/marshmallow/schema.py", line 727, in load
    return self._do_load(
  File "/Users/atsumitatsuya/Library/Caches/pypoetry/virtualenvs/python-datavalidation-frameworks-X7pON5WL-py3.9/lib/python3.9/site-packages/marshmallow/schema.py", line 909, in _do_load
    raise exc
marshmallow.exceptions.ValidationError: {'t': ['Field may not be null.']}
>>> M().load({"u": None})
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/atsumitatsuya/Library/Caches/pypoetry/virtualenvs/python-datavalidation-frameworks-X7pON5WL-py3.9/lib/python3.9/site-packages/marshmallow/schema.py", line 727, in load
    return self._do_load(
  File "/Users/atsumitatsuya/Library/Caches/pypoetry/virtualenvs/python-datavalidation-frameworks-X7pON5WL-py3.9/lib/python3.9/site-packages/marshmallow/schema.py", line 909, in _do_load
    raise exc
marshmallow.exceptions.ValidationError: {'u': ['Field may not be null.']}
>>> class M(ma.Schema):
...   t = ma.fields.Str(allow_none=False, required=False)
...
>>> M().load({"t": None})
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/atsumitatsuya/Library/Caches/pypoetry/virtualenvs/python-datavalidation-frameworks-X7pON5WL-py3.9/lib/python3.9/site-packages/marshmallow/schema.py", line 727, in load
    return self._do_load(
  File "/Users/atsumitatsuya/Library/Caches/pypoetry/virtualenvs/python-datavalidation-frameworks-X7pON5WL-py3.9/lib/python3.9/site-packages/marshmallow/schema.py", line 909, in _do_load
    raise exc
marshmallow.exceptions.ValidationError: {'t': ['Field may not be null.']}
>>> M().load({"t": ""})
{'t': ''}
>>> M().load({})
{}
>>> s = M().load({})
>>> type(s)
<class 'dict'>
>>> class M(ma.Schema):
...   t = ma.fields.Str(allow_none=False, required=False)
...   @ma.post_load
...   def make(self, data, **kwargs):
...     return
  File "<stdin>", line 4
    def make(self, data, **kwargs):
                                   ^
IndentationError: expected an indented block
>>> import jsonschema as js
>>> js.validate(schema={"type" : "object","properties" : {"price" : {"type" : ["number", "null"]}}}, instnaces={})
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: validate() missing 1 required positional argument: 'instance'
>>> js.validate(schema={"type" : "object","properties" : {"price" : {"type" : ["number", "null"]}}}, instnace={})
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: validate() missing 1 required positional argument: 'instance'
>>> js.validate(schema={"type" : "object","properties" : {"price" : {"type" : ["number", "null"]}}}, instance={})
>>> js.validate(schema={"type" : "object","properties" : {"price" : {"type" : ["number", "null"]}}}, instance={"price": None})
>>> js.validate(schema={"type" : "object","properties" : {"price" : {"type" : ["number", "null"]}}}, instance={"price": "hog"})
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/atsumitatsuya/Library/Caches/pypoetry/virtualenvs/python-datavalidation-frameworks-X7pON5WL-py3.9/lib/python3.9/site-packages/jsonschema/validators.py", line 934, in validate
    raise error
jsonschema.exceptions.ValidationError: 'hog' is not of type 'number', 'null'

Failed validating 'type' in schema['properties']['price']:
    {'type': ['number', 'null']}

On instance['price']:
    'hog'
>>> js.validate(schema={"type" : "object","properties" : {"price" : {"type" : ["number", "null"]}}}, instance={"price": 3})
>>> js.validate(schema={"type" : "object","properties" : {"price" : {"type" : ["number", "null"]}}, "required": ["price"]}, instance={"price": 3})
>>> js.validate(schema={"type" : "object","properties" : {"price" : {"type" : ["number", "null"]}}, "required": ["price"]}, instance={})
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/atsumitatsuya/Library/Caches/pypoetry/virtualenvs/python-datavalidation-frameworks-X7pON5WL-py3.9/lib/python3.9/site-packages/jsonschema/validators.py", line 934, in validate
    raise error
jsonschema.exceptions.ValidationError: 'price' is a required property

Failed validating 'required' in schema:
    {'properties': {'price': {'type': ['number', 'null']}},
     'required': ['price'],
     'type': 'object'}

On instance:
    {}
>>> js.validate(schema={"type" : "object","properties" : {"price" : {"type" : ["number", "null"]}}, "required": ["price"]}, instance={"price": None})
>>> js.validate(schema={"type" : "object","properties" : {"price" : {"type" : ["number", "null"]}}, "required": ["price"]}, instance={"price": None})
>>> import typing, attrs
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ModuleNotFoundError: No module named 'attrs'
>>> import typing, attr
>>> @attr.s(auto_attribs=True)
... class C:
...   i: int
...   j: typing.Optional[int]
...   k: int = 3
...
>>> C()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: __init__() missing 2 required positional arguments: 'i' and 'j'
>>> C(i=1)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: __init__() missing 1 required positional argument: 'j'
>>> C(i=1, j=2)
C(i=1, j=2, k=3)
>>> C(i=1, j=None)
C(i=1, j=None, k=3)
>>> C(i=None, j=None)
C(i=None, j=None, k=3)
>>> @attr.s
... class C:
...   x = attr.ib(validator=attr.validators.instance_of(int))
...   y = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(int)))
...   z = attr.ib(default=3, validator=attr.validators.instance_of(int))
...
>>> C()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: __init__() missing 2 required positional arguments: 'x' and 'y'
>>> C(x=1, y=2)
C(x=1, y=2, z=3)
>>> C(x=None, y=2)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<attrs generated init __main__.C-2>", line 6, in __init__
  File "/Users/atsumitatsuya/Library/Caches/pypoetry/virtualenvs/python-datavalidation-frameworks-X7pON5WL-py3.9/lib/python3.9/site-packages/attr/validators.py", line 35, in __call__
    raise TypeError(
TypeError: ("'x' must be <class 'int'> (got None that is a <class 'NoneType'>).", Attribute(name='x', default=NOTHING, validator=<instance_of validator for type <class 'int'>>, repr=True, eq=True, order=True, hash=None, init=True, metadata=mappingproxy({}), type=None, converter=None, kw_only=False, inherited=False, on_setattr=None), <class 'int'>, None)
>>> C(x=1, y=2)
C(x=1, y=2, z=3)
>>> C(x=1, y=None)
C(x=1, y=None, z=3)
>>> C(x=1)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: __init__() missing 1 required positional argument: 'y'
