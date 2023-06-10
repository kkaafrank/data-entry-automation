# Description
A code repository to automate data entry into the system13 audit website

# Goals
The goal of this repository is to completely automate the data entry into the system13 claims audit website  
Currently, this is not possible with the data I have available to me  
Inferences (manual work) need to be made regarding a patients ethnicity and race  
This inference is done after the execution of the practice_fusion_scrapper.py and before system13_entry.py  

# Requirements outside of Python modules
This automation codebase requires a couple packages outside of Python modules. Please download and install the following to run the code.

[Poppler](https://poppler.freedesktop.org/) for converting PDFs to images.

[Tesseract](https://tesseract-ocr.github.io/tessdoc/Installation.html) for OCR (converting images to text).

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
13 - POS
14 - EPO
16 - HMO
BL - BCBS
MA - Medicare Part A
MB - Medicare Part B
MC - Medicaid
ZZ - Self-Pay