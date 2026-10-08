# GRE Over IPsec

## Objective

Configure a GRE over IPsec overlay network with OSPF and an EIGRP underlay network.

## Key Technologies

- GRE Tunnels
- IPsec (IPsec profiles)
- Overlay Network
- EIGRP
- OSPFv2

## Relevant Commands

### R2 + R3

```cisco
router eigrp 1
 network 10.0.0.0
```

### R1

```cisco
router eigrp 1
 network 10.0.0.0 0.0.255.255
 network 10.255.0.0 0.0.255.255

crypto isakmp policy 1
 encr aes
 hash sha256
 authentication pre-share
 group 14
crypto isakmp key key1 address 0.0.0.0
crypto ipsec transform-set transform1 esp-aes esp-sha-hmac
 mode transport
crypto ipsec profile ipsec1
 set transform-set transform1

interface Tunnel1
 ip address 172.16.14.1 255.255.255.252
 tunnel source Loopback0
 tunnel destination 10.255.4.4
 tunnel protection ipsec profile ipsec1

router ospf 1
 network 10.1.0.0 0.0.255.255 area 0
 network 10.254.1.1 0.0.0.0 area 0
 network 172.16.0.0 0.0.255.255 area 0
```

### R4

```cisco
router eigrp 1
 network 10.0.0.0 0.0.255.255
 network 10.255.0.0 0.0.255.255

crypto isakmp policy 1
 encr aes
 hash sha256
 authentication pre-share
 group 14
crypto isakmp key key1 address 0.0.0.0
crypto ipsec transform-set transform1 esp-aes esp-sha-hmac
 mode transport
crypto ipsec profile profile1
 set transform-set transform1

interface Tunnel1
 ip address 172.16.14.2 255.255.255.252
 tunnel source Loopback0
 tunnel destination 10.255.1.1
 tunnel protection ipsec profile profile1

router ospf 1
 network 10.2.0.0 0.0.255.255 area 0
 network 10.254.4.4 0.0.0.0 area 0
 network 172.16.0.0 0.0.255.255 area 0
```

## Verification

### Verification on R1 + R4

```cisco
show interface tunnel 1
show crypto ipsec sa
show ip route
traceroute
```

### Example on R1

`traceroute` from R1 to R4's underlay loopback interface goes through the underlay network

```cisco
R1#traceroute 10.255.4.4 
Type escape sequence to abort.
Tracing the route to 10.255.4.4
VRF info: (vrf in name/id, vrf out name/id)
  1 10.0.12.2 92 msec 96 msec 92 msec
  2 10.0.23.2 188 msec 184 msec 188 msec
  3 10.0.34.2 272 msec 264 msec 272 msec
```

`traceroute` from R1 to R4's overlay loopback interface goes through the tunnel

```cisco
R1#traceroute 10.254.4.4
Type escape sequence to abort.
Tracing the route to 10.254.4.4
VRF info: (vrf in name/id, vrf out name/id)
  1 172.16.14.2 196 msec 256 msec 248 msec
```

command `show crypto ipsec sa` shows how many packets have been encapsulated (`pkts encaps`) and decapsulated (`pkts decaps`)

```cisco
R1#show crypto ipsec sa

interface: Tunnel1
    Crypto map tag: Tunnel1-head-0, local addr 10.255.1.1

   protected vrf: (none)
   local  ident (addr/mask/prot/port): (10.255.1.1/255.255.255.255/47/0)
   remote ident (addr/mask/prot/port): (10.255.4.4/255.255.255.255/47/0)
   current_peer 10.255.4.4 port 500
     PERMIT, flags={origin_is_acl,}
    #pkts encaps: 312, #pkts encrypt: 312, #pkts digest: 312
    #pkts decaps: 303, #pkts decrypt: 303, #pkts verify: 303
    #pkts compressed: 0, #pkts decompressed: 0
    #pkts not compressed: 0, #pkts compr. failed: 0
    #pkts not decompressed: 0, #pkts decompress failed: 0
    #send errors 0, #recv errors 0

     local crypto endpt.: 10.255.1.1, remote crypto endpt.: 10.255.4.4
     path mtu 1500, ip mtu 1500, ip mtu idb FastEthernet0/0
     current outbound spi: 0x2518B928(622377256)
     PFS (Y/N): N, DH group: none

     inbound esp sas:
      spi: 0x59D7440F(1507279887)
        transform: esp-aes esp-sha-hmac ,
        in use settings ={Transport, }
        conn id: 1, flow_id: 1, sibling_flags 80000000, crypto map: Tunnel1-head-0
        sa timing: remaining key lifetime (k/sec): (4608000/870)
        IV size: 16 bytes
        replay detection support: Y
        Status: ACTIVE(ACTIVE)
      spi: 0x22623FFF(576864255)
        transform: esp-aes esp-sha-hmac ,
        in use settings ={Transport, }
        conn id: 3, flow_id: 3, sibling_flags 80004000, crypto map: Tunnel1-head-0
        sa timing: remaining key lifetime (k/sec): (4299068/870)
        IV size: 16 bytes
        replay detection support: Y
        Status: ACTIVE(ACTIVE)

     inbound ah sas:

     inbound pcp sas:

     outbound esp sas:
      spi: 0xB827EDE3(3089624547)
        transform: esp-aes esp-sha-hmac ,
        in use settings ={Transport, }
        conn id: 2, flow_id: 2, sibling_flags 80000000, crypto map: Tunnel1-head-0
        sa timing: remaining key lifetime (k/sec): (4608000/870)
        IV size: 16 bytes
        replay detection support: Y
        Status: ACTIVE(ACTIVE)
      spi: 0x2518B928(622377256)
        transform: esp-aes esp-sha-hmac ,
        in use settings ={Transport, }
        conn id: 4, flow_id: 4, sibling_flags 80004000, crypto map: Tunnel1-head-0
        sa timing: remaining key lifetime (k/sec): (4299067/870)
        IV size: 16 bytes
        replay detection support: Y
        Status: ACTIVE(ACTIVE)

     outbound ah sas:

     outbound pcp sas:

```

## Conclusion

EIGRP was used to provide underlay connectivity between sites, GRE created the overlay network

OSPF was configured on the GRE tunnel to exchange routes independently of the underlay network

IPsec is applied to the GRE tunnel using an IPsec profile.  IPsec can only encapsulate unicast IP traffic.  GRE encapsulates a wide variety of protocols into a unicast IP packet.  Using GRE over IPsec enables a wide variety of protocols to be securely tunneled.
