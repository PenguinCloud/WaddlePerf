#! /usr/bin/env python3

import subprocess
import platform
import json

class MTUFinder:
    def __init__(self, host):
        self.host = host
        self.results = []

    def run(self):
        min_size, max_size = self.test_mtu(1000, 1900, 100)
        print("Range Found: ", min_size, max_size)
        min_size, max_size = self.test_mtu(min_size, max_size, 20)
        print("Range Found: ", min_size, max_size)
        min_size, max_size = self.test_mtu(min_size, max_size, 5)
        print("Range Found: ", min_size, max_size)
        min_size, max_size = self.test_mtu(min_size, max_size, 1)
        print("Range Found: ", min_size, max_size)
        return {"maxMTU": max_size}

    def test_mtu(self, min_size: int = 1000, max_size: int = 1900, step_size: int = 1):
        for c in range(min_size, max_size, step_size):
            if platform.system() == "Windows":
                result = subprocess.run(
                    ["ping", "-n", "1", "-f", "-l", str(c), self.host],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
            else:
                result = subprocess.run(
                    ["ping", "-c", "1", "-M", "do", "-s", str(c), self.host],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
            self.results.append({
                "size": c,
                "success": result.returncode == 0,
                "output": result.stdout.decode()
            })
            if result.returncode != 0:
                return c - step_size, c

if __name__ == "__main__":
    host = "8.8.8.8"  # Example host, you can change it to the desired host
    mtu_finder = MTUFinder(host)
    max_mtu = mtu_finder.run()
    print(f"The maximum MTU size for {host} is {max_mtu['maxMTU']} bytes")
    print(json.dumps(mtu_finder.results, indent=4))