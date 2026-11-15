# DMVPN

## Requirements

c7200-adventerprisek9-mz.152-4.S6.image

## Objective

Configure DMVPN Phase 2

## Key Technologies

- DMVPN Phase 2
- IPsec
- GRE Multipoint Tunnels
- EIGRP
- BGP

## Relevant Commands

### On Spoke + Hubs (R1, R3, R4, R5)

```cisco
crypto isakmp policy 999
 encr aes
 authentication pre-share
 group 19
crypto isakmp key securekey1 address 0.0.0.0
crypto ipsec transform-set set1 esp-aes esp-sha256-hmac
 mode tunnel
crypto ipsec profile profile1
 set transform-set set1
```

### On Hub (R1)

```cisco
interface Tunnel0
 bandwidth 10000
 ip address 172.16.1.1 255.255.255.0
 no ip redirects
 ip mtu 1400
 no ip next-hop-self eigrp 100
 no ip split-horizon eigrp 100
 ip nhrp authentication lab
 ip nhrp map multicast dynamic
 ip nhrp network-id 1
 ip tcp adjust-mss 1360
 tunnel source FastEthernet0/0
 tunnel mode gre multipoint
 tunnel protection ipsec profile profile1
```

### On Spokes (R2, R3, R4)

```cisco
interface Tunnel0
 bandwidth 10000
 ip address 172.16.1.3 255.255.255.0
 no ip redirects
 ip mtu 1400
 ip nhrp authentication lab
 ip nhrp map multicast 198.51.100.2
 ip nhrp map 172.16.1.1 198.51.100.2
 ip nhrp network-id 1
 ip nhrp nhs 172.16.1.1
 ip tcp adjust-mss 1360
 tunnel source FastEthernet0/0
 tunnel mode gre multipoint
 tunnel protection ipsec profile profile1
```

Note that `ip address` command changes depending on which router is being configured

## Verification

```cisco
show dmvpn
show run | section interface Tunnel
show run | section crypto
```

### Verification on Hub (R1)

```cisco
R1#show dmvpn
Legend: Attrb --> S - Static, D - Dynamic, I - Incomplete
        N - NATed, L - Local, X - No Socket
        # Ent --> Number of NHRP entries with same NBMA peer
        NHS Status: E --> Expecting Replies, R --> Responding, W --> Waiting
        UpDn Time --> Up or Down Time for a Tunnel
==========================================================================

Interface: Tunnel0, IPv4 NHRP Details
Type:Hub, NHRP Peers:3,

 # Ent  Peer NBMA Addr Peer Tunnel Add State  UpDn Tm Attrb
 ----- --------------- --------------- ----- -------- -----
     1 198.51.100.6         172.16.1.3    UP 00:12:06     D
     1 198.51.100.10        172.16.1.4    UP 00:12:10     D
     1 198.51.100.14        172.16.1.5    UP 00:11:59     D

```

### Verification on Spokes (R3, R4, R5)

```cisco
R3#show dmvpn
Legend: Attrb --> S - Static, D - Dynamic, I - Incomplete
        N - NATed, L - Local, X - No Socket
        # Ent --> Number of NHRP entries with same NBMA peer
        NHS Status: E --> Expecting Replies, R --> Responding, W --> Waiting
        UpDn Time --> Up or Down Time for a Tunnel
==========================================================================

Interface: Tunnel0, IPv4 NHRP Details
Type:Spoke, NHRP Peers:1,

 # Ent  Peer NBMA Addr Peer Tunnel Add State  UpDn Tm Attrb
 ----- --------------- --------------- ----- -------- -----
     1 198.51.100.2         172.16.1.1    UP 00:13:01     S

```

## Conclusion

Through this lab, I configured a Dynamic Multipoint VPN (DMVPN) Phase 2 network using multipoint GRE tunnels, NHRP, IPsec, and EIGRP.

Key takeaways:

- DMVPN Architecture: Implemented a hub-and-spoke VPN architecture that supports dynamic spoke registration and discovery through NHRP.

- Multipoint GRE: Used multipoint GRE tunnels to allow multiple remote sites to communicate through a shared tunnel interface.

- IPsec Encryption: Secured GRE tunnel traffic using IPsec profiles, transform sets, and pre-shared authentication keys.

- EIGRP Routing: Configured EIGRP to distribute routes across the DMVPN network while preserving next-hop information.

- Spoke-to-Spoke Communication: Enabled direct spoke-to-spoke tunnel establishment, reducing the need for traffic to traverse the hub.

- Troubleshooting: Used show dmvpn and configuration inspection commands to verify NHRP registrations and tunnel connectivity.