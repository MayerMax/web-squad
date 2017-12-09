from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    login = Column(String)
    password = Column(String)
    email = Column(String)
    visits = Column(Integer)
    last_activity = Column(Integer)

    def __init__(self, login, password, email, visits=None, last_activity=None):
        self.login = login
        self.password = password
        self.email = email
        self.visits = visits
        self.last_activity = last_activity

    def __repr__(self):
        return 'user - {}, with email - {}'.format(self.login, self.email)


class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    text = Column(String)
    image_path = Column(String)
    likes = Column(Integer)

    def __init__(self, id, title, text, image_path=None, likes=None):
        self.id = id
        self.title = title
        self.text = text
        self.image_path = image_path
        self.likes = likes

    def __repr__(self):
        return 'Article {}, named - {}'.format(self.id, self.title)


class Editions(Base):
    __tablename__ = 'edition'
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('post.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    comment_id = Column(Integer, ForeignKey('comment.id'))

    text = Column(String)
    date = Column(DateTime(timezone=True))

    def __init__(self, post_id, user_id, comment_id, text, date):
        self.post_id = post_id
        self.user_id = user_id
        self.comment_id = comment_id
        self.text = text
        self.date = date


class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('post.id'))  # foreign key
    user_id = Column(Integer, ForeignKey('user.id'))  # foreign key
    text = Column(String)
    date = Column(DateTime(timezone=True))

    post = relationship(Post)

    def __init__(self, post_id, user_id, text, date):
        self.post_id = post_id
        self.user_id = user_id
        self.text = text
        self.date = date

    def __repr__(self):
        return '{}'.format(self.date)


class Visits(Base):
    __tablename__ = 'visits'
    id = Column(Integer, primary_key=True)
    user_login = Column(String)  # login can divide users in 2 groups: anonymous and logged.
    activity = Column(String)
    date = Column(DateTime)
    unique = Column(Integer)

    def __init__(self, user_login, activity, date, unique):
        self.user_login = user_login
        self.activity = activity
        self.date = date
        self.unique = unique

    def __repr__(self):
        return '{}, {}'.format(self.user_login, self.activity)



# engine = create_engine('sqlite:///data.db')
# Visits.__table__.create(engine)