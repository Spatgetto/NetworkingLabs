# VLAN Checker

## Objective

Use Nornir and NAPALM to retrieve VLAN configurations from multiple switches and compare them to identify discrepancies and ensure VLAN consistency across the network.

## Key Technologies

- Python
- Nornir
- NAPALM
- Cisco IOS

## Relevant Scripts

`config.yml` is used by Nornir to define the inventory configuration, including the inventory, runner, and plugin settings used to manage network devices.

`inventory/defaults.yml` specifies `ios` as the default platform for network devices.

`inventory/groups.yml` defines the `switches` group, which specifies the connection settings shared by its members, including port 22, username `cisco`, and password `cisco`.

`inventory/hosts.yml` defines each switch, assigns its management IP address, and associates it with the `switches` group.

`main.py` uses Nornir and NAPALM to retrieve VLAN configurations from every switch as structured data. It then compares the VLAN data across devices to identify discrepancies between their configurations.

## Verification

Run the following checks to verify that Nornir can connect to the switches and retrieve their VLAN configurations.

| Command | What to look for |
|---|---|
| `ping <switch_management_ip>` | Confirms that each switch is reachable from the control node |
| `ssh cisco@<switch_management_ip>` | Confirms SSH connectivity and credentials |
| `show vlan brief` | Displays VLAN IDs, names, and associated access ports on each switch |
| `show running-config \| section vlan` | Displays VLAN-related configuration |
| `python main.py` | Confirms that Nornir successfully connects to devices, retrieves VLAN data, and compares configurations |

Verified that Nornir successfully loaded the inventory and connected to all switches.

Confirmed that NAPALM successfully retrieved VLAN configurations as structured data.

Compared VLAN configurations across switches and verified that discrepancies were correctly identified.

Cross-referenced the script's results against `show vlan brief` on individual switches to confirm the accuracy of the comparison.

## Conclusion

- **Network automation:** Used Nornir to manage and gather configuration information from multiple switches simultaneously.
- **Structured data collection:** Used NAPALM to retrieve VLAN configurations in a structured format rather than manually parsing CLI output.
- **Configuration auditing:** Developed a Python script to compare VLAN configurations across devices and identify inconsistencies.
- **Inventory management:** Gained experience organizing network devices using Nornir's inventory system, including hosts, groups, and defaults.
- **Configuration consistency:** Explored how network automation can simplify configuration auditing and help maintain consistent VLAN configurations across network infrastructure.