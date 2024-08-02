# -*- coding: utf-8 -*-
import asyncio
from fastapi import APIRouter, Query, BackgroundTasks
from fastapi_utils.cbv import cbv
from starlette.requests import Request
from tortoise.expressions import Q
from tortoise.functions import Count
from tortoise import Tortoise
from apps.admin.models import OpAssetGroupAccount
from apps.admin.resp import ResponseModel
from starlette.responses import JSONResponse
from apps.admin.utils import test

AdminRouter = APIRouter(tags=['后台'])


@cbv(AdminRouter)
class OeOpenAccountServer:
    request: Request

    @AdminRouter.get('/asset_group_accounts', description='资产组')
    async def asset_group_accounts(self,  background_tasks: BackgroundTasks, q=Query(""), limit=Query(10)):
        ids = await OpAssetGroupAccount.filter(
            Q(asset_group_id__icontains=q) | Q(asset_group_name__icontains=q)
        ).limit(int(limit)).order_by('-id').values_list("id", flat=True)
        res = OpAssetGroupAccount.filter(id__in=ids).annotate(
            count=Count('asset_group_account_details'),
        ).group_by('id')
        res = await res.values()
        background_tasks.add_task(test)
        return ResponseModel(data=res)

    @AdminRouter.get('/table', description='table')
    async def table(self):
        await Tortoise.generate_schemas()
        return JSONResponse({"code": 0})

    @AdminRouter.get('/test', description='test')
    async def test(self):
        await asyncio.sleep(1000)
        return JSONResponse({"code": 0})

    @AdminRouter.get('/test1111', description='test11111')
    async def test11(self):
        ids = await OpAssetGroupAccount.filter().limit(10).order_by('-id').values_list("id", flat=True)
        print(ids)
        await asyncio.sleep(60)
        res = await OpAssetGroupAccount.filter(id__in=ids).annotate(count=Count('asset_group_account_details')).values()
        return ResponseModel(data=res)

    @AdminRouter.get('/dev_op', description='1232133434')
    async def dev_op(self):
        await asyncio.sleep(1000)
        return JSONResponse({"code": 0})

    @AdminRouter.get('/dev_op_2', description='42312323')
    async def dev_op_2(self):
        await asyncio.sleep(1000)
        return JSONResponse({"code": 0})