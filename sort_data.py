import pandas as pd
import os
#Used to sort prices
'''
This fuction is used to sort data and to covert prices to floating point data types and sorts the price high to low and low to high
text: string
data: list
return: two excel sheets
                data = {"Website": "Amazon",
                        "Title": descrpition,
                        "Price": price,
                        "Stock": instock,
                        "Rating": rating,
                        "Review": review,
                        "Description":des,
                        "Color": colors,
                        "Size": all_size,
                        "Link": link
                        }
'''
def sort_price(text,data):
    data_2 = []
    for key in data:
        # If price has - take the average of two numbers and converts to floating values
        if ' - ' in key[3]:
                try:
                    lower, upper = key[3].split(' - ')
                    average = (float(lower.replace('£', '').replace(',', '')) + float(upper.replace('£', '').replace(',', ''))) / 2
                    average_float = round(float(average), 2)
                    data_2.append((key[0], average_float, key[2], key[1],  key[4], key[5], key[6], key[7], key[8], key[9], key[10]))
                except:
                    data_2.append((key[0], -1, key[2], key[1], key[4], key[5], key[6], key[7], key[8], key[9], key[10]))
        elif 'to' in key[3]:
            # If price has to take the average of two numbers and converts to floating values
            try:
                lower, upper = key[3].split(' to ')

                average = (float(lower.replace('£', '').replace(',', '')) + float(upper.replace('£', '').replace(',', ''))) / 2
                average_float = round(float(average), 2)
                data_2.append((key[0],average_float, key[1], key[2],  key[4], key[5], key[6], key[7], key[8], key[9], key[10]))
            except:
                data_2.append((key[0], -1, key[1], key[2], key[4], key[5], key[6], key[7], key[8], key[9], key[10]))
        else:
            # Replaces pound sign with and comma with empty charcter
            remove_sign = key[3].replace('£', '').replace(',', '')
            try:
                remove_sign = float(remove_sign)
            except:
                # If there is not value return - 1
                remove_sign = float(-1.0)
            data_2.append((key[0], remove_sign, key[2], key[1], key[4], key[5], key[6], key[7], key[8], key[9], key[10]))
    #Sort low to high
    sorted_low_data = sorted(data_2, key=lambda x: x[1], reverse=False)
    #Sort high to low
    sorted_high_data = sorted(data_2, key=lambda x: x[1], reverse=True)

    df = pd.DataFrame(sorted_high_data, columns=["Index","Price", "Title", "Website", "Stock", "Rating", "Review", "Description", "Color", "Size", "Link"])
    df2 = pd.DataFrame(sorted_low_data, columns=["Index","Price", "Title", "Website", "Stock", "Rating", "Review", "Description","Color", "Size", "Link"])



    filename1 = f"{text}_high.xlsx"
    filename2 = f"{text}_low.xlsx"


    #Checks if file names exist
    if os.path.isfile(filename1):
        # If it exists, delete the old file
        os.remove(filename1)
    if os.path.isfile(filename2):
        # If it exists, delete the old file
        os.remove(filename2)



    #Save the Excel file
    df.to_excel(filename1, index=False)
    df2.to_excel(filename2, index=False)
    return sorted_high_data, sorted_low_data

# This is just used for data which changes constantly, which does not need to be saved each time. So for removing items from the cart or
# Adding items
def sort_price2(data):
    data_2 = []
    for key in data:
        #If price has - take the average of two numbers
        if ' - ' in key[3]:
                try:
                    lower, upper = key[3].split(' - ')
                    average = (float(lower.replace('£', '').replace(',', '')) + float(upper.replace('£', '').replace(',', ''))) / 2
                    average_float = round(float(average), 2)
                    data_2.append((key[0], average_float, key[2], key[1],  key[4], key[5], key[6], key[7], key[8], key[9], key[10]))
                except:
                    data_2.append((key[0], -1, key[2], key[1], key[4], key[5], key[6], key[7], key[8], key[9], key[10]))
        elif 'to' in key[3]:
            #If price has to take the average of two numbers
            try:
                lower, upper = key[3].split(' to ')

                average = (float(lower.replace('£', '').replace(',', '')) + float(upper.replace('£', '').replace(',', ''))) / 2
                average_float = round(float(average), 2)
                data_2.append((key[0],average_float, key[1], key[2],  key[4], key[5], key[6], key[7], key[8], key[9], key[10]))
            except:
                data_2.append((key[0], -1, key[1], key[2], key[4], key[5], key[6], key[7], key[8], key[9], key[10]))
        else:
            #Covert price
            remove_sign = key[3].replace('£', '').replace(',', '')
            try:
                remove_sign = float(remove_sign)
            except:
                remove_sign = float(-1.0)
            data_2.append((key[0], remove_sign, key[2], key[1], key[4], key[5], key[6], key[7], key[8], key[9], key[10]))
    #Sort low to high
    sorted_low_data = sorted(data_2, key=lambda x: x[1], reverse=False)
    #Sort high to low
    sorted_high_data = sorted(data_2, key=lambda x: x[1], reverse=True)

    #df = pd.DataFrame(sorted_high_data, columns=["Index","Price", "Title", "Website", "Stock", "Rating", "Review", "Description", "Color", "Size", "Link"])
    #df2 = pd.DataFrame(sorted_low_data, columns=["Index","Price", "Title", "Website", "Stock", "Rating", "Review", "Description","Color", "Size", "Link"])
    return  sorted_high_data, sorted_low_data
