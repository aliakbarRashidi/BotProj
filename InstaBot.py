from testStat import Insta
import time
import random

loc_per = 406521032
user = '*'
password = '*'


class InstagramBot(Insta):
    likes = 0

    def get_like(self, post):
        if post['has_liked'] is False:
            self.insta.api.like(post['id'])
            InstagramBot.likes += 1
            time.sleep(random.randint(10, 20) + 60)
            print("Like {0} added".format(InstagramBot.likes))
            return True

    def like_by_location(self, location_id):
        # Get posts by location
        posts = self.insta.get_location_feed(location_id)
        for post in posts:
            self.get_like(post)

    def like_followings_followings(self):
        my_followings = self.insta.get_total_following(self.insta.user_id)
        followings = []
        for my_following in my_followings:
            fws = self.insta.get_total_following(my_following['user_id'])
            for fw in fws:
                if fw not in followings:
                    followings.append(fw)

        for following in followings:
            _ = self.insta.api.getUserFeed(following)
            user_posts = self.insta.api.LastJson.get('items', '')
            for post in user_posts:
                if self.get_like(post) is True:
                    break


inst_bot = InstagramBot(user, password)
inst_bot.like_by_location(loc_per)
inst_bot.like_followings_followings()
