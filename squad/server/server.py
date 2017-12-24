import json
from collections import OrderedDict

import bottle
import datetime
import httpagentparser
from beaker.middleware import SessionMiddleware
from bottle import route, request, error, template, static_file
from cork import Cork, AuthException

from db import login as LOGIN, password as PASSWORD, update_counter as upd, load_counter as lc
from db.alchemy import Alchemy
from db.data import User
from side.safeescaper import SafeEscape
from side.counters import convert_counter_in_html

alchemy = Alchemy(path='db/data.db')

aaa = Cork('us', email_sender='endurancemayer@gmail.com',
           smtp_url='starttls://{}:{}@smtp.gmail.com:587'.format(LOGIN, PASSWORD))

app = bottle.app()
update_list = {}

Counter = lc()

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
    alchemy.update_visits(user.username, 'Зашел на главную страницу')

    for i in range(0, len(posts)):
        back = alchemy.get_post_comments(posts[i][0])
        for comment in back:
            editions = alchemy.get_editions(comment[0], user.username)
            comment.append(editions)
        posts[i].append(back)
    s = SafeEscape()
    update_list[user.username] = datetime.datetime.now()
    return s(template('static/html/feed.tpl', name=user.username, posts=posts))


@route('/thr/<thread>', method='POST')
def leave_comment(thread):
    aaa.require(fail_redirect='/login')
    post_id = int(thread.replace('thread', ''))
    content = request.forms.get('comment')

    cur_user = aaa.current_user.username
    alchemy.add_comment(post_id, cur_user, content)
    alchemy.update_visits(cur_user, 'Оставил комментарий под постом {}'.format(post_id))


@route('/com/<comment>', method='POST')
def make_comment_edition(comment):
    aaa.require(fail_redirect='/login')
    comment_id = int(comment.replace('comment', ''))
    content = request.forms.get('edition')

    cur_user = aaa.current_user.username
    alchemy.make_edition(comment_id, cur_user, content)
    alchemy.update_visits(cur_user, 'Сделал правку под своим комментарием')
    return bottle.redirect('/')


@route('/upd')
def get_comments_updates():
    global update_list
    aaa.require(fail_redirect='/login')
    when = update_list[aaa.current_user.username]
    new_comments = alchemy.comments_updates(when, aaa.current_user.username)
    update_list[aaa.current_user.username] = datetime.datetime.now()
    result = {post_num: template('static/html/comment_section.tpl', post=new_comments[post_num])
              for post_num in new_comments}

    return json.dumps(result)


@route('/load_xml')
def prepare_xml_file():
    aaa.require(fail_redirect='/login')
    with open('static/resources/{}_report.xml'.format(aaa.current_user.username), 'w') as f:
        f.seek(0)
        f.truncate()
        f.write(template('static/html/xml_export.tpl', posts=alchemy.get_posts_tree()))
        # return static_file('resources/{}_report.xml'.format(aaa.current_user.username), root='static')
        return '../resources/{}_report.xml'.format(aaa.current_user.username)

@route('/validate_registration/<registration_code>')
def validate_registration(registration_code):
    aaa.validate_registration(registration_code)
    return 'Thanks. <a href="/">Go to login</a>'


@route('/<filename:path>')
def send_file(filename):
    return static_file(filename, root='static/')


@route('/login', method='POST')
def do_auth():
    global Counter
    Counter += 1
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
    global Counter
    Counter += 1
    try:
        _ = aaa.current_user
        return bottle.redirect('/')
    except AuthException as e:
        browser_info = httpagentparser.detect(request.environ.get('HTTP_USER_AGENT'))['browser']
        visited = bottle.request.get_cookie('visit')
        if not visited:
            bottle.response.set_cookie('visit', 'yes', path='/',
                                       expires=datetime.datetime.now() + datetime.timedelta(minutes=30))

            alchemy.update_visits()

        return template('static/html/landing.html',
                        last_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                        browser=browser_info.get('name'),
                        version=browser_info.get('version'),
                        size='',
                        heat=convert_counter_in_html(str(Counter)),
                        total_visits=convert_counter_in_html(str(alchemy.get_visits_count())),
                        visits_today=convert_counter_in_html(str(alchemy.get_visits_count(True))))


@route('/logout')
def logout():
    aaa.require(fail_redirect='/login')
    alchemy.update_visits(aaa.current_user.username, 'Вышел из профиля')
    aaa.logout(success_redirect='/login')


@route('/stat')
def statistics():
    aaa.require(fail_redirect='login')
    alchemy.update_visits(aaa.current_user.username, 'Перешел на страницу личной статистики')
    stats = alchemy.get_stat(aaa.current_user.username)
    visits = alchemy.get_visits_user(aaa.current_user.username)
    return template('static/html/statistics.html', name=aaa.current_user.username, stat=stats, visits=visits)


def main():
    bottle.debug(True)
    bottle.run(app=app, host='localhost', port=5050)


if __name__ == "__main__":
    main()
    upd(Counter)
