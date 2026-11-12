# UCMP EIGRP

## Objective

Configure EIGRP and use Unequal-Cost Multipathing

## Key Technologies

- EIGRP
- UCMP
- EIGRP Stub

## Relevant Commands

### R2 + R3 + R5

```cisco
router eigrp 100
 network 10.0.0.0
```

### R1

```cisco
router eigrp 100
 network 10.0.0.0
 eigrp stub connected summary
```

### R3

```cisco
router eigrp 100
 variance 2
 network 10.0.0.0

interface Ethernet0/1
 bandwidth 9000
 ip address 10.3.5.1 255.255.255.252
 delay 150
```

## Verification

```cisco
show run | include eigrp
show ip eigrp topology
show ip route eigrp
```

### Verifiying UCMP Works on R3

```cisco
EIGRP-IPv4 Topology Entry for AS(100)/ID(10.255.3.3) for 10.255.4.4/32
  State is Passive, Query origin flag is 1, 2 Successor(s), FD is 435200
  Descriptor Blocks:
  10.2.3.1 (Ethernet0/0), from 10.2.3.1, Send flag is 0x0
      Composite metric is (435200/409600), route is Internal
      Vector metric:
        Minimum bandwidth is 10000 Kbit
        Total delay is 7000 microseconds
        Reliability is 255/255
        Load is 1/255
        Minimum MTU is 1500
        Hop count is 2
        Originating router is 10.255.4.4
  10.3.5.2 (Ethernet0/1), from 10.3.5.2, Send flag is 0x0
      Composite metric is (476416/409600), route is Internal
      Vector metric:
        Minimum bandwidth is 9000 Kbit
        Total delay is 7500 microseconds
        Reliability is 255/255
        Load is 1/255
        Minimum MTU is 1500
        Hop count is 2
        Originating router is 10.255.4.

R3#show ip route 10.255.4.4
Routing entry for 10.255.4.4/32
  Known via "eigrp 100", distance 90, metric 435200, precedence routine (0), type internal
  Redistributing via eigrp 100
  Last update from 10.3.5.2 on Ethernet0/1, 01:39:28 ago
  Routing Descriptor Blocks:
    10.3.5.2, from 10.3.5.2, 01:39:28 ago, via Ethernet0/1
      Route metric is 476416, traffic share count is 73
      Total delay is 7500 microseconds, minimum bandwidth is 9000 Kbit
      Reliability 255/255, minimum MTU 1500 bytes
      Loading 1/255, Hops 2
  * 10.2.3.1, from 10.2.3.1, 01:39:28 ago, via Ethernet0/0
      Route metric is 435200, traffic share count is 80
      Total delay is 7000 microseconds, minimum bandwidth is 10000 Kbit
      Reliability 255/255, minimum MTU 1500 bytes
      Loading 1/255, Hops 2
```

## Conclusion

- Variance: Allows EIGRP to use multiple paths with different metrics. variance 2 allows paths up to twice the best path's metric.
- Feasibility Condition: A backup path must meet EIGRP's feasibility condition to be used for UCMP.
- Load Balancing: EIGRP distributes traffic across qualifying paths based on their metrics, rather than equally.
- Bandwidth and Delay: Changing interface bandwidth and delay affects EIGRP's metric and influences path selection.
- EIGRP Stub: Limits which routes a router advertises and helps reduce unnecessary EIGRP queries.
Overall: UCMP allows EIGRP to use multiple paths with different costs, improving bandwidth utilization and providing additional redundancy.
