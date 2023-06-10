from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from pdf2image import convert_from_path
from PIL import Image
import pytesseract

import difflib
import datetime
import openpyxl
import PySimpleGUI as sg
import json
import os
from time import sleep

from config import config
pytesseract.pytesseract.tesseract_cmd = config['tesseract_path']


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


# TODO: if 2fa code is wrong
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

    closest_matches: str = difflib.get_close_matches(
        word=full_name,
        possibilities=full_name_element_mapping.keys(),
        cutoff=0.75)
    if len(closest_matches) == 0:
        return False

    closest_match_element: WebElement = full_name_element_mapping[closest_matches[0]]
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


def get_patient_address(driver: webdriver.Chrome) -> tuple[str, str, str, str] | bool:
    try:
        address_line_1: str = driver.find_element(By.CSS_SELECTOR, config['pf_address1_css_select']).text
        address_line_2: str = driver.find_element(By.CSS_SELECTOR, config['pf_address2_css_select']).text
        city_state_zip: str = driver.find_element(By.CSS_SELECTOR, config['pf_address3_css_select']).text
    except:
        return False

    city_state_zip = city_state_zip.replace(',', '')
    address_3_parts = city_state_zip.split(' ')
    state = address_3_parts[-2]
    zip_code = address_3_parts[-1]
    city = ' '.join(address_3_parts[0:-2])

    return address_line_1, address_line_2, city, state, zip_code


def get_patient_sex(driver: webdriver.Chrome):
    age_and_sex_element: WebElement = driver.find_element(By.CSS_SELECTOR, config['pf_sex_css_select'])
    sex: str = age_and_sex_element.text[-1]

    return sex


def navigate_to_desired_document(driver: webdriver.Chrome, operation: str, operation_date: datetime.datetime) -> bool:
    documents_container: WebElement = driver.find_element(By.CSS_SELECTOR, config['pf_document_container_css_select'])
    documents: list[WebElement] = documents_container.find_elements(By.XPATH, config['pf_document_row_xpath'])
    document_found: bool = False

    for document in documents:
        document_information_containers: list[WebElement] = document.find_elements(By.XPATH, config['xpath_child_selector'])
        
        document_type: WebElement = document_information_containers[2]
        document_type_div: WebElement = document_type.find_element(By.XPATH, config['xpath_child_selector'])
        document_type_str: str = document_type_div.find_element(By.XPATH, config['xpath_child_selector']).text

        if operation.strip().lower() not in document_type_str.lower():
            continue

        document_date_str: WebElement = document.find_elements(By.XPATH, config['xpath_child_selector'])[5].text
        document_date: datetime.datetime = datetime.datetime.strptime(document_date_str, '%m/%d/%Y')
        end_date_range: datetime.datetime = operation_date + datetime.timedelta(days=10)

        if not (operation_date <= document_date <= end_date_range):
            continue

        document_link_container: WebElement = document_information_containers[1]
        document_link_div: WebElement = document_link_container.find_element(By.XPATH, config['xpath_child_selector'])
        document_link_element: WebElement = document_link_div.find_element(By.XPATH, config['xpath_child_selector'])
        document_link_element.click()
        document_found = True
        break

    sleep(3)
    return document_found


def download_document(driver: webdriver.Chrome, patient_name: str, date: datetime.datetime, operation_type: str) -> str:
    print_buttons_container: WebElement = driver.find_element(By.CSS_SELECTOR, config['pf_print_buttons_css_select'])
    download_button: WebElement = print_buttons_container.find_element(By.XPATH, config['pf_download_button_xpath'])
    download_button.click()

    patient_info_tabs_container: WebElement = driver.find_element(By.CSS_SELECTOR, config['pf_tab_list_css_select'])
    pdf_name_element: WebElement = patient_info_tabs_container.find_element(By.XPATH, config['pf_pdf_name_xpath'])
    pdf_name: str = pdf_name_element.text

    operation_type = operation_type.strip().lower()
    date_str: str = date.strftime('%Y-%m-%d')
    new_file_name: str = f'{date_str}_{patient_name}_{operation_type}.pdf'

    old_file_path: str = f'{config["pf_pdf_download_location"]}{pdf_name}'
    new_file_path: str = f'{config["pf_pdf_download_location"]}{new_file_name}'

    sleep(3)

    if not os.path.exists(new_file_path):
        os.rename(old_file_path, new_file_path)

    return new_file_path


def get_text_from_pdf(pdf_file_path: str) -> str:
    pdf_pages: list[Image.Image] = convert_from_path(pdf_file_path, 300)

    first_page: Image.Image = pdf_pages[0]
    first_page_text: str = pytesseract.image_to_string(first_page, lang='eng')

    return first_page_text


def parse_pdf_text(pdf_text: str) -> tuple[str, str, str]:
    pdf_text_by_line: list[str] = pdf_text.split('\n')

    id: str = ''
    procedure_code: str = ''
    diagnosis_code: str = ''
    for line in pdf_text_by_line:
        if line.startswith('ID:'):
            id_and_procedure: str = line.split(':')[1].strip()
            id = id_and_procedure.split(' ')[0]
        elif line.startswith('Procedure Code:'):
            proc_code_and_name: str = line.split(':')[1].strip()
            procedure_code = proc_code_and_name.split(' ')[0]
        elif line.startswith('Diagnosis code:'):
            diag_code_and_type: str = line.split(':')[1].strip()
            diagnosis_code = diag_code_and_type.split(' ')[0]

    return id, procedure_code, diagnosis_code


def close_patient_charts_tab(driver: webdriver.Chrome):
    try:
        potential_patient_list_containers: list[WebElement] = driver.find_elements(By.CLASS_NAME, config['pf_close_charts_container_class'])
        patient_list_container: WebElement
        for container in potential_patient_list_containers:
            if container.text.startswith('Patient lists'):
                patient_list_container: WebElement = container
                break

        patient_list_container = patient_list_container.find_element(By.XPATH, config['xpath_child_selector'])
        patient_chart_container: WebElement = patient_list_container.find_elements(By.XPATH, config['xpath_child_selector'])[1]
        patient_chart_container: WebElement = patient_chart_container.find_element(By.XPATH, config['xpath_child_selector'])
        close_charts_button: WebElement = patient_chart_container.find_elements(By.XPATH, config['xpath_child_selector'])[2]
        close_charts_button.click()

        sleep(3)
    except:
        pass

    try:
        potential_close_dob_filter_button: list[WebElement] = driver.find_elements(By.CSS_SELECTOR, config['pf_dob_close_css_select'])
        close_dob_filter_button: WebElement
        for button in potential_close_dob_filter_button:
            if button.accessible_name == '\uf139':
                close_dob_filter_button = button
                break

        close_dob_filter_button.click()

        sleep(1)
    except:
        pass

# TODO: randomly will open "quick view" menu, causes crashes
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
        'profile.default_content_settings.popups': False,
    }
    chrome_options.add_experimental_option('prefs', prefs)
    chrome_options.add_argument('log-level=3')
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    driver.get(config['pf_url'])
    practice_fusion_login(driver)
    sleep(3) # give time for webpage to load
    go_to_charts(driver)
    sleep(1) # give time for webpage to load

    for row_index in range(198, patient_data.max_row + 1):
        close_patient_charts_tab(driver)

        patient_dob: str = get_date_of_birth(patient_data, row_index)
        enter_date_of_birth(driver, patient_dob)
        
        patient_name: str = get_patient_full_name(patient_data, row_index)
        navigation_successful: bool = navigate_to_patient_info(driver, patient_name)
        if not navigation_successful:
            print(f'Unable to find patient: {patient_name} (excel row: {row_index})')
            continue

        navigate_to_profile_tab(driver)
        address_results = get_patient_address(driver)
        if address_results == False:
            print(f'Unable to find address for: {patient_name} (excel row: {row_index})')
            continue

        address_1, address_2, city, state, zip_code = address_results
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
        navigation_successful = navigate_to_desired_document(driver, operation_type, operation_date)
        if not navigation_successful:
            print(f'Unable to find {operation_type} document for {patient_name} on {operation_date.strftime("%m/%d")} (excel row: {row_index})')
            continue

        pdf_file_path: str = download_document(driver, patient_name, operation_date, operation_type)
        pdf_text: str = get_text_from_pdf(pdf_file_path)
        id, procedure_code, diagnosis_code = parse_pdf_text(pdf_text)

        patient_data.cell(row_index, config['column_name_mapping']["PROCEDURE ID"], id)
        patient_data.cell(row_index, config['column_name_mapping']["PROCEDURE CODE"], procedure_code)
        patient_data.cell(row_index, config['column_name_mapping']["DIAGNOSIS"], diagnosis_code)

        workbook.save(f'data/{config["cleaned_workbook_name"]}')

    driver.close()