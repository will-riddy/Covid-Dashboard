'''Peforms all data handling for the covid data'''

import csv, os
from uk_covid19 import Cov19API
from requests.exceptions import ConnectionError

LOCATION = os.environ['LOCATION']
LOCATION_TYPE = os.environ['LOCATION_TYPE']
NATION = os.environ['NATION']

def parse_csv_data(csv_file : str) -> list:

    '''reads from csv file and converts it into a list of headers and data'''

    csv_list = []
    with open(csv_file, 'r') as data:
        data = csv.reader(data)
        header = next(data)
        [csv_list.append(row) for row in data]
        csv_list.insert(0, header)
    return csv_list

def process_covid_data(covid_csv_data : list) -> tuple[int, int, int]:

    '''Processess data from the covid csv template'''

    hosp_cases_i = covid_csv_data[0].index('hospitalCases')
    deaths_i = covid_csv_data[0].index('cumDailyNsoDeathsByDeathDate')
    cum_cases_i = covid_csv_data[0].index('newCasesBySpecimenDate')

    hosp_cases_list = []
    deaths_list = []
    cum_cases_list = []

    for i, row in enumerate(covid_csv_data[1:]): # skips first row                
        hosp_cases_list.append(row[hosp_cases_i])
        deaths_list.append(row[deaths_i])
        cum_cases_list.append(row[cum_cases_i])


    cum_deaths = 0
    for death in deaths_list:
        if death != '':
            cum_deaths = int(death)
            break
    
    cum_cases = 0
    for case in cum_cases_list[2:9]:
        cum_cases += int(case)

    if hosp_cases_list[0] != '':
        curr_hospital_cases = int(hosp_cases_list[0])
    else:
        curr_hospital_cases = 0


    return cum_cases, curr_hospital_cases, cum_deaths


def covid_API_request(location : str = LOCATION, location_type : str = LOCATION_TYPE) -> dict:

    '''Fetches all the covid data from the uk-covid api'''

    # filters
    filter = [
        f'areaType={location_type}',
        f'areaName={location}'
    ]

    cases_and_deaths = {    
    "areaName": "areaName",
    "areaCode": "areaCode",
    "areaType": "areaType",
    "date": "date",
    "cumDailyNsoDeathsByDeathDate": "cumDailyNsoDeathsByDeathDate",
    "hospitalCases": "hospitalCases",
    "newCasesBySpecimenDate": "newCasesBySpecimenDate"
    }
    try:
        api = Cov19API(filters=filter, structure=cases_and_deaths)
        data = api.get_json()
    except ConnectionError:
        raise ConnectionError
    # create dictionary sorted with dates as key
    data_dic = {}
    for line in data['data']:
        data_dic[line['date']] = line
    return data_dic

def process_covid_dic(covid_dic_data : dict) -> tuple[float, float, float]:

    '''Processess covid data'''

    seven_day_cases = 0
    not_found_deaths = True
    deaths_total = None
    hospital_cases = None
    not_found_hospital = True
    day_rate_count = 0
    for i, data in enumerate(covid_dic_data):
        if covid_dic_data[data]['hospitalCases'] is not None and not_found_hospital:
            hospital_cases = covid_dic_data[data]['hospitalCases']
            not_found_hospital = False
        # skips first day because the first day is incomplete
        if i > 0 and i < 8:
            seven_day_cases += covid_dic_data[data]['newCasesBySpecimenDate']
            day_rate_count += 1

        if covid_dic_data[data]['cumDailyNsoDeathsByDeathDate'] is not None and not_found_deaths:
            deaths_total = covid_dic_data[data]['cumDailyNsoDeathsByDeathDate']
            not_found_deaths = False
        

    seven_day_rate = round(seven_day_cases / day_rate_count, 1)
    return seven_day_rate, hospital_cases, deaths_total

# returns data at given time interval
def schedule_covid_updates(time : float = None, nation : str = NATION) -> None:

    '''Used to schedule the covid data'''

    global covid_data_all
    seven_day, _, _ = process_covid_dic(covid_API_request())
    seven_day_nation, hospital, deaths = process_covid_dic(covid_API_request(location=nation, location_type='nation'))
    covid_data_all = (seven_day, seven_day_nation, hospital, deaths)
    
covid_data_all = None

if '__main__' == __name__:
    print(covid_API_request())