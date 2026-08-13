import subprocess


def ping_device(ip_address):
    result = subprocess.run(
        ["ping", "-c", "1", ip_address],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        return "UP"
    else:
        return "DOWN"


devices = [
    "127.0.0.1",
    "192.168.1.1",
    "192.168.1.46"
]

for device_ip in devices:
    status = ping_device(device_ip)
    print(f"Device {device_ip} is {status}")
