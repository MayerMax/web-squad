import bottle
from beaker.middleware import SessionMiddleware
from bottle import route, request, error, response, template, post, get, run, static_file
from cork import Cork, AuthException

from db.alchemy import Alchemy
from db.data import User

alchemy = Alchemy(path='db/data.db')

aaa = Cork('us', email_sender='endurancemayer@gmail.com',
           smtp_url='starttls://{}:{}@smtp.gmail.com:587'.format('email', 'password'))

app = bottle.app()

session_opts = {
    'session.cookie_expires': True,
    'session.encrypt_key': 'please use a random key and keep it secret!',
    'session.httponly': True,
    'session.timeout': 3600 * 24,  # 1 day
    'session.type': 'cookie',
    'session.validate_key': True,
}

app = SessionMiddleware(app, session_opts)


@route('/')
def feed():
    """
    auth user news feed
    :return:
    """
    aaa.require(fail_redirect='/login')
    user = aaa.current_user
    posts = alchemy.get_posts(100)
    for i in range(0, len(posts)):
        back = alchemy.get_post_comments(posts[i][0])
        posts[i].append(back)

    return template('static/html/feed.tpl', name=user.username, posts=posts)


@route('/:thread<:re:[0-9]*>', method='POST')
def leave_comment(thread):
    aaa.require(fail_redirect='/login')
    post_id = int(thread.replace('thread', ''))
    content = request.forms.get('comment')
    print(content)
    cur_user = aaa.current_user.username
    alchemy.add_comment(post_id, cur_user, content)
    return bottle.redirect('/')


@route('/validate_registration/<registration_code>')
def validate_registration(registration_code):
    aaa.validate_registration(registration_code)
    return 'Thanks. <a href="/">Go to login</a>'


@route('/<filename:path>')
def send_file(filename):
    return static_file(filename, root='static/')


@route('/login', method='POST')
def do_auth():
    # user login
    log_us = request.forms.get('user', '')
    log_pass = request.forms.get('password', '')

    if log_us and log_pass:
        aaa.login(log_us, log_pass, success_redirect='/', fail_redirect='/login')

    username = request.forms.get('user_start')
    password = request.forms.get('password_start')
    email = request.forms.get('email_start')

    if username and password and email:
        if alchemy.is_free_log_email(username, email):
            aaa.register(username, password, email, email_template='static/registration_temp.tpl')
            user = User(login=username, password=password, email=email)
            session = alchemy.get_session()
            session.add(user)
            session.commit()
            return 'Watch email'

    return template('static/html/landing.html')


@route('/login')
def login_static():
    try:
        user = aaa.current_user
        return bottle.redirect('/')
    except AuthException as e:
        return template('static/html/landing.html')


@route('/error')
def callback():
    return 'Hello, error happend!'


def main():
    bottle.debug(True)
    bottle.run(app=app, host='localhost', port=5050)


if __name__ == "__main__":
    main()
