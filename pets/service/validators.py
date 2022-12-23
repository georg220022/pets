from uuid import UUID
from typing import Union, Optional


def validate_uuid(
    data: Optional[str | list], many: bool = False
) -> Optional[bool | str] | Union[list[dict], list[str]]:
    if not many:
        try:
            val = UUID(data, version=4)
        except ValueError:
            return False
        return val
    errors = []
    white_list = []
    for obj in data:
        try:
            val = UUID(obj, version=4)
            white_list.append(val)
        except ValueError:
            errors.append(dict(id=obj, error="Не верный формат uuid"))
    return errors, white_list
