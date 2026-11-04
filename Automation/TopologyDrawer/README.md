# Topology Drawer

## Objective

Use Python, Ansible, and LLDP to automatically create automatically topology diagram for a network.

## Key Technologies

- Ansible
- Python

## Relevant Commands/Scripts

`ansible.cfg` used to disable host key checking by default.

`hosts.yml` contains a list of hosts and configurations for Ansible.  There are two groups, `switches` and `routers`.

`enable_lldp.yml` is an Ansible playbook that uses the LLDP module to enable LLDP on all devices.

`discover_lldp.yml` is an Ansible playbook that uses the IOS commands module to `show lldp neighbors` on all devices.  The output is printed to the console and copied into the `./tmp` folder as `(device_name)_lldp_output.txt`

`write_mem.yml` is an Ansible playbook that is used to save the running-configs on all devices.

`TopologyDrawer.py` parses the lldp data from the `./tmp` folder to create a topology map of the network using graphviz.  The topology map is exported as a pdf in the `./output`

## Verification

Verified LLDP was successfully enabled on all routers and switches using Ansible.

Confirmed that `show lldp neighbors` returned neighboring device information, including local interfaces, remote device IDs, and remote interfaces.

Verified that LLDP output files were successfully generated in the `./tmp` directory for each device.

Confirmed that TopologyDrawer.py successfully parsed the LLDP output and generated a network topology diagram.

Opened the exported PDF to verify that discovered devices and their connections were accurately represented

## Conclusion

Used Ansible to automate LLDP configuration and network device information gathering across multiple routers and switches.

Gained experience collecting and processing structured network information from Cisco IOS command output.

Used Python file handling and text parsing to extract network topology information from LLDP neighbor tables.

Used Graphviz to programmatically generate network topology diagrams based on discovered Layer 2 adjacencies.

Explored how network automation can reduce the need for manually documenting network infrastructure.
