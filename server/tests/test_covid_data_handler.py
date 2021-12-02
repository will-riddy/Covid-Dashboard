import pytest, os
from requests.exceptions import ConnectionError
from covid_data_handler import *

# read from config file
with open('config.json', 'r') as config:
    config_data = json.load(config)
    LOCATION = config_data['LOCATION']
    LOCATION_TYPE = config_data['LOCATION_TYPE']

def test_parse_csv_data():
    data = parse_csv_data ('nation_2021-10-28.csv')
    assert len(data) == 639

def test_process_covid_csv_data():
    
    last7days_cases , current_hospital_cases , total_deaths = process_covid_data(parse_csv_data('nation_2021-10-28.csv'))
    assert last7days_cases == 240_299
    assert current_hospital_cases == 7_019
    assert total_deaths == 141_544

def test_covid_API_request_connection():

    '''Tests if theres no wi-fi connection an error is raised'''

    with pytest.raises(ConnectionError):
        covid_API_request(LOCATION, LOCATION_TYPE)


#test_covid_API_request_connection()
#print(os.environ)
[print(x) for x in os.environ]