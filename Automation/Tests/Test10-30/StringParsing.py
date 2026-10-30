import json, os
from netmiko import ConnectHandler

defaults = {
    "device_type" : "cisco_ios",
    "username" : "cisco",
    "password" : "cisco"
}

devices = {
    "SW1" : { "host" : "10.99.99.10" },
    "SW2" : { "host" : "10.99.99.20" },
    "R1" : { "host" : "10.99.99.30" },
    "R2" : { "host" : "10.99.99.40" }
}

for device, info in devices.items():
    net_connect = ConnectHandler(
        device_type = defaults["device_type"],
        username = defaults["username"],
        password = defaults["password"],
        host = info["host"]
    )

    # USING use_textfsm THAT RETURNS STRUCTURED DATA

    # output = net_connect.send_command(
    #     "show ip int brief",
    #     use_textfsm=True
    # )

    # print(device)
    
    # for interface in output:
    #     if interface["proto"] == "down":
    #         print("!!! " + interface["interface"] + " is down!")
    #     elif interface["status"] == "up":
    #         print(interface["interface"] + " is up")
    
    print(device)
    
    output = net_connect.send_command(
        "show ip int brief"
    )

    lines = output.splitlines()
    lines.pop(0)

    for line in lines:
        columns = line.split()

        interface = {
            "name" : columns[0],
            "ip" : columns[1],
            "status" : " ".join(columns[4:-1]),
            "protocol" : columns[-1]
        }

        devices[device]["interfaces"] = interface

os.makedirs("./Output", exist_ok=True)
with open("./Output/device_interfaces.json", "w") as file:
    json.dump(devices, file, indent=4)