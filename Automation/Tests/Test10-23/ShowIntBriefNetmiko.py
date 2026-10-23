from netmiko import ConnectHandler

devices = [
    {"device_type": "cisco_ios", "host": "10.99.99.10", "username": "cisco", "password": "cisco"},
    {"device_type": "cisco_ios", "host": "10.99.99.20", "username": "cisco", "password": "cisco"},
    {"device_type": "cisco_ios", "host": "10.99.99.30", "username": "cisco", "password": "cisco"},
    {"device_type": "cisco_ios", "host": "10.99.99.40", "username": "cisco", "password": "cisco"},
]

for device in devices:
    net_connect = ConnectHandler(**device)
    output = net_connect.send_command("show ip interface brief")
    print(f"Output from {device['host']}:\n{output}\n")
    net_connect.disconnect()

