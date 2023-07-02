import PySimpleGUI as psg

import spreadsheet_parser
import practice_fusion_scraper
import system13_entry

PARSE_SPREADSHEET_KEY: str = 'PARSE_SPREADSHEET'
GET_PATIENT_DATA_KEY: str = 'GET_PATIENT_DATA'
CLAIM_ENTRY_KEY: str = 'ENTER_CLAIM_INFO'

def create_layout() -> list[list[psg.Element]]:
    parse_spreadsheet_text = psg.Text(
        text='Clean and Parse Spreadsheet:',
    )
    parse_spreadsheet_button = psg.Button(
        button_text='Clean and Parse Spreadsheet',
        key=PARSE_SPREADSHEET_KEY
    )

    get_patient_data_text = psg.Text(
        text='Get Required Patient Data from Practice Fusion:',
    )
    get_patient_data_button = psg.Button(
        button_text='Get Patient Data',
        key=GET_PATIENT_DATA_KEY
    )

    enter_claim_info_text = psg.Text(
        text='Enter Claims Information'
    )
    enter_claim_info_button = psg.Button(
        button_text='Enter Claims Info',
        key=CLAIM_ENTRY_KEY,
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

    while True:
        event, _ = window.read()

        if event == psg.WIN_CLOSED:
            break

        if event == PARSE_SPREADSHEET_KEY:
            print('spreadsheet')
            # spreadsheet_parser.parse_spreadsheet()

        if event == GET_PATIENT_DATA_KEY:
            print('get data')
            # practice_fusion_scraper.get_all_patient_data()

        if event == CLAIM_ENTRY_KEY:
            print('enter_claims')
            # system13_entry.enter_all_patient_data()


if __name__ == '__main__':
    start_gui()
