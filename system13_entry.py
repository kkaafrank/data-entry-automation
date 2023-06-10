from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from datetime import datetime
from time import sleep
import openpyxl

from config import config
COLUMN_NAME_MAPPING: dict = config['column_name_mapping']

def system13_login(driver: webdriver.Chrome):
    """Logs into system13

    driver: selenium webpage driver
    """
    username_element: WebElement = driver.find_element(By.CSS_SELECTOR, config['s13_username_field_css_select'])
    username_element.send_keys(config['s13_username'])
    password_element: WebElement = driver.find_element(By.CSS_SELECTOR, config['s13_password_field_css_select'])
    password_element.send_keys(config['s13_password'])
    login_button_element: WebElement = driver.find_element(By.CSS_SELECTOR, config['s13_login_button_css_select'])
    login_button_element.click()
    
    # allow new webpage to load
    sleep(1)

    security_notice_button: WebElement = driver.find_element(By.CLASS_NAME, config['s13_security_notice_button_class'])
    security_notice_button.click()

    sleep(1)


def navigate_to_web_claim_entry(driver: webdriver.Chrome):
    dashboard_button_container: WebElement = driver.find_element(By.ID, config['s13_dashboard_container_id'])
    dashboard_buttons: list[WebElement] = dashboard_button_container.find_elements(By.XPATH, config['xpath_child_selector'])
    web_claim_entry_button = WebElement = dashboard_buttons[0]
    web_claim_entry_button.click()

    sleep(1)


def enter_in_search_box(driver: webdriver.Chrome, parent_element: WebElement,
                        value: str, extra_down_input: bool = False):
    parent_element.send_keys(Keys.ENTER)
    search_bar: WebElement = driver.find_element(By.CSS_SELECTOR, config['s13_search_dropdown_css_select'])
    search_bar.send_keys(value)

    sleep(.5)

    if extra_down_input:
        search_bar.send_keys(Keys.DOWN)
    search_bar.send_keys(Keys.ENTER)


def enter_patient_fields(driver: webdriver.Chrome, claim_information: dict):
    pcn_field: WebElement = driver.find_element(By.ID, config['s13_pcn_id'])
    pcn_field.send_keys(claim_information['id'])
    sleep(.5)

    mrn_field: WebElement = driver.find_element(By.ID, config['s13_mrn_id'])
    mrn_field.send_keys(claim_entry_information['id'])
    sleep(.5)

    first_name_field: WebElement = driver.find_element(By.ID, config['s13_first_name_id'])
    first_name_field.send_keys(claim_entry_information['first_name'])
    sleep(.5)

    last_name_field: WebElement = driver.find_element(By.ID, config['s13_last_name_id'])
    last_name_field.send_keys(claim_entry_information['last_name'])
    sleep(.5)

    address_1_field: WebElement = driver.find_element(By.ID, config['s13_address_1_id'])
    address_1_field.send_keys(claim_entry_information['address_1'])
    sleep(.5)

    if claim_entry_information['address_2'] is not None:
        address_2_field: WebElement = driver.find_element(By.ID, config['s13_address_2_id'])
        address_2_field.send_keys(claim_entry_information['address_2'])
    sleep(.5)

    city_field: WebElement = driver.find_element(By.ID, config['s13_city_id'])
    city_field.send_keys(claim_entry_information['city'])
    sleep(.5)

    state_field: WebElement = driver.find_element(By.ID, config['s13_state_id'])
    state_field.send_keys(claim_entry_information['state'])
    sleep(.5)

    zip_code_field: WebElement = driver.find_element(By.ID, config['s13_zip_id'])
    zip_code_field.send_keys(claim_entry_information['zip_code'])
    sleep(.5)

    # "united states" is a substring of "united states minor outlying islands"
    country_field: WebElement = driver.find_element(By.ID, config['s13_country_id'])
    enter_in_search_box(driver, country_field, config['country'], True)
    sleep(.5)

    ssn_field: WebElement = driver.find_element(By.ID, config['s13_ssn_id'])
    ssn_field.send_keys(config['ssn'])
    sleep(.5)

    # "male" is a substring of "female"
    sex_field: WebElement = driver.find_element(By.ID, config['s13_sex_id'])
    if claim_entry_information['sex'] == 'M':
        enter_in_search_box(driver, sex_field, claim_entry_information['sex'], True)
    else:
        enter_in_search_box(driver, sex_field, claim_entry_information['sex'], False)
    sleep(.5)

    ethnicity_field: WebElement = driver.find_element(By.ID, config['s13_ethnicity_id'])
    enter_in_search_box(driver, ethnicity_field, claim_entry_information['ethnicity'], False)
    sleep(.5)

    dob_field: WebElement = driver.find_element(By.ID, config['s13_dob_id'])
    dob_field.send_keys(claim_entry_information['dob'])
    sleep(.5)

    race_field: WebElement = driver.find_element(By.ID, config['s13_race_id'])
    enter_in_search_box(driver, race_field, claim_entry_information['race'], False)
    sleep(.5)

    bill_from_field: WebElement = driver.find_element(By.ID, config['s13_bill_from_id'])
    bill_from_field.send_keys(claim_entry_information['date'])
    sleep(.5)

    bill_to_field: WebElement = driver.find_element(By.ID, config['s13_bill_to_id'])
    sleep(.5)
    bill_to_field.send_keys(claim_entry_information['date'])

    claim_frequency_field: WebElement = driver.find_element(By.ID, config['s13_frequency_id'])
    enter_in_search_box(driver, claim_frequency_field, config['frequency_code'], False)
    sleep(.5)

    admission_type_field: WebElement = driver.find_element(By.ID, config['s13_admission_type_id'])
    enter_in_search_box(driver, admission_type_field, config['admission_type'], False)
    sleep(.5)

    origin_field: WebElement = driver.find_element(By.ID, config['s13_origin_id'])
    enter_in_search_box(driver, origin_field, config['origin_code'], False)
    sleep(.5)

    patient_status_field: WebElement = driver.find_element(By.ID, config['s13_patient_status_id'])
    enter_in_search_box(driver, patient_status_field, config['patient_status_code'], False)
    sleep(.5)

    facility_field: WebElement = driver.find_element(By.ID, config['s13_facility_id'])
    enter_in_search_box(driver, facility_field, config['facility_code'], False)


def enter_payers_fields(driver: webdriver.Chrome, claim_entry_information: dict):
    primary_payer_type_field: WebElement = driver.find_element(By.ID, config['s13_primary_payer_type_id'])
    enter_in_search_box(driver, primary_payer_type_field, claim_entry_information['insurance_type'], False)

    primary_payer_name_field: WebElement = driver.find_element(By.ID, config['s13_primary_payer_name_id'])
    primary_payer_name_field.send_keys(claim_entry_information['insurance_name'])


def enter_charges_fields(driver: webdriver.Chrome, claim_entry_information: dict):
    revenue_code_field: WebElement = driver.find_element(By.ID, config['s13_revenue_code_id'])
    revenue_code_field.send_keys(config['s13_revenue_code'])
    sleep(.5)

    proceedure_code_field: WebElement = driver.find_element(By.ID, config['s13_procedure_code_id'])
    enter_in_search_box(driver, proceedure_code_field, claim_entry_information['procedure_code'], False)
    sleep(.5)

    procedure_date_field: WebElement = driver.find_element(By.ID, config['s13_procedure_date_id'])
    procedure_date_field.send_keys(claim_entry_information['date'])
    sleep(.5)

    procedure_date_to_field: WebElement = driver.find_element(By.ID, config['s13_procedure_to_date_id'])
    sleep(.5)
    procedure_date_to_field.send_keys(claim_entry_information['date'])

    rate_field: WebElement = driver.find_element(By.ID, config['s13_unit_rate_id'])
    if claim_entry_information['procedure_code'] == config['egd_code']:
        rate_field.send_keys(config['s13_edg_charge'])
    else:
        rate_field.send_keys(config['s13_colon_charge'])
    sleep(.5)

    quantity_field: WebElement = driver.find_element(By.ID, config['s13_quantity_id'])
    quantity_field.send_keys(config['s13_charge_quantity'])
    sleep(.5)

    # "un" is a substring of "international unit"
    units_field: WebElement = driver.find_element(By.ID, config['s13_unit_id'])
    enter_in_search_box(driver, units_field, config['s13_charge_unit'], True)
    sleep(.5)

    qualifier_field: WebElement = driver.find_element(By.ID, config['s13_charge_qualifier_id'])
    enter_in_search_box(driver, qualifier_field, config['s13_qualifier_code'], False)


def enter_diagnoses_fields(driver: webdriver.Chrome, diagnosis_code: str):
    diagnosis_code = diagnosis_code.replace('.', '')

    principal_diagnosis_field: WebElement = driver.find_element(By.ID, config['s13_principal_diagnosis_id'])
    enter_in_search_box(driver, principal_diagnosis_field, diagnosis_code, False)
    sleep(.5)

    visit_reason_field: WebElement = driver.find_element(By.ID, config['s13_visit_reason_id'])
    enter_in_search_box(driver, visit_reason_field, diagnosis_code, False)


def enter_practitioners_fields(driver: webdriver.Chrome):
    practitioner_id_field: WebElement = driver.find_element(By.ID, config['s13_practitioner_id_id'])
    practitioner_id_field.send_keys(config['practitioner_id'])
    sleep(.5)

    practitioner_first_name_field: WebElement = driver.find_element(By.ID, config['s13_practitioner_first_name_id'])
    practitioner_first_name_field.send_keys(config['practitioner_first_name'])
    sleep(.5)

    practitioner_last_name_field: WebElement = driver.find_element(By.ID, config['s13_practitioner_last_name_id'])
    practitioner_last_name_field.send_keys(config['practitioner_last_name'])
    sleep(.5)

    practitioner_type_field: WebElement = driver.find_element(By.ID, config['s13_practitioner_type_id'])
    enter_in_search_box(driver, practitioner_type_field, config['practitioner_type'], False)


def navigate_to_next_section(driver: webdriver.Chrome):
    sleep(1)
    
    next_section_button: WebElement = driver.find_element(By.CSS_SELECTOR, config['s13_next_section_css_select'])
    next_section_button.click()

    sleep(1)


def submit_claim(driver: webdriver.Chrome):
    sleep(1)
    
    check_for_errors_button: WebElement = driver.find_element(By.CSS_SELECTOR, config['s13_check_for_errors_css_select'])
    check_for_errors_button.click()

    sleep(1)


def add_new_claim(driver: webdriver.Chrome):
    sleep(1)

    add_new_claim_button: WebElement = driver.find_element(By.CSS_SELECTOR, config['s13_new_claim_css_select'])
    add_new_claim_button.click()

    sleep(1)

if __name__ == '__main__':
    workbook = openpyxl.load_workbook(f'data/{config["cleaned_workbook_name"]}')
    patient_data = workbook[config['main_worksheet_name']]

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('log-level=3')
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    driver.get(config['s13_url'])
    system13_login(driver)
    navigate_to_web_claim_entry(driver)

    for row_index in range(16, patient_data.max_row + 1):
        date: datetime = patient_data.cell(row_index, COLUMN_NAME_MAPPING['DATE']).value
        dob: datetime = patient_data.cell(row_index, COLUMN_NAME_MAPPING['DOB']).value
        claim_entry_information: dict = {
            'date': date.strftime('%m%d%Y'),
            'first_name': patient_data.cell(row_index, COLUMN_NAME_MAPPING['FIRST NAME']).value,
            'last_name': patient_data.cell(row_index, COLUMN_NAME_MAPPING['LAST NAME']).value,
            'id': patient_data.cell(row_index, COLUMN_NAME_MAPPING['PROCEDURE ID']).value,
            'procedure_code': patient_data.cell(row_index, COLUMN_NAME_MAPPING['PROCEDURE CODE']).value,
            'dob': dob.strftime('%m%d%Y'),
            'insurance_type': patient_data.cell(row_index, COLUMN_NAME_MAPPING['INSURANCE TYPE']).value,
            'insurance_name': patient_data.cell(row_index, COLUMN_NAME_MAPPING['INSURANCE']).value,
            'address_1': patient_data.cell(row_index, COLUMN_NAME_MAPPING['ADDRESS LINE 1']).value,
            'address_2': patient_data.cell(row_index, COLUMN_NAME_MAPPING['ADDRESS LINE 2']).value,
            'city': patient_data.cell(row_index, COLUMN_NAME_MAPPING['CITY']).value,
            'state': patient_data.cell(row_index, COLUMN_NAME_MAPPING['STATE']).value,
            'zip_code': patient_data.cell(row_index, COLUMN_NAME_MAPPING['ZIP CODE']).value,
            'sex': patient_data.cell(row_index, COLUMN_NAME_MAPPING['SEX']).value,
            'ethnicity': patient_data.cell(row_index, COLUMN_NAME_MAPPING['ETHNICITY']).value,
            'race': patient_data.cell(row_index, COLUMN_NAME_MAPPING['RACE']).value,
            'diagnosis_code': patient_data.cell(row_index, COLUMN_NAME_MAPPING['DIAGNOSIS']).value
        }

        enter_patient_fields(driver, claim_entry_information)
        navigate_to_next_section(driver)

        enter_payers_fields(driver, claim_entry_information)
        navigate_to_next_section(driver)

        enter_charges_fields(driver, claim_entry_information)
        navigate_to_next_section(driver)

        enter_diagnoses_fields(driver, claim_entry_information['diagnosis_code'])
        navigate_to_next_section(driver)

        enter_practitioners_fields(driver)
        submit_claim(driver)

        add_new_claim(driver)

    driver.close()