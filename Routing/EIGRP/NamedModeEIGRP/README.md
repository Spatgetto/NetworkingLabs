# Named Mode EIGRP

## Objective

Use named mode EIGRP to configure EIGRP for IPv4 and IPv6 networks.  Apply IPv6 ACLs and Prefix Lists.

## Key Technologies

- EIGRP Named Mode
- IPv6
- IPv6 Prefix List
- IPv6 ACLs

## Relevant Commands

### R1

```cisco
ipv6 prefix-list PERMIT_2001 seq 5 permit 2001::/16 le 128
ipv6 prefix-list PERMIT_2001 seq 10 deny ::/0 le 128

router eigrp lab
 !
 address-family ipv4 unicast autonomous-system 100
  !
  af-interface default
   passive-interface
  exit-af-interface
  !
  af-interface Ethernet0/0
   no passive-interface
  exit-af-interface
  !
  topology base
  exit-af-topology
  network 10.0.0.0
 exit-address-family
 !
 address-family ipv6 unicast autonomous-system 100
  !
  topology base
   distribute-list prefix-list PERMIT_2001 in 
  exit-af-topology
  eigrp router-id 1.1.1.1
 exit-address-family
```

### R2

```cisco
ipv6 access-list NO_2001:db8:45::2
 sequence 10 deny ipv6 2001:DB8:45::/64 any
 sequence 20 permit ipv6 any any

interface Ethernet0/0
 ip address 10.1.2.2 255.255.255.252
 ipv6 address 2001:DB8:12::2/64
 ipv6 traffic-filter NO_2001:db8:45::2 out

router eigrp lab
 !
 address-family ipv4 unicast autonomous-system 100
  !
  topology base
  exit-af-topology
  network 10.0.0.0
 exit-address-family
 !
 address-family ipv6 unicast autonomous-system 100
  !
  topology base
  exit-af-topology
  eigrp router-id 2.2.2.2
 exit-address-family
```

### R3

```cisco
router eigrp lab
 !
 address-family ipv4 unicast autonomous-system 100
  !
  topology base
  exit-af-topology
  network 10.0.0.0
 exit-address-family
 !
 address-family ipv6 unicast autonomous-system 100
  !
  topology base
  exit-af-topology
  eigrp router-id 3.3.3.3
 exit-address-family
```

### R4

```cisco
interface Loopback0
 ip address 10.255.4.4 255.255.255.255
 ipv6 address 2000:DB8:4:4::/128

router eigrp lab
 !
 address-family ipv4 unicast autonomous-system 100
  !
  topology base
  exit-af-topology
  network 10.0.0.0
 exit-address-family
 !
 address-family ipv6 unicast autonomous-system 100
  !
  topology base
  exit-af-topology
  eigrp router-id 4.4.4.4
 exit-address-family
```

### R5

```cisco
router eigrp lab
 !
 address-family ipv4 unicast autonomous-system 100
  !
  topology base
  exit-af-topology
  network 10.0.0.0
 exit-address-family
 !
 address-family ipv6 unicast autonomous-system 100
  !
  topology base
  exit-af-topology
  eigrp router-id 5.5.5.5
 exit-address-family
```

R2, R3, R4, and R5 all have similar EIGRP configurations, with the only difference being the IPv6 address family router ID.

## Verification

```cisco
show run | section eigrp
show ip eigrp topology
show ip route
ping
```

### Verification on R4

```cisco
ping 2001:db8:12::1
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 2001:DB8:12::1, timeout is 2 seconds:
!S!S!
Success rate is 60 percent (3/5), round-trip min/avg/max = 4/5/7 ms
```

The ACL on R2 blocks traffic outgoing R1 from the 2001:DB8:45::/64 network (e0/1).  However, the traffic is load-balanced and half the pings go through e0/0 and are successful.

### Verifying the Prefix List on R1

```cisco
ipv6 prefix-list PERMIT_2001 seq 5 permit 2001::/16 le 128
ipv6 prefix-list PERMIT_2001 seq 10 deny ::/0 le 128

address-family ipv6 unicast autonomous-system 100
  !
  topology base
   distribute-list prefix-list PERMIT_2001 in 
  exit-af-topology
```

```cisco
show ipv6 route eigrp
IPv6 Routing Table - default - 7 entries
Codes: C - Connected, L - Local, S - Static, U - Per-user Static route
       B - BGP, R - RIP, H - NHRP, HG - NHRP registered
       Hg - NHRP registration summary, HE - NHRP External, I1 - ISIS L1
       I2 - ISIS L2, IA - ISIS interarea, IS - ISIS summary, D - EIGRP
       EX - EIGRP external, ND - ND Default, NDp - ND Prefix, DCE - Destination
       NDr - Redirect, RL - RPL, O - OSPF Intra, OI - OSPF Inter
       OE1 - OSPF ext 1, OE2 - OSPF ext 2, ON1 - OSPF NSSA ext 1
       ON2 - OSPF NSSA ext 2, la - LISP alt, lr - LISP site-registrations
       ld - LISP dyn-eid, lA - LISP away, le - LISP extranet-policy
       lp - LISP publications, ls - LISP destinations-summary, a - Application
       m - OMP
D   2001:DB8:23::/64 [90/1536000]
     via FE80::A8BB:CCFF:FE00:2700, Ethernet0/0
D   2001:DB8:25::/64 [90/1536000]
     via FE80::A8BB:CCFF:FE00:2700, Ethernet0/0
D   2001:DB8:34::/64 [90/2048000]
     via FE80::A8BB:CCFF:FE00:2700, Ethernet0/0
D   2001:DB8:45::/64 [90/2048000]
     via FE80::A8BB:CCFF:FE00:2700, Ethernet0/0
```

The prefix list permits 2001::/16 networks and denies everything else.
The distribute list is working because there is not a route learned from EIGRP
to R4's loopback 0 with IPv6 address 2000:DB8:4:4::/128.

## Conclusion

- Configured EIGRP for IPv4 and IPv6 using named mode.
- Learned how to use IPv6 prefix lists and distribute lists to filter routes.
- Applied IPv6 ACLs to control traffic between networks.
- Verified EIGRP routing tables and tested connectivity.
- Observed how load balancing can affect traffic when ACLs block certain paths.
