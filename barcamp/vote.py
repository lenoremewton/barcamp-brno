# coding: utf-8

from barcamp import app
from flask import flash, url_for, redirect, request, session
from login_misc import check_auth, auth_required

KEYS = {
    'votes': 'votes_%s_%%s' % app.config['YEAR'],  # set
    'talks': 'talks_%s' % app.config['YEAR'],
}


@app.route('/hlas-pro-prednasku/<talk_hash>')
@auth_required
def vote_for_talk(talk_hash):
    user = check_auth()
    user_hash = user['user_hash']
    old_votes = app.redis.smembers(KEYS['votes'] % user_hash) or set()

    method = request.args.get('method', 'decrease')
    if method == 'increase' and talk_hash not in old_votes:
        app.redis.zincrby(KEYS['talks'], talk_hash, 1)
        app.redis.sadd(KEYS['votes'] % user_hash, talk_hash)

    if method == 'decrease' and talk_hash in old_votes:
        app.redis.zincrby(KEYS['talks'], talk_hash, -1)
        app.redis.srem(KEYS['votes'] % user_hash, talk_hash)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return str(int(app.redis.zscore(KEYS['talks'], talk_hash)) or 0)

    flash(u'Hlas byl zaznamenán', 'success')
    return redirect(url_for('talks_all'))


@app.route('/hlasovani-potrebuje-prihlaseni')
def voting_require_login():
    flash(u'Když chceš hlasovat, musíš se přihlásit ke svému účtu', 'warning')
    session['next'] = url_for('talks_all')
    return redirect(url_for('login'))

@app.route('/hlasovani-potrebuje-registraci')
def voting_require_going():
    flash(u'Když chceš hlasovat, musíš chtít přijít', 'warning')
    session['next'] = url_for('index')
    return redirect(url_for('index'))


def get_user_votes(user_hash):
    return tuple(app.redis.smembers(KEYS['votes'] % user_hash))


def remove_user_votes(user_hash):
    decrement = app.redis.smembers(KEYS['votes'] % user_hash) or set()
    for vote in decrement:
        app.redis.srem(KEYS['votes'] % user_hash, vote)
        app.redis.zincrby(KEYS['talks'], vote, -1)
