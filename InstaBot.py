from testStat import Insta
import time
import random


class InstagramBot(Insta):
    likes = 0

    def get_like(self, post):
        if post['has_liked'] is False:
            self.insta.api.like(post['id'])
            InstagramBot.likes += 1
            print("Like {0} added".format(InstagramBot.likes))
            time.sleep(random.randint(10, 20) + 60)
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
            _ = self.insta.api.getUserFeed(following['user_id'])
            user_posts = self.insta.api.LastJson.get('items', '')
            for post in user_posts:
                if self.get_like(post) is True:
                    break


def main():
    try:
        # Перевалово - 406521032
        # Perevalovo - 598476186
        # Зубарево Hills - 1029136137
        # Ушаково - 500419352
        loc_per = {406521032: "Перевалово", 598476186: "Perevalovo", 1029136137: "Зубарево", 500419352: "Ушаково"}
        user = '*'
        password = '*'
        inst_bot = InstagramBot(user, password)
        for loc in loc_per:
            print("Запуск лайк-бота по постам {0}".format(loc_per[loc]))
            inst_bot.like_by_location(loc)
        print("Запуск лайк-бота по фолловерам фолловеров")
        inst_bot.like_followings_followings()
    except KeyboardInterrupt:
        print("Прервано пользователем")
        print("Поставлено {0} лайков".format(InstagramBot.likes))

if __name__ == "__main__":
    main()
