# Multi-area OSPF lab

## Objective

Configure a working multi-area OSPF network with route summarization between areas.

## Key Technologies

- OSPFv2
- Multi-area OSPF
- OSPF route summarization

## Topology

<img width="710" height="542" alt="image" src="https://github.com/user-attachments/assets/77540b60-5aa8-4def-b8e3-8906a15afccf" />

## Network Design

| Router | Role | Area |
|---|---|---|
| R1 | ABR | Area 0 / Area 1 |
| R2 | ABR | Area 0 / Area 1 |
| R3 | ABR | Area 0 / Area 2 |
| R4 | Internal Router | Area 0 |
| R5 | ABR | Area 0 / Area 2 |

## Addressing

| Area | Address Space |
| --- | --- |
| Area 0 | 10.0.0.0/16 |
| Area 1 | 10.1.0.0/16 |
| Area 2 | 10.2.0.0/16 |

| Network | Purpose |
| --- | --- |
| 10.1.12.0/30 | R1-R2 |
| 10.0.23.0/30 | R2-R3 |
| 10.0.34.0/30 | R3-R4 |
| 10.0.24.0/30 | R2-R4 |
| 10.2.35.0/30 | R3-R5 |
| 10.255.1.1/32 | R1 Loopback |
| 10.255.0.2/32 | R2 Loopback |
| 10.255.0.3/32 | R3 Loopback |
| 10.255.0.4/32 | R4 Loopback |
| 10.255.2.5/32 | R5 Loopback |

## OSPF Design

Area 0 is the backbone area. Area 1 is connected to Area 0 via R1-R2. Area 2 is connected to Area 0 via R3-R5.
R1, R2, R3, and R5 operate as ABRs and advertise routes between their areas.
Routes within the backbone (10.0.0.0/16 and 10.255.0.0/24) are summarized when advertised out of Area 0.
