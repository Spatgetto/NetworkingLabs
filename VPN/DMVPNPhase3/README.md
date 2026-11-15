# DMVPN Phase 3

## Objective

Configure DMVPN Phase 3

## Key Technologies

- DMVPN Phase 3
- IPsec
- GRE Multipoint Tunnels
- EIGRP
- BGPs

## Relevant Commands

### On Hub (R1)

```cisco
interface Tunnel0
 bandwidth 10000
 ip address 172.16.1.1 255.255.255.0
 no ip redirects
 ip mtu 1400
 no ip split-horizon eigrp 100
 ip nhrp authentication lab
 ip nhrp map multicast dynamic
 ip nhrp network-id 1
 ip nhrp redirect
 ip tcp adjust-mss 1360
 tunnel source FastEthernet0/0
 tunnel mode gre multipoint
 tunnel protection ipsec profile profile1
```

### On Spokes

```cisco
interface Tunnel0
 ip address 172.16.1.4 255.255.255.0
 no ip redirects
 ip mtu 1400
 ip nhrp authentication lab
 ip nhrp map multicast 198.51.100.2
 ip nhrp map 172.16.1.1 198.51.100.2
 ip nhrp network-id 1
 ip nhrp nhs 172.16.1.1
 ip nhrp shortcut
 ip tcp adjust-mss 1360
 tunnel source FastEthernet0/0
 tunnel mode gre multipoint
 tunnel protection ipsec profile profile1
```

ip address changes depending on router

## Verification

```cisco
show dmvpn
show ip nhrp
show run | section interface Tunnel
show run | section crypto
```

### Verification on R1

```cisco
R1#show dmvpn
Legend: Attrb --> S - Static, D - Dynamic, I - Incomplete
        N - NATed, L - Local, X - No Socket
        # Ent --> Number of NHRP entries with same NBMA peer
        NHS Status: E --> Expecting Replies, R --> Responding, W --> Waiting
        UpDn Time --> Up or Down Time for a Tunnel
==========================================================================

Interface: Tunnel0, IPv4 NHRP Details
Type:Hub, NHRP Peers:2,

 # Ent  Peer NBMA Addr Peer Tunnel Add State  UpDn Tm Attrb
 ----- --------------- --------------- ----- -------- -----
     1 198.51.100.6         172.16.1.3    UP 00:10:22     D
     1 198.51.100.10        172.16.1.4    UP 00:10:21     D

```

## **Conclusion**

Successfully configured and verified DMVPN Phase 3 using mGRE, IPsec, and NHRP.

Key takeaways:

- Configured multipoint GRE tunnels between the hub and spokes.
- Implemented IPsec tunnel protection for secure communication.
- Established NHRP registration between spokes and the hub.
- Configured NHRP redirects and shortcuts for direct spoke-to-spoke communication.
- Verified tunnel connectivity and peer status using `show dmvpn` and `show ip nhrp`.
- Gained practical experience with DMVPN Phase 3 architecture and troubleshooting.
