import argparse

from cpx_client.client import CPXClient
from cpx_client.cmd_func import show_services_dashboard, watch_services, get_average
from cpx_client.errors import CPXInternalError


def cmd(
    operator: str,
    target: str,
    data_col: str,
    target_service_name: str,
    timeout_sec: int,
    update_rate: int,
):
    client = CPXClient(timeout_sec)
    if operator == "get":
        if target == "services":
            show_services_dashboard(client, target_service_name)
        elif target == "average":
            if not data_col or not target_service_name:
                raise CPXInternalError(
                    "'--data' and '--service' are required for 'get average'"
                )
            get_average(client, data_col, target_service_name)
        else:
            raise CPXInternalError(
                f"Unknown target '{target}'. Valid target options: 'services', 'average' for 'get'"
            )
    elif operator == "watch":
        if target == "services":
            watch_services(client, update_rate, target_service_name)
        else:
            raise CPXInternalError(
                f"Unknown target '{target}'. Valid target options: 'services' for 'watch'"
            )
    else:
        raise CPXInternalError(
            f"Unknown operator '{operator}'. Valid operator options: 'get', 'watch'"
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "operator",
        help="the option to select which operation to do to the target [options: get, watch] (Required)",
        type=str,
    )
    parser.add_argument(
        "target",
        help="the target to interact [options: services, average] (Required)",
        type=str,
    )
    parser.add_argument(
        "-n",
        help="the update rate for watch operation [watch services]",
        type=int,
        default=2,
    )
    parser.add_argument(
        "--data",
        help="the data you would to like to get its average [get average] (default: None)",
        type=str,
        default=None,
    )
    parser.add_argument(
        "--service",
        help="the service name you would to like to get its status [get services] or average [get average] (default: None)",
        type=str,
        default=None,
    )
    parser.add_argument(
        "--timeout",
        help="the request timeout limit (default: 60s)",
        type=int,
        default=60,
    )

    args = parser.parse_args()

    cmd(args.operator, args.target, args.data, args.service, args.timeout, args.n)
