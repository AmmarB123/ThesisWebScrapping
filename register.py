'''
This file is used for user generation and password generation
'''

import re
import data
import hashlib
'''
Used to check if the registeration matches
input string
return int/str
'''
def register_user(username):
    print("reg username", username)
    #result = re.fullmatch(r'^[A-Za-z][A-Za-z0-9_]{5,12}$', username)
    # Length of username should be 4 to 12
    if len(username) < 4 or len(username) > 12:
        return 2
    # Should contain a lower and uppercase letter
    elif not re.match(r'^[A-Za-z]', username):
        return 3
    # Should not contain any spaces
    elif not re.match(r'^[A-Za-z\d]*$', username):
        return 4
    else:
        hashed_username = hashlib.sha256(username.encode()).hexdigest()
        query = "SELECT username FROM userdata WHERE username = ?"
        cur = data.connect.cursor()
        cur.execute(query, (hashed_username,))
        result = cur.fetchone()
        if result is not None:
            # Username does not exist so return pop up on gui
            return 1
        else:
            # The username does not exist so we create a new user
            return username

'''
Used to check the password combination
password: str
return str/int
'''
def register_password(password):
    #result = re.fullmatch(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\w\s])\S{5,20}$', password)
    # Checks the length of password
    if len(password) < 5 or len(password) > 20:
        return 1
    # Checks if it has lower case
    elif not re.search(r'[a-z]', password):
        return 2
    # Checks if it has upper case
    elif not re.search(r'[A-Z]', password):
        return 3
    # Checks if there are numbers
    elif not re.search(r'\d', password):
        return 4
    # Checks if there are no spaces
    elif not re.search(r'[^\w\s]', password):
        return 5
    # Checks if there are no spaces
    elif re.search(r'\s', password):
        return 6
    else:
        return password



