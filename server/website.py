'''Web server'''

from flask import Flask, render_template, request
import api.covid_data_handler as covid_data_handler
import api.covid_news_handling as covid_news_handling
import sched, time, datetime, logging, os

logging.basicConfig(filename=os.environ['LOGGING_PATH'], level=logging.DEBUG, encoding='utf-8')

app = Flask(__name__)

LOCATION = os.environ['LOCATION']
NATION = os.environ['NATION']
TITLE = os.environ['TITLE']
IMAGE = os.environ['IMAGE']

s = sched.scheduler(time.time, time.sleep)



def epoch_to_time(epoch : float) -> str:

    '''Convertes epoch to time string'''

    return time.strftime('%d-%m-%Y %H:%M:%S', time.localtime(float(epoch)))



def time_to_epoch(time_string : str) -> int:

    '''convertes a time string to epoch'''

    return int(time.mktime(time.strptime(time_string, '%d-%m-%Y %H:%M:%S')))



def schedule_update(time : str, name : str, covid : bool = False, news: bool = False, repeat : str = ' ') -> None:

    '''Schedule an event with a time like 'hh:mm', and name of event'''

    # convert time to seconds
    current_time = datetime.datetime.now().timestamp()
    update_interval = time.split(':')

    timedate = datetime.time(int(update_interval[0]), int(update_interval[1]), 0)
    date = datetime.datetime.now().date()

    time_string = str(date) + ' ' + str(timedate)
    epoch = datetime.datetime.strptime(time_string, "%Y-%m-%d %H:%M:%S").timestamp()
    time_difference = epoch - current_time
    # if the time is set for the next day:
    if time_difference < 0:
        date += datetime.timedelta(days=1)
        time_string = str(date) + ' ' + str(timedate)
        epoch = datetime.datetime.strptime(time_string, "%Y-%m-%d %H:%M:%S").timestamp()
        time_difference = epoch - current_time

    if covid:
        s.enter(time_difference, 1, covid_data_handler.schedule_covid_updates, (f'{name} - Covid Data {repeat}',), kwargs={'nation': NATION})

    if news:
        s.enter(time_difference, 1, covid_news_handling.update_news, (f'{name} - News Data {repeat}',))

        

@app.route('/')
def main() -> None:

    '''Default webpage'''

    #global local_7day_rate, national_7day_rate, hospital_cases, deaths_total
    news_articles = covid_news_handling.update_news(delete_list)

    covid_data_handler.schedule_covid_updates(nation=NATION)
    local_7day_rate, national_7day_rate, hospital_cases, deaths_total = covid_data_handler.covid_data_all

    return render_template(
        'index.html',
        news_articles=news_articles,
        local_7day_infections=local_7day_rate,
        location=LOCATION,
        national_7day_infections=national_7day_rate,
        nation_location=NATION,
        hospital_cases=hospital_cases,
        deaths_total=deaths_total,
        updates=schedule_queue,
        title=TITLE,
        image=IMAGE)



@app.route('/index')
def index() -> None:

    '''INdex webpage'''

    global schedule_queue
    global previous_queue

    s.run(blocking=False)

    local_7day_rate=national_7day_rate=hospital_cases=deaths_total = None
    news_articles=schedule_queue = []
    alarm = request.args.get('alarm')
    name = request.args.get('two')
    repeat = request.args.get('repeat')
    covid_data = request.args.get('covid-data')
    news = request.args.get('news')
    delete_news = request.args.get('notif')
    delete_sched = request.args.get('alarm_item')

    refresh_news = request.args.get('refresh_news')

    if repeat:
        repeat = 'Repeat'
    else:
        repeat = ''
        
    if delete_news:
        delete_list.append(delete_news)

    elif refresh_news:
        delete_list.clear()
        news_articles = covid_news_handling.update_news(delete_list)

    if covid_news_handling.updates:
        delete_list.clear()
        news_articles = covid_news_handling.update_news(delete_list)

    try:
        news_articles = covid_news_handling.update_news(delete_list, update=False)
    except KeyError:
        news_articles = []

    if delete_sched:
        for i, event in enumerate(s.queue):
            if event._asdict()['argument'][0] == delete_sched:
                # if event._asdict()['argument'][0].split(' ')[4].lower() == 'repeat':
                #     repeat_list.append(event)
                previous_queue.pop(i)
                s.cancel(event)

    if alarm:
        
        if covid_data == 'covid-data':            
            schedule_update(alarm, name, covid=True, repeat=repeat)
            logging.info(f'Schedeuled Event: {alarm}, {name} covid data {repeat}')
        if news == 'news':
            schedule_update(alarm, name, news=True, repeat=repeat)
            logging.info(f'Schedeuled Event: {alarm}, {name} news data {repeat}') 

    schedule_queue = s.queue
    if len(schedule_queue) > 0:
        # turns named tuple into a modified dictionay
        for i, schedule in enumerate(schedule_queue):
            try:
                schedule_queue[i] = {'argument':schedule._asdict()['argument'][0],
                                    'content':epoch_to_time(schedule._asdict()['time'])}
            except AttributeError:
                pass

    if len(previous_queue) != len(schedule_queue):
        for event in previous_queue:
            if event not in schedule_queue:
                try:
                    if event['argument'].split(' ')[4].lower() == 'repeat':
                        if event['argument'].split(' ')[2].lower() == 'covid':
                            schedule_update(event['content'].split(' ')[1], event['argument'].split(' ')[0], covid=True, repeat='repeat')
                        elif event['argument'].split(' ')[2].lower() == 'news':
                            schedule_update(event['content'].split(' ')[1], event['argument'].split(' ')[0], news=True, repeat='repeat')
                except IndexError: # item timed out normaly
                    pass
        
        # refrom dictionary for ui
        schedule_queue = s.queue
        if len(schedule_queue) > 0:
            # turns named tuple into a modified dictionay
            for i, schedule in enumerate(schedule_queue):
                try:
                    schedule_queue[i] = {'argument':schedule._asdict()['argument'][0],
                                        'content':epoch_to_time(schedule._asdict()['time'])}
                except AttributeError:
                    pass
        
    previous_queue = schedule_queue

    try:
        local_7day_rate, national_7day_rate, hospital_cases, deaths_total = covid_data_handler.covid_data_all
    except TypeError:
        logging.warning('Covid data not accessed yet')
        covid_data_handler.schedule_covid_updates(nation=NATION)
        local_7day_rate, national_7day_rate, hospital_cases, deaths_total = covid_data_handler.covid_data_all

    return render_template(
        'index.html',
        news_articles=news_articles,
        local_7day_infections=local_7day_rate,
        location=LOCATION,
        national_7day_infections=national_7day_rate,
        nation_location=NATION,
        hospital_cases=hospital_cases,
        deaths_total=deaths_total,
        updates=schedule_queue,
        title=TITLE,
        image=IMAGE)

schedule_queue = []
previous_queue = []
delete_list = []

if __name__ == '__main__':    
    app.run()
