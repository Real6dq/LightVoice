import socket
import pyaudio

# Listen for user's input (REQUIRED, DO NOT TOUCH!)
host = input('Enter the host: ')
port = input('Enter the port: ')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((str(host), int(port)))

# Start the audio stream (THIS IS REQUIRED, DO NOT TOUCH!)
audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True)

print('We\'ve been been connected to the server!')
while True:
    try:
        data = stream.read(1024)
        client.sendall(data)
    except:
        break

# Clean up (Useless unless the server crashes of course)
print('We\'ve been disconnected from the server!')
stream.stop_stream()
stream.close()
audio.terminate()
client.close()
