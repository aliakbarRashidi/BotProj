import os
import sqlite3
import datetime
import hashlib


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
            unfollow BOOLEAN,
            date_unfollower DATETIME,
            FOREIGN KEY (main_user_user_id) REFERENCES users (user_id)
            ON DELETE CASCADE ON UPDATE NO ACTION,
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
            date_following DATETIME,
            unfollow BOOLEAN,
            date_unfollowing DATETIME,
            FOREIGN KEY (main_user_user_id) REFERENCES users (user_id)
            ON DELETE CASCADE ON UPDATE NO ACTION,
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
             post_id text PRIMARY KEY,
             user_id INTEGER,
             title text,
             filter_type INTEGER DEFAULT 0,
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
             like_id text PRIMARY KEY UNIQUE,
             post_id INTEGER,
             main_user_id INTEGER,
             like_user_id INTEGER,
             like_b BOOLEAN DEFAULT False,
             dislike_b BOOLEAN DEFAULT False,
             date_like DATETIME,
             date_dislike DATETIME,
             FOREIGN KEY (post_id) REFERENCES posts (post_id)
             ON DELETE CASCADE ON UPDATE NO ACTION,
             FOREIGN KEY (main_user_id) REFERENCES users (user_id)
             ON DELETE CASCADE ON UPDATE NO ACTION,
             FOREIGN KEY (like_user_id) REFERENCES users (user_id)
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
             comment_id INTEGER PRIMARY KEY NOT NULL UNIQUE,
             post_id text,
             user_id INTEGER,
             comment text,
             comment_add DATETIME DEFAULT 0,
             comment_remove DATETIME DEFAULT 0,
             add_c BOOLEAN DEFAULT 1,
             remove_c BOOLEAN DEFAULT 0,
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
             fr BOOLEAN DEFAULT 0,
             fw BOOLEAN DEFAULT 0, 
             un_fr BOOLEAN DEFAULT 0,
             un_fw BOOLEAN DEFAULT 0,
             fw_dynamic REAL DEFAULT 0,
             fr_dynamic REAL DEFAULT 0,
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

    def add_followers(self, user_id: int, followers: list):
        """
        Функция для добавления строки в базу данных
        user_id - пользователь, чьи подписчики добавляются в таблицу
        followers - подписчики [{'user_id': user_id, username': username, 'is_private': 1,0}]
        """
        followers_in_base = self.get_from_base('followers', col=False,
                                               where=True, where_column={'main_user_user_id': user_id})
        self.add_users(followers)
        # Удобней оперировать простыми списками
        cute_followers_in_base = []
        for follower in followers_in_base:
            cute_followers_in_base.append(follower[0])

        cute_followers_new = []
        for follower in followers:
            cute_followers_new.append(str(user_id) + '_' + str(follower['user_id']))

        # Находим список новых подписчиков
        new_followers = []
        for follower in cute_followers_new:
            if follower not in cute_followers_in_base:
                new_followers.append(follower)
        # Добавляем список новых подписчиков
        new_followers_to_base = []
        for follower in followers:
            if str(user_id) + '_' + str(follower['user_id']) in new_followers:
                new_followers_to_base.append((str(user_id) + '_' + str(follower['user_id']), user_id,
                                              follower['user_id'], datetime.datetime.today(), 0, 0))
        self.conn = sqlite3.connect(self.basename)
        c = self.conn.cursor()
        c.executemany("INSERT OR IGNORE INTO 'followers' VALUES (?, ?, ?, ?, ?, ?);", new_followers_to_base)
        self.conn.commit()
        self.conn.close()

        # Находим список отписчиков
        unfollowers = []
        for follower in cute_followers_in_base:
            if follower not in cute_followers_new:
                unfollowers.append(follower)

        # Добавляем заметку, что подписчики отписались
        unfollowers_to_base = []
        for follower in followers_in_base:
            if follower[2] in unfollowers:
                unfollowers_to_base.append((follower[0], follower[1].
                                            follower[2], follower[3], 1, datetime.datetime.today()))
        self.conn = sqlite3.connect(self.basename)
        c = self.conn.cursor()
        c.executemany("INSERT OR REPLACE INTO 'followers' VALUES (?, ?, ?, ?, ?, ?);", unfollowers_to_base)
        self.conn.commit()
        self.conn.close()

    def add_followings(self, user_id: int, followings: list):
        """
        Функция для добавления строки в базу данных
        user_id - пользователь, чьи подписки добавляются в таблицу
        followings - подписки [{'user_id': user_id, 'username': username, 'is_private': 1,0}]
        """
        followings_in_base = self.get_from_base('following', col=False,
                                                where=True, where_column={'main_user_user_id': user_id})
        self.add_users(followings)
        # Удобней оперировать простыми списками
        cute_followings_in_base = []
        for following in followings_in_base:
            cute_followings_in_base.append(following[0])

        cute_followings_new = []
        for following in followings:
            cute_followings_new.append(str(user_id) + '_' + str(following['user_id']))

        # Находим список новых подписчиков
        new_followings = []
        for following in cute_followings_new:
            if following not in cute_followings_in_base:
                new_followings.append(following)

        # Добавляем список новых подписчиков
        new_followings_to_base = []
        for following in followings:
            if str(user_id) + '_' + str(following['user_id']) in new_followings:
                new_followings_to_base.append((str(user_id) + '_' + str(following['user_id']), user_id,
                                               following['user_id'], datetime.datetime.today(), 0, 0))
        self.conn = sqlite3.connect(self.basename)
        c = self.conn.cursor()
        c.executemany("INSERT OR IGNORE INTO 'following' VALUES (?, ?, ?, ?, ?, ?);", new_followings_to_base)
        self.conn.commit()
        self.conn.close()

        # Находим список отписчиков
        unfollowings = []
        for following in cute_followings_in_base:
            if following not in cute_followings_new:
                unfollowings.append(following)

        # Добавляем отметку, что подписчики отписались
        unfollowings_to_base = []
        for following in followings_in_base:
            if following[2] in unfollowings:
                unfollowings_to_base.append((following[0], following[1].
                                             following[2], following[3], 1, datetime.datetime.today()))
        self.conn = sqlite3.connect(self.basename)
        c = self.conn.cursor()
        c.executemany("INSERT OR REPLACE INTO 'following' VALUES (?, ?, ?, ?, ?, ?);", unfollowings_to_base)
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
        if is_private is True:
            is_private = 1
        else:
            is_private = 0
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

    def add_like(self, post_id: str, main_user_id: int, like_user_id: int, like_b=1, dislike_b=0, date_like=0, date_dislike=0):
        """
        Функция для добавления лайка в базу данных
        like_id - id лайка
        post_id - id поста
        user_id - id пользователя
        main_user_id - id пользователя-владельца поста
        like_user_id - id пользователя, который поставил лайк
        like_b - признак действующего лайка
        dislike_b - признак того, что лайк отлайкнут
        date_like - дата лайка
        date_dislike - дата дизлайка
        """
        like_id = str(post_id) + '_' + str(main_user_id)
        columns = ['like_id', 'post_id', 'main_user_id', 'like_user_id',
                   'like_b', 'dislike_b', 'date_like', 'date_dislike']
        values = [like_id, post_id, main_user_id, like_user_id,
                  like_b, dislike_b, date_like, date_dislike]
        self.add_to_base('likes', columns, values)

    def add_likes(self, post_id: str, user_id: int, likers: list):
        """
        Функция для добавления лайка в базу данных
        post_id - id поста
        user_id - id пользователя
        like_b - признак действующего лайка
        dislike_b - признак того, что лайк отлайкнут
        date_like - дата лайка
        date_dislike - дата дизлайка
        likers - [{'user_id': user_id, 'username': username, 'is_private': True}]
        """
        # получить список лайков по данному посту
        likers_base = self.get_from_base('likes', col=False,
                                         where=True, where_column={'post_id': post_id})
        self.add_users(likers)
        # Оперировать удобней списками, поэтому делаем преобразование
        cute_likers_base = []
        for liker in likers_base:
            cute_likers_base.append(liker[0])

        cute_likers_new = []
        for liker in likers:
            cute_likers_new.append(str(post_id) + '_' + str(liker['user_id']))

        # Находим список новых лайкеров
        new_likers = []
        for liker in cute_likers_new:
            if liker not in cute_likers_base:
                new_likers.append(liker)

        # Добавляем список новых лайкеров
        new_likers_to_base = []
        for liker in likers:
            like_id = str(post_id) + '_' + str(liker['user_id'])
            if like_id in new_likers:
                new_likers_to_base.append((like_id, post_id, user_id, liker['user_id'],
                                           1, 0, datetime.datetime.today(), 0))
        self.conn = sqlite3.connect(self.basename)
        c = self.conn.cursor()
        c.executemany("INSERT OR IGNORE INTO 'likes' VALUES (?, ?, ?, ?, ?, ?, ?, ?);", new_likers_to_base)
        self.conn.commit()
        self.conn.close()

        # Находим список отлайкнутых
        unlikers = []
        for liker in cute_likers_base:
            if liker not in cute_likers_new:
                unlikers.append(liker)

        # Добавляем отметку, что убрали лайк
        unlikers_to_base = []
        for liker in likers_base:
            if liker[0] in unlikers:
                unlikers_to_base.append((liker[0], liker[1], liker[2], liker[3],
                                         liker[4], 1, liker[6], datetime.datetime.today()))
        self.conn = sqlite3.connect(self.basename)
        c = self.conn.cursor()
        c.executemany("INSERT OR REPLACE INTO 'likes' VALUES (?, ?, ?, ?, ?, ?, ?, ?);", unlikers_to_base)
        self.conn.commit()
        self.conn.close()

    def add_comment(self, post_id: str, user_id: int, comment: str,
                    comment_add=datetime.datetime.today(), comment_remove=0, add=1, remove=0):
        """
        Функция для добавления коммента в базу данных
        post_id - id поста
        user_id - id пользователя
        comment - комментарий
        """
        comment_hash = hashlib.sha1(str(comment).encode()).hexdigest()
        comment_id = str(post_id) + '_' + str(user_id) + '_' + str(comment_hash)
        columns = ['comment_id', 'post_id', 'user_id', 'comment', 'comment_add', 'comment_remove', 'add', 'remove']
        values = [comment_id, post_id, user_id, comment, comment_add, comment_remove, add, remove]
        self.add_to_base('comments', columns, values)

    def add_comments(self, post_id: str, user_id: int, comments: list):
        """
        Функция для добавления коммента в базу данных
        post_id - id поста
        user_id - id пользователя
        comments - [{'comment_id': comment_id, 'user_id': user_id, 'post_id': post_id, 'comment_add': datetime,
        'comment': text}]
        """
        # получить список комменов по данному посту
        comments_base = self.get_from_base('comments', col=False,
                                           where=True, where_column={'post_id': post_id})

        # Оперировать удобней списками, поэтому делаем преобразование
        cute_comments_base = []
        for comment in comments_base:
            cute_comments_base.append(comment[0])

        cute_comments_new = []
        for comment in comments:
            comment_id = comment['comment_id']
            cute_comments_new.append(comment_id)

        # Находим список новых комментов
        new_comments = []
        for comment in cute_comments_new:
            if comment not in cute_comments_base:
                new_comments.append(comment)

        # Добавляем список новых комментов
        new_comments_to_base = []
        for comment in comments:
            comment_id = comment['comment_id']
            if comment_id in new_comments:
                new_comments_to_base.append((comment_id, post_id, user_id,
                                             comment['text'], comment['comment_add'], 0, 1, 0))
        self.conn = sqlite3.connect(self.basename)
        c = self.conn.cursor()
        c.executemany("INSERT OR REPLACE INTO 'comments' VALUES (?, ?, ?, ?, ?, ?, ?, ?);", new_comments_to_base)
        self.conn.commit()
        self.conn.close()

        # Находим список откоментных
        uncomments = []
        for comment in cute_comments_base:
            if comment not in cute_comments_new:
                uncomments.append(comment)

        # Добавляем отметку, что коммент удалили
        uncomments_to_base = []
        for comment in comments_base:
            if comment[0] in uncomments:
                uncomments_to_base.append((comment[0], comment[1].comment[2],
                                           comment[3], comment[4], datetime.datetime.today(), 1, 1))
        self.conn = sqlite3.connect(self.basename)
        c = self.conn.cursor()
        c.executemany("INSERT OR REPLACE INTO 'comments' VALUES (?, ?, ?, ?, ?, ?, ?, ?);", uncomments_to_base)
        self.conn.commit()
        self.conn.close()

    def add_user_statistic(self, user_id: int, ratio_fw_fr=0, mutual_per=0, adherence_per=0,
                           like_per_post=0, likes=0, posts=0, likable=0, fr=0, fw=0,
                           un_fr=0, un_fw=0, fw_dynamic=0, fr_dynamic=0):
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
                   'like_per_post', 'likes', 'posts', 'likable', 'fr', 'fw',
                   'un_fr', 'un_fw', 'fw_dynamic', 'fr_dynamic']
        values = [user_id, ratio_fw_fr, mutual_per, adherence_per, like_per_post, likes, posts, likable, fr, fw,
                  un_fr, un_fw, fw_dynamic, fr_dynamic]
        self.add_to_base('users_statistic', columns, values)

    def add_posts(self, user_id: int, posts: list):
        """
        Функция для добавления строки в базу данных
        user_id - пользователь, чьи подписки добавляются в таблицу
        posts - подписки [{ 'post_id': post_id,
                            'like_count': like_count,
                            'comment_count': comment_count,
                            'filter_type': filter_type,
                            'has_liked': has_liked,
                            'has_more_comments': has_more_comments,
                            'post_lng': post_lng,
                            'post_lat': post_lat,
                            'add_loc_lng': add_loc_lng,
                            'add_loc_lat': add_loc_lat,
                            'add_loc_name': add_loc_name,
                            'date_post': date_post,
                            'likers': likers}]
        """
        posts_in_base = self.get_from_base('posts', col=False,
                                           where=True, where_column={'user_id': user_id})

        # Удобней оперировать простыми списками
        cute_posts_in_base = []
        for post in posts_in_base:
            cute_posts_in_base.append(post[0])

        cute_posts_new = []
        for post in posts:
            cute_posts_new.append(post['post_id'])

        # Находим список новых постов
        new_posts = []
        for post in cute_posts_new:
            if post not in cute_posts_in_base:
                new_posts.append(post)

        # Добавляем список новых постов
        new_posts_to_base = []
        for post in posts:
            if str(post['post_id']) in new_posts:
                new_posts_to_base.append((post['post_id'], user_id, post['title'], post['filter_type'],
                                          post['post_lng'], post['post_lat'],
                                          post['add_loc_lng'], post['add_loc_lat'], post['add_loc_name'],
                                          post['has_liked'], post['date_post']))
                self.add_likes(post['post_id'], user_id, post['likers'])
                self.add_comments(post['post_id'], user_id, post['comments'])
        self.conn = sqlite3.connect(self.basename)
        c = self.conn.cursor()
        c.executemany("INSERT OR IGNORE INTO 'posts' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", new_posts_to_base)
        self.conn.commit()
        self.conn.close()

    def add_users(self, users: list):
        """
        Функция для добавления строки в базу данных
        user_id - пользователь, чьи подписки добавляются в таблицу
        users - пользователи [{'user_id': user_id, username': username, 'is_private': 1,0}]
        """
        users_in_base = self.get_from_base('users', col=False, where=False)

        # Удобней оперировать простыми списками
        cute_users_in_base = []
        for user in users_in_base:
            cute_users_in_base.append(user[0])
        cute_users_new = []
        for user in users:
            cute_users_new.append(user['user_id'])
        # Находим список новых пользователей
        new_users = []
        for user in cute_users_new:
            if user not in cute_users_in_base:
                new_users.append(user)

        # Добавляем список новых пользователей
        new_users_to_base = []
        for user in users:
            if user['user_id'] in new_users:
                new_users_to_base.append((user['user_id'], user['username'], user['is_private'], 0, 0, 0))
        print()
        self.conn = sqlite3.connect(self.basename)
        c = self.conn.cursor()
        c.executemany("INSERT OR IGNORE INTO 'users' VALUES (?, ?, ?, ?, ?, ?);", new_users_to_base)
        self.conn.commit()
        self.conn.close()

