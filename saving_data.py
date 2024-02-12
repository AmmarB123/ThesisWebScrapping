import pandas as pd
import os
'''
This class is used for saving my data
'''
'''
Save data has parameters 
data_ls: list
item_name: str
returns and excel file on the compiler
'''
def save_data(data_ls, item_name):
    # Check if the file already exists
    filename = f"{item_name}.xlsx"
    if os.path.isfile(filename):
        # If it exists, delete the old file
        os.remove(filename)

    # Create a DataFrame and save it to Excel
    scraped_data = pd.DataFrame(data_ls)
    scraped_data.to_excel(filename, index=True)
    print("done")


def save_data2(data, item_name):
    filename = f"{item_name}.xlsx"
    if os.path.isfile(filename):
        # If it exists, delete the old file
        os.remove(filename)
    df = pd.DataFrame(data,
                      columns=["Index", "Price", "Title", "Website", "Stock", "Rating", "Review", "Description",
                               "Color", "Size", "Link"])
    df.to_excel(filename, index=False)


def save_data3(data, item_name):
    filename = f"{item_name}.xlsx"
    if os.path.isfile(filename):
        # If it exists, delete the old file
        os.remove(filename)
    df = pd.DataFrame(data,
                      columns=["Index", "Price", "Title", "Website", "Stock", "Rating", "Review", "Description",
                               "Color", "Size", "Link"])
    print(df)
    df.to_excel(filename, index=False)
