import socket

class Receiver:
    def __init__(self, ip='127.0.0.1', port=12345):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.ip, self.port))
        print(f"Receiver: Escuchando en {self.ip}:{self.port}")

    def calculate_checksum(self, data):
        total = 0
        for char in data:
            bits = bin(ord(char))[2:].zfill(8)
            total += bits.count('1')
        return str(total)

    def is_corrupted(self, data, checksum):
        calculated_checksum = self.calculate_checksum(data)
        return calculated_checksum != checksum

    def listen(self):
        while True:
            packet, addr = self.sock.recvfrom(1024)
            received_seq, data, recv_checksum = packet.decode().split('|')
            received_seq = int(received_seq)

            #print(f"receiver_checksum: {recv_checksum}")

            # Simular detección de corrupción
            if self.is_corrupted(data, recv_checksum):
                print(f"Receiver: Packet {received_seq} is corrupted. Sending NAK")
                self.sock.sendto(f"NAK".encode(), addr)
            else:
                print(f"Receiver: Successfully received Packet {received_seq}. Sending ACK.")
                self.sock.sendto(f"ACK".encode(), addr)


if __name__ == "__main__":
    receiver = Receiver()
    receiver.listen()
