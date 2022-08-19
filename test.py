import bcrypt

username= 'potato'
password =  b'potato'





if bcrypt.checkpw(password, hashed_password):
    print('Conf!')