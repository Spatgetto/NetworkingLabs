# MST

## Objective

Configure a switched network that uses Multiple Spanning Tree (MST)

## Key Technologies

- Multiple Spanning Tree (MST)
- VTP (VLAN Trunking Protocol)

## Relevant Commands

### VTP Server

```cisco
vtp domain LAB
vtp version 3
vtp mode server
vtp server primary
```

### VTP Client

```cisco
vtp domain LAB
vtp mode client
vtp version 3
```

### MST Region 01

```cisco
spanning-tree mode mst
spanning-tree mst configuration
 name REGION01
 revision 1
 instance 1 vlan 1-5
 instance 2 vlan 6-10
```

### MST Region 23

```cisco
spanning-tree mode mst
spanning-tree mst configuration
 name REGION23
 revision 1
 instance 1 vlan 1-2
 instance 2 vlan 3-10
```

### MST Region 4

```cisco
spanning-tree mode mst
spanning-tree mst configuration
 name REGION4
 revision 1
 instance 1 vlan 1-5
```

## Verification

### Verifying VTP

```cisco
show vtp status
show vlan brief
```

### Verifying MST

```cisco
show spanning-tree mst 
show spanning-tree mst 1
```

### Verification Example on SW1

```cisco
SW1#show vtp stat  
VTP Version capable             : 1 to 3
VTP version running             : 3
VTP Domain Name                 : LAB
VTP Pruning Mode                : Disabled (Operationally Disabled)
VTP Traps Generation            : Disabled
Device ID                       : aabb.cc80.0600

Feature VLAN:
--------------
VTP Operating Mode                : Client
Number of existing VLANs          : 15
Number of existing extended VLANs : 0
Maximum VLANs supported locally   : 4096
Configuration Revision            : 11
Primary ID                        : aabb.cc80.0700
Primary Description               : SW0
MD5 digest                        : 0xEB 0x7C 0x14 0xB1 0x78 0x68 0xD3 0x88 
                                    0x5D 0xFF 0x76 0x50 0x17 0xD0 0xA7 0x92 


Feature MST:
--------------
VTP Operating Mode                : Transparent


Feature UNKNOWN:
--------------
VTP Operating Mode                : Transparent
```

```cisco
SW1#show spanning-tree mst 1

##### MST1    vlans mapped:   1-5
Bridge        address aabb.cc00.0600  priority      32769 (32768 sysid 1)
Root          address aabb.cc00.0700  priority      4097  (4096 sysid 1)
              port    Et0/1           cost          2000000   rem hops 19

Interface                        Role Sts Cost      Prio.Nbr Type
----------------                 ---- --- --------- -------- --------------------------------
Et0/0                            Desg FWD 2000000   128.1    P2p 
Et0/1                            Root FWD 2000000   128.2    P2p 
Et0/2                            Desg FWD 2000000   128.3    P2p 
Et0/3                            Desg FWD 2000000   128.4    P2p 
```

## Conclusion

Configured VTPv3 to distribute VLAN information and MST to manage spanning-tree instances across multiple regions. Verified VTP status, VLAN propagation, and MST root bridge elections.
