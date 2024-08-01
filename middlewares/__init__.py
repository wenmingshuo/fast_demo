# -*- coding: utf-8 -*-
import json
import sys
import threading
import traceback
import random
import string
import time
from starlette.requests import Request
from starlette.concurrency import iterate_in_threadpool
from starlette.middleware.cors import CORSMiddleware
from fastapi.middleware.wsgi import WSGIMiddleware

def middleware_init(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["GET", 'POST', 'PUT', 'DELETE'],
        allow_headers=["*"],
    )


    # 校验token
    @app.middleware('http')
    async def auth_verify(request: Request, call_next):
        if request.url.path in [
            '/docs',
            '/openapi.json',
            '/api/v1/common/result_saver'
        ]:
            response = await call_next(request)
            return response
        try:
            print(222222)
            start_time = time.time()
            response = await call_next(request)
            content_type = response.headers.get('content-type', '')
            status_code = response.status_code
            response_body = [chunk async for chunk in response.body_iterator]
            print(response_body)
            response.body_iterator = iterate_in_threadpool(iter(response_body))
            json_res = json.loads(b''.join(response_body).decode())

            return response
        except Exception as e:
            idem = ''.join(random.choices(
                string.ascii_uppercase + string.digits, k=6))
            start_time = time.time()
            process_time = (time.time() - start_time) * 1000
            formatted_process_time = '{0:.2f}'.format(process_time)
            exc_type, exc_value, exc_traceback = sys.exc_info()
            tb_info = traceback.extract_tb(exc_traceback)
            filename, line, func, text = tb_info[-1]
            log_str = f"rid={idem} start request {request.method} " \
                      f"request_user={request.state.user.real_name if hasattr(request.state, 'user') else '匿名用户'} " \
                      f"path={request.url.path} " \
                      f"completed_in={formatted_process_time}ms " \
                      f"Line number={line}"

    WSGIMiddleware(app)
