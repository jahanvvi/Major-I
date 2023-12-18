

import speech_recognition as sr
import pyttsx3
import json
import difflib
#%%
# Initialize the speech recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()
#%%
# Function to recognize speech
def recognize_speech():
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
        print("Could not understand audio")
        return ""
    except sr.RequestError as e:
        print("Error fetching results; {0}".format(e))
        return ""
#%%
# Function to speak out the response
def speak(text):
    engine.say(text)
    engine.runAndWait()

#%%
def load_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data
#%%
def find_most_similar_question(user_input, data):
    questions = [entry["question"] for entry in data]
    similarity_scores = difflib.get_close_matches(user_input, questions, n=1, cutoff=0.6)

    if similarity_scores:
        most_similar_question = similarity_scores[0]
        for entry in data:
            if entry["question"] == most_similar_question:
                return most_similar_question, entry["answer"]
    else:
        return None, None
#%%
def answer(user_input):
    json_file_path =  "E:\\upes\\Semester 7\\Major 1\\Data.json"
    data = load_json_file(json_file_path)


    most_similar_question, most_similar_answer = find_most_similar_question(user_input, data)

    if most_similar_question:
        ans= most_similar_answer
    else:
        ans="No matching question found."
    return ans


#%%
# Main function to handle voice interaction
def voice_assistant():
    speak("Hello! I am Jarvis. How can I help you?")
    while True:
        user_input = recognize_speech().lower()
        
        if "exit" in user_input:
            speak("Exiting. Goodbye!")
            break
        
        else:
            speak(answer(user_input))
            print(answer(user_input))
        
        # Example response
#%%
if __name__ == "__main__":
    voice_assistant()
