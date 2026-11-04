# Topology Drawer

## Objective

Use Python, Ansible, and LLDP to automatically discover network devices and generate a network topology diagram based on their connections.

## Key Technologies

- Ansible
- Python
- LLDP
- Graphviz

## Relevant Scripts

`ansible.cfg` is used to disable host key checking by default.

`hosts.yml` is an Ansible inventory file that defines the devices managed by Ansible. It contains two groups: `switches` and `routers`.

`enable_lldp.yml` is an Ansible playbook that enables LLDP on all network devices.

`discover_lldp.yml` is an Ansible playbook that uses the IOS command module to execute `show lldp neighbors` on all devices. The output is printed to the console and saved to the `./tmp` directory as `(device_name)_lldp_output.txt`.

`write_mem.yml` is an Ansible playbook that saves the running configurations on all devices.

`TopologyDrawer.py` parses LLDP neighbor information from the `./tmp` directory and uses Graphviz to automatically generate a network topology diagram. The resulting diagram is exported as a PDF to the `./output` directory.

## Verification

Run these checks after the playbooks and Python script finish.

| Check | What to look for |
|---|---|
| `show lldp neighbors` | Neighboring device IDs, local interfaces, and remote interfaces are correctly displayed |
| `show lldp` | LLDP is enabled on the devices |
| `ls ./tmp` | LLDP output files exist for each device |
| `ls ./output` | The generated topology PDF exists |
| Open the exported PDF | Discovered devices and their connections are accurately represented |

Verified that LLDP was successfully enabled on all routers and switches using Ansible.

Confirmed that LLDP neighbor information was collected and saved to individual text files in the `./tmp` directory.

Verified that `TopologyDrawer.py` successfully parsed the LLDP output and generated a network topology diagram using Graphviz.

Opened the exported PDF to confirm that devices, interfaces, and network connections were accurately represented.

## Conclusion

- **Automated discovery:** Used Ansible to enable LLDP and collect neighbor information across multiple routers and switches.
- **Network data collection:** Gained experience gathering structured network information from Cisco IOS devices.
- **Python parsing:** Used Python file handling and text parsing to extract device and interface information from LLDP output.
- **Topology visualization:** Used Graphviz to programmatically generate network topology diagrams from discovered Layer 2 adjacencies.
- **Network documentation:** Explored how network automation can reduce manual infrastructure documentation and make topology diagrams easier to generate and maintain.