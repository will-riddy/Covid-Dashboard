'''Performs all the news data handling'''

import requests, os
from datetime import date

API_KEY = os.environ['API_KEY']
DATE = date.today().strftime("%Y-%m-%d")
LOCATION = os.environ['LOCATION_NEWS']
SEARCH_TERMS = os.environ['SEARCH_TERMS'].split(' ')


# access current news data
def news_API_request(covid_terms : list = SEARCH_TERMS) -> list:

    '''reads from news api and returns list of all the news whilst removing duplicate news'''

    responses = []
    for term in covid_terms:
        url = ('https://newsapi.org/v2/top-headlines?'
            f'q={term.lower()}&'
            f'from={DATE}&'
            'sortBy=popularity&'
            f'country={LOCATION}&'
            f'apiKey={API_KEY}')
        response = requests.get(url)
        responses.append(response.json()['articles'])

    final = responses[0]

    titles = []
    for article in final:
        titles.append(article['title'])
    
    # adds all responses into list and checks if the article is already in the list
    for i, resp in enumerate(responses):
        if i != 0:
            if len(resp) != 0:
                in_list = False
                for title in titles:
                    for r in resp:
                        if title == r['title']:
                            in_list = True
                
                if not in_list:
                    final.append(resp[0])


    return final

def update_news(delete_list : list = [], update : bool =True) -> dict:

    '''updates the news and removes news articles which have been deleted by the user'''

    global previous_news
    global updates
    updates = update
    # make less requests to the api
    if update:
        news_json = news_API_request()
        previous_news = news_json      
    else:
        news_json = previous_news

    if len(delete_list) > 0:    
        for delete in delete_list:
            for i, news in enumerate(news_json):
                if news['title'] == delete:
                    del news_json[i]
                    break
        if len(news_json) == 0:
            return news_json

    if news_json:
        return news_json
    else:
        return update_news()

previous_news = None
updates = False


if __name__ == '__main__':
    print(news_API_request())
