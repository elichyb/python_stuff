"""
Used structures and classes
"""
#from . import _load_users
from os import path
import json
import pandas as pd

def create_repository():
    return Repository()

class Repository(object):
    def __init__(self):
        self.name = 'Pandas'
        self.index = {}
# -------------------------------------------------------
# Opens the data base (json) that has the users database.
# return the data as a data frame
# -------------------------------------------------------
    def OpenUsersDB(self):
        # find file location
        users_db = path.join(path.dirname(__file__), '..\\static\\db\\users.json')

        try:
            with open(users_db, 'r') as usersfile:  
                s = json.load(usersfile)
                x = json.loads(s)
            
                df = pd.DataFrame.from_dict(x)

        except:
            Data = {'username': ['glidror','admin'],
                    'password': ['glidror', 'admin1234'],
                    'email': ['gady.lidror@gmail.com', 'gady.lidror@gmail.com'],
                    'phone': ['052-2684245', '052-2684245'],
                    'firstname': ['Gad', 'Teacher'],
                    'lastname': ['Lidror', 'Tichonet']
                    }
            df = pd.DataFrame(Data, columns=['username', 'password', 'email', 'phone', 'firstname', 'lastname'])

        finally: 
            return df


# -------------------------------------------------------
# Saves the datafram (input parameter) into the json 
# Users data base
# -------------------------------------------------------
    def WriteToFile_users(self, df):
        """Save the users dataframe into the local file"""
        users_db = path.join(path.dirname(__file__), '..\\static\\db\\users.json')

        with open(users_db, 'w') as usersfile:  
            json.dump(df.to_json(), usersfile, indent=4 , sort_keys=True)

