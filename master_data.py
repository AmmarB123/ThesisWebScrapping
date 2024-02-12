import os
import openpyxl

import pandas as pd
'''
Used to create a master data file which stores all the extracted data
data: List
'''
def excel_data(data):
    new_data = data
    df = pd.DataFrame(new_data)
    #Checks if file name exists
    if os.path.isfile('masterdata.xlsx'):
        #Read
        reader = pd.read_excel('masterdata.xlsx')
        #Write
        writer = pd.ExcelWriter('masterdata.xlsx', engine='openpyxl', mode='a', if_sheet_exists="overlay")
        #Covert to excel and after the last item index
        df.to_excel(writer, index=False, header=False, startrow=len(reader) + 1)
        writer.close()
    else:
        #If file name does not exist make a new masterdata file
        writer = pd.ExcelWriter('masterdata.xlsx', engine='openpyxl')
        df.to_excel(writer, index=False, header=True, startrow=0)
        writer.close()
'''
Used to get data from the masterdata file and is used to extract it
input: string
reutrn boolean
'''
def get_exact_data(input):
    df = pd.read_excel('masterdata.xlsx')
    words = input.split(" ")

    # Filter the rows based on the condition that the 'description' column contains input

    # Generate a list of conditions based on the words in the input string
    conditions = [
        df['Title'].str.contains(word, case=False) | df['Description'].str.contains(word, case=False)
        for word in words
    ]

    # Combine the conditions using the & operator just like str concentnations
    combined_conditions = conditions[0]
    for item in conditions[1:]:
        combined_conditions &= item

    # Filter the rows based on the combined conditions
    filtered_df = df[combined_conditions]
    # If length of filter is greater than 0 then save otherwise there is no item
    if len(filtered_df) == 0:
        return False

    else:
        filtered_df.to_excel(f'filtered_data{input}.xlsx', index=False)
        return True

    # Print the filtered dataframe