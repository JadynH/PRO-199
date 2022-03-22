from os import remove
import socket
from threading import Thread
import random

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.3'
port = 4000

server.bind((ip_address, port))
server.listen()

list_of_clients = []
questions = [
    "What is the Italian word for pie? \n a.Pizza \n b.Piza \n c.PI \n d.Pizza Pizza",

    "Which sea creature has three hearts? \n a.Octopus \n b.Walrus \n c.Dolphin \n d.Seal",

    "What element does not exist? \n a.Re \n b.Xf \n c.Si \n d.Pa",

    "Who is Loki? \n a.God of Thunder \n b.God of Light \n c.God of Ice \n d.God of Mischief",

    "Who was the first Avenger? \n a.Captain America \n b.Winter Soldier \n c.IronMan \n d.Nick Fury",

    "How many bones does an adult human have? \n a.206 \n b.208 \n c.201 \n d.196",

    "What was Black Widow's name when she was appointed as Tony Stark's new assitant? \n a.Natalie Rushman \n b.Natalia Romanoff \n c.Nicole Rohan \n d.Naya Robe",

    "What phrase does Tony Stark and his daughter share? \n a.It's just business. \n b.I got this! \n c.I love you 3000! \n c.Nothing"
]

answers=[ 'a.', 'a.', 'b.', 'd.', 'c.', 'a.', 'a.', 'c.']


def get_random_question_answer(conn):
    random_index = random.randint(0,len(questions)-1)
    random_question = questions[random_index]
    random_answer = answers[random_index]
    conn.send(random_question.encode('utf-8'))
    return random_index, random_question, random_answer

def remove_question(index):
    questions.pop(index)
    answers.pop(index)

def clientthread(conn):
    score=0
    conn.send("Welcome to this quiz game!".encode("utf-8"))
    conn.send("You will receive a question. The answer to that question should be either a, b, c, or d.")
    conn.send("Good luck!\n\n".encode("utf-8"))
    index, question, answer= get_random_question_answer(conn)
    while True:
        try:
            message = conn.recv(2048).decode("utf-8")
            if message:
                if message.lower() == answer:
                    score += 1
                    conn.send(f"Awesome! Your score is {score}\n\n".encode("utf-8"))
                else:
                    conn.send("Incorrect! Try again!\n\n".encode("utf-8"))
                remove_question(index)
                index, question, answer=get_random_question_answer(conn)
            else:
                remove(conn)
        except:
            continue