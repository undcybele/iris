import os
from glob import glob
import pandas as pd
import uuid

class User:
    def __init__(self,id, name, email): 
        self.id = id
        self.name = name
        self.email = email

CSV_PATH = 'iris/data/system_database/data.csv'

def delete_user(id: str):
    found_user = {}
    users = pd.read_csv(CSV_PATH, header=None).values
    print(users)

    for user in users:
      if user.id == id:
        found_user = user
        
    try:
      print('Trying to delete user %s' %user.name + '...')
      users.remove(user)
      files = glob(os.path.abspath('data/system_database/registered_users/%s_*' %user.iris_id))
      [os.remove(file) for file in files if file]
      return 'Successfully deleted!'
    except:
        return 'Could not delete user!'

def get_user_name(id: str):
    found_user = {}
    users = pd.read_csv(CSV_PATH, header=None).values
    print(users)

    for user in users:
      if user.id == id:
        found_user = user
    return found_user.name

def create_user(name: str, email: str):
    new_id=uuid.uuid1()
    users = pd.read_csv(CSV_PATH, header=None).values
    print(users)
    try:
        data = {new_id, name, email}
        df = pd.DataFrame(data)
        df.to_csv(CSV_PATH, mode='a', index=False, header=False)
        users2 = pd.read_csv(CSV_PATH, header=None).values
        print(users2)
        return 'Successfully created!'
    except: 
        return 'Could not create this user!'


if __name__ == '__main__':
    users.append(User('2', 'John Smith', 'js@gmail.com'))
    print('WTF')
    delete_user('2')
