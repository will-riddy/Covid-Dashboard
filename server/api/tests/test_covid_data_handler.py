import pytest, os
from requests.exceptions import ConnectionError
from server.api.covid_data_handler import *

# read from config file
LOCATION = os.environ['LOCATION']
LOCATION_TYPE = os.environ['LOCATION_TYPE']
NATION = os.environ['NATION']

def test_parse_csv_data():
    data = parse_csv_data ('nation_2021-10-28.csv')
    assert len(data) == 639

def test_process_covid_csv_data():
    
    last7days_cases , current_hospital_cases , total_deaths = process_covid_data(parse_csv_data('nation_2021-10-28.csv'))
    assert last7days_cases == 240_299
    assert current_hospital_cases == 7_019
    assert total_deaths == 141_544

def test_covid_API_request_connection():

    '''Tests if there's no wi-fi connection an error is raised'''

    with pytest.raises(ConnectionError):
        covid_API_request(LOCATION, LOCATION_TYPE)


test_data = {
    '2021-12-04': 
        {'areaName': 'Exeter', 'areaCode': 'E07000041', 'areaType': 'ltla', 'date': '2021-12-04', 'cumDailyNsoDeathsByDeathDate': None, 'hospitalCases': None, 'newCasesBySpecimenDate': 2},
    '2021-12-03': 
        {'areaName': 'Exeter', 'areaCode': 'E07000041', 'areaType': 'ltla', 'date': '2021-12-03', 'cumDailyNsoDeathsByDeathDate': None, 'hospitalCases': None, 'newCasesBySpecimenDate': 2},
    '2021-12-02': 
        {'areaName': 'Exeter', 'areaCode': 'E07000041', 'areaType': 'ltla', 'date': '2021-12-02', 'cumDailyNsoDeathsByDeathDate': None, 'hospitalCases': None, 'newCasesBySpecimenDate': 2},
    '2021-12-01': 
        {'areaName': 'Exeter', 'areaCode': 'E07000041', 'areaType': 'ltla', 'date': '2021-12-01', 'cumDailyNsoDeathsByDeathDate': None, 'hospitalCases': None, 'newCasesBySpecimenDate': 2},
    '2021-11-30':
        {'areaName': 'Exeter', 'areaCode': 'E07000041', 'areaType': 'ltla', 'date': '2021-11-30', 'cumDailyNsoDeathsByDeathDate': None, 'hospitalCases': 45, 'newCasesBySpecimenDate': 2},
    '2021-11-29':
        {'areaName': 'Exeter', 'areaCode': 'E07000041', 'areaType': 'ltla', 'date': '2021-11-29', 'cumDailyNsoDeathsByDeathDate': None, 'hospitalCases': None, 'newCasesBySpecimenDate': 2},
    '2021-11-28': 
        {'areaName': 'Exeter', 'areaCode': 'E07000041', 'areaType': 'ltla', 'date': '2021-11-28', 'cumDailyNsoDeathsByDeathDate': None, 'hospitalCases': None, 'newCasesBySpecimenDate': 2},
    '2021-11-27': 
        {'areaName': 'Exeter', 'areaCode': 'E07000041', 'areaType': 'ltla', 'date': '2021-11-27', 'cumDailyNsoDeathsByDeathDate': 23, 'hospitalCases': None, 'newCasesBySpecimenDate': 2},
    '2021-11-26': 
        {'areaName': 'Exeter', 'areaCode': 'E07000041', 'areaType': 'ltla', 'date': '2021-11-26', 'cumDailyNsoDeathsByDeathDate': None, 'hospitalCases': None, 'newCasesBySpecimenDate': 2}
}

def test_process_covid_dic():
    seven_day_rate, hospital_cases, death_total = process_covid_dic(test_data)
    assert seven_day_rate == 2
    assert hospital_cases == 45
    assert death_total == 23

test_process_covid_dic()