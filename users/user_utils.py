import os
from glob import glob

class User:
    def __init__(self,id, iris_id, name, email): 
        self.id = id
        self.iris_id = iris_id
        self.name = name
        self.email = email

users = []


def delete_user(id: str):
    user = next(user for user in users if user.id == id)
    try:
        print('Trying to delete user %s' %user.name + '...')
        users.remove(user)
        files = glob(os.path.abspath('data/system_database/registered_users/%s_*' %user.iris_id))
        [os.remove(file) for file in files if file]
        print('Successfully deleted!')
        return 0
    except:
        return 1



def get_user_name(iris_id: str):
    user = next(user for user in users if user.id == id)
    return user.name

def create_user(name: str, email: str, iris_id: str):
    new_id=1
    try:
        users.append(User(new_id,iris_id, name, email))
        return 0
    except: 
        return 1


if __name__ == '__main__':
    users.append(User(2, 233, 'John Smith', 'js@gmail.com'))
    print('WTF')
    delete_user(2)
