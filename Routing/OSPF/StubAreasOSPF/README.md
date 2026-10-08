# OSPF Stub Lab

## Objective

Configure a multi-area OSPF network with different OSPF stub types (stub, totally stubby, NSSA, totally NSSA)

## Key Technologies

- OSPFv2
- OSPF stub areas
- EIGRP
- Route redistribution
- OSPF LSAs

## Relevant Commands

Configure a stub area with: `area 1 stub` on every router in the area

Make the stub area totally stubby by including no-summary (only necessary on the ABR): `area 1 stub no-summary`

Make an area into an NSSA with: `area 1 nssa` on every router in the area

For an NSSA to reach external destinations the ABR needs to advertise a default route with: `area 1 nssa default-information-originate`

Make an NSSA into a Totally NSSA by adding no-summary on the ABR: `area 1 nssa no-summary`

### R1

```cisco
router eigrp 1
 network 10.0.0.0
```

### R2

```cisco
router eigrp 1
 network 10.20.0.0 0.0.255.255
 network 10.255.2.2 0.0.0.0
 redistribute ospf 1 metric 10000 100 255 1 1500
 redistribute eigrp 1 subnets
router ospf 1
 redistribute eigrp 1 subnets
 network 10.0.0.0 0.0.255.255 area 0
 network 10.255.2.2 0.0.0.0 area 0
```

### R3

```cisco
router ospf 1
 network 10.0.0.0 0.255.255.255 area 0
```

### R4

```cisco
router ospf 1
 area 1 nssa default-information-originate
 network 10.0.0.0 0.0.255.255 area 0
 network 10.1.0.0 0.0.255.255 area 1
 network 10.255.4.4 0.0.0.0 area 0
```

### R5

```cisco
router eigrp 1
 network 10.62.0.0 0.0.255.255
 network 10.255.5.5 0.0.0.0
 redistribute ospf 1 metric 10000 100 255 1 1500
router ospf 1
 area 1 nssa
 redistribute eigrp 1 subnets
 network 10.1.0.0 0.0.255.255 area 1
 network 10.255.5.5 0.0.0.0 area 1
```

### R6

```cisco
router eigrp 1
 network 10.0.0.0
```

### R7

```cisco
router ospf 1
 area 2 stub no-summary
 network 10.0.0.0 0.0.255.255 area 0
 network 10.2.0.0 0.0.255.255 area 2
 network 10.255.7.7 0.0.0.0 area 0
```

### R8

```cisco
router ospf 1
 area 2 stub
 network 10.2.0.0 0.0.255.255 area 2
 network 10.255.8.8 0.0.0.0 area 2
```

## Verification

### Verification Commands

```cisco
show ip ospf neighbors
show ip route
show ip ospf database
show run | section ospf
show run | section eigrp
```

### R5 Example

Because R5 is in an NSSA area there are no Type 5 External and no Type 4 ASBR Summary LSAs.  However, there is an EIGRP network being redistributed into this area.  The area needs to be an NSSA so that the redistributed EIGRP routes can be advertised as Type 7 NSSA External instead of the disallowed Type 5 External.

```cisco
R5#show ip ospf database

            OSPF Router with ID (10.255.5.5) (Process ID 1)

                Router Link States (Area 1)

Link ID         ADV Router      Age         Seq#       Checksum Link count
10.255.4.4      10.255.4.4      1704        0x80000003 0x00FD92 1
10.255.5.5      10.255.5.5      1714        0x80000003 0x0083E3 2

                Net Link States (Area 1)

Link ID         ADV Router      Age         Seq#       Checksum
10.1.45.2       10.255.5.5      1714        0x80000002 0x00823F

                Summary Net Link States (Area 1)

Link ID         ADV Router      Age         Seq#       Checksum
10.0.23.0       10.255.4.4      1704        0x80000002 0x0020E3
10.0.34.0       10.255.4.4      1704        0x80000002 0x009C5D
10.0.37.0       10.255.4.4      1704        0x80000002 0x008570
10.2.78.0       10.255.4.4      1704        0x80000002 0x00B217
10.255.2.2      10.255.4.4      1704        0x80000002 0x001003
10.255.3.3      10.255.4.4      1704        0x80000002 0x00F021
10.255.4.4      10.255.4.4      1704        0x80000002 0x00D13F
10.255.7.7      10.255.4.4      1704        0x80000002 0x00A662
10.255.8.8      10.255.4.4      1704        0x80000002 0x009B6A

                Type-7 AS External Link States (Area 1)

Link ID         ADV Router      Age         Seq#       Checksum Tag
0.0.0.0         10.255.4.4      1704        0x80000002 0x007C22 0
10.62.56.0      10.255.5.5      1714        0x80000002 0x00C12E 0
10.255.6.6      10.255.5.5      1714        0x80000004 0x00A6AE 0
```

### R8 Verification

R8 is in a totally stubby area.  Instead of individual  Type 3 Summary LSAs for inter-area networks, the totally stubby area receives one Type 3 Summary LSA advertising a default route (0.0.0.0/0) from the ABR.

```cisco
R8#show ip ospf data

            OSPF Router with ID (10.255.8.8) (Process ID 1)

                Router Link States (Area 2)

Link ID         ADV Router      Age         Seq#       Checksum Link count
10.255.7.7      10.255.7.7      1863        0x80000003 0x00F653 1
10.255.8.8      10.255.8.8      1889        0x80000003 0x00E832 2

                Net Link States (Area 2)

Link ID         ADV Router      Age         Seq#       Checksum
10.2.78.2       10.255.8.8      1889        0x80000002 0x00E5AF

                Summary Net Link States (Area 2)

Link ID         ADV Router      Age         Seq#       Checksum
0.0.0.0         10.255.7.7      1863        0x80000002 0x00F92B
```

## Conclusion

OSPF uses stub areas to reduce the size of the routing table.  Additionally, the LSDB is smaller and uses less memory and CPU for SPF calculations.

Stub areas stop Type 5 External and Type 4 ASBR Summary LSAs from entering the stub.  Instead, the ABR injects a default route so the stub area can reach external destinations.

Totally Stubby areas stop Type 3, Type 4, and Type 5 LSAs from entering the area.  Instead of these LSAs, the ABR injects a default route.

Not So Stubby areas (NSSAs) stop Type 4 and Type 5 LSAs, but they introduce the Type 7 LSA.  The Type 7 LSA is used to transmit redistributed routes inside of the NSSA area without using Type 5 LSAs.

Totally Not So Stubby areas have the same functionality as NSSAs while also stopping Type 3 LSAs.
