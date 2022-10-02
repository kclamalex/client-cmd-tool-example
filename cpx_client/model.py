from typing import Union
from ipaddress import IPv4Address, IPv6Address

from pydantic import BaseModel


class ServiceStat(BaseModel):
    ip_address: Union[IPv4Address, IPv6Address]
    service_name: str
    status: list  # A small trick to use pointer similar behaviour in python
    cpu: int
    memory: int

    def __str__(self):
        service_name = (
            self.service_name[:27] + "..."
            if self.service_name[30:]
            else self.service_name[:30]
        )
        return f"{str(self.ip_address):<39} {service_name:<30} {self.status[0]:<9} {self.cpu:>3}% {self.memory:>3}%"


class ServiceStatDashboard(BaseModel):
    service_stat_list: list[ServiceStat]

    def __str__(self):
        dashboard_str = ""
        # The total width of the dashboard
        dashboard_width = 49 + 30 + 9 + 4 + 4
        header = f"{'IP':<39} {'Service':<30} {'Status':<9} {'CPU':<4} {'Memory':<4}"
        dashboard_split_line = "-" * dashboard_width

        dashboard_str += header + "\n"
        dashboard_str += dashboard_split_line + "\n"

        for service_stat in self.service_stat_list:
            dashboard_str += str(service_stat) + "\n"

        return dashboard_str
