from base import BaseUser
import os
import logging
logger = logging.getLogger('test')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('test.log')
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)


bu = BaseUser('test', 11111)

logger.info('Добавление в базу')
columns = ['user_id', 'username', 'is_private']
values = [34214123, 'virta_ps', 0]
table_name = 'users'
bu.add_to_base(table_name, columns, values)

logger.info('Изменение в базе')
change_columns = {'is_private': 1}
where_column = {'user_id': 34214123}
bu.change_from_base(table_name, change_columns, where_column)

logger.info('Выборка')
columns = ['user_id', 'username', 'fr']
ans = bu.get_from_base(table_name, col=True, columns=columns, where=True, where_column=where_column)
logger.info(ans)

logger.info('Добавление пользователя в базу')
bu.add_user(555, 'back')

logger.info('Добавление поста в базу')
bu.add_post('151_151', 555, title='Okey')

logger.info('Добавление лайка в базу')
bu.add_like('151_151', 34214123, like_b=1, dislike_b=0)

logger.info('Добавление коммента в базу')
bu.add_comment('151_151', 34214123, 'hello')

logger.info('Добавление статистики в базу')
bu.add_user_statistic(34214123, ratio_fw_fr=0, mutual_per=0, adherence_per=0, like_per_post=0, likes=0, posts=0, likable=0)

logger.info('Удаление из базы')
bu.delete_from_base(table_name, where=True, where_column=where_column)


followers = [{'user_id': 1223123, 'username': '3123', 'is_private': 0}, {'user_id':1223124, 'username': '3124', 'is_private': 0}]
logger.info('Добавление фолловеров')
bu.add_followers(34214123, followers)

os.remove('test.db')
