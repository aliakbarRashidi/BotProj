from base import BaseUser
from InstaStatistick import InstaStat

loc_per = 598476186
user = 'syrnikov_pavel'
password = 'Nastya26042015'


class Insta:

    def __init__(self, user, password):
        self.user = user
        self.password = password
        self.insta = InstaStat(self.user, self.password)
        self.base_user = BaseUser(self.user, self.insta.user_id)

    def update_followers(self):
        """
        Функция обновляет список подписок пользователя
        """
        followers = self.insta.get_total_followers(self.insta.user_id)
        self.base_user.add_followers(self.insta.user_id, followers)
        for follower in followers:
            user_id = follower['user_id']
            print('Start add {0}'.format(user_id))
            if follower['is_private'] is False:
                user_stat = self.base_user.get_from_base('users_statistic', col=True, columns=['user_id'],
                                                         where=True, where_column={'user_id': user_id})
                if user_stat == []:
                    followers, followings, posts, ratio_fw_fr, mutual_per, \
                        adherence_per, like_per_post, n_likes, n_posts = self.insta.get_statistick_about_user(user_id)
                    print('Add followers for {0}'.format(user_id))
                    self.base_user.add_followers(user_id, followers)
                    print('Add followings for {0}'.format(user_id))
                    self.base_user.add_followings(user_id, followings)
                    print('Add posts for {0}'.format(user_id))
                    self.base_user.add_posts(user_id, posts)
                    print(follower['username'], ratio_fw_fr, mutual_per,
                          adherence_per, like_per_post, n_likes, n_posts)
                    self.base_user.add_user_statistic(user_id, ratio_fw_fr=ratio_fw_fr, mutual_per=mutual_per,
                                                      adherence_per=adherence_per, like_per_post=like_per_post,
                                                      likes=n_likes, posts=n_posts, likable=0, fr=1, fw=0, un_fr=0,
                                                      un_fw=0, fw_dynamic=0, fr_dynamic=0)
                else:
                    self.base_user.change_from_base('users_statistic', change_columns={'fr': 1},
                                               where_column={'user_id': user_id})
            else:
                self.base_user.add_user_statistic(user_id, ratio_fw_fr=0, mutual_per=0,
                                                  adherence_per=0, like_per_post=0, likes=0,
                                                  posts=0, likable=0, fr=1, fw=0, un_fr=0, un_fw=0,
                                                  fw_dynamic=0, fr_dynamic=0)

    def update_followings(self):
        """
        Функция обновляет список подписчиков пользователя
        """
        followings = self.insta.get_total_following(self.insta.user_id)
        self.base_user.add_followings(self.insta.user_id, followings)
        for following in followings:
            user_id = following['user_id']
            user_stat = self.base_user.get_from_base('users_statistic', col=True, columns=['user_id'],
                                                     where=True, where_column={'user_id': user_id})
            if user_stat == []:
                followers, followings, posts, ratio_fw_fr, mutual_per, \
                    adherence_per, like_per_post, n_likes, n_posts = self.insta.get_statistick_about_user(user_id)
                print('Add followers for {0}'.format(user_id))
                self.base_user.add_followers(user_id, followers)
                print('Add followings for {0}'.format(user_id))
                self.base_user.add_followings(user_id, followings)
                print('Add posts for {0}'.format(user_id))
                self.base_user.add_posts(user_id, posts)
                print(following['username'], ratio_fw_fr, mutual_per,
                      adherence_per, like_per_post, n_likes, n_posts)
                self.base_user.add_user_statistic(user_id, ratio_fw_fr=ratio_fw_fr, mutual_per=mutual_per,
                                                  adherence_per=adherence_per, like_per_post=like_per_post,
                                                  likes=n_likes, posts=n_posts, likable=0, fr=0, fw=1, un_fr=0, un_fw=0,
                                                  fw_dynamic=0, fr_dynamic=0)
            else:
                self.base_user.change_from_base('users_statistic', change_columns={'fw': 1}, where_column={'user_id': user_id})

    def update_users(self):
        users_base = self.base_user.get_from_base('users', col=True, columns=['user_id'], where=False)
        for user in users_base:
            user_id = user[0]
            user_stat = self.base_user.get_from_base('users_statistic', col=True, columns=['user_id'],
                                                     where=True, where_column={'user_id': user_id})
            if user_stat == []:
                followers, followings, posts, ratio_fw_fr, mutual_per, \
                    adherence_per, like_per_post, n_likes, n_posts = self.insta.get_statistick_about_user(user_id)
                print('Add followers for {0}'.format(user_id))
                self.base_user.add_followers(user_id, followers)
                print('Add followings for {0}'.format(user_id))
                self.base_user.add_followings(user_id, followings)
                print('Add posts for {0}'.format(user_id))
                self.base_user.add_posts(user_id, posts)
                print(user_id, ratio_fw_fr, mutual_per,
                      adherence_per, like_per_post, n_likes, n_posts)
                self.base_user.add_user_statistic(user_id, ratio_fw_fr=ratio_fw_fr, mutual_per=mutual_per,
                                                  adherence_per=adherence_per, like_per_post=like_per_post,
                                                  likes=n_likes, posts=n_posts, likable=0, fr=0, fw=0, un_fr=0, un_fw=0,
                                                  fw_dynamic=0, fr_dynamic=0)
        return users_base

    def mode_statistick(self):
        self.update_followers()
        self.update_followings()
        self.update_users()
