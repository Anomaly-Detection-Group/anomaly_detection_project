
# retrieve Codeup mySQL data
def get_db_access(database):
    # login info
    hostname = ""
    username = ""
    password = ""
    
    # acces url
    acc_url = f'mysql+pymysql://{username}:{password}@{hostname}/{database}'
    return acc_url


