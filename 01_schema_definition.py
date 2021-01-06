"""
スキーマ定義に関する比較
"""
import typing
import pydantic as pd


################################################################################
# Pydantic
################################################################################
print("=== Pydantic")


class PydanticModle1(pd.BaseModel):
    # Required
    i: int
    # Nullable & Required
    j: typing.Optional[int] = pd.Field(...)
    # Optional
    k: int = 0

print(PydanticModle1(i=1, j=None))

