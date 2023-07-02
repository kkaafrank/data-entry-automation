import PySimpleGUI as psg

import spreadsheet_parser
import practice_fusion_scraper
import system13_entry
from config import config

def create_layout() -> list[list[psg.Element]]:
    parse_spreadsheet_text = psg.Text(
        text='Clean and Parse Spreadsheet:',
    )
    parse_spreadsheet_button = psg.Button(
        button_text='Clean and Parse Spreadsheet',
        key=config['parse_spreadsheet_key'],
    )

    get_patient_data_text = psg.Text(
        text='Get Required Patient Data from Practice Fusion:',
    )
    get_patient_data_button = psg.Button(
        button_text='Get Patient Data',
        key=config['get_patient_data_key'],
    )

    enter_claim_info_text = psg.Text(
        text='Enter Claims Information'
    )
    enter_claim_info_button = psg.Button(
        button_text='Enter Claims Info',
        key=config['claim_entry_key'],
    )

    layout = [
        [parse_spreadsheet_text],
        [parse_spreadsheet_button],
        [get_patient_data_text],
        [get_patient_data_button],
        [enter_claim_info_text],
        [enter_claim_info_button],
    ]
    return layout

def start_gui():
    layout = create_layout()
    window = psg.Window('Clams Entry Automation', layout=layout)

    parse_spreadsheet_key: str = config['parse_spreadsheet_key']
    get_patient_data_key: str = config['get_patient_data_key']
    enter_claims_data_key: str = config['claim_entry_key']

    while True:
        event, _ = window.read()

        if event == psg.WIN_CLOSED:
            break

        if event == parse_spreadsheet_key:
            spreadsheet_parser.parse_spreadsheet()

        if event == get_patient_data_key:
            practice_fusion_scraper.get_all_patient_data()

        if event == enter_claims_data_key:
            system13_entry.enter_all_patient_data()


if __name__ == '__main__':
    start_gui()
