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
    return sent_per_min/1000, received_per_min/1000

audio_data = compute_data('./Diff_Wifi/Audio/audio.pcapng')
video_data = compute_data('./Diff_Wifi/Video/video.pcapng')
message_data = compute_data('./Diff_Wifi/Message/message.pcapng')
screen_data = compute_data('./Diff_Wifi/Screen/screen.pcapng')
file_data = compute_data('./Diff_Wifi/File/file.pcapng')

sent_data = [audio_data[0], video_data[0], screen_data[0], file_data[0], message_data[0]]
received_data = [audio_data[1], video_data[1], screen_data[1], file_data[1], message_data[1]]

barwidth = 0.4
x1 = [0, 1, 2, 3, 4]
x2 = [x + barwidth for x in x1]

plt.title("Volume de donnée en transit (Ko/min)")
b1 = plt.bar(x1, sent_data, edgecolor="black", color="red", width=0.4, linewidth=1)
b2 = plt.bar(x2, received_data, edgecolor="black", width=0.4, linewidth=1)
plt.grid(axis="y")
plt.legend([b1,b2], ["Données reçues", "Données envoyées"])
plt.xticks([r + barwidth / 2 for r in x1], ['Audio', 'Video', 'Screen', 'File', 'Message'])

plt.xlabel("Type de communication")
plt.ylabel("Volume de donnée (Ko/min)")
plt.savefig("Graphes_data.png")

plt.show()