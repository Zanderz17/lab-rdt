import socket
import random

class Sender:
    def __init__(self, receiver_ip='127.0.0.1', receiver_port=12345, timeout=2):
        self.receiver_ip = receiver_ip
        self.receiver_port = receiver_port
        self.timeout = timeout
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(self.timeout)
        self.seq = 0

    def calculate_checksum(self, data):
        total = 0
        for char in data:
            bits = bin(ord(char))[2:].zfill(8)
            total += bits.count('1')
        return str(total)

    def is_corrupted(self):
        return random.random() < 0.5  # Probabilidad de corrupción => 50 %

    def send_packet(self, data):
        checksum = self.calculate_checksum(data)

        if self.is_corrupted():
            checksum = self.calculate_checksum(data)
           
            data = self.corrupt_data(data)
            #print(f"Sending Packet: '{data}'")

        #print(f"sender_checksum: {checksum}")
        packet = f"{self.seq}|{data}|{checksum}"
        self.sock.sendto(packet.encode(), (self.receiver_ip, self.receiver_port))
        print(f"Sender: Sending Packet {self.seq}")

    def corrupt_data(self, data):
        # Altera UN carácter en los datos
        if len(data) == 0:
            return data
        index = random.randint(0, len(data)-1)
        corrupted_char = chr((ord(data[index]) + 1) % 256)
        return data[:index] + corrupted_char + data[index+1:]

    def wait_for_ack(self):
        try:
            response, _ = self.sock.recvfrom(1024)
            response = response.decode()
            return response
        except socket.timeout:
            print(f"Sender: Timeout, resending packet {self.seq}")
            return None

    def send_data(self, data_list):
        for data in data_list:
            while True:
                self.send_packet(data)
                response = self.wait_for_ack()
                if response == "ACK":
                    print(f"Sender: ACK received for Packet {self.seq}")
                    self.seq = self.seq + 1
                    break
                else:
                    print(f"Sender: Timeout, resending packet {self.seq}")



if __name__ == "__main__":
    sender = Sender()
    datos_a_enviar = ["Hola", "Somos", "El", "Grupo3"]
    sender.send_data(datos_a_enviar)
