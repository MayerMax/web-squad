from typing import Tuple, List

import datetime
from sqlalchemy import create_engine, or_, desc, asc, and_
from sqlalchemy.orm import sessionmaker

from db.data import Base, User, Post, Comment, Editions, Visits


class Alchemy:
    def __init__(self, path=''):
        engine = create_engine('sqlite:///{}'.format(path))
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        self.__session = DBSession()

    def get_session(self):
        """
        only for init is used, as inserting data as bulk
        :return: session object
        """
        return self.__session

    def update_visits(self, login='anonymous', activity='on main page'):
        unique = 1
        if login != 'anonymous':
            last_activity = self.__session.query(Visits)\
                .filter(Visits.user_login == login)\
                .order_by(desc(Visits.date))\
                .all()
            if last_activity:
                last_activity = last_activity[0]
                if datetime.datetime.now() - last_activity.date < datetime.timedelta(minutes=30):
                    unique = 0
        v = Visits(user_login=login, activity=activity, date=datetime.datetime.now(), unique=unique)

        self.__session.add(v)
        self.__session.commit()

    def get_visits_count(self, date=False):
        """
        :param date: datetime.datetime object
        :return: total count of unique views made earlier than this date or all unique views
        """
        if not date:
            return self.__session.query(Visits).filter(Visits.unique > 0).count()

        return len([i for i in self.__session.query(Visits)
                    if datetime.datetime.now().day == i.date.day  and i.unique > 0])

    def get_visits_user(self, login):
        return self.__session.query(Visits).filter(and_(Visits.user_login == login, Visits.unique > 0)).all()

    def get_stat(self, user_name):
        return self.__session.query(Visits).filter(Visits.user_login == user_name).all()

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
                comment.id,
                comment.date.strftime("%Y-%m-%d %H:%M"),
                comment.text,
                self.__session.query(User).filter(User.id == comment.user_id).all()[0].login
            ])
        return coms

    def add_comment(self, post_id, user, text):
        user_id = self.__session.query(User).filter(User.login == user).one().id
        c = Comment(date=datetime.datetime.now(), post_id=post_id, user_id=user_id, text=text)
        ed = Editions(comment_id=c.id, date=c.date, post_id=c.post_id, text=c.text, user_id=c.user_id)
        self.__session.add(c)
        self.__session.add(ed)
        self.__session.commit()

    def get_editions(self, comment_id, user):
        user_id = self.__session.query(User).filter(User.login == user).one().id
        editions = self.__session.query(Editions).filter(and_(Editions.comment_id == comment_id,
                                                              Editions.user_id == user_id)).order_by(
            desc(Editions.date)).all()
        eds = []
        for edition in editions:
            eds.append([edition.id, edition.date, edition.text])
        return eds

    def make_edition(self, comment_id, user, content):
        user_id = self.__session.query(User).filter(User.login == user).one().id
        comment = self.__session.query(Comment).filter(Comment.id == comment_id).one()

        post_id = comment.post_id

        e = Editions(comment_id=comment.id, date=comment.date, post_id=post_id, text=comment.text, user_id=user_id)
        comment.text = content

        self.__session.add(e)
        self.__session.commit()


if __name__ == '__main__':
    a = Alchemy('data.db')
    a.get_session().query(Comment).delete()
    a.get_session().commit()
    # for i in s:
    #     print(i.date)

    # print(datetime.datetime.now() - s[0].date <= datetime.timedelta(minutes=20))
    # print(s[0].date)
