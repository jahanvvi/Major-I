import socket
import speech_recognition as sr
import pyttsx3
# Function to recognize speech
recognizer=sr.Recognizer()
engine=pyttsx3.init()
def recognize_speech():
    while True:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            print("Recognizing...")
            text = recognizer.recognize_google(audio)
            print("You said:", text)
            return text
        except sr.UnknownValueError:
            print("Could not understand audio. Please try again.")
        except sr.RequestError as e:
            print(f"Error fetching results; {e}")
    
def speak(text):
    engine.say(text)
    engine.runAndWait()
    
# Set up the client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('192.168.0.195', 12345)  # Change to the IP address and port of the server
client_socket.connect(server_address)

while True:
    # Get text to send
    text=recognize_speech()
    text_to_send = text

    # Send text to the server
    client_socket.sendall(text_to_send.encode('utf-8'))

    # Exit loop if the user types 'exit'
    if text_to_send.lower() == 'exit':
        break
    server_response = client_socket.recv(1024).decode('utf-8')
    speak(server_response)
# Close the connection
client_socket.close()
