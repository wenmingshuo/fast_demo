# -*- coding: utf-8 -*-
from tortoise.models import Model
from tortoise import fields


class OpAssetGroupAccount(Model):
    id = fields.IntField(primary_key=True)
    created_time = fields.DatetimeField(description='创建时间')
    update_time = fields.DatetimeField(description='更新时间')
    is_delete = fields.BooleanField(default=False)
    request_id = fields.CharField(max_length=100, description='请求编号')
    asset_group_id = fields.CharField(max_length=100, description='资产组ID')
    asset_group_name = fields.CharField(max_length=100, description='资产组名称')
    operate_type = fields.CharField(max_length=20, description='操作类型')
    operate_result = fields.CharField(max_length=20, description='操作结果')
    operate_time = fields.DatetimeField(description='操作时间')
    user_id = fields.IntField(description='用户id')

    class Meta:
        table = "op_meta_asset_group_accounts"


# 资产组账户子表(绑定/解绑)
class OpAssetGroupAccountDetail(Model):
    __tablename__ = 'op_meta_asset_group_account_details'

    account_id = fields.CharField(max_length=32, description='广告账户ID')
    operate_result = fields.CharField(max_length=20, description='操作结果')
    operate_time = fields.DatetimeField(description='操作时间')
    remark = fields.CharField(max_length=2000, description='备注')
    asset_group_account = fields.ForeignKeyField("models.OpAssetGroupAccount", related_name="asset_group_account_details")

    class Meta:
        table = "op_meta_asset_group_account_details"