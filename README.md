# NetworkingLabs

A collection of networking labs completed using GNS3 and Cisco Modeling Labs.

Each lab contains:

- **README.md** – Overview of the lab, including its objective, key technologies, relevant commands, verification results, and takeaways.
- **Configs/** – Running configurations for each device used in the lab.
- **Topology/** – PNG image of the network topology and, for GNS3 labs, the GNS3 project file.
- **Project file** – CML labs include the YAML project file in the project folder.

## Index

### Automation

| Title | Link | Key Technologies | Software |
| --- | --- | --- | --- |
| Automatic Network Provisioner | [View Lab](./Automation/AutomaticProvisioning/) | Ansible | CML |
| Topology Drawer | [View Lab](./Automation/TopologyDrawer/) | Python, Ansible, Graphviz | CML |
| VLAN Checker | [View Lab](./Automation/VLANChecker/) | Python, Nornir, NAPALM | CML |

### Layer 2

| Title | Link | Key Technologies | Software |
| --- | --- | --- | --- |
| ROAS | [View Lab](./Layer2/ROAS/) | ROAS, Vlans, Trunk Interfaces, Router subinterfaces | CML |
| MST | [View Lab](./Layer2/MST/) | MST, VTP | CML |
| EtherChannel | [View Lab](./Layer2/EtherChannel/) | EtherChannel, LACP, PAgP | CML |

### FHRP

| Title | Link | Key Technologies | Software |
| --- | --- | --- | --- |
| GLBP | [View Lab](./FHRPs/GLBP/) | GLBP, Object Tracking | GNS3 |
| HSRP | [View Lab](./FHRPs/HSRP/) | HSRPv2 , Object Tracking | GNS3 |
| VRRP | [View Lab](./FHRPs/VRRP/) | VRRP, IP SLA, Object Tracking | GNS3 |

### OSPF

| Title | Link | Key Technologies | Software |
| --- | --- | --- | --- |
| Multi-Area OSPF | [View Lab](./Routing/OSPF/Multi-areaOSPF/) | OSPFv2, Route Summarization, OSPF areas | GNS3 |
| OSPF Stub Areas | [View Lab](./Routing/OSPF/StubAreasOSPF/) | OSPFv2, OSPF Stub areas, OSPF Redistribution, EIGRP, OSPF LSAs | GNS3 |

### BGP

| Title | Link | Key Technologies | Software |
| --- | --- | --- | --- |
| Dual-ISP BGP Routing, NAT/PAT, and Automatic Failover | [View Lab](./Routing/BGP/Dual-ISPBGP/) | eBGP, iBGP, BGP Weight, NAT Overload (PAT), ISP Redundancy, Route Maps | GNS3 |

### VPN

| Title | Link | Key Technologies | Software |
| --- | --- | --- | --- |
| GRE over IPsec | [View Lab](./VPN/GREOverIPsec/) | GRE Tunnels, IPsec (IPsec Profiles), OSPFv2, EIGRP | GNS3 |
