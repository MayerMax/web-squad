from typing import Tuple, List

from sqlalchemy import create_engine
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


if __name__ == '__main__':
    pass
