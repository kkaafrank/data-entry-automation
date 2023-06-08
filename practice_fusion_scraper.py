from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

import difflib
import datetime
import openpyxl
import PySimpleGUI as sg
import json
import os
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
    patient_first_name: str = patient_data.cell(row, config['column_name_mapping']['FIRST NAME']).value
    patient_last_name: str = patient_data.cell(row, config['column_name_mapping']['LAST NAME']).value
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


def navigate_to_documents_tab(driver: webdriver.Chrome):
    document_tab_element: WebElement = driver.find_element(By.CSS_SELECTOR, config['pf_documents_tab_css_select'])
    document_tab_element.click()
    sleep(1)

    document_filter_dropdown: WebElement = driver.find_element(By.CSS_SELECTOR, config['pf_documents_filter_css_select'])
    document_filter_dropdown.click()
    sleep(.5)

    signed_documents_button: WebElement = driver.find_element(By.CSS_SELECTOR, config['pf_signed_documents_css_select'])
    signed_documents_button.click()
    sleep(1)

def navigate_to_profile_tab(driver: webdriver.Chrome):
    document_tab_element: WebElement = driver.find_element(By.CSS_SELECTOR, config['pf_profile_tab_css_select'])
    document_tab_element.click()
    sleep(1)


def get_patient_address(driver: webdriver.Chrome):
    address_line_1: str = driver.find_element(By.CSS_SELECTOR, config['pf_address1_css_select']).text
    address_line_2: str = driver.find_element(By.CSS_SELECTOR, config['pf_address2_css_select']).text
    city_state_zip: str = driver.find_element(By.CSS_SELECTOR, config['pf_address3_css_select']).text
    
    city_state_zip = city_state_zip.replace(',', '')
    city, state, zip_code = city_state_zip.split(' ')

    return address_line_1, address_line_2, city, state, zip_code


def get_patient_sex(driver: webdriver.Chrome):
    age_and_sex_element: WebElement = driver.find_element(By.CSS_SELECTOR, config['pf_sex_css_select'])
    sex: str = age_and_sex_element.text[-1]

    return sex


def navigate_to_desired_document(driver: webdriver.Chrome, operation: str, operation_date: datetime.datetime):
    documents: list[WebElement] = driver.find_elements(By.CSS_SELECTOR, config['pf_document_info_css_select'])

    for document in documents:
        document_type: WebElement = document.find_element(By.CSS_SELECTOR, config['pf_document_type_css_select'])
        document_type_str: str = document_type.find_element(By.XPATH, config['pf_document_type_xpath']).text
        
        if operation.strip().lower() not in document_type_str.lower():
            continue

        document_date_str: str = document.find_element(By.XPATH, config['pf_document_date_xpath']).text
        document_date: datetime.datetime = datetime.datetime.strptime(document_date_str, '%m/%d/%Y')
        end_date_range: datetime.datetime = operation_date + datetime.timedelta(days=5)

        if not (operation_date <= document_date <= end_date_range):
            continue

        document_link_element: WebElement = document.find_element(By.XPATH, config['pf_document_link_xpath'])
        document_link_element.click()
        break

    sleep(3)


def download_document(driver: webdriver.Chrome, patient_name: str, date: datetime.datetime, operation_type: str):
    print_buttons_container: WebElement = driver.find_element(By.CSS_SELECTOR, config['pf_print_buttons_css_select'])
    download_button: WebElement = print_buttons_container.find_element(By.XPATH, config['pf_download_button_xpath'])
    download_button.click()

    patient_info_tabs_container: WebElement = driver.find_element(By.CSS_SELECTOR, config['pf_tab_list_css_select'])
    pdf_name_element: WebElement = patient_info_tabs_container.find_element(By.XPATH, config['pf_pdf_name_xpath'])
    pdf_name: str = pdf_name_element.text

    operation_type = operation_type.strip().lower()
    date_str: str = date.strftime('%Y-%m-%d')
    new_file_name: str = f'{patient_name}_{date_str}_{operation_type}.pdf'

    old_file_path: str = f'{config["pf_pdf_download_location"]}{pdf_name}'
    new_file_path: str = f'{config["pf_pdf_download_location"]}{new_file_name}'

    sleep(3)

    os.rename(old_file_path, new_file_path)


# TODO: turn sleeps into sophisticated waits
# https://selenium-python.readthedocs.io/waits.html#explicit-waits
if __name__ == '__main__':
    # read the cleaned patient data
    workbook = openpyxl.load_workbook(f'data/{config["cleaned_workbook_name"]}')
    patient_data = workbook[config['main_worksheet_name']]
    
    # loads the practice fusion webpage
    chrome_options = webdriver.ChromeOptions()
    prefs = {
        'download.default_directory': config['pf_pdf_download_location'],
        'profile.default_content_settings.popups': True,
    }
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(options=chrome_options)
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

        navigate_to_profile_tab(driver)
        address_1, address_2, city, state, zip_code = get_patient_address(driver)
        patient_data.cell(row_index, config['column_name_mapping']["ADDRESS LINE 1"], address_1)
        patient_data.cell(row_index, config['column_name_mapping']["ADDRESS LINE 2"], address_2)
        patient_data.cell(row_index, config['column_name_mapping']["CITY"], city)
        patient_data.cell(row_index, config['column_name_mapping']["STATE"], state)
        patient_data.cell(row_index, config['column_name_mapping']["ZIP CODE"], zip_code)

        sex: str = get_patient_sex(driver)
        patient_data.cell(row_index, config['column_name_mapping']['SEX'], sex)

        navigate_to_documents_tab(driver)
        operation_date: datetime.datetime = patient_data.cell(row_index, config['column_name_mapping']['DATE']).value
        operation_type: str = patient_data.cell(row_index, config['column_name_mapping']['PROCEDURE']).value
        navigate_to_desired_document(driver, operation_type, operation_date)
        download_document(driver, patient_name, operation_date, operation_type)

    #   convert pdf to image
    #   character recognition on the image
    #   split resulting string on new line (\n)
    #   for each line in the pdf
    #       search for "ID:", "Procedure Code:", "Diagnosis code"
    #       parse found lines for desired information
    #   
    #   add id, procedure code, and diagnosis code to the excel sheet
        pass

    # save the dataframe

    driver.close()