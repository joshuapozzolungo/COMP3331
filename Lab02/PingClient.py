import socket
import random
import time
import sys
from datetime import datetime

NUM_PACKETS = 15

hostname = sys.argv[1]
port = int(sys.argv[2])

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(0.6)

seq = random.randint(40000, 50000)

packetsLost = 0
packetRTTs = []

totalTransTimeStart = time.time()

for i in range(0, NUM_PACKETS):
    pingMessage = f"PING {seq} {datetime.now()}"
    encodedMessage = pingMessage.encode("utf-8")

    try:
        startTime = time.time()

        sock.sendto(encodedMessage, (hostname, port))
        response, _ = sock.recvfrom(1024)

        totalTransTimeEnd = time.time()
        endTime = time.time()
        RTT = (endTime - startTime) * 1000
        
        packetRTTs.append(round(RTT))

        print(f"PING to {hostname}, seq={seq}, rtt={round(RTT)} ms")

    except socket.timeout:
        print(f"PING to {hostname}, seq={seq}, rtt=timeout")
        packetsLost += 1         
    except socket.gaierror:
        print("Invalid hostname")
        exit(1)
    except ConnectionRefusedError:
        print("No server listening on selected port")
        exit(1)
    except ConnectionResetError:
        print("Server droppoed our unexpectedly")
        exit(1)
    except Exception:
        print("something went wrong")
        exit(1)

    seq += 1

sock.close()

packetLoss = (packetsLost / NUM_PACKETS) * 100
differences = [abs(packetRTTs[n] - packetRTTs[n - 1]) for n in range(1, len(packetRTTs))]
totalTransmissionTime = (totalTransTimeEnd - totalTransTimeStart) * 1000

if len(packetRTTs) == 0:
    jitter = 0
else:
    jitter = sum(differences) / len(packetRTTs) - 1

print(f"Packet loss: {round(packetLoss)}%")
print(f"Minimum RTT: {min(packetRTTs)} ms, Maximum RTT: {max(packetRTTs)} ms, Average RTT: {round(sum(packetRTTs) / NUM_PACKETS)} ms")
print(f"Total Transmission Time: {round(totalTransmissionTime)} ms")
print(f"Jitter: {round(jitter)} ms")