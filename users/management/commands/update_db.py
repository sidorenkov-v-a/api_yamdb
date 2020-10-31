import csv
import datetime
import sqlite3

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        conn = sqlite3.connect('db.sqlite3')
        c = conn.cursor()

        with open('data/users.csv', 'r', encoding='utf8') as users_data:
            reader = csv.DictReader(users_data)
            for row in reader:
                pk = row['id']
                password = ' '
                username = row['username']
                email = row['email']
                role = row['role']
                bio = row['description']
                first_name = row['first_name']
                last_name = row['last_name']
                date_joined = datetime.datetime.now()
                if role == 'user':
                    is_superuser = False
                    is_staff = False
                    is_active = True
                elif role == 'moderator':
                    is_superuser = False
                    is_staff = True
                    is_active = True
                elif role == 'admin':
                    is_superuser = True
                    is_staff = False
                    is_active = True

                try:
                    c.execute(
                        'INSERT INTO users_user '
                        '(id, password, username, email, role, bio, '
                        'first_name, last_name, is_superuser, '
                        'is_staff, is_active, date_joined) '
                        'VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                        (pk, password, username, email, role, bio, first_name,
                         last_name, is_superuser, is_staff, is_active,
                         date_joined)
                    )
                except sqlite3.IntegrityError:
                    pass
                conn.commit()

        with open('data/category.csv', 'r', encoding='utf8') as category_data:
            reader = csv.DictReader(category_data)
            for row in reader:
                pk = row['id']
                name = row['name']
                slug = row['slug']
                try:
                    c.execute(
                        'INSERT INTO titles_category'
                        '(id, name, slug)'
                        'VALUES(?, ?, ?)',
                        (pk, name, slug)
                    )
                except sqlite3.IntegrityError:
                    pass
                conn.commit()

        with open('data/comments.csv', 'r', encoding='utf8') as comments_data:
            reader = csv.DictReader(comments_data)
            for row in reader:
                pk = row['id']
                text = row['text']
                pub_date = row['pub_date']
                author_id = row['author']
                review_id = row['review_id']
                try:
                    c.execute(
                        'INSERT INTO reviews_comment'
                        '(id, text, pub_date, author_id, review_id)'
                        'VALUES(?, ?, ?, ?, ?)',
                        (pk, text, pub_date, author_id, review_id)
                    )
                except sqlite3.IntegrityError:
                    pass
                conn.commit()

        with open('data/genre.csv', 'r', encoding='utf8') as genre_data:
            reader = csv.DictReader(genre_data)
            for row in reader:
                pk = row['id']
                name = row['name']
                slug = row['slug']
                try:
                    c.execute(
                        'INSERT INTO titles_genre'
                        '(id, name, slug)'
                        'VALUES(?, ?, ?)',
                        (pk, name, slug)
                    )
                except sqlite3.IntegrityError:
                    pass
                conn.commit()

        with open('data/genre_title.csv', 'r',
                  encoding='utf8') as genre_titles_data:
            reader = csv.DictReader(genre_titles_data)
            for row in reader:
                pk = row['id']
                title_id = row['title_id']
                genre_id = row['genre_id']
                try:
                    c.execute(
                        'INSERT INTO titles_title_genre'
                        '(id, title_id, genre_id)'
                        'VALUES(?, ?, ?)',
                        (pk, title_id, genre_id)
                    )
                except sqlite3.IntegrityError:
                    pass
                conn.commit()

        with open('data/review.csv', 'r', encoding='utf8') as review_data:
            reader = csv.DictReader(review_data)

            for row in reader:
                pk = row['id']
                text = row['text']
                score = row['score']
                pub_date = row['pub_date']
                author_id = row['author']
                title_id = row['title_id']

                try:
                    c.execute(
                        'INSERT INTO reviews_review'
                        '(id, text, score, pub_date, author_id, title_id)'
                        'VALUES(?, ?, ?, ?, ?, ?)',
                        (pk, text, score, pub_date, author_id, title_id)
                    )
                except sqlite3.IntegrityError:
                    pass
                conn.commit()

        with open('data/titles.csv', 'r', encoding='utf8') as titles_data:
            reader = csv.DictReader(titles_data)

            for row in reader:
                pk = row['id']
                name = row['name']
                year = row['year']
                description = ''
                category_id = row['category']

                try:
                    c.execute(
                        'INSERT INTO titles_title'
                        '(id, name, year, description, category_id)'
                        'VALUES(?, ?, ?, ?, ?)',
                        (pk, name, year, description, category_id)
                    )
                except sqlite3.IntegrityError:
                    pass
                conn.commit()

        conn.close()
