import pyshark
import matplotlib.pyplot as plt

def compute_data(path):
    file = pyshark.FileCapture(path)

    sent = 0
    received = 0
    first_packet = None

    for packet in file:
        if packet.transport_layer == 'UDP':
            if packet.udp.srcport == '443' or packet.udp.dstport == '443':
                last_packet = packet.sniff_time
                if sent == 0 and received == 0:
                    first_packet = packet.sniff_time
                if packet.udp.srcport == '443':
                    sent += int(packet.udp.length)
                else:
                    received += int(packet.udp.length)

    print("for " + path)
    diff_time = last_packet-first_packet
    print("diff_time : " + str(diff_time.total_seconds()))
    print("sent : " + str(sent))
    sent_per_min = (sent/(diff_time.total_seconds()/60))
    print("sent_per_min : " + str(sent_per_min) + "\n")
    received_per_min = (received/(diff_time.total_seconds()/60))
    print("received : " + str(received))
    print("received_per_min : " + str(received_per_min) + "\n\n")
    return sent_per_min, received_per_min

audio_data = compute_data('./Diff_Wifi/Audio/audio.pcapng')
video_data = compute_data('./Diff_Wifi/Video/video.pcapng')
message_data = compute_data('./Diff_Wifi/Message/message.pcapng')

sent_data = [audio_data[0], video_data[0], message_data[0]]
received_data = [audio_data[1], video_data[1], message_data[1]]

fig, ax1 = plt.subplots()
plt.title("Volume de donnée en transit")
ax1.bar(["audio", "video", "message"], sent_data, 0.5, label='Première paire')
ax1.set_title('Donnée envoyées (en octets/min)')
plt.savefig("Graphes_data_sent.png")

fig2, ax2 = plt.subplots()
ax2.bar(["audio", "video", "message"], received_data, 0.5, label='Première paire')
ax2.set_title('Donnée recues (en octets/min)')
plt.xlabel("Type de communication")
plt.ylabel("Volume de donnée (Bytes/min)")

plt.savefig("Graphes_data_received.png")

""" plt.subplots_adjust(hspace=0.5) """

plt.show()