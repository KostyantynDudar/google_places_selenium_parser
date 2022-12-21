# This Python file uses the following encoding: utf-8

import shutil

from open_txt_file_with_strings import get_dict
import xlwt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Firefox, ActionChains
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
import time
import string
import openpyxl
import os
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import urllib.request
import logging

# Finding the search box
def search_places(word):
    try:
        driver.switch_to.default_content()
        go_on = True
        searchbox = driver.find_element(by=By.XPATH,
                                        value='/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input')

        print("enter frase to search")

        searchbox.send_keys(word)
        searchbox.send_keys(Keys.ENTER)
        time.sleep(5)
    except Exception as e:
        print(e)
        print("def search_places(word):")

# return (main_page) driver.page_source
def main_page_sourse(driver):
    main_page = driver.page_source

def get_all_results_in_one_page(result_elements):
    list_of_dicts_of_results = []
    name_of_item_for_save_file = ""

    for i in result_elements:
        i.click()
        time.sleep(3)
        #  into res{} input parameters of place.
        res = {"title": "", "category": "",
               "adress": "", "phone": "",
               "day": "", "time1": "",
               "time2": "", "site": ""}

        name = ""
        try:
            name_of_item = driver.find_element(by=By.CSS_SELECTOR, value=".qrShPb > span:nth-child(1)")
            print("name = " + str(name_of_item.text))
            res.update({"title": str(name_of_item.text)})
            name_of_item_for_save_file = str(name_of_item.text)
        except Exception as e:
            print(e)

        #  category
        try:
            res.update({"category": str(category)})

        except Exception as e:
            print(e)

        adress = ""
        try:
            name_of_item = driver.find_element(by=By.CSS_SELECTOR, value=".LrzXr")
            print("adress = " + str(name_of_item.text))

            res.update({"adress": str(name_of_item.text)})
        except Exception as e:
            print(e)

        telephone_number = ""
        try:
            name_of_item = driver.find_element(by=By.CSS_SELECTOR, value="span.LrzXr:nth-child(1)")
            print("telephone_number = " + str(name_of_item.text))
            telephone_number = str(name_of_item.text)
            res.update({"phone": str(name_of_item.text)})
        except Exception as e:
            print(e)

        # open shedulle time table
        try:
            name_of_item = driver.find_element(by=By.CSS_SELECTOR, value=".JjSWRd")
            name_of_item.click()
            time.sleep(1)
        except Exception as e:
            print(e)
            res.update({"day": "пн-пт"})
            res.update({"time1": "10:00"})
            res.update({"time2": "18:00"})

        try:
            # ищем кнопку для закрытия окна расписания работы .fkbZ7b > div:nth-child(2)
            is_time_table_with_delyvery_table_close_window = driver.find_element(by=By.CSS_SELECTOR,
                                                                    value=".fkbZ7b > div:nth-child(2)")
            # print(f"is_time_table_with_delyvery_table is = {is_time_table_with_delyvery_table}")
            #name_of_item = driver.find_element(by=By.CSS_SELECTOR, value="#_6LmKYv2yKoWSrgSIzpW4Dg6 > div:nth-child(1) > div:nth-child(1) > table:nth-child(1)")
            #formated_time = time_formating(str(name_of_item.text))
            #res.update({"day": str(formated_time["day"])})
            #res.update({"time1": str(formated_time["open"])})
            #res.update({"time2": str(formated_time["close"])})
            is_time_table_with_delyvery_table_close_window.click()
        except Exception as e:
            res.update({"day": "пн-пт"})
            res.update({"time1": "10:00"})
            res.update({"time2": "18:00"})

        #  time_table
        try:
            name_of_item = driver.find_element(by=By.CSS_SELECTOR, value=".WgFkxc")
            print("table = " + str(name_of_item.text))
            name_of_item_str = str(name_of_item.text)


            # res.update({"time_table": str(name_of_item.text)})
            formated_time = time_formating(str(name_of_item.text))
            res.update({"day": str(formated_time["day"])})
            res.update({"time1": str(formated_time["open"])})
            res.update({"time2": str(formated_time["close"])})
            #  is_time_table_with_delyvery_table

        except Exception as e:
            print("TIME DEFOLT")
            print(e)
            res.update({"day": "пн-пт"})
            res.update({"time1": "10:00"})
            res.update({"time2": "18:00"})

        url_link = ""
        try:
            site_link_of_item = driver.find_element(by=By.CSS_SELECTOR,
                                                    value="a.dHS6jb:nth-child(1)")
            print("url link = " + site_link_of_item.get_attribute("href"))
            url_link = str(site_link_of_item.get_attribute("href"))
            if "google" in url_link:
                res.update({"site": ""})
            else:
                res.update({"site": url_link})
        except Exception as e:
            print("нет ссылки на сайт. ОШИБКА" + e)

        ''''#closed_temperary
        try:
            name_of_item = driver.find_element(by=By.CSS_SELECTOR, value=".b4cFMb")

            res.update({"closed_temperary": "Тимчасово зачинено"})
        except Exception as e:
            print(e)
'''

        #  photografies
        '''try:
            name_of_item = driver.find_element(by=By.CSS_SELECTOR, value=".Rbx14")
            classes = name_of_item.find_elements(by=By.CLASS_NAME, value="llfsGb")  #llfsGb
            url_str = ""
            for item in classes:
                print(item.get_attribute("href"))
                print("___")
                photo_url = item.find_element(by=By.CLASS_NAME, value="vwrQge")
                print(photo_url.get_attribute("href"))
                print("+++++")
                url_str = str(url_str) + " " + str(item.get_attribute("href"))
            res.update({"photos_hi_quolity": str(url_str)})
        except Exception as e:
            print("DONT FIND PHOTO WEBOBJECT " + str(e))'''

        #  photografies
        try:
            name_of_item = driver.find_element(by=By.CSS_SELECTOR, value=".Rbx14")
            classes = name_of_item.find_elements(by=By.CLASS_NAME, value="vwrQge")  # llfsGb
            url_str = ""
            count = 1

            for item in classes:

                url_str = url_str + str(item.get_attribute("style"))[23:-3]

                # save to url_data for all photos for one place

                url_data_for_all_items.append({(name_of_item_for_save_file + " " + str(count) + "_photo"): str(
                    item.get_attribute("style"))[23:-3]})
                #  save photo file
                imgURL = str(item.get_attribute("style"))[23:-3]
                name = str(name_of_item_for_save_file) + "_" + str(count) + "_photo.jpg"
                count = count + 1
            # res.update({"photos_low_quolity": url_str})
        except Exception as e:
            print("DONT FIND PHOTO WEBOBJECT " + str(e))

        #  category
        try:
            res.update({"category": str(category)})
        except Exception as e:
            print(e)

        #  is_closed
        try:
            name_of_item = driver.find_element(by=By.CSS_SELECTOR, value="#Shyhc")
            print("name = " + str(name_of_item.text))
            res = {"title": "закрыто", "category": "", "adress": "", "phone": "", "day": "", "time1": "", "time2": "",
                   "site": ""}
        except Exception as e:
            print(e)

        list_of_dicts_of_results.append(res)
        # print(list_of_dicts_of_results)
    return list_of_dicts_of_results

def next_page(driver):
    try:
        next_page_button = driver.find_element(by=By.CSS_SELECTOR, value="#pnnext")
        driver.get(str(next_page_button.get_attribute("href")))
        time.sleep(5)
    except Exception as e:
        print(e)

    #try:
     #   next_page_button.click()
      #  time.sleep(5)
    #except Exception as e:
     #   print(e)

def is_next_page(driver):
    try:
        next_page_button = driver.find_element(by=By.CSS_SELECTOR, value="#pnnext") #pnnext > span:nth-child(2) #pnprev > span:nth-child(2)
        return True
    except Exception as e:
        print(e)
        return False

def add_list_to_data(data, list):
    for res in list:
        print(res)
        data.append(res)
    return data

    pass

def time_formating(format):
    res = {"day": "пн-пт", "10:00": "", "close": "18:00"}
    list = format.split("\n")
    dict_res = {}

    def list_to_dict(list):
        for day in list:
            day_time = day.split(" ", 1)
            dict_res.update({day_time[0]: day_time[1]})

    list_to_dict(list)
    #print(dict_res)

    def split_time_to_open_and_slose(time_str):
        res = time_str.split("–")
        return res

    def get_reformating_date_and_time(dict_res):
        #  24:00
        for day in dict_res:
            current_time = dict_res[day]
            if current_time == "24 часа в сутки":
                res["day"] = "пн-вс"
                res["open"] = "24:00"
                res["close"] = "00:00"
                return res

        #  if seven days are same
        if dict_res['понедельник'] == dict_res['вторник'] \
                and dict_res['вторник'] == dict_res['среда'] \
                and dict_res['среда'] == dict_res['четверг'] \
                and dict_res['четверг'] == dict_res['пятница'] \
                and dict_res['пятница'] == dict_res['суббота'] \
                and dict_res['суббота'] == dict_res['воскресенье']:
            res["day"] = "пн-вс"
            res["open"] = split_time_to_open_and_slose(dict_res['понедельник'])[0]
            res["close"] = split_time_to_open_and_slose(dict_res['понедельник'])[1]
            return res
        #  if six days are same
        if dict_res['понедельник'] == dict_res['вторник'] \
                and dict_res['вторник'] == dict_res['среда'] \
                and dict_res['среда'] == dict_res['четверг'] \
                and dict_res['четверг'] == dict_res['пятница'] \
                and dict_res['пятница'] == dict_res['суббота']:
            res["day"] = "пн-сб"
            res["open"] = split_time_to_open_and_slose(dict_res['понедельник'])[0]
            res["close"] = split_time_to_open_and_slose(dict_res['понедельник'])[1]
            return res

        #  if five days are same
        if dict_res['понедельник'] == dict_res['вторник'] \
                and dict_res['вторник'] == dict_res['среда'] \
                and dict_res['среда'] == dict_res['четверг'] \
                and dict_res['четверг'] == dict_res['пятница']:
            res["day"] = "пн-пт"
            res["open"] = split_time_to_open_and_slose(dict_res['понедельник'])[0]
            res["close"] = split_time_to_open_and_slose(dict_res['понедельник'])[1]
            return res

        if dict_res['понедельник'] == "Закрыто" \
                and dict_res['вторник'] == dict_res['среда'] \
                and dict_res['среда'] == dict_res['четверг'] \
                and dict_res['четверг'] == dict_res['пятница'] \
                and dict_res['воскресенье'] == "Закрыто":
            res["day"] = "пн-сб"
            res["open"] = split_time_to_open_and_slose(dict_res['вторник'])[0]
            res["close"] = split_time_to_open_and_slose(dict_res['вторник'])[1]
            return res

    #  if all time are same
    return get_reformating_date_and_time(dict_res)


# save data for all plases. Input {date_for_one_keyword_all_pages} and str: search_name_to_find
def dict_to_exl(date_for_one_keyword_all_pages, search_name_to_find):
    df = pd.DataFrame(data=date_for_one_keyword_all_pages)
    df.to_excel(str(search_name_to_find) + ".xlsx", index=False)
    print("File created")
#  save urls for all photos. Input {} whis url and str: search_name_to_find
def diction_to_file(dict, search_name_to_find):
    book = xlwt.Workbook(encoding="utf-8")
    sheet1 = book.add_sheet("Python Sheet 1")

    count = 0
    for item in dict:
        sheet1.write(count, 0, list(item.keys())[0])
        sheet1.write(count, 1, item[list(item.keys())[0]])
        count = count + 1
    book.save(search_name_to_find + "_photos.xls")


def start_scrint_to_one_word(adress_to_find, word_to_find, category_):
    #  START
    global driver
    global url_data_for_all_items
    global adress
    global word
    global new_dir_path
    global category
    category = category_

    adress = adress_to_find
    word = word_to_find
    search_name_to_find = adress + " " + word  # name input google search
    #  make new directory
    url_data_for_all_items = []

    directory = str(search_name_to_find)

    parent_dir = "C:\\Users\\dubro\\PycharmProjects\\Google maps parser"
    path = os.path.join(parent_dir, directory)

    new_dir_path = parent_dir + "\\" + str(search_name_to_find) #  what????

    profile_path = r"C:\Users\dubro\AppData\Roaming\Mozilla\Firefox\Profiles\rf908hxj.default"
    options = Options()
    options.set_preference('profile', profile_path)
    service = Service(r'C:\Users\dubro\Downloads\geckodriver-v0.31.0-win64\geckodriver.exe')

    # driver get google.com
    go_on = True
    while go_on:
        try:
            # open browser window

            driver = webdriver.Firefox(service=service, options=options)
            wait = WebDriverWait(driver, 5)

            # Opening Google
            driver.get("https://www.google.com")
            time.sleep(3)
            main_page_html = main_page_sourse(driver)

            # input search keys and press Enter.
            search_places(search_name_to_find)

            #  search button "Еще компании"
            #link_to_results_page = driver.find_element(by=By.XPATH, value="/html/body/div[7]/div/div[10]/div[1]/div[2]/div/div/div/div/div/div[2]/div[1]/div[2]/g-more-link/a")
            link_to_results_page = driver.find_element(by=By.CSS_SELECTOR, value=".tiS4rf")
            print(link_to_results_page)
            print(link_to_results_page.get_attribute("href"))


            #link_to_results_page = driver.find_element(by=By.CSS_SELECTOR, value=".wUrVib")
            go_on = False
        except Exception as e:
            print(e)
            print("Не проходит где-то в гугле 352-370")
            go_on = False

    #  go to results page whit 20 items in page
    driver.get(link_to_results_page.get_attribute("href"))

    #  SEARCH ON EACH PAGE WITH 20 ITEMS
    date_for_one_keyword_all_pages = []
    go_on = True
    count = 1
    while go_on:
        result_elements = driver.find_elements(by=By.CSS_SELECTOR, value=".OSrXXb")  # find webelement on page with 20 elemenst in one page CSS_SELECTOR

        #  get list {} res from get_all_results_in_one_page
        list_of_results_element_one_page = get_all_results_in_one_page(result_elements[2:])
        add_list_to_data(date_for_one_keyword_all_pages,
                         list_of_results_element_one_page)  # data for all pages for one keyword
        print(date_for_one_keyword_all_pages)

        if is_next_page(driver):
            print(f'{is_next_page(driver)=}')
            next_page(driver)
            #print(list_of_results_element_one_page)  # []
        else:
            go_on = False

    #  create new folder
    os.mkdir(path)
    os.chdir(new_dir_path)
    #  save to exl file date all items Input {date_for_one_keyword_all_pages} and str: search_name_to_find
    dict_to_exl(date_for_one_keyword_all_pages, search_name_to_find)
    #  save urls nj file
    diction_to_file(url_data_for_all_items, search_name_to_find)


def multy_search(adress: str, keyowrd: str, category: str):
    flag = True
    while flag == True:
        try:
            start_scrint_to_one_word(adress, keyowrd, category)
            flag = False
        except Exception as e:
            print(e)
            flag = True


print("go!")
list_of_all_search_frases = get_dict()
print(list_of_all_search_frases)
for index in range(0, len(list_of_all_search_frases)):
    print(list_of_all_search_frases[index])
    print(list_of_all_search_frases[index]["adress"] + list_of_all_search_frases[index]["keyword"] + list_of_all_search_frases[index]["category"])
    multy_search(list_of_all_search_frases[index]["adress"],\
                 list_of_all_search_frases[index]["keyword"],\
                 list_of_all_search_frases[index]["category"])
#adress, keyowrd, category = "Полтава", "химчистки", "chemical_clining"
#  сделать химчистки. на 12 карточек. 12 хичисток и 2 прачечные.
#multy_search(adress, keyowrd, category)
