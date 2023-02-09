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

def seleniumStart(url_original):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url_original)
    driver.maximize_window()
    driver.set_window_size(1920, 1080)
    driver.implicitly_wait(30)