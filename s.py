import socket
import time
import argparse
from tqdm import tqdm

def udp_stress_test(target_host, target_port, packets_per_second):
    packet_size = 32  # Размер пакета в байтах (статический)
    packet_count = 9999999  # Общее количество пакетов (статический)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (target_host, target_port)
    message = b'A' * packet_size
    delay = 1 / packets_per_second if packets_per_second > 0 else 0

    print(f"Отправка {packet_count} пакетов на {target_host}:{target_port}")
    print(f"Лимит: {packets_per_second} пакетов/сек. Размер пакета: {packet_size} байт.")
    
    for _ in tqdm(range(packet_count), desc="Отправка пакетов"):
        sock.sendto(message, server_address)
        if delay > 0:
            time.sleep(delay)
    sock.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UDP стресс-тест клиента.")
    parser.add_argument("target_host", help="Целевой IP-адрес или хостнейм.")
    parser.add_argument("target_port", type=int, help="Целевой порт.")
    parser.add_argument("packets_per_second", type=int, help="Лимит отправки пакетов в секунду.")

    args = parser.parse_args()

    udp_stress_test(
        target_host=args.target_host,
        target_port=args.target_port,
        packets_per_second=args.packets_per_second
    )
