from testStat import Insta
import time
import random

loc_per = 598476186
user = '*'
password = '*'


class InstagramBot(Insta):
    likes = 0

    def like_by_location(self, location_id):
        # Get posts by location
        posts = self.insta.get_location_feed(location_id)
        for post in posts:
            if post['has_liked'] is False:
                self.insta.api.like(post['id'])
                InstagramBot.likes += 1
                time.sleep(random.randint(10, 20)+60)
                print("Like {0} added".format(InstagramBot.likes))

inst_bot = InstagramBot(user, password)
inst_bot.like_by_location(loc_per)
