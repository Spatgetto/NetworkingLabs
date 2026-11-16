# BGP Communities

## Requirements

c7200-adventerprisek9-mz.152-4.S6.image

## Objective

Configure BGP communities to establish routing policy across autonomou systems.

## Key Technologies

- BGP
- BGP Communities
- Route Maps

## Relevant Commands

### On R1

```cisco
router bgp 65001
 bgp log-neighbor-changes
 network 10.1.1.1 mask 255.255.255.255
 network 10.1.1.2 mask 255.255.255.255
 neighbor 198.51.100.2 remote-as 65002
 neighbor 198.51.100.2 send-community
ip bgp-community new-format
```

### On R2

```cisco
ip access-list extended MATCH_10.1.1.1
 permit ip host 10.1.1.1 any
ip access-list extended MATCH_10.1.1.2
 permit ip host 10.1.1.2 any

route-map TAG-R1 permit 10
 match ip address MATCH_10.1.1.1
 set community 65001:1
route-map TAG-R1 permit 20
 match ip address MATCH_10.1.1.2
 set community 65001:2
route-map TAG-R1 permit 30

router bgp 65002
 bgp log-neighbor-changes
 neighbor 198.51.100.1 remote-as 65001
 neighbor 198.51.100.1 send-community
 neighbor 198.51.100.1 route-map TAG-R1 in
 neighbor 198.51.100.6 remote-as 65003
 neighbor 198.51.100.6 send-community
ip bgp-community new-format
```

### On R3

```cisco
ip community-list standard MATCH-65001:1 permit 65001:1
ip community-list standard MATCH-65001:2 permit 65001:2

route-map 65001-POLICY deny 10
 match community MATCH-65001:1
route-map 65001-POLICY permit 20
 match community MATCH-65001:2
route-map 65001-POLICY deny 999

router bgp 65003
 bgp log-neighbor-changes
 network 10.3.3.1 mask 255.255.255.255
 neighbor 198.51.100.5 remote-as 65002
 neighbor 198.51.100.5 send-community
 neighbor 198.51.100.5 route-map 65001-POLICY in
ip bgp-community new-format
```

## Verification

```cisco
show ip community-list
show ip access-lists
show route-map 
show ip bgp neighbors 
clear ip bgp [neighbor-ip] soft in
show ip bgp 10.1.1.1
show ip route 10.1.1.1
```

`clear ip bgp [neighbor-ip] soft in` refreshes incoming routes from a neighbor without resetting the entire session.  It re-evaluates routes using updated policies.

## Conclusion

- Learned how BGP communities can communicate routing policies between autonomous systems.
- Used inbound route-maps to tag received prefixes with distinct standard communities.
- Used community-lists to identify routes based on their community attributes.
- Applied route-map policies to selectively permit or deny BGP routes.
- Verified community propagation and route filtering using BGP show commands.
- Used soft inbound refreshes to reprocess previously received routes after policy changes.
- Demonstrated how communities provide a scalable way to implement routing policies without relying solely on individual prefix filters.
