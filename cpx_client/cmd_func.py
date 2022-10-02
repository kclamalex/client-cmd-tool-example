import asyncio
import time

from cpx_client.client import BaseClient
from cpx_client.utils import clear_stdout


def _get_services_dashboard_str(client: BaseClient, target_service_name: str) -> str:

    loop = asyncio.get_event_loop()
    services_dashboard = loop.run_until_complete(
        client.get_services_dashboard(target_service_name)
    )

    services_dashboard_str = str(services_dashboard)

    return services_dashboard_str


def show_services_dashboard(client: BaseClient, target_service_name: str):
    services_dashboard_str = _get_services_dashboard_str(client, target_service_name)
    print(services_dashboard_str)


def watch_services(client: BaseClient, update_rate_sec: int, target_service_name: str):
    while True:
        try:
            services_dashboard_str = _get_services_dashboard_str(
                client, target_service_name
            )
            print(services_dashboard_str)
            time.sleep(update_rate_sec)
            clear_stdout(services_dashboard_str)
        except KeyboardInterrupt:
            break


def get_average(client: BaseClient, data_col: str, service_name: str):
    loop = asyncio.get_event_loop()
    average = loop.run_until_complete(client.get_average(data_col, service_name))
    print(f"The average {data_col} of {service_name}: {average}%")
