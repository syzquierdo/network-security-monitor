import logging
import subprocess
import re
from datetime import datetime

logging.basicConfig(
    filename="security_events.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

def ping_device(ip_address):
    result = subprocess.run(
        ["ping", "-c", "1", ip_address],
        capture_output=True,
        text=True
    )

    status = "UP" if result.returncode == 0 else "DOWN"
    latency = None

    if status == "UP":
        match = re.search(r"time[=<]([\d.]+) ms", result.stdout)

        if match:
            latency = float(match.group(1))

    return {
        "ip_address": ip_address,
        "status": status,
        "latency_ms": latency,
        "timestamp": datetime.now().isoformat()
    }

devices = [
      {
        "ip_address": "127.0.0.1",
        "name": "Localhost",
        "trusted": True
    },
    {
        "ip_address": "192.168.1.1",
        "name": "Router",
        "trusted": True
    },
    {
        "ip_address": "192.168.1.46",
        "name": "Raspberry Pi",
        "trusted": True
    },
    {
        "ip_address": "192.168.1.250",
        "name": "Unknown Test Device",
        "trusted": False
    }
]



def monitor_all_devices():
    results = []

    for device in devices:
        result = ping_device(device["ip_address"])

        result["name"] = device["name"]
        result["trusted"] = device["trusted"]

        if not device["trusted"]:
            result["security_status"] = "UNKNOWN_DEVICE"
            logging.critical(
                f'Unknown device detected: {device["ip_address"]}'
            )

        elif result["status"] == "DOWN":
            result["security_status"] = "TRUSTED_DEVICE_DOWN"
            logging.warning(
                f'Trusted device offline: {device["name"]} '
                f'({device["ip_address"]})'
            )

        else:
            result["security_status"] = "TRUSTED"
            logging.info(
                f'Trusted device online: {device["name"]} '
                f'({device["ip_address"]})'
            )

        results.append(result)

    return results
