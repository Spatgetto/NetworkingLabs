# GLBP Lab

## Objective

Configure Gateway Load Balancing Protocol (GLBP) with Object Tracking to automatically change GLBP weight upon an interface going down

## Key Technologies

- GLBP
- Object Tracking

## Relevant Commands

### R2

```cisco
track 1 interface FastEthernet0/0 line-protocol
 glbp 1 weighting track 1 decrement 50


interface f1/0
 glbp 1 ip 10.1.1.1
 glbp 1 priority 110
 glbp 1 preempt
 glbp 1 weighting 100 lower 60 upper 80
 glbp 1 authentication md5 key-string uncrackable001
 glbp 1 weighting track 1 decrement 50
```

### R3

```cisco
interface f1/0
 glbp 1 ip 10.1.1.1
 glbp 1 preempt
 glbp 1 authentication md5 key-string uncrackable001
```

## Verification

### PC1

```text
ping 10.255.1.1
trace 10.255.1.1
```

### R2 + R3

```cisco
show run | section glbp
show run | section track
show glbp
show glbp brief
show track brief
```

### R2 Example

R2 has a weight of 100, packets are load balanced 50/50 between R2 and R3
```cisco
R2#show glbp
FastEthernet1/0 - Group 1
  State is Active
    1 state change, last state change 00:19:20
  Virtual IP address is 10.1.1.1
  Hello time 3 sec, hold time 10 sec
    Next hello sent in 2.208 secs
  Redirect time 600 sec, forwarder time-out 14400 sec
  Authentication MD5, key-string
  Preemption enabled, min delay 0 sec
  Active is local
  Standby is 10.1.1.3, priority 100 (expires in 9.504 sec)
  Priority 110 (configured)
  Weighting 100 (configured 100), thresholds: lower 60, upper 80
    Track object 1 state Up decrement 50
  Load balancing: round-robin
  Group members:
    ca03.2c75.001c (10.1.1.3) authenticated
    ca04.2c92.001c (10.1.1.2) local
  There are 2 forwarders (1 active)
  Forwarder 1
    State is Active
      3 state changes, last state change 00:10:19
    MAC address is 0007.b400.0101 (default)
    Owner ID is ca04.2c92.001c
    Redirection enabled
    Preemption enabled, min delay 30 sec
    Active is local, weighting 100
    Arp replies sent: 1
  Forwarder 2
    State is Listen
    MAC address is 0007.b400.0102 (learnt)
    Owner ID is ca03.2c75.001c
    Redirection enabled, 599.520 sec remaining (maximum 600 sec)
    Time to live: 14399.520 sec (maximum 14400 sec)
    Preemption enabled, min delay 30 sec
    Active is 10.1.1.3 (primary), weighting 100 (expires in 10.944 sec)
```

After making shutting down F0/0, weight is decremented by 50 and the weight is beneath the lower bound.  R2 is no longer used to load balance.

```cisco
R2(config)#do show glbp
FastEthernet1/0 - Group 1
  State is Active
    1 state change, last state change 00:20:45
  Virtual IP address is 10.1.1.1
  Hello time 3 sec, hold time 10 sec
    Next hello sent in 0.480 secs
  Redirect time 600 sec, forwarder time-out 14400 sec
  Authentication MD5, key-string
  Preemption enabled, min delay 0 sec
  Active is local
  Standby is 10.1.1.3, priority 100 (expires in 8.608 sec)
  Priority 110 (configured)
  Weighting 50, low (configured 100), thresholds: lower 60, upper 80
    Track object 1 state Down decrement 50
  Load balancing: round-robin
  Group members:
    ca03.2c75.001c (10.1.1.3) authenticated
    ca04.2c92.001c (10.1.1.2) local
  There are 2 forwarders (1 active)
  Forwarder 1
    State is Active
      3 state changes, last state change 00:11:44
    MAC address is 0007.b400.0101 (default)
    Owner ID is ca04.2c92.001c
    Redirection enabled
    Preemption enabled, min delay 30 sec
    Active is local, weighting 50
    Arp replies sent: 1
  Forwarder 2
    State is Listen
    MAC address is 0007.b400.0102 (learnt)
    Owner ID is ca03.2c75.001c
    Redirection enabled, 598.624 sec remaining (maximum 600 sec)
    Time to live: 14398.624 sec (maximum 14400 sec)
    Preemption enabled, min delay 30 sec
    Active is 10.1.1.3 (primary), weighting 100 (expires in 10.432 sec)
```

## Conclusion

GLBP provides redundacy and load balancing by providing hosts with a virtual IP address (10.1.1.1)

GLBP weight determines the load balancing ratio between forwarders, higher weight means more packets are sent to that router

Weight can be automatically decremented by Object Tracking

Set a lower weight to determine when a router's weight is too low to forward traffic.  The upper weight determines when the router's weight is high enough to start forwarding traffic again.