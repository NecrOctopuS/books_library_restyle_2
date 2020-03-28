from livereload import Server
from jinja2 import Environment, FileSystemLoader, select_autoescape
import json
import os

folder = 'pages'
BOOKS_PER_PAGE = 6


def on_reload():
    template = env.get_template('template.html')
    os.makedirs(folder, exist_ok=True)
    max_page_number = len(chunks)
    for chunk_number, chunk in enumerate(chunks):
        current_page_number = chunk_number
        rendered_page = template.render(books=chunk, current_page_number=current_page_number,
                                        max_page_number=max_page_number)
        with open(f'{folder}/index{chunk_number}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

with open("book_informations.json", "r", encoding="utf8") as my_file:
    book_informations = my_file.read()
books = json.loads(book_informations)
chunks = [books[x:x + BOOKS_PER_PAGE] for x in range(0, len(books), BOOKS_PER_PAGE)]

on_reload()
server = Server()
server.watch('template.html', on_reload)
server.serve(root='.')