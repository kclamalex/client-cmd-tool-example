import pytest
from aiohttp import web

from cpx_client.model import ServiceStat, ServiceStatDashboard


@pytest.fixture
def test_ip_address_list():
    test_ip_address_list = [
        "10.58.1.9",
        "10.58.1.25",
        "10.58.1.28",
        "10.58.1.26",
        "10.58.1.27",
    ]
    return test_ip_address_list


@pytest.fixture
def test_service_stat_dict():
    service_stat_dict = {
        "10.58.1.9": {
            "cpu": "99%",
            "memory": "99%",
            "service": "test_service_1",
        },
        "10.58.1.25": {
            "cpu": "25%",
            "memory": "40%",
            "service": "test_service_2",
        },
        "10.58.1.28": {
            "cpu": "35%",
            "memory": "40%",
            "service": "test_service_2",
        },
        "10.58.1.26": {
            "cpu": "35%",
            "memory": "65%",
            "service": "test_service_3",
        },
        "10.58.1.27": {
            "cpu": "12%",
            "memory": "23%",
            "service": "test_service_3",
        },
    }
    return service_stat_dict


@pytest.fixture
def test_service_1_stat_object(test_service_stat_dict):
    for ip_address in test_service_stat_dict:
        service_stat = test_service_stat_dict[ip_address]
        service_name = service_stat["service"]

        if service_name == "test_service_1":
            status = ["Unhealthy"]
            cpu = service_stat["cpu"].rstrip("%")
            memory = service_stat["memory"].rstrip("%")
            service_stat = ServiceStat(
                ip_address=ip_address,
                service_name=service_name,
                status=status,
                cpu=cpu,
                memory=memory,
            )
            break
    return service_stat


@pytest.fixture
def test_service_dashboard_object(test_service_stat_dict):
    service_stat_list = []
    for ip_address in test_service_stat_dict:
        service_stat = test_service_stat_dict[ip_address]
        service_name = service_stat["service"]
        cpu = service_stat["cpu"].rstrip("%")
        memory = service_stat["memory"].rstrip("%")
        if service_name == "test_service_1":
            status = ["Unhealthy"]
        else:
            status = ["Healthy"]
        service_stat = ServiceStat(
            ip_address=ip_address,
            service_name=service_name,
            status=status,
            cpu=cpu,
            memory=memory,
        )
        service_stat_list.append(service_stat)
    return ServiceStatDashboard(service_stat_list=service_stat_list)


@pytest.fixture
def test_service_1_dashboard_object(test_service_1_stat_object):
    service_stat_list = []
    service_stat_list.append(test_service_1_stat_object)
    return ServiceStatDashboard(service_stat_list=service_stat_list)


@pytest.fixture
def test_service_1_stat_str(test_service_stat_dict):

    dashboard_str = (
        f"{'IP':<39} {'Service':<30} {'Status':<9} {'CPU':<4} {'Memory':<4}\n"
    )
    dashboard_str += "------------------------------------------------------------------------------------------------\n"
    for ip_address in test_service_stat_dict:
        service_stat = test_service_stat_dict[ip_address]
        service_name = service_stat["service"]
        if service_name == "test_service_1":
            cpu = service_stat["cpu"].rstrip("%")
            memory = service_stat["memory"].rstrip("%")
            status = "Unhealthy"

            dashboard_str += f"{ip_address:<39} {service_name:<30} {status:<9} {cpu:>3}% {memory:>3}%\n"
    return dashboard_str


@pytest.fixture
def test_service_1_stat_print_str(test_service_1_stat_str):
    test_service_1_stat_str += "\n"
    return test_service_1_stat_str


@pytest.fixture
def test_service_stat_str(test_service_stat_dict):

    dashboard_str = (
        f"{'IP':<39} {'Service':<30} {'Status':<9} {'CPU':<4} {'Memory':<4}\n"
    )
    dashboard_str += "------------------------------------------------------------------------------------------------\n"
    for ip_address in test_service_stat_dict:
        service_stat = test_service_stat_dict[ip_address]
        service_name = service_stat["service"]
        cpu = service_stat["cpu"].rstrip("%")
        memory = service_stat["memory"].rstrip("%")
        if service_name == "test_service_1":
            status = "Unhealthy"
        else:
            status = "Healthy"

        dashboard_str += (
            f"{ip_address:<39} {service_name:<30} {status:<9} {cpu:>3}% {memory:>3}%\n"
        )
    return dashboard_str


@pytest.fixture
def test_service_stat_print_str(test_service_stat_str):
    test_service_stat_str += "\n"
    return test_service_stat_str


@pytest.fixture
def test_service_2_cpu_average(test_service_stat_dict):
    average_sum = 0
    average_len = 0
    for ip_address in test_service_stat_dict:
        service_stat = test_service_stat_dict[ip_address]
        service_name = service_stat["service"]
        if service_name == "test_service_2":
            cpu = service_stat["cpu"].rstrip("%")
            average_sum += int(cpu)
            average_len += 1
    average = average_sum / average_len
    average = round(average, 1)
    return average


@pytest.fixture
def test_service_2_cpu_average_str(test_service_2_cpu_average):
    return f"The average cpu of test_service_2: {test_service_2_cpu_average}%\n"


@pytest.fixture
def test_service_2_memory_average(test_service_stat_dict):
    average_sum = 0
    average_len = 0
    for ip_address in test_service_stat_dict:
        service_stat = test_service_stat_dict[ip_address]
        service_name = service_stat["service"]
        if service_name == "test_service_2":
            memory = service_stat["memory"].rstrip("%")
            average_sum += int(memory)
            average_len += 1
    average = average_sum / average_len
    average = round(average, 1)
    return average


@pytest.fixture
def test_service_2_memory_average_str(test_service_2_memory_average):
    return f"The average memory of test_service_2: {test_service_2_memory_average}%\n"


@pytest.fixture
def test_app(test_ip_address_list, test_service_stat_dict):
    async def get_servers(request):

        res_json = web.json_response(data=test_ip_address_list)
        return res_json

    async def get_service(request):
        ip = str(request.rel_url).lstrip("/")
        res_json = web.json_response(data=test_service_stat_dict[ip])
        return res_json

    test_app = web.Application()
    test_app.router.add_get("/servers", get_servers)
    test_app.router.add_resource("/{ip}", name="ip").add_route("GET", get_service)
    return test_app
