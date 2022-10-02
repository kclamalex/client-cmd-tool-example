import time
import random
import sys

from cpx_client.utils import clear_stdout


def test():
    while True:
        try:
            res = (
                f"{'IP':<40}|{'Service':<30}|{'Status':<9}|{'CPU':<4}|{'Memory':<4}\n"
                f"{random.randint(0,100):<40}|{random.randint(0,100):<30}|{random.randint(0,100):<9}|{random.randint(0,100):<3}%|{random.randint(0,100):<3}%\n"
                f"{random.randint(0,100):<40}|{random.randint(0,100):<30}|{random.randint(0,100):<9}|{random.randint(0,100):<3}%|{random.randint(0,100):<3}%\n"
                f"{random.randint(0,100):<40}|{random.randint(0,100):<30}|{random.randint(0,100):<9}|{random.randint(0,100):<3}%|{random.randint(0,100):<3}%\n"
                f"{random.randint(0,100):<40}|{random.randint(0,100):<30}|{random.randint(0,100):<9}|{random.randint(0,100):<3}%|{random.randint(0,100):<3}%\n"
            )
            print(res)
            time.sleep(2)
            clear_stdout(res)
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    test()
