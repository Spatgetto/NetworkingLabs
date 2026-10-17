# NetworkingLabs

A collection of networking labs completed using GNS3 and Cisco Modeling Labs.

Each lab contains:

* **README.md** - Summary of the lab, including its objective, key technologies, relevant commands, verification results, and takeaways.
* **Configs/** - Running configurations for every device used in the lab.
* **Topology/** - PNG image of the network topology and the corresponding GNS3/CML project file.

## Index

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
