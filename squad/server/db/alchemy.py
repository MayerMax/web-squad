from typing import Tuple, List

from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker

from db.data import Base, User, Post, Comment, Editions


class Alchemy:
    def __init__(self, path=''):
        engine = create_engine('sqlite:///{}'.format(path))
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        self.__session = DBSession()

    def get_session(self):
        """
        only for init is used, as inserting data as bulk
        :return:
        """
        return self.__session

    def get_posts(self, count=2):
        results = self.__session.query(Post).all()
        if count >= len(results):
            count = len(results)

        posts = []
        for post in results[0:count]:
            posts.append([post.title, post.text, post.image_path])

        return posts

    def is_free_log_email(self, potential_login, potential_email):
        user_filter = self.__session.query(User).filter(or_(User.login == potential_login,
                                                            User.email == potential_email)).all()
        if user_filter:
            return False
        return True


if __name__ == '__main__':
    a = Alchemy('data.db')
    p = a.get_session().query(User).filter(User.login == 'Max').all()[0]
    # a.get_session().delete(p)
    # a.get_session().commit()
    print(p)
    print(a.is_free_log_email('Max', 'endurancemayer@yandex.ru'))
