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

def seleniumChromeBooking_1st(list_url,list_dates, dia, almacen):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(list_url[dia])
    driver.maximize_window()
    driver.set_window_size(1920, 1080)
    driver.implicitly_wait(30)
    driver.find_element('css selector', '#onetrust-accept-btn-handler').click()
    try:
        try:
            for i in range(3, 50):
                print('item:', i)
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
                    time.sleep(5)
                    url = driver.current_url
                    almacen['url'].append(url)
                    res = requests.get(url)
                    soup = BeautifulSoup(res.content, 'html.parser')
                    pagina = soup.text
                    almacen['pagina'].append(pagina)
                    almacen['address'].append(re.findall('(.*, \d{3,5} .*)', pagina.lower()))
                    print('dict:', len(almacen['url']), len(almacen['pagina']))
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
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
        # driver.find_element('xpath', '//*[@id="search_results_table"]/div[2]/div/div/div/div[4]/div[2]/nav/div/div[3]/button').click()
        # driver.implicitly_wait(2)
        # clear_output(wait=True)
        except:
            pass
    except:
        print('me rompí')

def seleniumChromeBooking(list_url, list_dates, dia, almacen):
    driver = webdriver.Chrome(ChromeDriverManager().install())
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
                    print(driver.current_window_handle)
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
                        before = driver.window_handles[0]
                        after = driver.window_handles[-1]
                        time.sleep(7)
                        driver.switch_to.window(after)
                        print(driver.current_window_handle)
                        driver.implicitly_wait(15)
                        url = driver.current_url
                        almacen['url'].append(url)
                        res = requests.get(url)
                        soup = BeautifulSoup(res.content, 'html.parser')
                        pagina = soup.text
                        almacen['pagina'].append(pagina)
                        almacen['address'].append(re.findall('(.*, \d{3,5} .*)', pagina.lower()))
                        print('dict:', len(almacen['url']), len(almacen['pagina']))
                        driver.close()
                        driver.switch_to.window(before)
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
                clear_output(wait=True)
                with open(f'../data/dict_booking_{dia}.pickle', 'wb') as data_scrapeado:
                    pickle.dump(almacen, data_scrapeado)
            except:
                pass
    except:
        print('me rompí')
    
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


def seleniumFirefoxBooking2(url, dia, almacen):
    driver = webdriver.Firefox()
    driver.get(url)
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
                                                                #div.a826ba81c4:nth-child(4) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > h3:nth-child(1) > a:nth-child(1) > div:nth-child(1)
                                                                #/html/body/div[3]/div/div[4]/div[1]/div[1]/div[4]/div[2]/div[2]/div/div/div[3]/div[4]/div[1]/div[2]/div/div[1]/div/div[1]/div/div[1]/div[1]/h3/a/div[1]
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
                        almacen['checkingDate'].append(dia)
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

def get_hotel_info(driver, i):
    name = driver.find_element('css selector', 'div.a826ba81c4:nth-child({i}) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > h3:nth-child(1) > a:nth-child(1) > div:nth-child(1)'.format(i=i+1)).text
                                                #div.a826ba81c4:nth-child(8) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > h3:nth-child(1) > a:nth-child(1) > div:nth-child(1)
    try:
        previousPrice = driver.find_element('css selector', 'div.a826ba81c4:nth-child({i}) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > span:nth-child(2) > div:nth-child(1) > span:nth-child(1)'.format(i=i+1)).text
    except:
        previousPrice = np.nan
    currentPrice = driver.find_element('css selector', 'div.a826ba81c4:nth-child({i}) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > span:nth-child(2) > div:nth-child(1) > span:nth-child(1)'.format(i=i+1)).text
    rating = driver.find_element('css selector', 'div.a826ba81c4:nth-child({i}) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > a:nth-child(1) > span:nth-child(2) > span:nth-child(1)'.format(i=i+1)).text
    reviewNumber = driver.find_element('css selector', 'div.a826ba81c4:nth-child({i}) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > a:nth-child(1) > span:nth-child(2) > span:nth-child(2)'.format(i=i+1)).text
    image = driver.find_element('css selector', 'div.a826ba81c4:nth-child({i}) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > a:nth-child(1) > img:nth-child(1)'.format(i=i+1))
    image_src = image.get_attribute('src')
    print(name, previousPrice, currentPrice, rating, reviewNumber, image_src)
    return name, previousPrice, currentPrice, rating, reviewNumber, image_src

def get_hotel_page(driver,i):
    driver.find_element('css selector', 'div.a826ba81c4:nth-child({i}) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > a:nth-child(1) > img:nth-child(1)'.format(i=i+1)).click()
    original_window = driver.current_window_handle
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(7)
    url = driver.current_url
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')
    page = soup.text
    address = re.findall('(.*, \d{3,5} .*)', page.lower())
    driver.close()
    driver.switch_to.window(original_window)
    return url, page, address

def save_data(data, dia):
    with open(f'../data/dict_booking_{dia}.pickle', 'wb') as data_scrapeado:
        pickle.dump(data, data_scrapeado)

def seleniumFirefoxBooking3(url, dia, data):
    #with webdriver.Firefox() as driver:
    driver = webdriver.Firefox()
    driver.get(url)
    driver.maximize_window()
    driver.set_window_size(1920, 1080)
    driver.implicitly_wait(30)
    driver.find_element(By.CSS_SELECTOR, '#onetrust-accept-btn-handler').click()
    try:
        for page in range (1,40):
            for i in range(3, 50):
                try:
                    print('item:', i, 'page:', page)
                    driver.implicitly_wait(15)
                    name = driver.find_element(By.CSS_SELECTOR, f'div.a826ba81c4:nth-child({i}) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > h3:nth-child(1) > a:nth-child(1) > div:nth-child(1)').text
                                                #div.a826ba81c4:nth-child(8) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > h3:nth-child(1) > a:nth-child(1) > div:nth-child(1)
                                                #div.a826ba81c4:nth-child(46) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > h3:nth-child(1) > a:nth-child(1) > div:nth-child(1)
                    try:
                        previousPrice = driver.find_element(By.CSS_SELECTOR, f'div.a826ba81c4:nth-child({i}) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > span:nth-child(2) > div:nth-child(1) > span:nth-child(1)').text
                    except:
                        previousPrice = np.nan
                    currentPrice = driver.find_element(By.CSS_SELECTOR, f'div.a826ba81c4:nth-child({i}) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > span:nth-child(2) > div:nth-child(1) > span:nth-child(1)').text
                    rating = driver.find_element(By.CSS_SELECTOR, f'div.a826ba81c4:nth-child({i}) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > a:nth-child(1) > span:nth-child(2) > span:nth-child(1)').text
                    reviewNumber = driver.find_element(By.CSS_SELECTOR, f'div.a826ba81c4:nth-child({i}) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > a:nth-child(1) > span:nth-child(2) > span:nth-child(2)').text
                    image = driver.find_element(By.CSS_SELECTOR, f'div.a826ba81c4:nth-child({i}) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > a:nth-child(1) > img:nth-child(1)')
                    image_src = image.get_attribute('src')
                    print(name, previousPrice, currentPrice, rating, reviewNumber, image_src)
                    driver.find_element(By.CSS_SELECTOR, f'div.a826ba81c4:nth-child({i}) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > a:nth-child(1) > img:nth-child(1)').click()
                    driver.switch_to.window(driver.window_handles[1])
                    time.sleep(7)
                    url = driver.current_url
                    data['url'].append(url)
                    res = requests.get(url)
                    soup = BeautifulSoup(res.content, 'html.parser')
                    pagina = soup.text
                    data['pagina'].append(pagina)
                    data['address'].append(re.findall('(.*, \d{3,5} .*)', pagina.lower()))
                    print('dict:', len(data['url']), len(data['pagina']))
                    #url, page, address = get_hotel_page(driver)
                    #data['url'].append(url)
                    #data['pagina'].append(page)
                    #data['address'].append(address)
                    data['name'].append(name)
                    data['previousPrice'].append(previousPrice)
                    data['currentPrice'].append(currentPrice)
                    data['rating'].append(rating)
                    data['reviewNumber'].append(reviewNumber)
                    data['image'].append(image)
                    data['checkingDate'].append(dia)
                    print('dict:', len(data['url']), len(data['pagina']))
                    print('hasta aquí')
                    clear_output(wait=True)
                except:
                    pass
            driver.find_element('xpath', '/html/body/div[3]/div/div[4]/div[1]/div[1]/div[4]/div[2]/div[2]/div/div/div[4]/div[2]/nav/div/div[3]/button').click()
                                        #/html/body/div[3]/div/div[4]/div[1]/div[1]/div[4]/div[2]/div[2]/div/div/div[4]/div[2]/nav/div/div[3]/button
            print(len(data['name']), len(data['url']), len(data['currentPrice']), len(data['previousPrice']))
            driver.implicitly_wait(2)
            clear_output(wait=True)
            save_data(data, dia)
    except:
        print('me rompi')