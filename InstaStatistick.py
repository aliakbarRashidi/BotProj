from InstagramAPI import InstagramAPI
import datetime
import time


class InstaStat:

    def __init__(self, user, password):
        self.user = user
        self.password = password
        self.api, self.user_id = self.insta_login()

    def insta_login(self):
        api = InstagramAPI(self.user, self.password)
        api.login()
        api.getSelfUsernameInfo()
        user_id = api.LastJson.get('user')['pk']
        return api, user_id

    def get_total_followers(self, user_id):
        """
        Возвращает список подписчиков в инстагаме
        """

        followers = []
        next_max_id = True
        while next_max_id:
            # first iteration hack
            if next_max_id is True:
                next_max_id = ''
            try:
                _ = self.api.getUserFollowers(user_id, maxid=next_max_id)
                followers.extend(self.api.LastJson.get('users', []))
                next_max_id = self.api.LastJson.get('next_max_id', '')
            except json.decoder.JSONDecodeError:
                time.sleep(1)
                _ = self.api.getUserFollowers(user_id, maxid=next_max_id)
                followers.extend(self.api.LastJson.get('users', []))
                next_max_id = self.api.LastJson.get('next_max_id', '')

        true_followers = []
        for follower in followers:
            true_followers.append(
                {'user_id': follower['pk'], 'username': follower['username'], 'is_private': follower['is_private']})

        return true_followers

    def get_total_following(self, user_id):
        """
        Возвращает список последователей в инстагаме
        """

        following = []
        next_max_id = True
        while next_max_id:
            # first iteration hack
            if next_max_id is True:
                next_max_id = ''
            _ = self.api.getUserFollowings(user_id, maxid=next_max_id)
            following.extend(self.api.LastJson.get('users', []))
            next_max_id = self.api.LastJson.get('next_max_id', '')
        true_following = []
        for user in following:
            true_following.append({'user_id': user['pk'], 'username': user['username'],
                                   'is_private': user['is_private']})

        return true_following

    def get_likers(self, post_id):
        """
        Возвращает список лайкнувших пост пользователей
        """
        answer = {}

        sucsess = True
        while sucsess:
            _ = self.api.getMediaLikers(post_id)
            answer = self.api.LastJson
            if answer['status'] == 'ok':
                sucsess = False

        likers = []
        users = answer['users']
        for user in users:
            likers.append({'user_id': user['pk'], 'username': user['username'], 'is_private': user['is_private']})

        return likers

    def get_user_posts(self, user_id):
        """
        Возвращает последние посты пользователя
        """

        user_posts = []
        sucsess = True
        next_max_id = ''
        while sucsess:
            _ = self.api.getUserFeed(user_id, maxid=next_max_id)
            user_posts.extend(self.api.LastJson.get('items'))
            next_max_id = self.api.LastJson.get('next_max_id', '')
            if next_max_id == '':
                sucsess = False

        return user_posts

    def get_statistick(self, post):
        """
        Возвращает данные о посте
        """

        post_id = post['id']
        like_count = post['like_count']
        comment_count = post['comment_count']
        filter_type = post['filter_type']
        has_liked = post['has_liked']
        has_more_comments = post['has_more_comments']
        try:
            date_post = datetime.datetime.fromtimestamp(int(post['device_timestamp'] / 1000000)).strftime(
                '%Y-%m-%d %H:%M:%S')
        except OSError:
            try:
                date_post = datetime.datetime.fromtimestamp(int(post['device_timestamp'])).strftime('%Y-%m-%d %H:%M:%S')
            except ValueError:
                date_post = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                print(post['device_timestamp'])
            except OSError:
                date_post = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                print(post['device_timestamp'])
        try:
            post_lng = post['lng']
            post_lat = post['lat']
        except KeyError:
            post_lng = 0
            post_lat = 0
        try:
            add_loc_lng = post['location']['lng']
            add_loc_lat = post['location']['lat']
            add_loc_name = post['location']['name']
        except KeyError:
            add_loc_lng = 0
            add_loc_lat = 0
            add_loc_name = 0

        likers = self.get_likers(post_id)

        answer = {
            'post_id': post_id,
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
            'likers': likers
        }
        return answer

    @staticmethod
    def get_s_w_stat(follrs, follws):
        """
        Возвращает два коэффициента, относящихся к вероятности быть зафоловленным в ответ
        """
        mutual = 0
        for follower in follrs:
            if follower in follws:
                mutual += 1
        # соотношение последователей с подписчиками
        # если коэффициент больше 1, то человек имеет больше подписок, чем подписчиков
        # скорее всего такой человек вероятнее всего подпишется в ответ
        ratio_fw_fr = round(len(follws) / len(follrs), 2)
        # процент взаимных подписок
        # чем больше коэффициент, тем вероятнее взаимная подписка
        mutual_per = round(mutual / len(follrs), 2)

        return ratio_fw_fr, mutual_per

    @staticmethod
    def get_like_stat(stat_post, follrs):
        """
        Возвращает два показателя, описывающие приверженность подписчиков
        пользователю и среднее количество лайков на пост
        """

        adherence_count = 0
        all_like = 0
        for post in stat_post:
            for like in post['likers']:
                if like['user_id'] in follrs:
                    adherence_count += 1
                all_like += 1

        # коэффициент приверженности подписчиков
        adherence_per = round(adherence_count / len(stat_post) / len(follrs), 2)
        # коэффициент генерирования лайков, среднее количество лайков на пост
        like_per_post = round(all_like / len(stat_post), 2)

        return adherence_per, like_per_post, all_like, len(stat_post)

    def create_data(self, followers, following, posts):
        # Преобразование для более простого оперирования списками
        follrs = []
        for follower in followers:
            follrs.append(follower['user_id'])

        follws = []
        for follow in following:
            follws.append(follow['user_id'])

        stat_post = []
        for post in posts:
            stat_post.append(self.get_statistick(post))

        return follrs, follws, stat_post

    def get_location_feed(self, location_id):
        posts = []
        sucsess = True
        next_max_id = ''
        while sucsess:
            _ = self.api.getLocationFeed(location_id, maxid=next_max_id)
            posts.extend(self.api.LastJson.get('items'))
            next_max_id = self.api.LastJson.get('next_max_id', '')
            if next_max_id == '':
                sucsess = False
        return posts

    def get_statistick_about_user(self, user_id):
        followers = self.get_total_followers(user_id)
        followings = self.get_total_following(user_id)
        posts = self.get_user_posts(user_id)
        follrs, follws, stat_post = self.create_data(followers, followings, posts)
        ratio_fw_fr, mutual_per = self.get_s_w_stat(follrs, follws)
        adherence_per, like_per_post, n_likes, n_posts = self.get_like_stat(stat_post, follrs)
        return followers, followings, posts, ratio_fw_fr, mutual_per, adherence_per, like_per_post, n_likes, n_posts
