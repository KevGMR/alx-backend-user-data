#!/usr/bin/env python3
'''A simple end-to-end (E2E) integration test for `app.py`.
'''
import requests


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
BASE_URL = "http://0.0.0.0:5000"


def register_user(email: str, password: str) -> None:
    '''Tests registering a user.
    '''
    url = "{}/users".format(BASE_URL)
    body = {
        'email': email,
        'password': password,
    }
    r = requests.post(url, data=body)
    assert r.status_code == 200
    assert r.json() == {"email": email, "message": "user created"}
    r = requests.post(url, data=body)
    assert r.status_code == 400
    assert r.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    '''Tests logging in with a wrong password.
    '''
    url = "{}/sessions".format(BASE_URL)
    body = {
        'email': email,
        'password': password,
    }
    r = requests.post(url, data=body)
    assert r.status_code == 401


def log_in(email: str, password: str) -> str:
    '''Tests logging in.
    '''
    url = "{}/sessions".format(BASE_URL)
    body = {
        'email': email,
        'password': password,
    }
    r = requests.post(url, data=body)
    assert r.status_code == 200
    assert r.json() == {"email": email, "message": "logged in"}
    return r.cookies.get('session_id')


def profile_unlogged() -> None:
    '''Tests retrieving profile information whilst logged out.
    '''
    url = "{}/profile".format(BASE_URL)
    r = requests.get(url)
    assert r.status_code == 403


def profile_logged(session_id: str) -> None:
    '''Tests retrieving profile information whilst logged in.
    '''
    url = "{}/profile".format(BASE_URL)
    req_cookies = {
        'session_id': session_id,
    }
    r = requests.get(url, cookies=req_cookies)
    assert r.status_code == 200
    assert "email" in r.json()


def log_out(session_id: str) -> None:
    '''Tests logging out of a session.
    '''
    url = "{}/sessions".format(BASE_URL)
    req_cookies = {
        'session_id': session_id,
    }
    r = requests.delete(url, cookies=req_cookies)
    assert r.status_code == 200
    assert r.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    '''Tests requesting a password reset.
    '''
    url = "{}/reset_password".format(BASE_URL)
    body = {'email': email}
    r = requests.post(url, data=body)
    assert r.status_code == 200
    assert "email" in r.json()
    assert r.json()["email"] == email
    assert "reset_token" in r.json()
    return r.json().get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    '''Tests updating a user's password.
    '''
    url = "{}/reset_password".format(BASE_URL)
    body = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password,
    }
    r = requests.put(url, data=body)
    assert r.status_code == 200
    assert r.json() == {"email": email, "message": "Password updated"}


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
