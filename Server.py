import socket
import threading
import socket
import json
import difflib
import streamlit as st
import asyncio

def load_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

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

def answer(user_input):
    json_file_path =  "E:/college_projects/Major-1/try/Data.json"
    data = load_json_file(json_file_path)


    most_similar_question, most_similar_answer = find_most_similar_question(user_input, data)

    if most_similar_question:
        ans= most_similar_answer
    else:
        ans="No matching question found."
    return ans

import asyncio

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print("Accepted connection from", addr)

    try:
        while True:
            data = await reader.read(100)
            if not data:
                break

            message = data.decode()
            print(f"Received {message!r} from {addr}")

            server_response = answer(message)
            writer.write(server_response.encode())
            await writer.drain()

            if server_response.lower() == 'exit':
                break
    except asyncio.CancelledError:
        pass
    finally:
        print("Connection with", addr, "closed")
        writer.close()

async def main():
    server = await asyncio.start_server(
        handle_client, '192.168.111.178', 12345)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()

if name == 'main':
    asyncio.run(main())import socket
import threading
import socket
import json
import difflib
import streamlit as st
import asyncio


def load_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

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

def answer(user_input):
    json_file_path =  "E:/college_projects/Major-1/try/Data.json"
    data = load_json_file(json_file_path)


    most_similar_question, most_similar_answer = find_most_similar_question(user_input, data)

    if most_similar_question:
        ans= most_similar_answer
    else:
        ans="No matching question found."
    return ans

import asyncio

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print("Accepted connection from", addr)

    try:
        while True:
            data = await reader.read(100)
            if not data:
                break

            message = data.decode()
            print(f"Received {message!r} from {addr}")

            server_response = answer(message)
            writer.write(server_response.encode())
            await writer.drain()

            if server_response.lower() == 'exit':
                break
    except asyncio.CancelledError:
        pass
    finally:
        print("Connection with", addr, "closed")
        writer.close()

async def main():
    server = await asyncio.start_server(
        handle_client, '192.168.111.178', 12345)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()

if name == 'main':
    asyncio.run(main())