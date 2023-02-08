import socket
import pyaudio
import threading

streams = []


def handle_client(client, address):
    print("User connected:", address)

    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1,
                        rate=44100, output=True)

    streams.append(stream)

    while True:
        try:
            data = client.recv(1024)
            if not data:
                break
            for listeners in streams:
                if listeners != stream:
                    listeners.write(data)
        except:
            # This means the client disconnected, and now time for clean up.
            break

    streams.remove(stream) # Do not remove this, if a client disconnects, it'd spam errors, thank you.
    stream.stop_stream()
    stream.close()
    audio.terminate()
    print('User disconnected:', address) # Making sure the client disconnected perfectly.


# Listen for user's input (REQUIRED, DO NOT TOUCH)
host = input('Enter the host: ')
port = input('Enter the port: ')

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((str(host), int(port)))
server.listen(5)


# Accept connections, multi-threading is required here.
print('I\'m live and I\'ll be accepting connections!')
while True:
    client, address = server.accept()
    client_thread = threading.Thread(
        target=handle_client, args=(client, address))
    client_thread.start()
