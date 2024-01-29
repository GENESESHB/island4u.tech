#!/usr/bin/python3

import uuid

class User:
    def __init__(self, username, email, password=None, user_id=None):
        self.user_id = user_id if user_id else str(uuid.uuid4())
        self.username = username
        self.email = email
        self.password = password
