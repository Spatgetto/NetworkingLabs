# HSRP Lab

## Objective

Configure Hot Standby Router Protocol (HSRP) and use Object Tracking to automatically decrement HSRP priority

## Key Technologies

- HSRPv2
- Object Tracking

## Relevant Commands

### R2

```cisco
track 1 interface FastEthernet0/0 line-protocol
track 2 ip route 10.255.1.1 255.255.255.255 reachability

interface f1/0
 standby version 2
 standby 1 ip 10.1.1.1
 standby 1 priority 105
 standby 1 preempt
 standby 1 authentication md5 key-string securepassword1
 standby 1 track 1 decrement 10
 standby 1 track 2 decrement 20
```

### R3

```cisco
interface f1/0
 standby version 2
 standby 1 ip 10.1.1.1
 standby 1 preempt
 standby 1 authentication md5 key-string securepassword1
```

## Verification

### PC1

```pc
ping 10.255.1.1
trace 10.255.1.1
```

### R2 + R3

```cisco
show run | section standbys
show run | section track
show standby
show standby brief
show track brief
```

### R2 Example

R2 is the Active router due to a higher priority

```cisco
R2#show standby brief
                     P indicates configured to preempt.
                     |
Interface   Grp  Pri P State   Active          Standby         Virtual IP
Fa1/0       1    105 P Active  local           10.1.1.3        10.1.1.1
```

After making shutting down F0/0, priority is decremented by 10 and R2 is now the Standby router

```cisco
R2(config-if)#do show standby brief
                     P indicates configured to preempt.
                     |
Interface   Grp  Pri P State   Active          Standby         Virtual IP
Fa1/0       1    95  P Standby 10.1.1.3        local           10.1.1.1
```

## Conclusion

HSRP provides redundancy by providing hosts with a virtual gateway (10.1.1.1)

Object Tracking links reachability and interface line-protocol status to HSRP

When the tracked destination becomes unreachable, R2's HSRP priority decrements by 20.  When f0/0's line-protocol is down then the HSRP priority is decremented by 10

HSRP premption enables the higher-priority router to automatically become Active