# VRRP Lab

## Objective

Configure Virtual Router Redundancy Protocol (VRRP) and use IP SLA + Object Tracking to automatically decrement VRRP priority upon loss of reachability to a tracked destination

## Key Technologies

- VRRP
- IP SLA
- Object Tracking

## Relevant Commands

### R2

```cisco
ip sla 1
 icmp-echo 10.255.1.1
 frequency 5
ip sla schedule 1 life forever start-time now

track 1 ip sla 1 reachability
 delay down 1 up 1

interface f1/0
 vrrp 1 ip 10.1.1.1
 vrrp 1 priority 110
 vrrp 1 track 1 decrement 40
```

### R3

```cisco
interface f1/0
 vrrp 1 ip 10.1.1.1
```

Note that preemption is enabled by default in VRRP

## Verification

### PC1

```text
ping 10.255.1.1
trace 10.255.1.1
```

### R2 + R3

```cisco
show track brief
show ip sla
show run | section vrrp
show vrrp brief
show vrrp
```

### R2 Example

R2 is the Master router due to a higher priority

```cisco
R2#show vrrp brief
Interface          Grp Pri Time  Own Pre State   Master addr     Group addr
Fa1/0              1   110 3570       Y  Master  10.1.1.2        10.1.1.1
```

After making R1 unreachable by shutting down R1's interfaces, R2 is now the Backup router due to having a lower priority

```cisco
*Oct  7 18:30:20.003: %TRACKING-5-STATE: 1 ip sla 1 reachability Up->Down
R2#show
*Oct  7 18:30:23.647: %VRRP-6-STATECHANGE: Fa1/0 Grp 1 state Master -> Backup
R2#show vrrp brief
Interface          Grp Pri Time  Own Pre State   Master addr     Group addr
Fa1/0              1   70  3570       Y  Backup  10.1.1.3        10.1.1.1
```

## Conclusion

VRRP provides redundancy by providing hosts with a virtual gateway (10.1.1.1)

IP SLA monitors reachability to a destination by sending ICMP echoes every 5 seconds

Object Tracking links the IP SLA result to VRRP

When the tracked destination becomes unreachable, R2's VRRP priority decreases from 110 to 70

VRRP premption enables the higher-priority router to automatically become the Master
