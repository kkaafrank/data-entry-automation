# Description
A code repository to automate data entry into the system13 audit website

# Background
The goal of this repository is to completely automate the data entry into the system13 claims audit website. Currently, this is not possible with the data I have available to me. Inferences (manual work) need to be made regarding a patients ethnicity and race, and manual cleanup of the initial excel file is needed. This inference is done after the execution of the practice_fusion_scrapper.py and before system13_entry.py  

# Setup
1. Install [Python](https://www.python.org/downloads/) (version 3.10 or greater)
2. Install the packages in [this section](#requirements-outside-of-python-modules)
3. Add the `*/bin` directories for the installed packages to your [PATH Environment Variable](https://learn.microsoft.com/en-us/previous-versions/office/developer/sharepoint-2010/ee537574(v=office.14))
4. Run `python -m pip install -r requirements.txt`
5. Duplicate the ".env.example" file
6. Rename it to ".env"
7. Change the fields in the ".env" file labled "CHANGE ME" to the desired values  
    - For the "excel_folder_name" I recommend setting it to "data" because it is already in the .gitignore
    - Likewise, I recommend setting "pf_pdf_download_location" to "data\\patient_pdfs\\\\"

# Instructions
1. Edit the excel file to match the template columns and worksheet name
2. Rename the excel file to "procedure_schedule.xlsx"
3. Run `python .\spreadsheet_parser.py`
4. Wait for the "Done with excel cleanup" message
5. _Optional but recommended:_ Check the excel file for bad fields
6. Run `python .\practice_fusion_scraper.py`  
    - __Note:__ DO NOT close or minimize the browser window that is opened
7. Enter the two factor authentication code in the small blue popup
8. Wait for the "Done with Practice Fusion scraping" message
9. _Optional but recommended:_ Check the excel file for bad/empty fields
10. Fill in the "Ethnicity" and "Race" columns of the excel file using the numbers in the [enumerations section](#enumerations)
11. Run `python .\system13_entry.py`
    - __Note:__ DO NOT close or minimize the browser window that is opened
12. Wait for the "Done with System13 entry" message

# Requirements outside of Python modules
This automation codebase requires a couple packages outside of Python modules. Please download and install the following to run the code.

[Poppler](https://poppler.freedesktop.org/) for converting PDFs to images.

[Tesseract](https://tesseract-ocr.github.io/tessdoc/Installation.html) for OCR (recognizing text in images).

# Enumerations
## Sex Enumeration
F - Female  
M - Male  
U - Unknown  

## Ethnicity Enumeration
1 - Hispanic  
2 - Not Hispanic  

## Race Enumeration
1 - American Inidan/Eskimo/Aleut  
2 - Asian/Native Hawaiian/Pacific Islander  
3 - Black/African American  
4 - White  
5 - Other  

## Insurance Source Code Enumeration
12 - PPO  
16 - HMO  
BL - BCBS  
ZZ - Self-Pay  
