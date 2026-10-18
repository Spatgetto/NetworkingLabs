# EtherChannel

## Objective

Configure EtherChannel in a switched network

## Key Technologies

- Etherchannel
- PAgP
- LACP

## Relevant Commands

### SW0

```cisco
interface Port-channel1
 switchport access vlan 10
 switchport mode access

interface Ethernet0/0
 switchport access vlan 10
 switchport mode access
 channel-group 1 mode active

interface Ethernet0/1
 switchport access vlan 10
 switchport mode access
 channel-group 1 mode active
```

### SW1

```cisco
interface Port-channel1
 switchport access vlan 10
 switchport mode access

interface Port-channel2
 switchport access vlan 10
 switchport trunk allowed vlan 10,20,30,40
 switchport mode dynamic desirable

interface Ethernet0/0
 switchport access vlan 10
 switchport mode access
 channel-group 1 mode passive

interface Ethernet0/1
 switchport access vlan 10
 switchport trunk allowed vlan 10,20,30,40
 switchport mode dynamic desirable
 channel-group 2 mode desirable

interface Ethernet0/2
 switchport access vlan 10
 switchport mode access
 channel-group 1 mode passive

interface Ethernet0/3
 switchport trunk allowed vlan 10,20,30,40
 switchport mode dynamic desirable
 channel-group 2 mode desirable
```

### SW2

```cisco
interface Port-channel2
 switchport trunk allowed vlan 10,20,30,40
 switchport mode dynamic desirable

interface Ethernet0/0
 switchport trunk allowed vlan 10,20,30,40
 switchport mode dynamic desirable
 channel-group 2 mode auto

interface Ethernet0/1
 switchport trunk allowed vlan 10,20,30,40
 switchport mode dynamic desirable
 channel-group 2 mode auto
```

## Verification

### Verifiying EtherChannel

```cisco
show etherchannel
show lacp neighbor
show etherchannel 1 detail
show etherchannel summary
```

### Verification Example on SW1

```cisco
SW1#show etherchannel summary 
Flags:  D - down        P - bundled in port-channel
        I - stand-alone s - suspended
        H - Hot-standby (LACP only)
        R - Layer3      S - Layer2
        U - in use      f - failed to allocate aggregator

        M - not in use, minimum links not met
        u - unsuitable for bundling
        w - waiting to be aggregated
        d - default port

        A - formed by Auto LAG


Number of channel-groups in use: 2
Number of aggregators:           2

Group  Port-channel  Protocol    Ports
------+-------------+-----------+-----------------------------------------------
1      Po1(SU)         LACP        Et0/0(P)        Et0/2(P)        
2      Po2(SU)         PAgP        Et0/1(P)        Et0/3(P)        
```

```cisco
SW1#show etherchannel 2 detail
Group state = L2 
Ports: 2   Maxports = 4
Port-channels: 1 Max Port-channels = 1
Protocol:   PAgP
Minimum Links: 0


                Ports in the group:
                -------------------
Port: Et0/1
------------

Port state    = Up Mstr In-Bndl 
Channel group = 2           Mode = Desirable-Sl    Gcchange = 0
Port-channel  = Po2         GC   = 0x00020001      Pseudo port-channel = Po2
Port index    = 0           Load = 0x00            Protocol =   PAgP


Age of the port in the current state: 0d:00h:14m:18s

Port: Et0/3
------------

Port state    = Up Mstr In-Bndl 
Channel group = 2           Mode = Desirable-Sl    Gcchange = 0
Port-channel  = Po2         GC   = 0x00020001      Pseudo port-channel = Po2
Port index    = 0           Load = 0x00            Protocol =   PAgP


Age of the port in the current state: 0d:00h:14m:17s

                Port-channels in the group: 
                ---------------------------

Port-channel: Po2
------------

Age of the Port-channel   = 0d:00h:16m:53s
Logical slot/port   = 16/1          Number of ports = 2
GC                  = 0x00020001      HotStandBy port = null
Port state          = Port-channel Ag-Inuse 
Protocol            =   PAgP
Port security       = Disabled
Fast-switchover     = disabled
Fast-switchover Dampening = disabled

Ports in the Port-channel: 

Index   Load   Port        EC state        No of bits
------+------+------+------------------+-----------
  0     00     Et0/1          Desirable-Sl       0
  0     00     Et0/3          Desirable-Sl       0

Time since last port bundled:    0d:00h:14m:17s     Et0/3
```

## Conclusion

EtherChannel bundles multiple links into one virtual link for load balancing.  LACP is open standard while PAgP is Cisco Proprietary.  LACP uses states Active and Passive, while PAgP uses states Desirable and Auto.
