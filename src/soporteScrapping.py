from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import numpy as np
from IPython.display import clear_output
from selenium.webdriver.common.by import By
import requests
import re
from bs4 import BeautifulSoup
import time
import pickle

def getLinks(url):
    res = requests.get(url)
    print(res.status_code)
    sopa = BeautifulSoup(res.content, 'html.parser')
    urls_todos = sopa.find_all("tr")
    resultados = []
    for item in urls_todos:
        item = item.text
        resultados.append(item)
    patron = r'([\w-]{1,}?-latest-free.shp.zip)'
    links_final = []
    for index, item in enumerate(resultados):
        links_final.append(re.findall(patron, resultados[index]))
    res_list = []
    [res_list.append(x) for x in links_final if x not in res_list]
    flattened = [val for sublist in res_list for val in sublist]
    return [(url+item) for item in flattened], flattened

def url(rooms, country, checkin, checkout, adults):
    return str(
    'https://www.booking.com/searchresults.en-gb.html?'
    'ss=Sicily%2C+Italy&ssne=Sicily%2C+Italy&ssne_untouched=Sicily%2C+Italy'
    '&efdco=1&label'
    '=gen173nr-1DCAEoggJCAlhYSDNYBGiTAYgBAZgBLsIBCnd'
    'pbmRvd3MgMTDIAQzYAQPoAQGSAgF5qAID&'
    'sid=716ea5d78c4043fd78b7a1410d639e3d&'
    'aid=304142&'
    'lang=en-gb'
    '&sb=1&'
    'src_elem=sb&'
    'src=index&'
    'dest_id=909&'
    'dest_type=region&'
    'ac_position=0&'
    'ac_click_type=b&'
    'ac_langcode=en&'
    'ac_suggestion_list_length=5&'
    'search_selected=true&'
    'search_pageview_id=36746f79352b0064&'
    'ac_meta=GhAzNjc0NmY3OTM1MmIwMDY0IAAoATICZW46BFNpY2lAAEoAUAA%3D&'
    'checkin={checkin}&'
    'checkout={checkout}&'
    'group_adults={adults}&'
    'no_rooms={rooms}&'
    'group_children=0&'
    'sb_travel_purpose=leisure'.format(
        rooms=rooms,
        country=country.replace(" ", "+"),
        checkin=checkin,
        checkout=checkout,
        adults=adults,
    )
)

def opcionesSelenium():
    ## opciones selenium
    opciones= Options()
    opciones.add_experimental_option('excludeSwitches', ['enable-automation'])
    #para ocultarme como robot
    opciones.add_experimental_option('useAutomationExtension', False)
    opciones.add_argument('--start-maximized') #empezar maximizado
    opciones.add_argument('user.data-dir=selenium') #guarda las cookies
    opciones.add_argument('--incognito')#incognito window

def seleniumFirefoxBooking(list_url, list_dates, dia, almacen):
    driver = webdriver.Firefox()
    driver.get(list_url[dia])
    driver.maximize_window()
    driver.set_window_size(1920, 1080)
    driver.implicitly_wait(30)
    driver.find_element('css selector', '#onetrust-accept-btn-handler').click()
    try:
        for page in range (1,40):
            try:
                for i in range(3, 50):
                    print('item:', i, 'page:', page)
                    driver.implicitly_wait(15)
                    # Store the ID of the original window
                    original_window = driver.current_window_handle
                    try:
                        try:
                            name = driver.find_element('xpath', '//*[@id="search_results_table"]/div[2]/div/div/div/div[3]/div[{i}]/div[1]/div[2]/div/div[1]/div/div[1]/div/div[1]/div/h3/a/div[1]'.format(i=i)).text
                            previousPrice = driver.find_element('xpath', '//*[@id="search_results_table"]/div[2]/div/div/div/div[3]/div[{i}]/div[1]/div[2]/div/div[3]/div[2]/div/div[1]/span/div/span[1]'.format(i=i)).text
                            currentPrice = driver.find_element('xpath', '//*[@id="search_results_table"]/div[2]/div/div/div/div[3]/div[{i}]/div[1]/div[2]/div/div[3]/div[2]/div/div[1]/span/div/span[2]'.format(i=i)).text
                            rating = driver.find_element('xpath', '//*[@id="search_results_table"]/div[2]/div/div/div/div[3]/div[{i}]/div[1]/div[2]/div/div[1]/div/div[2]/div/div/div/a/span/div/div[1]'.format(i=i)).text
                            reviewNumber = driver.find_element('xpath', '//*[@id="search_results_table"]/div[2]/div/div/div/div[3]/div[{i}]/div[1]/div[2]/div/div[1]/div/div[2]/div/div/div/a/span/div/div[2]/div[2]'.format(i=i)).text
                            image = driver.find_element('xpath', '//*[@id="search_results_table"]/div[2]/div/div/div/div[3]/div[{i}]/div[1]/div[1]/div/a/img'.format(i=i)).get_attribute('src')
                            driver.find_element('xpath', f'//*[@id="search_results_table"]/div[2]/div/div/div/div[3]/div[{i}]/div[1]/div[2]/div/div[1]/div/div[1]/div/div[1]/div/h3/a').click()
                        except:
                            name = driver.find_element('xpath', '//*[@id="search_results_table"]/div[2]/div/div/div/div[3]/div[{i}]/div[1]/div[2]/div/div[1]/div/div[1]/div/div[1]/div/h3/a/div[1]'.format(i=i)).text
                            try:
                                previousPrice = driver.find_element('xpath', '//*[@id="search_results_table"]/div[2]/div/div/div/div[3]/div[{i}]/div[1]/div[2]/div/div[3]/div[2]/div/div/span/div/span[1]'.format(i=i)).text
                                currentPrice = driver.find_element('xpath', '//*[@id="search_results_table"]/div[2]/div/div/div/div[3]/div[{i}]/div[1]/div[2]/div/div[3]/div[2]/div/div/span/div/span[2]'.format(i=i)).text
                            except:
                                previousPrice = np.nan
                                currentPrice = driver.find_element('xpath', '//*[@id="search_results_table"]/div[2]/div/div/div/div[3]/div[{i}]/div[1]/div[2]/div/div[2]/div[2]/div/div[1]/span'.format(i=i)).text
                            rating = driver.find_element('xpath', '//*[@id="search_results_table"]/div[2]/div/div/div/div[3]/div[{i}]/div[1]/div[2]/div/div[1]/div/div[2]/div/div/div/a/span/div/div[1]'.format(i=i)).text
                            reviewNumber = driver.find_element('xpath', '//*[@id="search_results_table"]/div[2]/div/div/div/div[3]/div[{i}]/div[1]/div[2]/div/div[1]/div/div[2]/div/div/div/a/span/div/div[2]/div[2]'.format(i=i)).text
                            image = driver.find_element('xpath', '//*[@id="search_results_table"]/div[2]/div/div/div/div[3]/div[{i}]/div[1]/div[1]/div/a/img'.format(i=i)).get_attribute('src')
                            driver.find_element('xpath', f'//*[@id="search_results_table"]/div[2]/div/div/div/div[3]/div[{i}]/div[1]/div[2]/div/div[2]/div[2]/div/div[2]/a').click()
                        driver.switch_to.window(driver.window_handles[1])
                        time.sleep(7)
                        url = driver.current_url
                        print(url, driver.title)
                        almacen['url'].append(url)
                        res = requests.get(url)
                        soup = BeautifulSoup(res.content, 'html.parser')
                        pagina = soup.text
                        almacen['pagina'].append(pagina)
                        almacen['address'].append(re.findall('(.*, \d{3,5} .*)', pagina.lower()))
                        print('dict:', len(almacen['url']), len(almacen['pagina']))
                        print('hasta aquí')
                        driver.close()
                        driver.switch_to.window(original_window)
                        almacen['name'].append(name)
                        almacen['previousPrice'].append(previousPrice)
                        almacen['currentPrice'].append(currentPrice)
                        almacen['rating'].append(rating)
                        almacen['reviewNumber'].append(reviewNumber)
                        almacen['image'].append(image)
                        almacen['checkingDate'].append(list_dates[dia])
                        print(len(almacen['name']), len(almacen['url']), len(almacen['currentPrice']), len(almacen['previousPrice']))
                        clear_output(wait=True)
                    except:
                        pass
                    clear_output
                driver.find_element('xpath', '//*[@id="search_results_table"]/div[2]/div/div/div/div[4]/div[2]/nav/div/div[3]/button').click()
                print(len(almacen['name']), len(almacen['url']), len(almacen['currentPrice']), len(almacen['previousPrice']))
                driver.implicitly_wait(2)
                clear_output(wait=True)
                with open(f'../data/dict_booking_{dia}.pickle', 'wb') as data_scrapeado:
                    pickle.dump(almacen, data_scrapeado)
            except:
                pass
    except:
        print('me rompí')