from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

import difflib
import datetime
import openpyxl
import PySimpleGUI as sg
import json
from time import sleep

from config import config


def practice_fusion_login(driver: webdriver.Chrome):
    """Logs into practice fusion

    driver: selenium webpage driver
    """
    username_element: WebElement = driver.find_element(By.ID, config['pf_username_field_id'])
    username_element.send_keys(config['pf_username'])
    password_element: WebElement = driver.find_element(By.ID, config['pf_password_field_id'])
    password_element.send_keys(config['pf_password'])
    login_button_element: WebElement = driver.find_element(By.ID, config['pf_login_button_id'])
    login_button_element.click()
    
    # allow new webpage to load
    sleep(1)

    # 2 factor authentication
    return two_factor_authentication(driver)


def two_factor_authentication(driver: webdriver.Chrome) -> bool:
    """Helps automate the 2fa process

    driver: selenium webpage driver
    return: if 2fa was successful
    """
    send_code_button: WebElement = driver.find_element(By.ID, config['pf_send_2fa_code_button_id'])
    send_code_button.click()
    code: str = sg.popup_get_text(message='Enter two factor authentication code:', keep_on_top=True)
    
    if code is None or code == '':
        return False

    enter_code_element: WebElement = driver.find_element(By.ID, config['pf_enter_code_field_id'])
    enter_code_element.send_keys(code)
    send_code_button: WebElement = driver.find_element(By.ID, config['pf_send_code_button_id'])
    send_code_button.click()

    return True


def go_to_charts(driver: webdriver.Chrome):
    sidebar_elements: list[WebElement] = driver.find_elements(By.CLASS_NAME, config['pf_sidebar_label_class'])
    charts_label: WebElement = [element for element in sidebar_elements 
                                if element.text == config['pf_charts_element_text']][0]
    charts_label.click()


def get_date_of_birth(patient_data, row: int) -> str:
    patient_dob: datetime.datetime = patient_data.cell(row, config['column_name_mapping']['DOB']).value
    patient_dob_str: str = patient_dob.strftime('%m/%d/%Y')

    return patient_dob_str

def enter_date_of_birth(driver: webdriver.Chrome, dob: str):
    patient_search_element: WebElement = driver.find_element(By.CSS_SELECTOR, config['pf_patient_search_css_select'])
    patient_search_element.send_keys(f'{dob}')
    sleep(.5)
    patient_search_element.send_keys(Keys.RETURN)
    sleep(1)


def get_patient_full_name(patient_data, row: int) -> str:
    patient_first_name: str = patient_data.cell(row_index, config['column_name_mapping']['FIRST NAME']).value
    patient_last_name: str = patient_data.cell(row_index, config['column_name_mapping']['LAST NAME']).value
    patient_full_name: str = f'{patient_first_name} {patient_last_name}'

    return patient_full_name


# TODO: error checking/report on patient names
def navigate_to_patient_info(driver: webdriver.Chrome, full_name: str) -> bool:
    search_patient_first_names: list[WebElement] = driver.find_elements(
        By.CSS_SELECTOR, config['pf_first_name_css_select'])
    search_patient_last_names: list[WebElement] = driver.find_elements(
        By.CSS_SELECTOR, config['pf_last_name_css_select'])
    full_name_element_mapping: dict = {}
    for first_name_ele, last_name_ele in zip(search_patient_first_names, search_patient_last_names):
        search_first_name: str = first_name_ele.text.lower()
        search_last_name: str = last_name_ele.text.lower()
        search_full_name: str = f'{search_first_name} {search_last_name}'
        full_name_element_mapping[search_full_name] = first_name_ele

    closest_match_name: str = difflib.get_close_matches(
        word=full_name,
        possibilities=full_name_element_mapping.keys())[0]
    closest_match_element: WebElement = full_name_element_mapping[closest_match_name]
    closest_match_element.click()
    sleep(1) # wait for the webpage to load

    return True


# TODO: turn sleeps into sophisticated waits
# https://selenium-python.readthedocs.io/waits.html#explicit-waits
if __name__ == '__main__':
    # read the cleaned patient data
    workbook = openpyxl.load_workbook(f'data/{config["cleaned_workbook_name"]}')
    patient_data = workbook[config['main_worksheet_name']]
    
    # loads the practice fusion webpage
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(config['pf_url'])
    practice_fusion_login(driver)
    sleep(3) # give time for webpage to load
    go_to_charts(driver)
    sleep(1) # give time for webpage to load

    for row_index in range(2, patient_data.max_row + 1):
        patient_dob: str = get_date_of_birth(patient_data, row_index)
        enter_date_of_birth(driver, patient_dob)
        
        patient_name: str = get_patient_full_name(patient_data, row_index)
        navigate_to_patient_info(driver, patient_name)

    #   select documents tab
    #   select signed documents
    #   use document type and date range (~3 days of procedure) to find documnet
    #   download procedure pdf
    #   convert pdf to image
    #   character recognition on the image
    #   split resulting string on new line (\n)
    #   for each line in the pdf
    #       search for "ID:", "Sex:", "Procedure Code:", "Diagnosis code"
    #       parse found lines for desired information
    #   
    #   add id, gender, procedure code, and diagnosis code to the pandas dataframe
    #
    #   select the profile tab
    #   grab the address card element
    #   get address info from the element (address line 1, address line 2, city, state, zip)
    #   add address info to the pandas datafram
    #
    # save the dataframe

    driver.close()