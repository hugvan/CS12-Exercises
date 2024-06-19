import wikipedia
from wikipedia import WikipediaPage
import flet as ft
from random import choice

def change_frequency_file():
    w = ""
    with open("PythonFlet/frequents.txt") as file:
        w = file.readline().lower()

    with open("PythonFlet/frequents.txt", "a") as file:
        print(w)
        file.write(w)

def get_frequent_words() -> list[str]:
    with open("PythonFlet/frequents.txt") as file:
        words = file.readline().split()
        return words


def run_game():
    frequent_words = get_frequent_words()
    article = wikipedia.random()
    page = wikipedia.page(article)
    content: list[str] = page.content.split()

    chosen = choice(content).lower()
    while chosen in frequent_words:
        chosen = choice(content)
    

    print(chosen)
    input()
    print(article)


def main(page: ft.Page):
    page.add(ft.SafeArea(ft.Text("Hello, Flet!")))

ft.app(main)
