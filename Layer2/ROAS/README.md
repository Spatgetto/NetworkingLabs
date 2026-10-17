# Router on a Stick

## Objective

Configure Router on a Stick (ROAS)

## Key Technologies

- ROAS
- Vlans
- Trunk Interfaces
- Router subinterfaces

## Relevant Commands

### SW1

```cisco
interface Ethernet0/0
 switchport trunk encapsulation dot1q
 switchport trunk native vlan 99
 switchport trunk allowed vlan 10,20,30
 switchport mode trunk

interface Ethernet0/1
 switchport access vlan 10
 switchport mode access

interface Ethernet0/2
 switchport access vlan 20
 switchport mode access

interface Ethernet0/3
 switchport access vlan 30
 switchport mode access
```

### R1

```cisco
interface Ethernet0/0.10
 encapsulation dot1Q 10
 ip address 192.168.10.1 255.255.255.0

interface Ethernet0/0.20
 encapsulation dot1Q 20
 ip address 192.168.20.1 255.255.255.0

interface Ethernet0/0.30
 encapsulation dot1Q 30
 ip address 192.168.30.1 255.255.255.0
```

## Verification

### SW1 Verificaiton

```cisco
show vlan brief
show interfaces trunk
show interfaces Ethernet0/0 switchport
```

### R1 Verification

```cisco
show ip interface brief
show ip route
```

### Verifying Reachability

From end devices, ping their default gateway and devices in other VLANs.

```text
PC1> ping 192.168.10.1
PC1> ping 192.168.20.100
```

Confirm that devices in different VLANs can communicate through the router.

## Conclusion

Router on a Stick enables inter-vlan routing using 802.1Q subinterfaces.  VLANs provide logical network segmentation, while trunk links carry traffic from multiple VLANs between switches and the router. Successful connectivity tests verified that the router could route traffic between the configured VLANs.
