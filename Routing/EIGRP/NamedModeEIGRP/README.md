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

## Verification

What commands are used to ensure everything is working

## Conclusion

Takeaways from completing this lab
