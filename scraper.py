'''
This class is used for all the built in web scraping processes
'''

import requests
from bs4 import BeautifulSoup
#import pandas as pd
from nltk.stem import WordNetLemmatizer
#used to hold our data

import random
import time
#from colour import Color
from saving_data import save_data
from urllib.parse import urlparse
import urllib.robotparser
import master_data

import nltk
import spacy
# Load the small English model
nlp = spacy.load("en_core_web_sm")
import re as r


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}
wordnet_lemmatizer = WordNetLemmatizer()
headerx = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'}

import re

class scrape:

    def __init__(self):
        self.values = []
        self.count_items = 0
        self.endlinks = [".com/", ".co.uk/"]
        self.amazon_soup = 0

    '''
    Used to remove none alphanumeric values. Mainly used for ebay because it has
    emojis in the data name
    '''
    def check_reg(self, description):
        description = re.sub(r'[^\w\s]', '', description)
        description = description.strip()
        return description
    '''
    The main web scraping function of the code
    Consists of four websites: amazon, argos, john lewis, and ebay
    parameters:
    url: list
    searct_text: list
    activated_counter: boolean
    recommend_items: boolean
    headers: User-agent (dict)
    '''


    def extract_items(self, soup, url, search_text, activate_counter, recommend_items, header):

        front = False
        #r = requests.get(url, headers=header)
        #soup = BeautifulSoup(r.content, "lxml")
        #hypertext = soup.find_all('div', {"data-test":"component-grid-column"})
        #input_nam = soup.find("span", class_="Header_heading__main__PGKhL").text
        if "www.johnlewis.com" in url:
            hypertext = soup.find_all('div', {"data-test": "component-grid-column"})
            #print(len(hypertext))
            for hyper in hypertext:
                product_description = []
                self.countdown()
                price = False
                link = False
                descrpition = False
                review = False
                all_size = []
                unavailiable_sizes = []
                colors = []
                title = False
                count = 0
                review = "0"
                rating = "0"
                instock = "Out of Stock"

                try:
                    descrpition = hyper.find("span", class_="title_title__desc__ZCdyp title_title__desc--three-lines__VHz1t title_title__desc--branded__8SluU").text
                    print(descrpition)

                    try:
                        price = (hyper.find("span", {"data-test": "product-card-price-now"})).text
                        print(price)
                    except:
                        pass
                    try:
                        price = (hyper.find("em", {"data-test": "product-card-price-now"})).text[6:]
                        print(price)
                    except:
                        pass
                    try:
                        title = hyper.find("span", {"class": "title_title__brand__UX8j9 undefined"}).text
                        print(title, "brand brand")
                    except:
                        #All title_title__brand__UX8j9 undefined which cannot be found is john lewis anyday delcaring it is faster
                        title = "John Lewis Anyday"
                        pass
                    try:
                        # Used to find the link inside the url
                        link = "https://www.johnlewis.com" + (hyper.find("a", href=True))["href"]
                        # Loops thorugh the new link, if cannt be found in 5 seconds ignore and go to the next one
                        r = requests.get(link, headers=header, timeout=5)
                        soup1 = BeautifulSoup(r.content, "lxml")
                        try:
                            istock = soup1.find_all('button', {"type": "submit"})
                            instock = "In stock"
                            for stock in istock:
                                # Does not have a "out of stock" when scraping so we need to change
                                if "Notify me" in stock.text:
                                    instock = "Out of stock"
                        except:
                            instock = "In stock"
                            pass
                        try:
                            hypertext1 = soup1.find_all('button', {"data-cy": "size-selector-item"})
                            for hype1 in hypertext1:
                                # cant find instock  sizes
                                all_size.append(hype1.text)
                        except:
                            pass
                        try:
                            hypertext1 = soup1.find_all('button',
                                                        class_="Sizes_size-button__GWdtT Sizes_size-button--out-of-stock__VPThU")
                            for hype1 in hypertext1:
                                unavailiable_sizes.append(hype1.text)
                        except:
                            pass
                        try:
                            reviews = soup1.find('span', {"aria-hidden": "true"}).find_next().text
                            if "review" in reviews:
                                review = reviews

                        except:
                            pass
                        try:
                            reviews = soup1.find_all('button', {"type": "button"})
                            for re in reviews:
                                if "review" in re.text:
                                    review = re.text

                        except:
                            pass
                        try:
                            x1 = soup1.find("div", {"class": "DefaultTemplate_product-information__E3LSg"}).text

                            x1 = self.description_break_down(x1, product_description)
                        except:
                            pass
                        try:
                            x1 = soup1.find("div", {"data-cy": "product-info-section"}).text

                            x1 = self.description_break_down(x1, product_description)
                        except:
                            pass
                        try:
                            x1 = soup1.find("div", {"data-testid": "description:content"}).text

                            x1 = self.description_break_down(x1, product_description)
                        except:
                            pass
                        try:
                            x1 = soup1.find("details", {"data-testid": "accordion:specification"}).text
                            x1 = self.description_break_down(x1, product_description)
                        except:
                            pass
                        try:
                            x1 = soup1.find("details", {"data-testid": "accordion:specification"}).text
                            x1 = self.description_break_down(x1, product_description)
                        except:
                            pass
                        try:
                            x1 = soup1.find("details", {"data-testid": "accordion:description"}).text
                            x1 = self.description_break_down(x1, product_description)
                        except:
                            pass
                        try:
                            if len(x1) > 0:
                                x1 = list(set(x1))
                            else:
                                x1 = []
                        except:
                            pass


                        try:
                            rating = soup1.find('span', {"data-test":"rating"}).text[63:68]

                        except:
                            rating = "0"

                            pass
                    except:
                        print("no link")
                    try:
                        # Checking colors
                        input_name = hyper.find_all("a", title=True)
                        for colo in input_name:
                            colors.append(colo["title"])
                    except:
                        pass

                    try:
                        # Colors do not exist then replace the description and manually check each text
                        if len(colors) == 0:

                            new_sentence = descrpition.replace("/", " ").replace(",", " ")
                            new_sentence = new_sentence.split(" ")

                            for token in new_sentence:

                                if token == "" or token == ",":
                                    pass
                                elif self.color_checker(token) == True:

                                    colors.append(token)
                    except:
                        pass
                    try:
                        if len(all_size) == 0:
                            # Size do not exist then replace the description and manually check each text
                            break_des = descrpition.replace(",", " ")
                            break_des = break_des.split(" ")
                            for idx, word in enumerate(break_des):
                                if '"' in word:
                                    all_size = word
                                elif "inch" in word:
                                    all_size = break_des[idx-1]
                    except:
                        pass

                    data = {"Website": "John Lewis",
                            "Title": descrpition,
                            "Price": price,
                            "Stock": instock,
                            "Rating": rating,
                            "Review": review,
                            "Description": product_description,
                            "Color": colors,
                            "Size":all_size,
                            "Link":link
                            }
                    print(data)
                    # Adds data based on users input
                    if recommend_items == True:
                        print(descrpition)
                        for word in search_text:
                            if word.lower() in descrpition.lower():
                                count += 1
                        if count >= (len(search_text) - 1):
                            print("yes")
                            self.values.append(data)
                    else:
                        self.values.append(data)


                except:
                    pass
                # Counter
                if self.count_items == 70 and activate_counter == True:
                    return self.values
                self.count_items += 1
                print(self.count_items)
        elif "www.argos.co.uk" in url:
            hypertext = soup.find_all('a', {"data-test": "component-product-card-link"})
            for hyper in hypertext:
                product_description = []
                flag = False
                all_size = []
                # unavailiable_sizes = []
                count1 = 0
                count2 = 0
                colors = []
                self.countdown()
                title = "None"
                instock = "Out of stock"
                try:
                    # Loops thorugh the new link, if cannt be found in 5 seconds ignore and go to the next one
                    link = "https://www.argos.co.uk" + hyper["href"]
                    r = requests.get(link, headers=header)
                    soup2 = BeautifulSoup(r.content, "lxml")
                    try:

                        try:
                            price = soup2.find('h2', class_="Pricestyles__OfferPriceTitle-sc-1oev7i-4 hEuzyG").text

                        except:
                            price = soup2.find('span', {"itemprop": "priceCurrency"}).find_next().text

                        try:
                            title = soup2.find('span', {"data-test": "product-title"}).text

                        except:
                            pass
                        try:
                            rating = soup2.find('span', {"itemprop": "ratingValue"}).text

                        except:
                            rating = "0"
                            pass
                        try:
                            review = soup2.find('span', {"itemprop": "ratingCount"}).text
                            if len(rating) > 3:
                                rating = str(round(float(rating), 1))
                            else:
                                pass
                        except:
                            review = "0"
                            pass

                        try:
                            #stock = soup2.find('option', value=True).text
                            if soup2.find('option', value=True).text:
                                instock = "In stock"
                                print(instock)
                        except:
                            instock = "Out of stock"
                            pass
                        try:
                            sizes = soup2.find_all('button', {"data-test": "tiled-size-picker-tile-button"})
                            for size in sizes:
                                all_size.append(size.text)
                        except:
                            pass
                        try:
                            color = soup2.find_all('li', {"class":"ColorSwatchstyles__ColorSwatchListLi-jvpifx-4 bSUblL"})
                            #print(color)
                            for colo in color:
                                colors.append(colo.text)
                        except:
                            pass
                        # Usef for unavliable sizes
                        #try:
                            #div = soup2.find('div', {'class': 'product-description-content-text'})
                            #ul = div.find('ul')
                            #li_items = ul.find_all('li')
                            #descrption = '\n'.join([item.text.strip() for item in li_items])
                            #print(descrption)
                        #except:
                            #pass

                        try:
                            descrption = soup2.find('div', {"id":"pdp-description"}).text
                            des = self.description_break_down(descrption, product_description)
                        except:
                            descrption = "None"
                            des = []
                            pass
                        try:

                            if len(colors) == 0:

                                sentence = descrption.lower().split(" ")

                                # Used to check for colors in the descrption
                                for token in sentence:
                                    if self.color_checker(token) == True:
                                        colors.append(token)


                        except:
                            pass
                        try:
                            # Used to check for colors in the title if it is not in the description
                            if len(colors) == 0:
                                sentence = title.lower().split(" ")

                                for token in sentence:
                                    # If the token is an adjective and its lemma is a color
                                    if self.color_checker(token) == True:
                                        colors.append(token)

                        except:
                            pass

                        try:
                            # Used to check for sizes if size is not found
                            if len(all_size) == 0:
                                div = soup2.find('div', {'class': 'product-description-content-text'}).text.split(" ")
                                for idx, word in enumerate(div):
                                    if "inch" in word:
                                        all_size.append(div[idx - 1][-4:])
                                    elif "-inch" in word:
                                        all_size = word
                                        print(all_size)
                                    elif "size" in word:
                                        try:
                                            all_size = div[idx:idx+3]
                                        except:
                                            all_size = div[idx+1]
                        except:
                            pass

                        data = {"Website": "Argos",
                                "Title": title,
                                "Price": price,
                                "Stock": instock,
                                "Rating": rating,
                                "Review": review,
                                "Description": des,
                                "Color": colors,
                                "Size": all_size,
                                "Link": link
                                }
                        print(data)
                        try:
                            # If user wants the same input check title first
                            if recommend_items == True:
                                word_not_found = []

                                for words in search_text:
                                    if words.lower() in title.lower():
                                        count1 += 1
                                    else:
                                        word_not_found.append(words)
                                    if count1 >= len(search_text):
                                        self.values.append(data)

                                        flag = True
                            else:
                                self.values.append(data)

                        except:
                            pass
                        try:
                            # If user wants the same input after checking the title
                            if flag == False and recommend_items == True:
                                #print(descrption)
                                for words in word_not_found:
                                    if words.lower() in descrption.lower():
                                        count2 += 1
                                        #print(count, search_text)
                                    if count2 >= len(word_not_found):
                                        self.values.append(data)

                        except:
                            pass

                    except:
                        pass
                except:
                    link = False
                    pass
                if self.count_items == 70 and activate_counter == True:
                    return self.values
                self.count_items += 1
                print(self.count_items)
        elif "www.ebay.co.uk" in url:
            title = "None"

            hypertext = soup.find_all('div', {"class": "s-item__wrapper clearfix"})
            #print(hypertext)
            # unavailiable_sizes = []

            print(recommend_items, "ssaaaaaaaaaaaaaaaassax")
            for hyper in hypertext:
                product_description = []
                count = 0
                all_size = []
                colors = []
                flag = False
                count1 = 0
                count2 = 0
                self.countdown()
                try:
                    price = hyper.find('span', class_="s-item__price").text
                    #print(price)
                except:
                    price = "None"
                    pass
                try:
                    # Used to check for the new link
                    link = hyper.find("a", href=True)["href"]

                    r = requests.get(link, headers=header, timeout=5)
                    soup2 = BeautifulSoup(r.content, "lxml")
                    try:
                        item_label = soup2.find_all('span', {"class": "ux-textspans"})
                        for index,item in enumerate(item_label):
                            if "Brand:" in item.text:
                                title = item_label[index+1].text

                    except:
                        pass

                    try:
                        title = soup2.find('h1', {"class": "x-item-title__mainTitle"}).find_next().text
                        title = self.check_reg(title)
                        print(title)

                    except:
                        title = "None"
                        pass
                    try:
                        instock = soup2.find('span', {"itemprop": "availability"}).get("content")
                        if "InStock" in instock:
                            instock = "In stock"
                        else:
                            instock = "Out of stock"
                    except:
                        instock = "Out of stock"
                        pass
                    try:
                        # Since ebay has different number boxes for color, and size we need to search for them manually. This is used to check
                        # For items in the boxes
                        sizes = soup2.find('select', {'id': 'x-msku__select-box-1000'})
                        question = sizes.get("aria-label")

                        if "Colour" in question or "Color" in question or "Pattern" in question:
                            color_select = soup2.find('select', {'aria-label': question})
                            colors = [option.text.strip() for option in color_select.find_all('option')][1:]
                            print(colors)
                        elif "Size" in question or "Waist" in question or "Measurement" in question:
                            size_select = soup2.find('select', {'aria-label': question})
                            all_size = [option.text.strip() for option in size_select.find_all('option')][1:]
                            print(all_size)

                    except:
                        pass
                    try:
                        # Since ebay has different number boxes for color, and size we need to search for them manually. This is used to check
                        # For items in the boxes
                        sizes = soup2.find('select', {'id': 'x-msku__select-box-1001'})
                        question = sizes.get("aria-label")

                        if "Colour" in question or "Color" in question or "Pattern" in question:
                            color_select = soup2.find('select', {'aria-label': question})
                            colors = [option.text.strip() for option in color_select.find_all('option')][1:]
                            print(colors)
                        elif "Size" in question or "Waist" in question or "Measurement" in question:
                            size_select = soup2.find('select', {'aria-label': question})
                            all_size = [option.text.strip() for option in size_select.find_all('option')][1:]
                            print(all_size)

                    except:
                        pass
                    try:
                        descrpition = soup2.find('div', {"class": "ux-layout-section__item ux-layout-section__item--table-view"}).text
                        des = self.description_break_down(descrpition, product_description)

                    except:
                        descrpition = "None"
                        des = []
                        pass
                    try:
                        # Since ebay has different number boxes for color, and size we need to search for them manually. This is used to check
                        # For items in the boxes
                        sizes = soup2.find('select', {'id': 'x-msku__select-box-1002'})
                        question = sizes.get("aria-label")

                        if "Colour" in question or "Color" in question or "Pattern" in question:
                            color_select = soup2.find('select', {'aria-label': question})
                            colors = [option.text.strip() for option in color_select.find_all('option')][1:]
                            print(colors)
                        elif "Size" in question or "Waist" in question or "Measurement" in question:
                            size_select = soup2.find('select', {'aria-label': question})
                            all_size = [option.text.strip() for option in size_select.find_all('option')][1:]
                            print(all_size)

                    except:
                        pass

                    try:
                        # Auctions do not display colors so we check if manually
                        if len(colors) == 0:
                            item_label = soup2.find_all('span', {"class": "ux-textspans"})
                            for index,item in enumerate(item_label):
                                if "Colour:" in item.text or "Color" in item.text or "Pattern" in item.text:
                                    colors = item_label[index+1].text
                                    print(colors)
                                    break
                    except:
                        pass
                    try:
                        # Auctions do not display sizes so we check if manually
                        if len(all_size) == 0:

                            item_label = soup2.find_all('span', {"class": "ux-textspans"})
                            for index,item in enumerate(item_label):
                                if "Size:" in item_label[index].text or "Waist" in item.text or "Measurement" in item.text:
                                    all_size = item_label[index+1].text
                                    print(all_size)
                                    break
                    except:
                        pass
                    try:
                        rating = soup2.find('a', {'id': 'review-ratings-cntr'})
                        rating = rating.get("aria-label")
                        rating = rating.split()
                        review = rating[9]
                        rating = rating[0]
                        print(rating, review)
                    except:
                        rating = '0'
                        review = "0"
                        pass
                    # not ava sizes
                    #try:
                        #descrpition = []
                        #des = soup2.find('div', {"class":"ux-layout-section__item ux-layout-section__item--table-view"})
                        #de = des.find_all('span', {"class":"ux-textspans"})
                        #for d in range(len(de)):
                            #if d % 2:
                                #continue
                            #else:
                                #descrpition.append(de[d].text + " " + de[d+1].text)
                    #except:
                        #pass
                    data = {"Website": "Ebay",
                            "Title": title,
                            "Price": price,
                            "Stock": instock,
                            "Rating": rating,
                            "Review": review,
                            "Description": des,
                            "Color": colors,
                            "Size":all_size,
                            "Link":link
                            }
                    print(data)
                    try:
                        # If user wants the same input check title first
                        if recommend_items == True:

                            #print(title)
                            words_not_found = []
                            for words in search_text:
                                if words.lower() in descrpition.lower():
                                    count1 += 1
                                    # print(count, search_text)
                                else:
                                    words_not_found.append(words)
                                if count1 >= len(search_text):
                                    self.values.append(data)

                                    #print(data)
                                    flag = True
                        else:
                            self.values.append(data)

                    except:
                        pass
                    try:
                        # If user wants the same input after checking the title
                        if flag == False and recommend_items == 1:

                            for words in words_not_found:
                                if words.lower() in descrpition.lower():
                                    count2 += 1
                                    # print(count, search_text)
                                if count2 >= len(words_not_found):
                                    self.values.append(data)

                    except:
                        pass
                except:

                    pass
                if self.count_items == 70 and activate_counter == True:
                    return self.values
                self.count_items += 1
                print(self.count_items)

        elif "www.amazon.co.uk" in url:

            print("enter")
            print(soup)
            hypertext = soup.find_all('div', {'data-component-type': "s-search-result"})
            print(hypertext)
            for hyper in hypertext:
                product_description = []
                count = 0
                title = "None"
                all_size = []
                colors = []
                descrpition = []
                link = 'https://www.amazon.co.uk/' + hyper.h2.a.get('href')
                self.countdown()
                flag = False
                count1 = 0
                count2 = 0

                try:
                    # Used to get the link inside the html code for the specfic item
                    r = requests.get(link, headers=header, timeout=5)
                    soup2 = BeautifulSoup(r.content, "lxml")
                    try:
                        title = soup2.find('a', {'id': "bylineInfo"}).text[9:]
                        title = title.replace("Store", "").strip()
                    except:
                        pass
                    try:
                        title = soup2.find('span', {'class': "a-size-base po-break-word"}).text
                    except:
                        pass
                    try:
                        price = soup2.find('span', class_='a-offscreen').text
                        print(price)
                    except:
                        price = "None"
                    try:
                        d2 = soup2.find('div', {'id': "centerCol"}).text
                        des = self.description_break_down(d2, product_description)
                    except:
                        des = []
                        d2 = 'None'
                    try:
                        descrpition = soup2.find('span', {'id': "productTitle"}).text.strip()
                        print(descrpition)
                    except:
                        descrpition = "None"
                        pass
                    try:
                        rating = soup2.find('span', {'class': "a-icon-alt"}).text
                        if "Previous" in rating:
                            rating = "0"
                        else:
                            rating = rating[:3]
                            print(rating)
                    except:
                        rating = "0"
                        pass
                    try:
                        review = soup2.find('span', {'id': "acrCustomerReviewText"}).text
                        review = review.split(" ")[0]
                        print(review)
                    except:
                        review = "0"
                        pass
                    try:
                        flag= True
                        count = 0
                        while flag:
                            value = soup2.find("li", {"id": f"color_name_{count}"}).get("title")
                            if len(value)> 0:
                                count += 1
                                colors.append(value[16:])
                                print(colors)
                            else:
                                flag = False
                    except:
                        pass
                    try:
                        # For sizes add size [2:] into excel
                        options = soup2.find_all("option", {"data-a-html-content": True})
                        for option in options:
                            size = option.get("data-a-html-content")
                            all_size.append(size)
                            print(all_size)
                    except:
                        pass
                    try:
                        instock = soup2.find("div", {"id": "availability"}).find_next().text.strip()
                    except:
                        instock = "Select size for stock"
                        pass
                    try:
                        # Checks if size is in the text because the html elements are different
                        if len(all_size) == 0:
                            word = []
                            selection = soup2.find("table", {"class": "a-normal a-spacing-micro"}).text
                            selection = selection.strip("       ").lower()
                            selection = selection.split(" ")
                            for words in selection:
                                if words == '':
                                    pass
                                else:
                                    word.append(words)
                            for idx, selected_word in enumerate(word):
                                if "size" in selected_word:
                                    all_size = word[idx+1]
                                    print(all_size)
                                    break
                    except:
                        pass
                    try:
                        # Checks if color is in the text because the html elements are different
                        if len(colors) == 0:
                            word = []
                            selection = soup2.find("table", {"class": "a-normal a-spacing-micro"}).text
                            selection = selection.strip("       ").lower()
                            selection = selection.split(" ")
                            for words in selection:
                                if words == '':
                                    pass
                                else:
                                    word.append(words)
                            for idx, selected_word in enumerate(word):
                                if "color" in selected_word or "colour" in selected_word:
                                    colors = word[idx+1]
                                    print(colors)
                                    break
                    except:
                        pass
                    try:
                        # Checks for color
                        if len(colors) == 0:
                            color_div = soup2.find('div', {'id': 'variation_color_name'})
                            if color_div:
                                color_spans = color_div.find_all('span', {'class': 'selection'})
                                colors = [span.text.strip() for span in color_spans]
                                print(colors)
                    except:
                        pass
                    try:
                        # Checks for sizes
                        if len(all_size) == 0:
                            size_div = soup2.find('div', {'id': 'variation_size_name'})
                            if size_div:
                                size_spans = size_div.find_all('span', {'class': 'selection'})
                                all_size = [span.text.strip() for span in size_spans]
                                print(all_size)
                    except:
                        pass
                    # If price is not extracted for the normal area then check for different tags
                    if "£" not in price:
                        try:
                            price = soup2.find('span', {'class': 'a-color-price a-text-bold'}).text

                            if "stock" in price or "unavailable" in price:
                                price = "Price is not displayed"
                            else:
                                try:
                                    price = soup2.find('span', {'class': 'a-size-medium a-color-price'}).text

                                except:
                                    pass
                                try:

                                    price = soup2.find('span', {
                                        'class': 'a-size-base a-color-price offer-price a-text-normal'}).text

                                except:
                                    pass
                                try:
                                    price = soup2.find('span', {
                                        'class': 'a-size-medium a-color-price'}).text
                                except:
                                    pass
                        except:
                            pass
                    # Price cannot be extracted or not displayed
                    if "Page" in price or "%" in price:
                        price = "Price is not displayed"
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
                    print(data)

                    # Used to check input is the same as description
                    try:
                        # If user wants the same input check title first
                        if recommend_items == 1:


                            for words in search_text:
                                if words.lower() in descrpition.lower():
                                    count1 += 1

                                if count1 >= len(search_text):
                                    self.values.append(data)


                                    flag = True
                        else:
                            self.values.append(data)

                    except:
                        pass
                    try:
                        # If user wants the same input after checking the title
                        if flag == False and recommend_items == 1:
                            for words in search_text:
                                if words.lower() in d2.lower():
                                    count2 += 1

                                if count2 >= len(search_text):
                                    self.values.append(data)

                    except:
                        pass
                except:
                    pass
                if self.count_items == 70 and activate_counter == True:
                    return self.values
                self.count_items += 1
                print(self.count_items)




        #print(len(values))
        return self.values

    '''
    Used to check if the link has a product on the page
    url: list
    soup: list
    return boolean
    '''
    def check_url_has_products(self, url, soup):
        condition = False
        if "www.johnlewis.com" in url:
            try:
                product = soup.find_all("span", class_="Header_heading__main__PGKhL")
                if "couldn't find any results for" not in product:
                    print("True")
                    condition = True
            except:
                pass
        elif "https://www.argos.co.uk/" in url:
            try:
                results = soup.find_all("h1", {"data-test":"no-results-suggestions-heading"})
                if len(results) == 0:
                    condition = True
            except:
                pass
        elif "www.ebay.co.uk" in url:
            try:
                product = soup.find("h3", class_="srp-save-null-search__heading").text
                if "No exact matches found" in product:
                    condition = False
            except:
                condition = True
                pass
        elif "www.amazon.co.uk" in url:
            try:

                #product = soup.find("span", class_="a-size-medium a-color-base").text
                product = soup.find("span", class_="a-size-medium a-color-base").text
                print(product, "check url has product")
                if "No results for " in product:
                    condition = False
                else:
                    condition = True
            except:
                condition = True
                pass

        return condition
    '''
    Used to break down the urls
    input url: list
    return: list
    '''
    def get_url_end(self, url):
        new_url = ""
        for endlink in self.endlinks:
            if endlink in url:
                #creating a new link with added search
                new_url = url.split(endlink)
                new_url = new_url[0]+endlink
        return new_url


    '''
    Count down acts as a sechdular, makes sure we do not over send traffic on a server
    '''
    def countdown(self):
        timer = [2, 3]
        t = random.choice(timer)
        while t:
            mins, secs = divmod(t, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            print(timer, end="\r")
            time.sleep(1)
            t -= 1

        return True


    '''
    Used to get the pages for single search
    base_url: list
    soup: list
    text: string
    '''
    def get_pages(self, base_url, soup, text):
        count = 0
        page_links = [base_url]
        new_url = self.get_url_end(base_url)
        #print(new_url, "xxxxx")
        length = 0
        if "https://overclockedstore.com/" in new_url:
            hypertext = soup.find_all('div', id='tt-pageContent')
            for hyper in hypertext:
                for h1 in hyper.find_all("div", class_="tt-pagination"):
                        for page in h1.find_all("a", title=True):
                            page_links.append(new_url+page["href"])
        elif "www.johnlewis.com" in new_url:
            try:
                input_name = soup.find_all("a", class_="Pagination_c-pagination__btn__gaTFF")
                length = len(input_name)
            except:
                pass
            if length > 0:
                list1 = []
                for number in input_name:
                    count +=1
                    list1.append(int(number["href"].split("page=")[-1]))
                    max_num = max(list1)
                    #Additional check because page has hidden data
                    if count == len(input_name)/2:
                        page_links.clear()
                        for i in range(1, max_num + 1):
                            page_links.append(f'{new_url}search?search-term={text}&page={i}&imageId=&chunk=8')
                        break
            else:
                page_links[0] = f'{new_url}search?search-term={text}&chunk=8'
        elif "https://www.argos.co.uk/" in new_url:
            try:
                page_category = soup.find_all('a',  class_='Paginationstyles__PageLink-sc-1temk9l-1 kRMYil xs-hidden sm-row')
                for category in page_category:
                    category = category["href"]
                try:
                    pages = soup.find("span", {"data-test":"component-pagination-numbers"}).text.split(" ")[-1]
                    #Checking if there is more than one page
                    if int(pages) > 1:
                        page_links.clear()
                        for i in range(1, int(pages) + 1):
                            # Meging category because certain links has a product ID
                            page_links.append(f'{new_url[:-1]}{category}opt/page:{i}/')

                except:
                    pass
            except:
                pass
        elif "https://www.ebay.co.uk/" in new_url:
            try:
                page = soup.find_all("a", class_="pagination__item")
                for p in page:
                    page_links.append(f'https://www.ebay.co.uk/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313&_nkw={text}&_sacat=0&rt=nc&_pgn={p.text}')

            except:
                pass
        elif "www.amazon.co.uk" in new_url:
            print("amazon")
            number = 0
            try:
                pages = soup.find_all("span", {"aria-disabled":"true"})
                for page in pages:
                    number = page.text
                    #for i in range(int(page.text)):
                        #print(i)
                for i in range(2, int(number) + 1):
                    page_links.append(f'https://www.amazon.co.uk/s?k={text}&page={i}')
            except:
                pass


        print(page_links)
        return page_links
    '''
    Used to add the links into the url
    urls: list
    search_text: list
    return list of new links
    '''
    def get_search_string(self, urls, search_text):
        new_links = []
        new_link = ""
        for link in urls:
            link_search = ""
            if "https://www.johnlewis.com/search?search-term=" in link:
                for word in search_text:
                    #print(word)
                    link_search += word + "+"
                #print(link_search)
                new_link = "https://www.johnlewis.com/search?search-term="+link_search
                new_links.append(new_link)
            elif "https://www.argos.co.uk/search/" in link:
                for word in search_text:
                    link_search += word + "-"
                new_link = "https://www.argos.co.uk/search/"+link_search
                new_links.append(new_link)
            elif "ebay" in link:
                for word in search_text:
                    link_search += word + "+"
                new_link = f"https://www.ebay.co.uk/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313&_nkw={link_search}&_sacat=0"
                #https://www.ebay.co.uk/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=fdgjdfjsdjksd&_sacat=0&LH_TitleDesc=0&_odkw=iphone+14&_osacat=0
                new_links.append(new_link)
            elif "www.amazon.co.uk" in link:
                for word in search_text:
                    link_search += word + "+"
                new_link = f'https://www.amazon.co.uk/s?k={link_search}'
                new_links.append(new_link)
        return new_links

    '''
    This function is used to covert single website link to contain the product url link
    search_text: list
    link: string
    return list
    '''
    def get_one_search_string(self, search_text, link):
        new_links = []
        #new_link = ""
        link_search = ""
        if "https://www.johnlewis.com/search?search-term=" in link:
            for word in search_text:
                #print(word)
                link_search += word + "+"
            #print(link_search)
            new_link = "https://www.johnlewis.com/search?search-term="+link_search
            new_links.append(new_link)
        elif "https://www.argos.co.uk/search/" in link:
            for word in search_text:
                link_search += word + "-"
            new_link = "https://www.argos.co.uk/search/"+link_search
            new_links.append(new_link)
        elif "https://www.ebay.co.uk/" in link:
            print("enter")
            for word in search_text:
                link_search += word + "+"
            new_link = f"https://www.ebay.co.uk/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313&_nkw={link_search}&_sacat=0"
            #https://www.ebay.co.uk/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=fdgjdfjsdjksd&_sacat=0&LH_TitleDesc=0&_odkw=iphone+14&_osacat=0
            new_links.append(new_link)
        elif "www.amazon.co.uk" in link:
            for word in search_text:
                link_search += word + "+"
            new_link = f'https://www.amazon.co.uk/s?k={link_search}'
            new_links.append(new_link)
        return new_links, link_search
    '''
    This function is used to check if the token has a color
    token: string
    return: boolean
    '''
    def color_checker(self, token):
        # List of colors in CSS python library. Added a few extract colors which was a common color in the websites
        color_names = ['aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure', 'beige', 'bisque', 'black', 'blanchedalmond', 'blue',
                       'blueviolet', 'brown', 'burlywood', 'cadetblue', 'chartreuse', 'chocolate', 'coral', 'cornflowerblue', 'cornsilk',
                       'crimson', 'cyan', 'darkblue', 'darkcyan', 'darkgoldenrod', 'darkgray', 'darkgreen', 'darkgrey', 'darkkhaki',
                       'darkmagenta', 'darkolivegreen', 'darkorange', 'darkorchid', 'darkred', 'darksalmon', 'darkseagreen', 'darkslateblue',
                       'darkslategray', 'darkslategrey', 'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue', 'dimgray', 'dimgrey', 'dodgerblue', 'firebrick', 'floralwhite', 'forestgreen', 'fuchsia', 'gainsboro', 'ghostwhite', 'gold', 'goldenrod', 'gray', 'green', 'greenyellow', 'grey', 'honeydew', 'hotpink', 'indianred', 'indigo', 'ivory', 'khaki', 'lavender', 'lavenderblush', 'lawngreen', 'lemonchiffon', 'lightblue', 'lightcoral', 'lightcyan', 'lightgoldenrodyellow', 'lightgray', 'lightgreen', 'lightgrey', 'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue', 'lightslategray', 'lightslategrey', 'lightsteelblue', 'lightyellow', 'lime', 'limegreen', 'linen', 'magenta', 'maroon', 'mediumaquamarine', 'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumseagreen', 'mediumslateblue', 'mediumspringgreen', 'mediumturquoise', 'mediumvioletred', 'midnightblue', 'mintcream', 'mistyrose', 'moccasin', 'navajowhite', 'navy', 'oldlace', 'olive', 'olivedrab', 'orange', 'orangered', 'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise', 'palevioletred', 'papayawhip', 'peachpuff', 'peru', 'pink', 'plum', 'powderblue', 'purple', 'rebeccapurple', 'red', 'rosybrown', 'royalblue', 'saddlebrown', 'salmon', 'sandybrown', 'seagreen', 'seashell', 'sienna', 'silver', 'skyblue', 'slateblue', 'slategray', 'slategrey', 'snow', 'springgreen', 'steelblue', 'tan', 'teal', 'thistle', 'tomato', 'turquoise', 'violet', 'wheat', 'white', 'whitesmoke', 'yellow', 'yellowgreen', "multi"]
        if token.lower() in color_names:
            return True
        else: return False
        #try:
            #Color(token)
            #return True
        #except:
            #return False

    '''
    This function acts makes us check what options we can use
    text: STRING
    options: boolean
    recommen_items: boolean
    return data and name
    '''
    def pick_options(self, text, option, recommend_items):
        original = text
        text = text.lower()
        text = text.split(" ")
        print(text, option, "entered")
        singular_words = []
        #Limitzed the text to make nouns singular
        for word in text:
            singular_word = wordnet_lemmatizer.lemmatize(word, pos='n')
            singular_words.append(singular_word)
        if option == "1":
            base_url = ["https://www.amazon.co.uk/", "https://www.johnlewis.com/", "https://www.ebay.co.uk/",
                        "https://www.argos.co.uk/"]
            url = ["www.amazon.co.uk", "https://www.johnlewis.com/search?search-term=",
                   "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313&_nkw=",
                   "https://www.argos.co.uk/search/"]
            self.start2(url,text, singular_words, recommend_items, base_url)
        elif option == "2":
            #john lewis
            url = ["https://www.johnlewis.com/search?search-term="]
            base_url = ["https://www.johnlewis.com/"]
            self.start(url, base_url, text, singular_words, recommend_items)
        elif option == "3":
            url = ["https://www.argos.co.uk/search/"]
            base_url = ["https://www.argos.co.uk/"]
            self.start(url, base_url, text, singular_words, recommend_items)
        elif option == "4":
            url = ["https://www.ebay.co.uk/"]
            self.start(url, url, text, singular_words, recommend_items)
        elif option == "5":
            url = ["www.amazon.co.uk"]
            base_url = ["www.amazon.co.uk/"]
            self.start(url, base_url, text, singular_words, recommend_items)
        #saves data to a single file
        save_data(self.values, original)
        #saves data to all the data file
        master_data.excel_data(self.values)
        return self.values, original

    '''
    This function is used to check if the user-agent abids with the robot.txt and checks if the page can be scraped
    url: string
    product_url: string
    '''
    def can_scrape_website_page(self, url, product_url):
        all_user_agents = [ {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3','Accept-Language': 'en-US,en;q=0.5','Accept-Encoding': 'gzip, deflate, br','Connection': 'keep-alive',},{'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'},{'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}, {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36'}, {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/15.15063'}, {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3','Accept-Language': 'en-US,en;q=0.5','Accept-Encoding': 'gzip, deflate, br','Connection': 'keep-alive',},{'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko'}, {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.56'}, {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}, {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'}, {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'}, {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'}]

        # Get the base URL
        parsed_url = urlparse(url)
        # Used to break down the http and retrives the netloc from the parsed url
        base_url = parsed_url.scheme + '://' + parsed_url.netloc

        # Send a request to the robots.txt file
        robots_url = base_url + '/robots.txt'
        print("inside robot")
        for user_agent in all_user_agents:
            print(user_agent)

            if "johnlewis" in url:
                print("enter")
                print(robots_url)
                try:
                #Will set to the working agent
                    response = requests.get(robots_url, headers=user_agent, timeout=10)
                    rp = urllib.robotparser.RobotFileParser()
                    rp.parse(response.text)
                    if rp.can_fetch(user_agent, url):
                        r = requests.get(product_url, headers=user_agent)
                        soup = BeautifulSoup(r.content, "lxml")
                        return user_agent, soup
                #return {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 JohnLewisScraperBot'}
                except Exception as e:
                    pass
            elif "argos" in url:
                try:
                    response = requests.get(robots_url, headers=user_agent, timeout=10)
                    rp = urllib.robotparser.RobotFileParser()
                    rp.parse(response.text)
                    if rp.can_fetch(user_agent, url):
                        r = requests.get(product_url, headers=user_agent)
                        soup = BeautifulSoup(r.content, "lxml")

                        if soup.find('h1', text='Access Denied') is not None:
                            print('Page is unavailable')
                        else:
                            return user_agent, soup
                except:
                    print(f"Error: Could not retrieve {robots_url}")
            elif "amazon" in url:
                try:
                    amazon_robot = "https://www.amazon.com/robots.txt"
                    response = requests.get(amazon_robot, headers=user_agent, timeout=10)
                    rp = urllib.robotparser.RobotFileParser()
                    rp.parse(response.text)
                    if rp.can_fetch(user_agent, url):
                        r = requests.get(product_url, headers=user_agent)
                        soup = BeautifulSoup(r.content, "lxml")
                        title_tag = soup.title
                        if title_tag is not None and 'Service Unavailable' in title_tag.string:
                            print('Service is unavailable')

                        else:
                            print("working")
                            return user_agent, soup

                except:
                    print(f"Error: Could not retrieve {robots_url}")


            elif "ebay" in url:

                try:
                    response = requests.get(robots_url, headers=user_agent, timeout=10)
                    rp = urllib.robotparser.RobotFileParser()
                    rp.parse(response.text)
                    if rp.can_fetch(user_agent, url):
                        r = requests.get(product_url, headers=user_agent)
                        soup = BeautifulSoup(r.content, "lxml")
                        #print(soup)
                        return user_agent, soup

                except:
                    print(f"Error: Could not retrieve {robots_url}")
        return "None", "None"
    '''
    This function is used to scrape data from single websites
    Parameters:
    urls: list
    search_text: text
    recommend_items: boolean
    base_url: list
    limitized_text: list
    '''
    def start(self, urls, base_url, search_text, limitized_text, recommend_items):
        #Generates links
        new_urls, link_search = self.get_one_search_string(search_text, urls)
        #Checks robot.txt and gives us a header
        headers, soup = self.can_scrape_website_page(base_url[0], new_urls[0])
        '''
        I ran 30-40 tests and it never ended up going in this if statement but if it does i will use the most common header
        '''
        # Does not happen, just an additional parameter incase nothing is found
        if headers == "None":
            r = requests.get(new_urls[0], headers=headerx)
            soup = BeautifulSoup(r.content, "lxml")


        for url in new_urls:

            #Checks if the product page has items
            condition = self.check_url_has_products(url,soup)
            if condition == True:
                #Gets the amount of pages on a website
                pages = self.get_pages(url, soup, link_search)
                print(pages, "new links")
                for page_url in pages:
                    r = requests.get(page_url, headers=headers)
                    soup = BeautifulSoup(r.content, "lxml")
                    print("enter")
                    self.extract_items(soup, page_url, limitized_text, activate_counter=True, recommend_items=recommend_items, header=headers)
                    if self.count_items == 70:
                        break
            else:
                pass
        return self.values

    '''
    This function is used to scrape data from all websites
    Parameters:
    urls: list
    search_text: text
    recommend_items: boolean
    base_url: list
    '''
    def start2(self, urls, search_text, limitized_text, recommend_items, base_url):
        #Used to generate new links
        urls = self.get_search_string(urls, search_text)
        print(urls)
        for idx in range(len(urls)):
            header, soup = self.can_scrape_website_page(urls[idx], base_url[idx])
            if header == "None":
                header = headerx
            r = requests.get(urls[idx], headers=header)
            soup = BeautifulSoup(r.content, "lxml")
            #print(soup)
            #self.amazon_soup = soup
            #Checks if the product page has items
            condition = self.check_url_has_products(urls[idx],soup)
            print(condition)
            if condition == True:
                #IT enters
                print("enter")
                self.extract_items(soup, urls[idx], limitized_text, activate_counter=False, recommend_items=recommend_items, header=header)
                print("exit")
            else:
                pass
        return self.values
    '''
    This function is used to break down the product description into smaller and more meaningful data
    This function uses pos_tag to first get the Nouns, numbers ect
    Then i used spacy to extract the actual meaning full data from the pos tags
    This is because i get more data when using pos tag and entity reg in comparison to using just spacy entity reg
    '''
    def description_break_down(self, text, product_list):
        # Tokenize
        tokens = nltk.word_tokenize(text)

        # Perform POS tagging on the tokens
        pos_tags = nltk.pos_tag(tokens)

        # Extract relevant information based on POS tags
        important_info = []
        for tag in pos_tags:
            if tag[1] == 'NN' or tag[1] == 'NNP' or tag[1] == 'NNPS':
                important_info.append(tag[0])
            elif tag[1] == 'VB' or tag[1] == 'VBD' or tag[1] == 'VBG' or tag[1] == 'VBN' or tag[1] == 'VBP':
                important_info.append(tag[0])
            elif tag[1] == 'JJ' or tag[1] == 'JJR' or tag[1] == 'JJS':
                important_info.append(tag[0])
            elif tag[1] == "CD":
                important_info.append(tag[0])

        # Remove duplicate values
        new_list = list(set(important_info))
        # Covert list into string
        my_string = ', '.join(new_list)
        # Covert it into a nlp format
        doc = nlp(my_string)
        # Take out meaningful information
        entities = [entity.text for entity in doc.ents if
                    entity.label_ in ['ORG', 'PRODUCT', 'PERSON', 'DATE', 'GPE', 'MONEY']]
        # Add to the list
        for entity in entities:
            product_list.append(entity)
        return product_list

