import asyncio
import pytest

from cpx_client.client import CPXClient


@pytest.mark.asyncio
async def test__update_service_status(test_app, aiohttp_server):
    await aiohttp_server(test_app, port=32768)
    client = CPXClient(60)

    # Initialised the services_status of test_services_1
    assert client.services_status["test_services_1"] == ["Unhealthy"]

    client._update_service_status("test_services_1", "Healthy")
    assert client.services_status["test_services_1"] == ["Healthy"]


@pytest.mark.asyncio
async def test__get_service_stat(
    test_app, aiohttp_server, test_ip_address_list, test_service_1_stat_object
):
    await aiohttp_server(test_app, port=32768)
    client = CPXClient(60)

    test_service_1_ip_address = test_ip_address_list[0]

    service_stat = await client._get_service_stat(test_service_1_ip_address)

    assert service_stat == test_service_1_stat_object


@pytest.mark.asyncio
async def test__get_service_ip_address_list(
    test_app, aiohttp_server, test_ip_address_list
) -> list:
    await aiohttp_server(test_app, port=32768)
    client = CPXClient(60)

    res_json = await client._get_service_ip_address_list()

    assert res_json == test_ip_address_list


@pytest.mark.asyncio
@pytest.mark.parametrize("test_target_service_name", [None, "test_service_1"])
async def test_get_services_dashboard(
    test_target_service_name,
    test_app,
    aiohttp_server,
    test_service_dashboard_object,
    test_service_1_dashboard_object,
):
    await aiohttp_server(test_app, port=32768)
    client = CPXClient(60)
    service_stat_dashboard = await client.get_services_dashboard(
        test_target_service_name
    )

    if test_target_service_name:
        assert service_stat_dashboard == test_service_1_dashboard_object
    else:
        assert service_stat_dashboard == test_service_dashboard_object


@pytest.mark.asyncio
@pytest.mark.parametrize("data_col", ["cpu", "memory"])
async def test_get_average(
    data_col,
    test_app,
    aiohttp_server,
    test_service_2_cpu_average,
    test_service_2_memory_average,
):
    await aiohttp_server(test_app, port=32768)
    client = CPXClient(60)
    average = await client.get_average(data_col, "test_service_2")
    if data_col == "cpu":
        assert average == test_service_2_cpu_average
    elif data_col == "memory":
        assert average == test_service_2_memory_average
