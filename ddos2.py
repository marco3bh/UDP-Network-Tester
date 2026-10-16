import argparse
import socket
import time

MODES = {
    "UDP-Flood": 375,
    "UDP-Power": 750,
    "UDP-Mix": None,
}


def run_test(host, port, method, duration, pps):
    if host not in ("127.0.0.1", "localhost", "::1"):
        raise ValueError("Only localhost testing is supported.")

    if method not in MODES:
        raise ValueError("Invalid test mode.")

    if duration <= 0 or duration > 30:
        raise ValueError("Duration must be between 1 and 30 seconds.")

    if pps <= 0 or pps > 1000:
        raise ValueError("Packet rate must be between 1 and 100 PPS.")

    target = ("127.0.0.1", port)
    interval = 1.0 / pps
    packets = 0
    bytes_sent = 0

    print(f"Target: {target[0]}:{port}")
    print(f"Mode: {method}")
    print(f"Duration: {duration}s")
    print(f"Maximum rate: {pps} packets/sec")

    start = time.monotonic()
    end = start + duration
    next_send = start

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        while time.monotonic() < end:
            now = time.monotonic()

            if now < next_send:
                time.sleep(min(next_send - now, end - now))
                continue

            if method == "UDP-Mix":
                size = 375 if packets % 2 == 0 else 750
            else:
                size = MODES[method]

            payload = b"X" * size
            sent = sock.sendto(payload, target)

            packets += 1
            bytes_sent += sent

            next_send = max(next_send + interval, time.monotonic())

    elapsed = time.monotonic() - start

    print("\n--- Results ---")
    print(f"Packets sent: {packets}")
    print(f"Bytes sent: {bytes_sent}")
    print(f"Elapsed: {elapsed:.2f}s")
    print(f"Average PPS: {packets / elapsed:.2f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Local UDP load testing experiment"
    )

    parser.add_argument("host")
    parser.add_argument("port", type=int)
    parser.add_argument("method", choices=MODES.keys())
    parser.add_argument("--duration", type=int, default=5)
    parser.add_argument("--pps", type=int, default=20)

    args = parser.parse_args()

    if not 1 <= args.port <= 65535:
        parser.error("Port must be between 1 and 65535.")

    try:
        run_test(
            args.host,
            args.port,
            args.method,
            args.duration,
            args.pps,
        )
    except (OSError, ValueError) as error:
        parser.exit(1, f"Error: {error}\n")
