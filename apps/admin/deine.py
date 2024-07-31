# -*- coding: utf-8 -*-
# 绑定解绑
from cuenum import BaseEnum


class OperateType(BaseEnum):
    BIND = ('1', '绑定')
    UNBIND = ('2', '解绑')