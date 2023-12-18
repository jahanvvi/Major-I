# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 00:35:12 2023

@author: Lenovo
"""

import socket
import tkinter as tk
import speech_recognition as sr
import pyttsx3
import sys
import threading
import time

# Function to recognize speech
recognizer = sr.Recognizer()
engine = pyttsx3.init()
#%%
def update_listening_status(status):
    listening_label.config(text=status)
    root.update()  # Update the GUI to display changes immediately
user_input=""
def recognize_speech():
    while True:
        with sr.Microphone() as source:
            update_listening_status("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
    
        try:
            update_listening_status("Recognizing...")
            text = recognizer.recognize_google(audio)
           #print(text)
            return text
        except sr.UnknownValueError:
            update_listening_status("Could not understand audio")
            speak("Sorry, Could not understand Audio") 
            time.sleep(1)  # Display "Could not understand audio" for 5 seconds
             # Clear the message after 5 seconds
        except sr.RequestError as e:
            update_listening_status(f"Error fetching results; {e}")
#%%
def speak(text):
    engine.say(text)
    engine.runAndWait()
#%%
def start_server():
    global server_running
    server_address = ('192.168.0.195', 12345)  # Change to the server's IP address and port
    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(server_address)
    server_running = True

    while server_running:
        text = recognize_speech()
        text_to_send = text

        client_socket.sendall(text_to_send.encode('utf-8'))

        if text_to_send.lower() == 'exit'or text_to_send.lower()=="thank you" or text_to_send.lower()=="thank":
            speak("Thank You")
            break

        server_response = client_socket.recv(1024).decode('utf-8')
        speak(server_response)
        text_box.insert(tk.END,f"\nUser: {text}\n","User")
        text_box.insert(tk.END, f"Agent: {server_response}\n\n","Agent")
        text_box.see(tk.END)  # Auto-scroll to the bottom of the text widget

    client_socket.close()
#%%
def stop_server():
    root.destroy()
    execfile("SERVER_UI.py",globals())
#%%
class ConsoleRedirector:
    def __init__(self, widget):
        self.widget = widget
        self.widget.tag_config("User", foreground="red")   # Tag for user messages (red text)
        self.widget.tag_config("Agent", foreground="green")  # Tag for server messages (green text)
        self.widget.tag_config("heading", font=("Arial", 16, "bold"), foreground="green")  # Tag for heading (blue text)
        self.widget.insert(tk.END, "Chat Box\n", "heading")  # Insert the heading at the beginning

    def write(self, message, is_user=True):
        tag = "user" if is_user else "server"
        self.widget.insert(tk.END, f"{message}\n", (tag,))
        self.widget.see(tk.END)
         
root = tk.Tk()
root.title("Speech Recognition Client")

# Create left and right frames to divide the GUI vertically
left_frame = tk.Frame(root, width=400, height=600)
left_frame.pack(side=tk.LEFT)

right_frame = tk.Frame(root, width=400, height=600)
right_frame.pack(side=tk.RIGHT)

# Load the background image for the right frame
bg_image_right = tk.PhotoImage(file="E:\\upes\\Semester 7\\Major 1\\pic2.png")
right_canvas = tk.Canvas(right_frame, width=bg_image_right.width(), height=bg_image_right.height())
right_canvas.pack(fill=tk.BOTH, expand=True)
right_canvas.create_image(0, 0, anchor=tk.NW, image=bg_image_right)

# Set background color of the message box in the left frame
text_box = tk.Text(left_frame, height=120, width=40, bg="black", fg="white", insertbackground="white")
 
text_box.pack(padx=10, pady=10)

# Create a Label widget in the left frame
listening_label = tk.Label(right_frame, text="", font=("Arial", 14),bg="black",fg="white")
listening_label.place(relx=0.54, rely=0.4, anchor=tk.CENTER)

# Redirect console output to the Text widget
console_redirector = ConsoleRedirector(text_box)
sys.stdout = console_redirector

# Create buttons in the left frame
start_button = tk.Button(right_frame, text="Connect Agent", command=start_server, height=2, width=15,bg="black",fg="white")
start_button.place(relx=0.1, rely=0.3, anchor=tk.CENTER)

stop_button = tk.Button(right_frame, text="Refresh", command=stop_server, height=2, width=15,bg="black",fg="white")
stop_button.place(relx=0.9, rely=0.3, anchor=tk.CENTER)

server_running = False
client_socket = None

root.mainloop()