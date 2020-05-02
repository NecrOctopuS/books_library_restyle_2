from livereload import Server
from jinja2 import Environment, FileSystemLoader, select_autoescape
import json
import os
from dotenv import load_dotenv
from more_itertools import chunked

load_dotenv()
PAGES_FOLDER = os.getenv('PAGES_FOLDER')
BOOKS_PER_PAGE = int(os.getenv('BOOKS_PER_PAGE'))
STATIC_URL = '../' + os.getenv('STATIC_URL')
MEDIA_URL = '../' + os.getenv('MEDIA_URL')
BOOK_INFO_PATH = os.getenv('BOOK_INFO_PATH')


def on_reload(env, chunks):
    template = env.get_template('template.html')
    os.makedirs(PAGES_FOLDER, exist_ok=True)
    max_page_number = len(chunks)
    for chunk_number, chunk in enumerate(chunks):
        current_page_number = chunk_number
        rendered_page = template.render(books=chunk, current_page_number=current_page_number,
                                        max_page_number=max_page_number, static_url=STATIC_URL, media_url=MEDIA_URL,
                                        )
        with open(f'{PAGES_FOLDER}/index{chunk_number}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)


def main():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml']),
        trim_blocks=True
    )

    with open(BOOK_INFO_PATH, "r", encoding="utf8") as my_file:
        file_contents = my_file.read()
    books = json.loads(file_contents)
    chunks = list(chunked(books, BOOKS_PER_PAGE))

    on_reload(env, chunks)
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')


if __name__ == '__main__':
    main()
