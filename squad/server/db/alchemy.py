from typing import Tuple, List

import datetime
from sqlalchemy import create_engine, or_, desc, asc
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
            posts.append([post.id, post.title, post.text, post.image_path])

        return posts

    def is_free_log_email(self, potential_login, potential_email):
        user_filter = self.__session.query(User).filter(or_(User.login == potential_login,
                                                            User.email == potential_email)).all()
        if user_filter:
            return False
        return True

    def get_post_comments(self, post_id):
        comments = self.__session.query(Comment).filter(Comment.post_id == post_id).order_by(desc(Comment.date)).all()
        coms = []
        for comment in comments:
            coms.append([
                comment.date,
                comment.text,
                self.__session.query(User).filter(User.id == comment.user_id).all()[0].login
            ])
        return coms

    def add_comment(self, post_id, user, text):
        user_id = self.__session.query(User).filter(User.login == user).one().id
        c = Comment(date=datetime.datetime.utcnow(), post_id=post_id, user_id=user_id, text=text)

        self.__session.add(c)
        self.__session.commit()


if __name__ == '__main__':
    a = Alchemy('data.db')
    a.get_session().query(Comment).delete()
    a.get_session().commit()
