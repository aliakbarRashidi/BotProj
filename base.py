import os
import sqlite3
import datetime


class BaseUser:
    current_directory = os.getcwd()

    def __init__(self, username, user_id):
        """
        Иницилизация класса
        """
        self.username = username
        self.user_id = user_id
        self.basename = (BaseUser.current_directory + '/' + self.username + '.db')
        self.conn = ''
        self.create_base()
        self.create_table_users()
        self.create_table_followers()
        self.create_table_following()
        self.create_table_posts()
        self.create_table_likes()
        self.create_table_comments()
        self.create_table_users_statistic()

    def create_base(self):
        """
        Функция для создания базы данных
        """
        self.conn = sqlite3.connect(self.basename)
        self.conn.close()

    def create_table_users(self):
        """
        Функция для создания таблицы users
        """
        self.conn = sqlite3.connect(self.basename)
        c = self.conn.cursor()
        c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY NOT NULL UNIQUE,
            username text,
            is_private BOOLEAN DEFAULT TRUE,
            fr BOOLEAN DEFAULT 0,
            fw BOOLEAN DEFAULT 0,
            old_fw BOOLEAN DEFAULT 0
        );
        ''')
        self.conn.commit()
        self.conn.close()

    def create_table_followers(self):
        """
        Функция для создания таблицы followers
        """
        self.conn = sqlite3.connect(self.basename)
        c = self.conn.cursor()
        c.execute('''
        CREATE TABLE IF NOT EXISTS followers (
            main_follower_user_id text,
            main_user_user_id INTEGER,
            follower_user_id INTEGER,
            date_follower DATETIME,
            FOREIGN KEY (main_user_user_id) REFERENCES users (user_id)
            ON DELETE CASCADE ON UPDATE NO ACTION
            FOREIGN KEY (follower_user_id) REFERENCES users (user_id)
            ON DELETE CASCADE ON UPDATE NO ACTION
        );
        ''')
        self.conn.commit()
        self.conn.close()

    def create_table_following(self):
        """
        Функция для создания таблицы following
        """
        self.conn = sqlite3.connect(self.basename)
        c = self.conn.cursor()
        c.execute('''
        CREATE TABLE IF NOT EXISTS following (
            main_following_user_id text,
            main_user_user_id INTEGER,
            following_user_id INTEGER,
            date_follower DATETIME,
            FOREIGN KEY (main_user_user_id) REFERENCES users (user_id)
            ON DELETE CASCADE ON UPDATE NO ACTION
            FOREIGN KEY (following_user_id) REFERENCES users (user_id)
            ON DELETE CASCADE ON UPDATE NO ACTION
        );
        ''')
        self.conn.commit()
        self.conn.close()

    def create_table_posts(self):
        """
        Функция для создания таблицы posts
        """
        self.conn = sqlite3.connect(self.basename)
        c = self.conn.cursor()
        c.execute('''
        CREATE TABLE IF NOT EXISTS posts (
             post_id text,
             user_id INTEGER,
             title text,
             u_long REAL DEFAULT 0,
             u_lat REAL DEFAULT 0,
             p_long REAL DEFAULT 0,
             p_lat REAL DEFAULT 0,
             p_lock_name TEXT DEFAULT None,
             has_liked BOOLEAN DEFAULT False,
             post_datetime DATETIME,
             FOREIGN KEY (user_id) REFERENCES users (user_id)
             ON DELETE CASCADE ON UPDATE NO ACTION
            );
        ''')
        self.conn.commit()
        self.conn.close()

    def create_table_likes(self):
        """
        Функция для создания таблицы likes
        """
        self.conn = sqlite3.connect(self.basename)
        c = self.conn.cursor()
        c.execute('''
        CREATE TABLE IF NOT EXISTS likes (
             like_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
             post_id INTEGER,
             user_id INTEGER,
             like_b BOOLEAN DEFAULT False,
             dislike_b BOOLEAN DEFAULT False,
             date_like DATETIME,
             date_dislike DATETIME,
             FOREIGN KEY (post_id) REFERENCES posts (post_id)
             ON DELETE CASCADE ON UPDATE NO ACTION,
             FOREIGN KEY (user_id) REFERENCES users (user_id)
             ON DELETE CASCADE ON UPDATE NO ACTION
            );
        ''')
        self.conn.commit()
        self.conn.close()

    def create_table_comments(self):
        """
        Функция для создания таблицы comments
        """
        self.conn = sqlite3.connect(self.basename)
        c = self.conn.cursor()
        c.execute('''
        CREATE TABLE IF NOT EXISTS comments (
             comment_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
             post_id INTEGER,
             user_id INTEGER,
             comment text,
             FOREIGN KEY (post_id) REFERENCES posts (post_id)
             ON DELETE CASCADE ON UPDATE NO ACTION,
             FOREIGN KEY (user_id) REFERENCES users (user_id)
             ON DELETE CASCADE ON UPDATE NO ACTION
            );
        ''')
        self.conn.commit()
        self.conn.close()

    def create_table_users_statistic(self):
        """
        Функция для создания таблицы users_statistic
        """
        self.conn = sqlite3.connect(self.basename)
        c = self.conn.cursor()
        c.execute('''
        CREATE TABLE IF NOT EXISTS users_statistic (
             user_id INTEGER,
             ratio_fw_fr REAL DEFAULT 0,
             mutual_per REAL DEFAULT 0,
             adherence_per REAL DEFAULT 0,
             like_per_post REAL DEFAULT 0,
             likes REAL DEFAULT 0,
             posts REAL DEFAULT 0,
             likable REAL DEFAULT 0,
             FOREIGN KEY (user_id) REFERENCES users (user_id)
             ON DELETE CASCADE ON UPDATE NO ACTION
            );
        ''')
        self.conn.commit()
        self.conn.close()

    def add_to_base(self, table_name: str, columns: list, values: list):
        """
        Функция для добавления строки в базу данных
        table_name - имя таблицы
        columns - наименование колонок таблицы
        values - вставляемые в колонки значения
        """
        # Формирование строки с наименованием колонок для вставки в sql запрос
        columns_insert = ''
        for col in columns:
            columns_insert += str(col) + ', '
        columns_insert = columns_insert[:-2]

        # Формирование строки со значениями для вставки в sql запрос
        values_insert = ''
        for val in values:
            if type(val) == str:
                values_insert += "'" + str(val) + "'" + ', '
            else:
                values_insert += str(val) + ', '
        values_insert = values_insert[:-2]

        sql_req = '''INSERT OR IGNORE INTO {0} ({1}) VALUES ({2});'''.format(table_name, columns_insert, values_insert)
        self.conn = sqlite3.connect(self.basename)
        c = self.conn.cursor()
        c.execute(sql_req)
        self.conn.commit()
        self.conn.close()

    def add_followers(self, user_id: int, followers: dict):
        """
        Функция для добавления строки в базу данных
        user_id - пользователь, чьи подписчики добавляются в таблицу
        followers - подписчики {user_id: {'username': username, 'is_private': 1,0}
        """
        new_followers = []
        for f_user_id, info in followers.items():
            self.add_user(f_user_id, info['username'], info['is_private'])
            new_followers.append((str(user_id) + '_' + str(f_user_id), user_id, f_user_id, datetime.datetime.today()))
        self.conn = sqlite3.connect(self.basename)
        c = self.conn.cursor()
        c.executemany("INSERT OR IGNORE INTO 'followers' VALUES (?, ?, ?, ?);", new_followers)
        self.conn.commit()
        self.conn.close()

    def add_followings(self, user_id: int, followings: dict):
        """
        Функция для добавления строки в базу данных
        user_id - пользователь, чьи подписки добавляются в таблицу
        followings - подписки {user_id: {'username': username, 'is_private': 1,0}
        """
        new_followings = []
        for f_user_id, info in followings.items():
            self.add_user(f_user_id, info['username'], info['is_private'])
            new_followings.append((str(user_id) + '_' + str(f_user_id), user_id, f_user_id, datetime.datetime.today()))
        self.conn = sqlite3.connect(self.basename)
        c = self.conn.cursor()
        c.executemany("INSERT OR IGNORE INTO 'following' VALUES (?, ?, ?, ?);", new_followings)
        self.conn.commit()
        self.conn.close()

    def change_from_base(self, table_name: str, change_columns: dict, where_column: dict):
        """
        Функция для добавления строки в базу данных
        table_name - имя таблицы
        change_columns - изменяемые по колонкам (key) значения (value) в строке
        where_column - выборка по колонкам (key), которые равны значение (value)
        """
        # Формирование строки со списком изменяемых значений для вставки в sql запрос
        change_columns_insert = ''
        for key, value in change_columns.items():
            change_columns_insert += str(key) + '=' + str(value) + ', '
        change_columns_insert = change_columns_insert[:-2]

        # Формирование выборки для вставки в sql запрос
        where_column_insert = ''
        for key, value in where_column.items():
            where_column_insert += str(key) + '=' + str(value) + ', '
        where_column_insert = where_column_insert[:-2]

        sql_req = '''UPDATE {0} SET {1} WHERE {2};'''.format(table_name, change_columns_insert, where_column_insert)

        self.conn = sqlite3.connect(self.basename)
        c = self.conn.cursor()
        c.execute(sql_req)
        self.conn.commit()
        self.conn.close()

    def delete_from_base(self, table_name: str, where=True, where_column={}):
        """
        Функция для добавления строки в базу данных
        table_name - имя таблицы
        where - присутствует или нет переменная where (если нет, то таблица полностью очищается)
        where_column - выборка по колонкам (key), которые равны значение (value)
        """
        if where is True:
            # Формирование выборки для вставки в sql запрос
            where_column_insert = ''
            for key, value in where_column.items():
                where_column_insert += str(key) + '=' + str(value) + ', '
            where_column_insert = where_column_insert[:-2]
            sql_where = """ WHERE {0}""".format(where_column_insert)
        else:
            sql_where = ''

        sql_req = '''DELETE FROM {0}{1};'''.format(table_name, sql_where)
        self.conn = sqlite3.connect(self.basename)
        c = self.conn.cursor()
        c.execute(sql_req)
        self.conn.commit()
        self.conn.close()

    def get_from_base(self, table_name: str, col=True, columns=[], where=True, where_column={}):
        """
        Функция для добавления строки в базу данных
        table_name - имя таблицы
        col - присутствует или нет список колонок
        columns - наименование колонок таблицы
        where - присутствует или нет переменная where (если нет, то таблица полностью очищается)
        where_column - выборка по колонкам (key), которые равны значение (value)
        """

        # формируется список колонок, которые необходимо выбрать
        if col is True:
            columns_insert = ''
            for col_n in columns:
                columns_insert += str(col_n) + ', '
            columns_insert = columns_insert[:-2]
            sql_col = columns_insert
        else:
            sql_col = '*'

        if where is True:
            # Формирование выборки для вставки в sql запрос
            where_column_insert = ''
            for key, value in where_column.items():
                if type(value) == str:
                    where_column_insert += str(key) + '=' + "'" + str(value) + "'" + ', '
                else:
                    where_column_insert += str(key) + '=' + str(value) + ', '
            where_column_insert = where_column_insert[:-2]
            sql_where = ''' WHERE {0}'''.format(where_column_insert)
        else:
            sql_where = ''

        sql_req = '''SELECT {0} FROM {1}{2};'''.format(sql_col, table_name, sql_where)
        self.conn = sqlite3.connect(self.basename)
        c = self.conn.execute(sql_req)
        answer = c.fetchall()
        self.conn.commit()
        self.conn.close()

        return answer

    def add_user(self, user_id: int, username: str, is_private=0, fr=0, fw=0, old_fw=0):
        """
        Функция для добавления пользователя в базу данных
        user_id - id пользователя
        username - имя пользователя
        is_private - скрытый профиль или нет
        fr - подписчики
        fw - последователи
        """
        columns = ['user_id', 'username', 'is_private', 'fr', 'fw', 'old_fw']
        values = [user_id, username, is_private, fr, fw, old_fw]
        self.add_to_base('users', columns, values)

    def add_post(self, post_id: str, user_id: int, title='', u_long=0, u_lat=0,
                 p_long=0, p_lat=0, p_lock_name='', has_liked=0, post_datetime=0):
        """
        Функция для добавления поста в базу данных
        post_id - id поста
        user_id - id пользователя
        title - подпись под фото
        u_long - долгота места, в котором пользователь выложил фото
        u_lat - широта места, в котором пользователь выложил фото
        p_long - долгота места, которое пользователь отметил
        p_lat - широта места, которое пользователь отметил
        p_lock_name - название места, которое пользователь отметил
        has_liked - лайкнут ли администратором пост или нет
        post_datetime - дата поста
        """
        columns = ['post_id', 'user_id', 'title', 'u_long', 'u_lat', 'p_long', 'p_lat',
                   'p_lock_name', 'has_liked', 'post_datetime']
        values = [post_id, user_id, title, u_long, u_lat, p_long, p_lat, p_lock_name, has_liked, post_datetime]
        self.add_to_base('posts', columns, values)

    def add_like(self, post_id: str, user_id: int, like_b=1, dislike_b=0, date_like=0, date_dislike=0):
        """
        Функция для добавления лайка в базу данных
        like_id - id лайка
        post_id - id поста
        user_id - id пользователя
        like_b - признак действующего лайка
        dislike_b - признак того, что лайк отлайкнут
        date_like - дата лайка
        date_dislike - дата дизлайка
        """
        columns = ['post_id', 'user_id', 'like_b', 'dislike_b', 'date_like', 'date_dislike']
        values = [post_id, user_id, like_b, dislike_b, date_like, date_dislike]
        self.add_to_base('likes', columns, values)

    def add_comment(self, post_id: str, user_id: int, comment: str):
        """
        Функция для добавления коммента в базу данных
        post_id - id поста
        user_id - id пользователя
        comment - комментарий
        """
        columns = ['post_id', 'user_id', 'comment']
        values = [post_id, user_id, comment]
        self.add_to_base('comments', columns, values)

    def add_user_statistic(self, user_id: int, ratio_fw_fr=0, mutual_per=0, adherence_per=0,
                           like_per_post=0, likes=0, posts=0, likable=0):
        """
        Функция для добавления коммента в базу данных
        user_id - id пользователя
        ratio_fw_fr - соотношение последователей с подписками
        mutual_per - процент взаимной подписки
        adherence_per - среднее количество лайков на пост от подписчиков
        like_per_post - среднее количество лайков на пост
        likes - количество лайков
        posts - количество постов
        likable - лайкабельность
        """
        columns = ['user_id', 'ratio_fw_fr', 'mutual_per', 'adherence_per',
                   'like_per_post', 'likes', 'posts', 'likable']
        values = [user_id, ratio_fw_fr, mutual_per, adherence_per, like_per_post, likes, posts, likable]
        self.add_to_base('users_statistic', columns, values)
