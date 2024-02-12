import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import urllib.robotparser
import validators
from saving_data import save_data
class build_scraper:
    def __init__(self,item_name, normal_url, url, html_tag1, html_tag2, html_tag3, html_tag4, html_tag5):
        self.normal_url = normal_url

        self.item_name = item_name
        self.url = url
        self.data = []
        self.html_tag1 = html_tag1
        self.html_tag2 = html_tag2
        self.html_tag3 = html_tag3
        self.html_tag4 = html_tag4
        self.html_tag5 = html_tag5
        self.user_agents = [{'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}, {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}, {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36'}, {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/15.15063'}, {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko'}, {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.56'}, {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}, {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'}, {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'}, {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'}]
        print(url, html_tag1, html_tag2, html_tag3)
    '''
    This function is used for built in scraper where it checks the robot.txt file of the website then it scrapes for item link or input 
    data
    '''

    def scraper(self):
        robot_accepted = False
        # Checks what user-agents are working
        for key in self.user_agents:
            robot_accepted, head = self.can_scrape_website(key)
            print(robot_accepted, key)
            # If they work make a request and scrape
            if robot_accepted == True:
                r = requests.get(self.url, headers=head)
                soup = BeautifulSoup(r.content, "lxml")
                #print(soup)
                hypertext = soup.find_all(self.html_tag1[0], {self.html_tag1[1]: self.html_tag1[2]})

                #print(hypertext)
                for hype in hypertext:
                    data_1 = "None"
                    data_2 = "None"
                    data_3 = "None"
                    data_4 = "None"
                    try:
                        data_1 = hype.find(self.html_tag2[0], {self.html_tag2[1]: self.html_tag2[2]}).text
                        print(data_1)
                    except:
                        pass
                    try:
                        l = hype.find(self.html_tag2[0], {self.html_tag2[1]: self.html_tag2[2]})[self.html_tag2[1]]
                        if validators.url(l):
                            data_1 = l
                            # print(link)
                        else:
                            # print("fALSE")
                            data_1 = self.normal_url + l
                    except:
                        pass
                    try:
                        data_2 = hype.find(self.html_tag3[0], {self.html_tag3[1]: self.html_tag3[2]}).text
                        print(data_2)
                    except:
                        pass
                    try:
                        l = hype.find(self.html_tag3[0], {self.html_tag3[1]: self.html_tag3[2]})[self.html_tag3[1]]
                        if validators.url(l):

                            data_2 = l
                        else:
                            # print("fALSE")
                            data_2 = self.normal_url + l
                    except:
                        pass
                    try:
                        data_3 = hype.find(self.html_tag4[0], {self.html_tag4[1]: self.html_tag4[2]}).text
                        print(data_3)
                    except:
                        pass
                    try:
                        l = hype.find(self.html_tag4[0], {self.html_tag4[1]: self.html_tag4[2]})[self.html_tag4[1]]
                        if validators.url(l):
                            print("True")
                            data_3 = l

                        else:
                            # print("fALSE")
                            data_3 = self.normal_url + l
                    except:
                        pass
                    try:
                        data_4 = hype.find(self.html_tag5[0], {self.html_tag5[1]: self.html_tag5[2]}).text
                        print(data_4)
                    except:
                        pass
                    try:
                        l = hype.find(self.html_tag5[0], {self.html_tag5[1]: self.html_tag5[2]})[self.html_tag5[1]]
                        if validators.url(l):
                            print("True")
                            data_4 = l

                        else:
                            # print("fALSE")
                            data_4 = self.normal_url + l
                    except:
                        pass
                    try:
                        values = {
                                "Data One": data_1,
                                "Data Two": data_2,
                                "Data Three": data_3,
                                "Data Four": data_4
                                }
                        self.data.append(values)
                    except:
                        pass
                if len(self.data) == 0:
                    pass
                else:
                    print(self.data)
                    return self.data
            else:
                pass
    # Used to save the data
    def data_save(self):
        save_data(self.data, self.item_name)
    # Used to check if the website can be scraped
    def can_scrape_website(self, header):
        # Get the base URL
        parse_the_url = urlparse(self.normal_url)
        base_url = parse_the_url.scheme + '://' + parse_the_url.netloc

        # Send a request to the robots.txt file
        robots_url = base_url + '/robots.txt'
        try:
            response = requests.get(robots_url, headers=header, timeout=10)
        except:
            print(f"Error: Could not retrieve {robots_url}")
            return False

        # Parse the robots.txt file and check if scraping is allowed for the given user agent
        rp = urllib.robotparser.RobotFileParser()
        rp.parse(response.text)

        return rp.can_fetch(header, self.normal_url), header
    # Coverts true statements to a boolean
    def check_tags(self):
        if self.html_tag1[2].lower() == "true":
            self.html_tag1[2] = True
        if self.html_tag2[2].lower() == "true":
            self.html_tag2[2] = True
        if self.html_tag3[2].lower() == "true":
            self.html_tag3[2] = True
        if self.html_tag4[2].lower() == "true":
            self.html_tag4[2] = True
        if self.html_tag5[2].lower() == "true":
            self.html_tag5[2] = True
'''
    def data_input_name(self):
        if self.data_title[0] == '':
            self.data_title[0] == "Data One"
        if len(self.data_title[1]) == 0:
            self.data_title[1] == "Data Two"
        if len(self.data_title[2]) == 0:
            self.data_title[1] == "Data Three"
        if len(self.data_title[3]) == 0:
            self.data_title[1] == "Data Four"
'''





