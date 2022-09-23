# get_first_paragraph fct does extract wiki content selectfirst paragreaph and clean it
import os



cache = {}
def hashable_cache(f):
    def inner(url, session):
        if url not in cache:
            cache[url] = f(url, session)
        return cache[url]
    return inner

# <20 lines
@hashable_cache
def get_first_paragraph(wikipedia_url, session):
    from bs4 import BeautifulSoup
    import re
    first_paragraph = ''
    wiki_req = session.get(wikipedia_url).text
    soup = BeautifulSoup(wiki_req, 'html.parser')
    for paragraph in soup.find_all('p'):
        if paragraph.find('b'):
            break
    pattern = '\(([^)]*\[e\][^)]*)\)|\\n'
    first_paragraph = re.sub(pattern,"",paragraph.text)
    return first_paragraph

def save(leaders_per_country,file_name):
    import json
    #create a file or overwrite the file if it does already exist
    with open(str(file_name), 'w') as jf:
        json.dump(leaders_per_country,jf)

#def get leaders does 
def get_leaders():
    import requests
    # 1 URL 
    root_url = "http://country-leaders.herokuapp.com"
    cookie_url = root_url+"/cookie"
    country_url = root_url+"/countries"
    leaders_url = root_url + "/leaders"
    # 2 function in order to update the cookies
    def get_cookies():
        cookies = requests.get(cookie_url).cookies
        return cookies

    # 3 request the list of countries and create a json file
    countries_req = requests.get(country_url, cookies=get_cookies())
    countries = countries_req.json()
    # 4 create hte dict leaders_per_country
    leaders_per_country = {}
    leaders_wiki = {}
    # 5 creation of the loop to fill leaders_per_country dict
    for country in countries:
        params = {"country":country}
        leaders_per_country[country] = requests.get(leaders_url, cookies=get_cookies(), params=params).json()
        for leader in leaders_per_country[country]:
            first_paragraph = get_first_paragraph(leader['wikipedia_url'],session)
            leader['first_paragaph'] = first_paragraph
    return leaders_per_country

save(get_leaders(),'leader2.json')