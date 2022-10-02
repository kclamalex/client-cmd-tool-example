from abc import abstractmethod
from collections import defaultdict

import cpx_client.requests as requests
from cpx_client.model import ServiceStat, ServiceStatDashboard


class BaseClient:
    """
    Base client to call server
    """

    def __init__(self, base_url: str, timeout_sec: int):
        self.base_url: str = base_url
        self.timeout_sec: int = timeout_sec
        # A small trick to use pointer similar behaviour in python
        self.services_status: dict = defaultdict(lambda: ["Unhealthy"])

    @abstractmethod
    async def _get_service_ip_address_list(self) -> list:
        raise NotImplementedError

    @abstractmethod
    async def _get_service_stat(self, service_ip_address: str) -> ServiceStat:
        raise NotImplementedError

    def _update_service_status(self, service_name, status):
        # A small trick to use pointer similar behaviour in python
        self.services_status[service_name][0] = status

    async def get_services_dashboard(
        self, target_service_name: str
    ) -> ServiceStatDashboard:
        ip_address_list = await self._get_service_ip_address_list()
        services_counter: dict = defaultdict(int)
        service_stat_list = []

        for ip_address in ip_address_list:
            service_stat: ServiceStat = await self._get_service_stat(ip_address)
            service_name = service_stat.service_name

            if target_service_name and service_name != target_service_name:
                continue
            services_counter[service_name] += 1
            if services_counter[service_name] > 1:
                self._update_service_status(service_name, status="Healthy")

            service_stat_list.append(service_stat)

        service_stat_list.sort(key=lambda service_stat: service_stat.service_name)

        service_dashboard = ServiceStatDashboard(service_stat_list=service_stat_list)

        return service_dashboard

    async def get_average(
        self,
        data_col: str,
        service_name: str,
    ) -> float:
        average_sum = 0
        average_len = 0
        ip_address_list = await self._get_service_ip_address_list()

        for ip_address in ip_address_list:
            service_stat: ServiceStat = await self._get_service_stat(ip_address)
            if service_stat.service_name == service_name:
                try:
                    data = getattr(service_stat, data_col)
                    if type(data) not in {int, float}:
                        raise ValueError(
                            f"Data used in get_average should be integer or float. The type it get: {type(data)}"
                        )
                    average_sum += data
                    average_len += 1
                except AttributeError:
                    raise AttributeError(
                        f"No data column named {data_col}"
                    ) from AttributeError
                except Exception as e:
                    raise e

        average = average_sum / average_len
        return round(average, 1)


class CPXClient(BaseClient):
    """
    CPX client to call CPX server
    """

    def __init__(self, timeout_sec: int):
        base_url: str = "http://localhost:32768"
        super().__init__(base_url=base_url, timeout_sec=timeout_sec)

    async def _get_service_ip_address_list(self) -> list:
        url = f"{self.base_url}/servers"
        service_ip_address_list = await requests.get(url, self.timeout_sec)
        return service_ip_address_list

    async def _get_service_stat(self, service_ip_address: str) -> ServiceStat:
        url = f"{self.base_url}/{service_ip_address}"
        res_json = await requests.get(url, self.timeout_sec)
        service_name = res_json.get("service", "")
        cpu = res_json.get("cpu", 0).rstrip("%")
        memory = res_json.get("memory", 0).rstrip("%")
        service_stat = ServiceStat(
            ip_address=service_ip_address,
            service_name=service_name,
            status=self.services_status[service_name],
            cpu=int(cpu),
            memory=int(memory),
        )
        return service_stat
