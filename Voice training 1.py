# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 22:44:34 2023

@author: Lenovo
"""

import speech_recognition as sr
import pyttsx3
import json
import difflib
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
#%%
# Download NLTK resources if not already downloaded
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
#%%
# Initialize the speech recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Initialize WordNet Lemmatizer, Porter Stemmer, and Stopwords
lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()
stop_words = set(stopwords.words('english'))
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
def speak(text):
    engine.say(text)
    engine.runAndWait()
#%%
# Function to preprocess text: stop words removal, lemmatization, and stemming
def preprocess_text(text):
    tokens = word_tokenize(text.lower())  # Tokenize and convert to lowercase
    filtered_tokens = [lemmatizer.lemmatize(stemmer.stem(token)) for token in tokens if token not in stop_words]  # Remove stop words, lemmatize, and stem
    return ' '.join(filtered_tokens)  # Return the preprocessed text as a string
#%%
# Function to load JSON file and preprocess its contents
def load_and_preprocess_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        for entry in data:
            entry['processed_question'] = preprocess_text(entry['question'])  # Preprocess question in the JSON file
    return data
#%%
# Function to find most similar question
def find_most_similar_question(user_input, data):
    user_input_processed = preprocess_text(user_input)
    questions = [entry["processed_question"] for entry in data]
    similarity_scores = difflib.get_close_matches(user_input_processed, questions, n=1, cutoff=0.6)

    if similarity_scores:
        most_similar_question = similarity_scores[0]
        for entry in data:
            if entry["processed_question"] == most_similar_question:
                return most_similar_question, entry["answer"]
    else:
        return None, None
#%%
# Function to generate answer
def answer(user_input):
    json_file_path =  "E:\\upes\\Semester 7\\Major 1\\Data.json"
    data = load_and_preprocess_json(json_file_path)

    most_similar_question, most_similar_answer = find_most_similar_question(user_input, data)

    if most_similar_question:
        ans = most_similar_answer
    else:
        ans = "No matching question found."
    return ans
#%%
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

