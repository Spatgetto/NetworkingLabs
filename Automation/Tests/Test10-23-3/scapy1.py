from scapy.all import *

def icmp_ping(destination):
    ans, unans = sr(IP(dst=destination)/ICMP())
    return ans

def answer_summary(ans):
    for send, recv in ans:
        print(recv.sprintf("%IP.src% is alive"))

def main():
    print("** ICMP Ping **")
    ans = icmp_ping("10.99.99.10")
    answer_summary(ans)

if __name__ == "__main__":
    main()