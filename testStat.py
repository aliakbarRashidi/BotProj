from base import BaseUser
from InstaStatistick import InstaStat

loc_per = 598476186
user = '*'
password = '*'
insta = InstaStat(user, password)
base_user = BaseUser(user, insta.user_id)


def update_followers(insta, base_user):
    """
    Функция обновляет список подписок пользователя
    :param insta: Объект ИнстаСтатистик
    :param base_user: Объект БазыДанных
    """
    followers = insta.get_total_followers(insta.user_id)
    base_user.add_followers(insta.user_id, followers)
    for follower in followers:
        user_id = follower['user_id']
        print('Start add {0}'.format(user_id))
        if follower['is_private'] is False:
            user_stat = base_user.get_from_base('users_statistic', col=True, columns=['user_id'],
                                                where=True, where_column={'user_id': user_id})
            if user_stat == []:
                followers, followings, posts, ratio_fw_fr, mutual_per, \
                    adherence_per, like_per_post, n_likes, n_posts = insta.get_statistick_about_user(user_id)
                print('Add followers for {0}'.format(user_id))
                base_user.add_followers(user_id, followers)
                print('Add followings for {0}'.format(user_id))
                base_user.add_followings(user_id, followings)
                print('Add posts for {0}'.format(user_id))
                base_user.add_posts(user_id, posts)
                print(follower['username'], ratio_fw_fr, mutual_per,
                      adherence_per, like_per_post, n_likes, n_posts)
                base_user.add_user_statistic(user_id, ratio_fw_fr=ratio_fw_fr, mutual_per=mutual_per,
                                             adherence_per=adherence_per, like_per_post=like_per_post, likes=n_likes,
                                             posts=n_posts, likable=0, fr=1, fw=0, un_fr=0, un_fw=0,
                                             fw_dynamic=0, fr_dynamic=0)
            else:
                base_user.change_from_base('users_statistic', change_columns={'fr': 1},
                                           where_column={'user_id': user_id})
        else:
            base_user.add_user_statistic(user_id, ratio_fw_fr=0, mutual_per=0,
                                         adherence_per=0, like_per_post=0, likes=0,
                                         posts=0, likable=0, fr=1, fw=0, un_fr=0, un_fw=0,
                                         fw_dynamic=0, fr_dynamic=0)


def update_followings(insta, base_user):
    """
    Функция обновляет список подписчиков пользователя
    :param insta: Объект ИнстаСтатистик
    :param base_user: Объект БазыДанных
    """
    followings = insta.get_total_following(insta.user_id)
    base_user.add_followings(insta.user_id, followings)
    for following in followings:
        user_id = following['user_id']
        user_stat = base_user.get_from_base('users_statistic', col=True, columns=['user_id'],
                                            where=True, where_column={'user_id': user_id})
        if user_stat == []:
            followers, followings, posts, ratio_fw_fr, mutual_per, \
                adherence_per, like_per_post, n_likes, n_posts = insta.get_statistick_about_user(user_id)
            base_user.add_followers(user_id, followers)
            base_user.add_followings(user_id, followings)
            base_user.add_posts(user_id, posts)
            print(following['username'], ratio_fw_fr, mutual_per,
                  adherence_per, like_per_post, n_likes, n_posts)
            base_user.add_user_statistic(user_id, ratio_fw_fr=ratio_fw_fr, mutual_per=mutual_per,
                                         adherence_per=adherence_per, like_per_post=like_per_post, likes=n_likes,
                                         posts=n_posts, likable=0, fr=0, fw=1, un_fr=0, un_fw=0,
                                         fw_dynamic=0, fr_dynamic=0)
        else:
            base_user.change_from_base('users_statistic', change_columns={'fw': 1}, where_column={'user_id': user_id})
