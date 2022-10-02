import asyncio
import pytest

import cpx_client.requests as requests


@pytest.mark.asyncio
async def test__request(test_app, test_ip_address_list, aiohttp_server):
    await aiohttp_server(test_app, port=32768)
    test_url = "http://localhost:32768/servers"
    res_json = await requests._request(url=test_url, method="GET", timeout_sec=30)
    assert res_json == test_ip_address_list


@pytest.mark.asyncio
async def test_get(test_app, test_ip_address_list, aiohttp_server):
    await aiohttp_server(test_app, port=32768)
    test_url = "http://localhost:32768/servers"
    res_json = await requests.get(url=test_url, timeout_sec=30)
    assert res_json == test_ip_address_list
