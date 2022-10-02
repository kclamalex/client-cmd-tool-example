import asyncio
import nest_asyncio

nest_asyncio.apply()

import io
from unittest.mock import patch

import pytest

from cpx_client.cmd_func import (
    _get_services_dashboard_str,
    show_services_dashboard,
    get_average,
)

from cpx_client.client import CPXClient


@pytest.mark.asyncio
@pytest.mark.parametrize("test_target_service_name", [None, "test_service_1"])
async def test__get_services_dashboard_str(
    test_target_service_name,
    test_app,
    test_service_stat_str,
    test_service_1_stat_str,
    aiohttp_server,
):
    await aiohttp_server(test_app, port=32768)
    client = CPXClient(60)
    dashboard_str = _get_services_dashboard_str(client, test_target_service_name)
    if test_target_service_name:
        assert test_service_1_stat_str == dashboard_str
    else:
        assert test_service_stat_str == dashboard_str


@pytest.mark.asyncio
@pytest.mark.parametrize("test_target_service_name", [None, "test_service_1"])
async def test_show_services_dashboard(
    test_target_service_name,
    test_app,
    test_service_stat_print_str,
    test_service_1_stat_print_str,
    aiohttp_server,
):
    await aiohttp_server(test_app, port=32768)
    client = CPXClient(60)
    with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
        show_services_dashboard(client, test_target_service_name)
        if test_target_service_name:
            assert test_service_1_stat_print_str == mock_stdout.getvalue()
        else:
            assert test_service_stat_print_str == mock_stdout.getvalue()


@pytest.mark.asyncio
@pytest.mark.parametrize("data_col", ["cpu", "memory"])
async def test_get_average(
    data_col,
    test_app,
    aiohttp_server,
    test_service_2_cpu_average_str,
    test_service_2_memory_average_str,
):
    await aiohttp_server(test_app, port=32768)
    client = CPXClient(60)
    with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
        get_average(client, data_col, "test_service_2")
        if data_col == "cpu":
            assert test_service_2_cpu_average_str == mock_stdout.getvalue()
        elif data_col == "memory":
            assert test_service_2_memory_average_str == mock_stdout.getvalue()
