import asyncio
from typing import Coroutine

import aiohttp
from aiohttp.web import HTTPClientError, HTTPServerError

from cpx_client.errors import (
    CPXNotImplementedError,
    CPXHttpClientError,
    CPXHttpServerError,
    CPXUnknownError,
)


async def _request(
    url: str, method: str, timeout_sec: int, *args, **kwargs
) -> Coroutine:
    timeout = aiohttp.ClientTimeout(timeout_sec)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        http_methods = {
            "GET": session.get,
        }
        if method not in http_methods:
            raise CPXNotImplementedError

        try:
            async with http_methods[method](url, *args, **kwargs) as res:
                res_json = await res.json()
                if type(res_json) == dict:
                    if error_message := res_json.get("error"):
                        raise CPXHttpClientError(error_message)
                return res_json
        except HTTPClientError as client_error:
            raise CPXHttpClientError(client_error)
        except HTTPServerError as server_error:
            raise CPXHttpServerError(server_error)
        except Exception as e:
            raise CPXUnknownError(e)


async def get(url: str, timeout_sec: int, *args, **kwargs) -> dict:
    return await _request(url, "GET", timeout_sec, *args, **kwargs)
