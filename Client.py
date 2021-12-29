import requests
import random, string 
from datetime import datetime, timedelta
import threading

def get_token():
    tokenEndPoint = f'{baseURL}/api/token/'
    response = requests.post(tokenEndPoint, data={'username': 'admin', 'password': 'app123'})
    token = response.json()['access']
    return token

#get data
def get_data():
    getEndPoint = f'{baseURL}/api/member/'
    header = {'Authorization': f'Bearer {get_token()}'}
    response = requests.get(getEndPoint, headers = header)
    emp_data = response.json()
    return emp_data 

#post(add) data
def post_data(random_mrn, random_name, random_dob):
    postEndPoint = f'{baseURL}/api/member/'
    header = {'Authorization': f'Bearer {get_token()}'}
    data = {
        'mrn': f'{random_mrn}', 'name': f'{random_name}', 'dob': f'{random_dob}'
    }
    response = requests.post(postEndPoint, data = data, headers = header)
    print(response.text, response.status_code)

#edit data
def edit_data(id, name, dob):
    editEndPoint = f'{baseURL}/api/member/{id}/'
    header = {'Authorization': f'Bearer {get_token()}'}
    data = {
        'name': f'{name}', 'dob': {dob}
    }
    response = requests.put(editEndPoint, data = data, headers = header)
    print(response.text, response.status_code)

#delete data
def delete_data(id):
    deleteEndPoint = f'{baseURL}/api/member/{id}/'
    header = {'Authorization': f'Bearer {get_token()}'}
    response = requests.delete(deleteEndPoint, headers = header)
    print(response.text, response.status_code)

def get_random_name(name_len):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(name_len)).capitalize()

def get_random_dob(min_year=1900, max_year=datetime.today().year):
    start = datetime(min_year, 1, 1)
    years = max_year - min_year + 1
    end = start + timedelta(days=365 * years)
    dob = (start + (end - start) * random.random()).date()
    return dob 

def get_largest_member_id():
    return get_data()[-1]['id'] if get_data() else -1

def get_random_mrn():
    return random.randint(1000, 10000)


if __name__ == "__main__":
    baseURL = 'http://127.0.0.1:8000'

    def do_request():
        while True:
            post_data(get_random_mrn(), f'{get_random_name(3)} {get_random_name(6)}', get_random_dob())

    threads = []

    for i in range(8):
        t = threading.Thread(target=do_request())
        t.daemon = True
        threads.append(t)
    
    for i in range(8):
        threads[i].start()
    
    for i in range(8):
        threads[i].join()

    