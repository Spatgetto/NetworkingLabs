# Automatic Network Provisioner

## Objective

Use Ansible to assign IP addresses to point-to-point interfaces, configure loopback interfaces, and advertise the correct (non-management) networks into OSPF.

## Key Technologies

- Ansible

## Relevant Scripts

`hosts.yml` is an Ansible hosts file that defines the routers to configure.

`links.yml` contains interface information pertaining to the point-to-point links between routers.

`ip_provisioning.yml` is an Ansible playbook that automatically assigns IP addresses to routers based on the `links.yml` file.

`configure_ospf.yml` is an Ansible playbook that configures OSPF and verifies that neighborships have formed by printing the output of `show ip ospf neighbor` to the console.

`create_loopbacks.yml` is an Ansible playbook that creates loopback interfaces on all devices with the addressing scheme: `"ip address 10.255.router_id.router_id 255.255.255.255"`. The loopback interfaces are then advertised into OSPF.

`write_mem.yml` is an Ansible playbook that saves the running-config.

## Verification

Run these on any router after the playbooks finish.

| Command | What to look for |
|---|---|
| `show ip interface brief` | Point-to-point interfaces and `Loopback0` are `up/up` with the addresses from `links.yml` and the `10.255.x.x` scheme |
| `show ip ospf neighbor` | Every expected neighbor is in `FULL` state (this is also what `configure_ospf.yml` prints) |
| `show ip ospf interface brief` | Point-to-point links and the loopback are in OSPF; the management interface is not |
| `show ip protocols` | The OSPF `network` statements cover only the point-to-point and loopback networks, not the management network |
| `show ip route ospf` | Every other router's loopback `/32` is learned via OSPF |
| `ping 10.255.<id>.<id> source Loopback0` | Loopback-to-loopback reachability between routers |
| `show running-config \| section ospf` | Configuration matches the intent of `configure_ospf.yml` |
| `show startup-config \| section ospf` | Saved config matches running config after `write_mem.yml` |

Quick check across all devices via an Ansible ad-hoc command.

```bash
ansible all -i hosts.yml -m cisco.ios.ios_command -a "commands='show ip ospf neighbor'"
```

Re-running a playbook should report no unexpected changes, which confirms it is safe to run repeatedly.

## Conclusion

- **Data-driven configuration:** keeping link addressing in `links.yml` means a topology change is a data edit, not a rewrite of every router config.
- **Predictable loopbacks:** deriving each loopback from the router ID (`10.255.id.id/32`) gives every device a stable, unique, easy-to-recognize address.
- **Keep management out of OSPF:** advertising only point-to-point and loopback networks keeps the management network out of the routing table.
- **Repeatable by design:** splitting the work into small playbooks (addressing, loopbacks, OSPF, saving) makes each stage easy to run, test, and troubleshoot on its own.