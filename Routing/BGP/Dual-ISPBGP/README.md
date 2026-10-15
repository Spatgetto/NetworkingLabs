# Dual-ISP BGP, PAT, and Automatic Failover

## Objective

Configure a dual-multihomed BGP connection to two ISPs.  

## Key Technologies

- eBGP
- iBGP
- Cisco BGP Weight
- NAT Overload
- ISP Redundancy
- Route Maps

## Relevant Commands

### R1

```cisco
access-list 101 permit ip 10.0.0.0 0.255.255.255 any
access-list 102 permit ip 10.0.0.0 0.255.255.255 any

route-map ISP2_NAT permit 10
 match ip address 102
 match interface FastEthernet2/0
route-map ISP1_NAT permit 10
 match ip address 101
 match interface FastEthernet1/0

ip nat inside source route-map ISP1_NAT interface FastEthernet1/0 overload
ip nat inside source route-map ISP2_NAT interface FastEthernet2/0 overload

router ospf 1
 network 10.0.0.0 0.255.255.255 area 0

router bgp 100
 bgp log-neighbor-changes
 neighbor 10.255.2.2 remote-as 100
 neighbor 10.255.2.2 update-source Loopback0
 neighbor 192.0.2.2 remote-as 300
 neighbor 192.0.2.6 remote-as 400
 !
 address-family ipv4
  network 192.0.2.0 mask 255.255.255.252
  network 192.0.2.4 mask 255.255.255.252
  neighbor 10.255.2.2 activate
  neighbor 192.0.2.2 activate
  neighbor 192.0.2.2 weight 500
  neighbor 192.0.2.6 activate
 exit-address-family
```

### R2

```cisco
access-list 101 permit ip 10.0.0.0 0.255.255.255 any
access-list 102 permit ip 10.0.0.0 0.255.255.255 any

route-map ISP2_NAT permit 10
 match ip address 102
 match interface FastEthernet2/0
route-map ISP1_NAT permit 10
 match ip address 101
 match interface FastEthernet1/0

ip nat inside source route-map ISP1_NAT interface FastEthernet1/0 overload
ip nat inside source route-map ISP2_NAT interface FastEthernet2/0 overload

router ospf 1
 network 10.0.0.0 0.255.255.255 area 0

router bgp 100
 bgp log-neighbor-changes
 neighbor 10.255.1.1 remote-as 100
 neighbor 10.255.1.1 update-source Loopback0
 neighbor 192.0.2.10 remote-as 300
 neighbor 192.0.2.14 remote-as 400
 !
 address-family ipv4
  network 192.0.2.8 mask 255.255.255.252
  network 192.0.2.12 mask 255.255.255.252
  neighbor 10.255.1.1 activate
  neighbor 192.0.2.10 activate
  neighbor 192.0.2.14 activate
  neighbor 192.0.2.14 weight 500
 exit-address-family
```

### R3

```cisco
router bgp 300
 bgp log-neighbor-changes
 neighbor 192.0.2.1 remote-as 100
 neighbor 192.0.2.9 remote-as 100
 neighbor 192.0.2.22 remote-as 500
 !
 address-family ipv4
  network 192.0.2.8 mask 255.255.255.252
  network 198.51.100.3 mask 255.255.255.255
  neighbor 192.0.2.1 activate
  neighbor 192.0.2.9 activate
  neighbor 192.0.2.22 activate
 exit-address-family
```

### R4

```cisco
router bgp 400
 bgp log-neighbor-changes
 neighbor 192.0.2.5 remote-as 100
 neighbor 192.0.2.13 remote-as 100
 neighbor 192.0.2.18 remote-as 500
 !
 address-family ipv4
  network 192.0.2.4 mask 255.255.255.255
  network 198.51.100.4 mask 255.255.255.255
  neighbor 192.0.2.5 activate
  neighbor 192.0.2.13 activate
  neighbor 192.0.2.18 activate
 exit-address-family
```

### R5

```cisco
router bgp 500
 bgp log-neighbor-changes
 neighbor 192.0.2.17 remote-as 400
 neighbor 192.0.2.21 remote-as 300
 !
 address-family ipv4
  network 198.51.100.5 mask 255.255.255.255
  neighbor 192.0.2.17 activate
  neighbor 192.0.2.21 activate
 exit-address-family
```

## Verification

### Verification Commands

```cisco
show ip route
show ip bgp summary
show ip bgp <destination-ip>
show ip nat translations
show ip nat statistics
show route-map
```

### BGP Automatic Failover Verification

Use Ping to test reachability to R5

```cisco
R1#ping 198.51.100.5
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 198.51.100.5, timeout is 2 seconds:
!!!!!
```

Show route to R5.  The next hop is R3 because R3 has a configured weight of 500, making it the preferred path

```cisco
R1#show ip route 198.51.100.5
Routing entry for 198.51.100.5/32
  Known via "bgp 100", distance 20, metric 0
  Tag 300, type external
  Last update from 192.0.2.2 00:36:51 ago
  Routing Descriptor Blocks:
  * 192.0.2.2, from 192.0.2.2, 00:36:51 ago
      Route metric is 0, traffic share count is 1
      AS Hops 2
      Route tag 300
      MPLS label: none
```

Shutdown f1/0 (Connection to R3), R1 now goes directly through R4 to reach R5

```cisco
R1(config)#int f1/0
R1(config-if)#shut
R1#show ip route 198.51.100.5
Routing entry for 198.51.100.5/32
  Known via "bgp 100", distance 20, metric 0
  Tag 400, type external
  Last update from 192.0.2.6 00:01:02 ago
  Routing Descriptor Blocks:
  * 192.0.2.6, from 192.0.2.6, 00:01:02 ago
      Route metric is 0, traffic share count is 1
      AS Hops 2
      Route tag 400
      MPLS label: none
```

Because R1 has no direct connection to R3, it uses an iBGP route advertised by R2 to reach R3

```cisco
R1#show ip route 198.51.100.3
Routing entry for 198.51.100.3/32
  Known via "bgp 100", distance 200, metric 0
  Tag 300, type internal
  Last update from 192.0.2.10 00:02:27 ago
  Routing Descriptor Blocks:
  * 192.0.2.10, from 10.255.2.2, 00:02:27 ago
      Route metric is 0, traffic share count is 1
      AS Hops 1
      Route tag 300
      MPLS label: none
```

### PAT Verification

PC1 sucessfully pings R5 (198.51.100.5) 

```text
PC1> ping 198.51.100.5

84 bytes from 198.51.100.5 icmp_seq=1 ttl=253 time=121.776 ms
84 bytes from 198.51.100.5 icmp_seq=2 ttl=253 time=158.843 ms
84 bytes from 198.51.100.5 icmp_seq=3 ttl=253 time=141.258 ms
84 bytes from 198.51.100.5 icmp_seq=4 ttl=253 time=189.862 ms
84 bytes from 198.51.100.5 icmp_seq=5 ttl=253 time=190.536 ms
```

View R1's NAT translations to see that PAT is converting the private IP address into a public one

```cisco
R1#show ip nat translation
Pro Inside global      Inside local       Outside local      Outside global
icmp 192.0.2.1:1024    10.1.0.2:61245     198.51.100.5:61245 198.51.100.5:1024
icmp 192.0.2.1:1025    10.1.0.2:61501     198.51.100.5:61501 198.51.100.5:1025
icmp 192.0.2.1:1026    10.1.0.2:61757     198.51.100.5:61757 198.51.100.5:1026
icmp 192.0.2.1:1027    10.1.0.2:62013     198.51.100.5:62013 198.51.100.5:1027
icmp 192.0.2.1:1028    10.1.0.2:62269     198.51.100.5:62269 198.51.100.5:1028
```

## Conclusion

OSPF uses areas to divide the network into smaller logical sections. Type 1 (Router) and Type 2 (Network) LSAs remain within their respective areas, while Type 3 Summary LSAs are used by ABRs to advertise routes between areas.

Area 0 is the OSPF backbone area, and non-backbone areas must have a connection to Area 0 in a standard multi-area OSPF design.

The `area range` command is configured on an ABR to summarize routes originating within a area before advertising them into other OSPF areas. In this lab, R2 and R3 use `area 0 range` to summarize Area 0 routes into the `10.0.0.0/16` and `10.255.0.0/24` prefixes.

The routing table on R1 confirms that these summarized routes are being learned as OSPF inter-area (`O IA`) routes. The OSPF database also shows Type 3 Summary LSAs being generated by the ABR to advertise routes between areas.
