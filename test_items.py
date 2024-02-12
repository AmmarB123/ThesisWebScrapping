import requests
from register import register_password
import random
import time
from bs4 import BeautifulSoup
import unittest
'''
This class is used for unit test
'''
class test_items(unittest.TestCase):

    def setUp(self):
        self.url = 'https://www.johnlewis.com/search?search-term=gaming+laptop'
        self.expected_descrption = 'Polo Ralph Lauren Poplin Slim Shirt, Navy'
        self.expected_price = '£1,089.99'
        self.expected_color = ["Navy", "Black"]
        self.expected_rating = '4.00'
        self.expected_review = "4 reviews"
        self.expected_size = "['S', 'M', 'L', 'XL', 'XXL']"
        self.expected_brand = "Ralph Lauren"
        self.expected_stock = "In stock"
        response = requests.get(self.url, headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 JohnLewisScraperBot'})
        self.soup = BeautifulSoup(response.content, "lxml")


    def test_name(self):

        name = self.soup.find("span", class_="title_title__desc__ZCdyp title_title__desc--three-lines__VHz1t title_title__desc--branded__8SluU").text
        self.assertEqual(name, self.expected_descrption)

    def test_price(self):
        try:
            price = (self.soup.find("span", {"data-test": "product-card-price-now"})).text
        except:
            pass
        try:
            price = (self.soup.find("em", {"data-test": "product-card-price-now"})).text[6:]
        except:
            pass
        print(price)
        self.assertEqual(price, self.expected_price)

    def test_color(self):
        colors = []

        input_name = self.soup.find_all("a", title=True)
        for colo in input_name:
            colors.append(colo["title"])
        self.assertEqual(colors, self.expected_color)

    def test_color_not_list(self):
        descrpition = self.soup.find("span",
                              class_="title_title__desc__ZCdyp title_title__desc--three-lines__VHz1t title_title__desc--branded__8SluU").text
        new_sentence = descrpition.replace("/", " ").replace(",", " ")
        new_sentence = new_sentence.split(" ")
        # print(new_sentence)
        for token in new_sentence:
            if token in color_list:
                color = token
        self.assertEqual(color, self.expected_color)

    def test_size_not_list(self):
        descrpition = self.soup.find("span",
                                     class_="title_title__desc__ZCdyp title_title__desc--three-lines__VHz1t title_title__desc--branded__8SluU").text
        break_des = descrpition.replace(",", " ")
        break_des = break_des.split(" ")
        for idx, word in enumerate(break_des):
            if '"' in word:
                all_size = word
            elif "inch" in word:
                all_size = break_des[idx - 1]
        self.assertEqual(all_size, self.expected_color)

    def test_brand(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, "lxml")
        brand = soup.find("span", {"class": "title_title__brand__UX8j9 undefined"}).text
        self.assertEqual(brand, self.expected_brand)

    def test_size(self):
        all_size = []
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, "lxml")
        hypertext1 = soup.find_all('button', {"data-cy": "size-selector-item"})
        for hype1 in hypertext1:
            # cant find instock  sizes
            all_size.append(hype1.text)
        self.assertEqual(all_size, self.expected_size)

    def test_review(self):
        review = 0
        reviews = self.soup.find_all('button', {"type": "button"})
        for re in reviews:
            if "review" in re.text:
                review = re.text
        self.assertEqual(review, self.expected_review)

    def test_rating(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, "lxml")
        rating = soup.find('span', {"data-test": "rating"}).text[63:68]
        self.assertEqual(rating, self.expected_rating)

    def test_stock(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, "lxml")
        istock = soup.find_all('button', {"type": "submit"})

        instock = "In stock"
        for stock in istock:

            # print(stock.text)
            if "Notify me" in stock.text:
                instock = "Out of stock"
        self.assertEqual(instock, self.expected_stock)

#Argos
class test_items2(unittest.TestCase):

    def setUp(self):
        self.url = 'https://www.argos.co.uk/product/1187238?clickSR=slp:term:iphone%2014:1:126:1'
        self.expected_name = 'SIM Free iPhone 14 Pro Max 5G 128GB Mobile Phone Deep Purple'
        self.expected_price = '£1139.00'
        self.expected_rating = '4.7'
        self.expected_review = "85"
        self.expected_size = "16.1"
        self.expected_stock = "In stock"
        self.expected_color = ["Purple", "Gold", "Silver", "Black"]
        response = requests.get(self.url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'})
        self.soup = BeautifulSoup(response.content, "lxml")

    def test_name(self):
        title = self.soup.find('span', {"data-test": "product-title"}).text
        self.assertEqual(title, self.expected_name)

    def test_price(self):

        try:
            price = self.soup.find('span', {"itemprop": "priceCurrency"}).find_next().text
            price = self.soup.find('h2', class_="Pricestyles__OfferPriceTitle-sc-1oev7i-4 hEuzyG")
            print(price, "dc")
        except:
            price = self.soup.find('span', {"itemprop": "priceCurrency"}).find_next().text
            print(price, "no dc")
        self.assertEqual(price, self.expected_price)
    #Only testing for multiple colors for an item
    def test_color(self):
        colors = []

        color = self.soup.find_all('li', {"class": "ColorSwatchstyles__ColorSwatchListLi-jvpifx-4 bSUblL"})
        # print(color)
        for colo in color:
            colors.append(colo.text)
        self.assertEqual(colors, self.expected_color)


    def test_size(self):
        all_size = []
        hypertext1 = self.soup.find_all('button', {"data-cy": "size-selector-item"})
        for hype1 in hypertext1:
            # cant find instock  sizes
            all_size.append(hype1.text)
        if len(all_size) == 0:
            div = self.soup.find('div', {'class': 'product-description-content-text'}).text.split(" ")
            for idx, word in enumerate(div):
                if "inch" in word:
                    all_size = div[idx - 1][-4:]
                elif "-inch" in word:
                    all_size = word
        self.assertEqual(all_size, self.expected_size)

    def test_review(self):
        review = "0"
        try:
            review = self.soup.find('span', {"itemprop": "ratingCount"}).text
        except:
            pass
        self.assertEqual(review, self.expected_review)

    def test_rating(self):
        try:
            rating = self.soup.find('span', {"itemprop": "ratingValue"}).text
        except:
            rating = 0
        self.assertEqual(rating, self.expected_rating)

    def test_stock(self):

        try:
            istock = self.soup.find_all('button', {"type": "submit"})
            instock = "In stock"
            for stock in istock:
                # Does not have a "out of stock" when scraping so we need to change
                if "Notify me" in stock.text:
                    instock = "Out of stock"
        except:
            instock = "In stock"
            pass

#Ebay
class test_items3(unittest.TestCase):

    def setUp(self):
        self.url = 'https://www.ebay.com/itm/134496789407?epid=9056253598&hash=item1f50a2239f:g:mtIAAOSweYxkFyVv&amdata=enc%3AAQAHAAAA4PhRVpHBRaceztv6AhIn6h0VxMawnqyXC2Gtfse6gFIJz0W0wcAuFjc0R6fHF6wttHIrqDOLTHlRVYj6EI%2Fo7OhbXVGxxFrXnqlp5U2mEPpwICfrxBQbG%2Fd2QRkqa5kq076rdf1kkuSYlEg6i1XXBUjrUJ3Q2uw0xoDXe9pIXQUfmc%2BjUGNbqetDEj%2F8tNOQJPZJvnGKV1I0ZnNTgVsHbN1149DRB1oF9yux1qgMBF1KXHvAidyR2mwCcms%2B9g65H9EbQQNxTbsQfSyEvfk4NbqAumvZf1OiHhHwah6PDZZH%7Ctkp%3ABFBMsvfq9exh'
        self.expected_name = 'Apple iPhone 14 Pro Max -1TB- Gold. Physical SIM tray, Dual Sim - Fast Ship✈️'
        self.expected_price = 'C $2,794.99'
        self.expected_rating = '5.0'
        self.expected_review = "3"
        self.expected_size = "6.7 in"
        self.expected_stock = "In stock"
        self.color = "Gold"
        response = requests.get(self.url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'})
        self.soup = BeautifulSoup(response.content, "lxml")


    def test_name(self):
        try:
            descrpition = self.soup.find('h1', {"class": "x-item-title__mainTitle"}).find_next().text
            # print((descrpition))
        except:
            descrpition = "None"
            pass
        self.assertEqual(descrpition, self.expected_name)

    def test_price(self):
        try:
            price = self.soup.find('span', {'itemprop': 'price'}).text

        # print(price)

        except:
            price = "None"
            pass
        print(price)
        self.assertEqual(price, self.expected_price)
    #Only testing for multiple colors for an item



    def test_size1000(self):
        try:
            # Since ebay has different number boxes for color, and size we need to search for them manually. This is used to check
            # For items in the boxes
            sizes = self.soup.find('select', {'id': 'x-msku__select-box-1000'})
            question = sizes.get("aria-label")
            print(question)
            if "Colour" in question or "Color" in question or "Pattern" in question:
                color_select = self.soup.find('select', {'aria-label': question})
                colors = [option.text.strip() for option in color_select.find_all('option')][1:]
                print(colors)
            elif "Size" in question or "Waist" in question or "Measurement" in question:
                size_select = self.soup.find('select', {'aria-label': question})
                all_size = [option.text.strip() for option in size_select.find_all('option')][1:]
                print(all_size)
        except:
            pass
        self.assertEqual(all_size, self.expected_size)

    def test_color1000(self):
        try:
            # Since ebay has different number boxes for color, and size we need to search for them manually. This is used to check
            # For items in the boxes
            sizes = self.soup.find('select', {'id': 'x-msku__select-box-1000'})
            question = sizes.get("aria-label")
            print(question)
            if "Colour" in question or "Color" in question or "Pattern" in question:
                color_select = self.soup.find('select', {'aria-label': question})
                colors = [option.text.strip() for option in color_select.find_all('option')][1:]
                print(colors)
            elif "Size" in question or "Waist" in question or "Measurement" in question:
                size_select = self.soup.find('select', {'aria-label': question})
                all_size = [option.text.strip() for option in size_select.find_all('option')][1:]
                print(all_size)
        except:
            pass
        self.assertEqual(colors, self.color)

    def test_size1001(self):
        try:
            # Since ebay has different number boxes for color, and size we need to search for them manually. This is used to check
            # For items in the boxes
            sizes = self.soup.find('select', {'id': 'x-msku__select-box-1001'})
            question = sizes.get("aria-label")
            print(question)
            if "Colour" in question or "Color" in question or "Pattern" in question:
                color_select = self.soup.find('select', {'aria-label': question})
                colors = [option.text.strip() for option in color_select.find_all('option')][1:]
                print(colors)
            elif "Size" in question or "Waist" in question or "Measurement" in question:
                size_select = self.soup.find('select', {'aria-label': question})
                all_size = [option.text.strip() for option in size_select.find_all('option')][1:]
                print(all_size)
        except:
            pass
        self.assertEqual(all_size, self.expected_size)

    def test_color1001(self):
        try:
            # Since ebay has different number boxes for color, and size we need to search for them manually. This is used to check
            # For items in the boxes
            sizes = self.soup.find('select', {'id': 'x-msku__select-box-1001'})
            question = sizes.get("aria-label")
            print(question)
            if "Colour" in question or "Color" in question or "Pattern" in question:
                color_select = self.soup.find('select', {'aria-label': question})
                colors = [option.text.strip() for option in color_select.find_all('option')][1:]
                print(colors)
            elif "Size" in question or "Waist" in question or "Measurement" in question:
                size_select = self.soup.find('select', {'aria-label': question})
                all_size = [option.text.strip() for option in size_select.find_all('option')][1:]
                print(all_size)
        except:
            pass
        self.assertEqual(colors, self.color)

    def test_size1002(self):
        try:
            # Since ebay has different number boxes for color, and size we need to search for them manually. This is used to check
            # For items in the boxes
            sizes = self.soup.find('select', {'id': 'x-msku__select-box-1002'})
            question = sizes.get("aria-label")
            print(question)
            if "Colour" in question or "Color" in question or "Pattern" in question:
                color_select = self.soup.find('select', {'aria-label': question})
                colors = [option.text.strip() for option in color_select.find_all('option')][1:]
                print(colors)
            elif "Size" in question or "Waist" in question or "Measurement" in question:
                size_select = self.soup.find('select', {'aria-label': question})
                all_size = [option.text.strip() for option in size_select.find_all('option')][1:]
                print(all_size)
        except:
            pass
        self.assertEqual(all_size, self.expected_size)

    def test_color1002(self):
        try:
            # Since ebay has different number boxes for color, and size we need to search for them manually. This is used to check
            # For items in the boxes
            sizes = self.soup.find('select', {'id': 'x-msku__select-box-1002'})
            question = sizes.get("aria-label")
            print(question)
            if "Colour" in question or "Color" in question or "Pattern" in question:
                color_select = self.soup.find('select', {'aria-label': question})
                colors = [option.text.strip() for option in color_select.find_all('option')][1:]
                print(colors)
            elif "Size" in question or "Waist" in question or "Measurement" in question:
                size_select = self.soup.find('select', {'aria-label': question})
                all_size = [option.text.strip() for option in size_select.find_all('option')][1:]
                print(all_size)
        except:
            pass
        self.assertEqual(colors, self.color)

    def test_color_if_not_found(self):
        try:
            # Auctions do not display colors so we check if manually
            item_label = self.soup.find_all('span', {"class": "ux-textspans"})
            for index, item in enumerate(item_label):
                if "Colour:" in item.text or "Color" in item.text or "Pattern" in item.text:
                    colors = item_label[index + 1].text
                    break
        except:
            pass
        self.assertEqual(colors, self.color)

    def test_size_if_not_found(self):
        all_size = ''
        item_label = self.soup.find_all('span', {"class": "ux-textspans"})
        for index, item in enumerate(item_label):
            if "Size:" in item_label[index].text or "Waist" in item.text or "Measurement" in item.text:
                all_size = item_label[index + 1].text
                print(all_size)
                break

        self.assertEqual(all_size, self.expected_size)

    def test_size3(self):
        all_size = []
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, "lxml")
        hypertext1 = soup.find_all('button', {"data-cy": "size-selector-item"})
        for hype1 in hypertext1:
            # cant find instock  sizes
            all_size.append(hype1.text)
        if len(all_size) == 0:
            div = soup.find('div', {'class': 'product-description-content-text'}).text.split(" ")
            for idx, word in enumerate(div):
                if "inch" in word:
                    all_size = div[idx - 1][-4:]
                elif "-inch" in word:
                    all_size = word
        self.assertEqual(all_size, self.expected_size)

    def test_rating(self):
        try:
            rating = self.soup.find('a', {'id': 'review-ratings-cntr'})
            rating = rating.get("aria-label")
            rating = rating.split()
            review = rating[9]
            rating = rating[0]
            print(rating, review)
        except:
            rating = '0'
            review = "0"
            pass
        self.assertEqual(rating, self.expected_rating)

    def test_review(self):
        try:
            rating = self.soup.find('a', {'id': 'review-ratings-cntr'})
            rating = rating.get("aria-label")
            rating = rating.split()
            review = rating[9]
            rating = rating[0]
            print(rating, review)
        except:
            rating = '0'
            review = "0"
            pass
        self.assertEqual(review, self.expected_review)

    def test_stock(self):
        try:
            instock = self.soup.find('span', {"itemprop": "availability"}).get("content")
            if "InStock" in instock:
                instock = "In stock"
            else:
                instock = "Out of stock"
        except:
            instock = "Out of stock"
            pass
        self.assertEqual(instock, self.expected_stock)
#Amazon
#These tests have to be changed based on the input
class test_items4(unittest.TestCase):

    def setUp(self):
        self.url = 'https://www.ebay.com/itm/134496789407?epid=9056253598&hash=item1f50a2239f:g:mtIAAOSweYxkFyVv&amdata=enc%3AAQAHAAAA4PhRVpHBRaceztv6AhIn6h0VxMawnqyXC2Gtfse6gFIJz0W0wcAuFjc0R6fHF6wttHIrqDOLTHlRVYj6EI%2Fo7OhbXVGxxFrXnqlp5U2mEPpwICfrxBQbG%2Fd2QRkqa5kq076rdf1kkuSYlEg6i1XXBUjrUJ3Q2uw0xoDXe9pIXQUfmc%2BjUGNbqetDEj%2F8tNOQJPZJvnGKV1I0ZnNTgVsHbN1149DRB1oF9yux1qgMBF1KXHvAidyR2mwCcms%2B9g65H9EbQQNxTbsQfSyEvfk4NbqAumvZf1OiHhHwah6PDZZH%7Ctkp%3ABFBMsvfq9exh'
        self.expected_name = 'Apple iPhone 14 Pro Max -1TB- Gold. Physical SIM tray, Dual Sim - Fast Ship✈️'
        self.expected_price = 'C $2,794.99'
        self.expected_rating = '5.0'
        self.expected_review = "3"
        self.expected_size = "6.7 in"
        self.expected_stock = "In stock"
        self.expected_color = "Gold"
        response = requests.get(self.url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'})
        self.soup = BeautifulSoup(response.content, "lxml")

    def size(self):
        all_size = []
        try:
            # For sizes add size [2:] into excel
            options = self.soup.find_all("option", {"data-a-html-content": True})
            for option in options:
                size = option.get("data-a-html-content")
                all_size.append(size)
        except:
            pass
        self.assertEqual(all_size, self.expected_size)



    def test_name(self):
        try:
            descrpition = self.soup.find('span', {'id': "productTitle"}).text.strip()
            # descrpition = soup2.find('span', {'class': "a-size-large product-title-word-break"}).text.strip()
            # print(descrpition)
        except:
            descrpition = "None"
            pass
        self.assertEqual(descrpition, self.expected_name)

    def test_price(self):
        try:
            # symbol = soup2.find('span', {'class': "a-price-symbol"}).text
            # decimal = soup2.find('span', {'class': "a-price-fraction"}).text
            # price = soup2.find('span', {'class': "a-price-whole"}).text
            # price = symbol + price + decimal
            price = self.soup.find('span', class_='a-offscreen').text
            print(price)
        except:
            price = "None"

        self.assertEqual(price, self.expected_price)
    #Only testing for multiple colors for an item


    def size_not_found(self):
        word = []
        selection = self.soup.find("table", {"class": "a-normal a-spacing-micro"}).text
        selection = selection.strip("       ").lower()
        selection = selection.split(" ")
        for words in selection:
            if words == '':
                pass
            else:
                word.append(words)
        for idx, selected_word in enumerate(word):
            if "size" in selected_word:
                all_size = word[idx + 1]
                print(all_size)
                break
        self.assertEqual(all_size, self.expected_size)

    def color_not_found(self):
        word = []
        selection = self.soup.find("table", {"class": "a-normal a-spacing-micro"}).text
        selection = selection.strip("       ").lower()
        selection = selection.split(" ")
        for words in selection:
            if words == '':
                pass
            else:
                word.append(words)
        for idx, selected_word in enumerate(word):
            if "color" in selected_word or "colour" in selected_word:
                colors = word[idx + 1]
                print(colors)
                break
        self.assertEqual(colors, self.expected_color)

    def color_not_found2(self):
        try:
            color_div = self.soup.find('div', {'id': 'variation_color_name'})
            if color_div:
                color_spans = color_div.find_all('span', {'class': 'selection'})
                colors = [span.text.strip() for span in color_spans]
            self.assertEqual(colors, self.expected_color)
        except:
            pass

    def size_not_found2(self):
        try:
            size_div = self.soup.find('div', {'id': 'variation_size_name'})
            if size_div:
                size_spans = size_div.find_all('span', {'class': 'selection'})
                all_size = [span.text.strip() for span in size_spans]
                print(all_size)
        except:
            pass
        self.assertEqual(all_size, self.expected_size)

    def test_rating(self):
        try:
            rating = self.soup.find('span', {'class': "a-icon-alt"}).text
            if "Previous" in rating:
                rating = "0"
            else:
                rating = rating[:3]
        except:
            rating = "0"
            pass
        self.assertEqual(rating, self.expected_rating)

    def test_review(self):
        try:
            review = self.soup.find('span', {'id': "acrCustomerReviewText"}).text
            review = review.split(" ")[0]
            # print(review[0])
        except:
            review = "0"
            pass
        self.assertEqual(review, self.expected_review)

    def test_stock(self):
        try:
            instock = self.soup.find("div", {"id": "availability"}).find_next().text.strip()
        except:
            instock = "Select size for stock"
            pass
        self.assertEqual(instock, self.expected_stock)

class TestRegisterPassword(unittest.TestCase):

    def test_valid_password(self):
        password = "ValidPassword1!"
        result = register_password(password)
        self.assertEqual(result, password)

    def test_password_too_short(self):
        password = "Short"
        result = register_password(password)
        self.assertEqual(result, 1)

    def test_password_too_long(self):
        password = "ThisPasswordIsTooLongToBeAccepted"
        result = register_password(password)
        self.assertEqual(result, 1)

    def test_password_no_lowercase(self):
        password = "PASSWORD1!"
        result = register_password(password)
        self.assertEqual(result, 2)

    def test_password_no_uppercase(self):
        password = "password1!"
        result = register_password(password)
        self.assertEqual(result, 3)

    def test_password_no_number(self):
        password = "Password!"
        result = register_password(password)
        self.assertEqual(result, 4)

    def test_password_no_special_character(self):
        password = "Password1"
        result = register_password(password)
        self.assertEqual(result, 5)

    def test_password_contains_whitespace(self):
        password = "Password 1!"
        result = register_password(password)
        self.assertEqual(result, 6)

color_list = [
    "Amaranth",
    "Amber",
    "Apricot",
    "Aquamarine",
    "Azure",
    "Beige",
    "Black",
    "Blue",
    "Blush",
    "Bronze",
    "Brown",
    "Burgundy",
    "Byzantium",
    "Carmine",
    "Cerise",
    "Cerulean",
    "Champagne",
    "Chartreuse",
    "Chocolate",
    "Coffee",
    "Copper",
    "Coral",
    "Crimson",
    "Cyan",
    "Desert Sand",
    "Electric Blue",
    "Emerald",
    "Erin",
    "Gold",
    "Gray",
    "Green",
    "Harlequin",
    "Indigo",
    "Ivory",
    "Jade",
    "Jungle Green",
    "Lavender",
    "Lemon",
    "Lilac",
    "Lime",
    "Magenta",
    "Maroon",
    "Mauve",
    "Navy",
    "Olive",
    "Orange",
    "Orchid",
    "Peach",
    "Pear",
    "Periwinkle",
    "Persimmon",
    "Pink",
    "Platinum",
    "Plum",
    "Powder Blue",
    "Purple",
    "Raspberry",
    "Red",
    "Rose",
    "Ruby",
    "Russet",
    "Rust",
    "Saffron",
    "Salmon",
    "Sangria",
    "Sapphire",
    "Scarlet",
    "Silver",
    "Slate Gray",
    "Spring Bud",
    "Spring Green",
    "Tan",
    "Tangerine",
    "Teal",
    "Turquoise",
    "Ultramarine",
    "Violet",
    "Viridian",
    "White",
    "Yellow",
    "Zinnwaldite",
]
if __name__ == '__main__':
    unittest.main()