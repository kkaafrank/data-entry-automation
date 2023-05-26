import selenium
import pandas as pd
import difflib


if __name__ == '__main__':
    # read the cleaned patient data with pandas
    
    # navigate to practice fusion login
    # login
    # go to charts tab

    # for each row in the patient data
    #   query with DoB and name
    #   select patient
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
    # add empty ethnicity and race columns to the dataframe
    # save the dataframe

    print('')