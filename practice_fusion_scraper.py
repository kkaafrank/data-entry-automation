from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

import difflib
import pandas as pd
import PySimpleGUI as sg
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
    two_factor_authentication(driver)


def two_factor_authentication(driver: webdriver.Chrome):
    """Helps automate the 2fa process

    driver: selenium webpage driver
    """
    send_code_element: WebElement = driver.find_element(By.ID, config['pf_send_2fa_code_button_id'])
    # send_code_element.click()
    code: str = sg.popup_get_text(message='Enter two factor authentication code:')

    # TODO: WIP, error checking on empty string or wrong code


if __name__ == '__main__':
    # read the cleaned patient data with pandas
    
    # loads the practice fusion webpage
    driver = webdriver.Chrome()
    driver.get('https://static.practicefusion.com/apps/ehr/index.html#/login')
    practice_fusion_login(driver)
    # go to charts tab

    # for each row in the patient data
    #   query with DoB and name
    #   select patient
    #   report error when no patient is found
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