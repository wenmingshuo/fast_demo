# -*- coding: utf-8 -*-
from pydantic import BaseModel
from typing import Optional, Any

class ResponseModel(BaseModel):
    code: int = 0
    msg: str = "成功"
    data: Optional[Any] = None
