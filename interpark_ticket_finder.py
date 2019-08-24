from selenium import webdriver
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta

def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        print(s + " is not english")
        return False
    else:
        print(s + " is english")
        return True

def throw_up_unicode(character):
    unicode_escaped_letters = str(character.encode("raw_unicode_escape"))
    #print(unicode_escaped_letters)
    separated_list = unicode_escaped_letters.split('\\')
    #print(separated_list)
    semi_code_list = separated_list[2:]
    code_list =semi_code_list[::2]
    #print(code_list)

    query = ""

    for i in code_list:
        x = re.sub('[^a-zA-Z0-9]+', '', i)
        query+="%"+str(x.capitalize().swapcase())
        #print(query)

    #print("unicode escaped query is: " + query)
    return query

def interpark_ticket_finder(query):
    #find artist
    target_interpark_url="http://ticket.interpark.com/search/ticket.asp?search="+ query #This contains ticket URL

    # setup Driver|Chrome
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(r"C:\Users\pc\Desktop\chromedriver", chrome_options=options)
    driver.implicitly_wait(10) # waiting web source for three seconds implicitly

    #get interpark url
    driver.get(target_interpark_url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    #parsing
    active_ticket_information_soup = soup.find_all("div", {"class": "result_Ticket", "id": "ticketplay_result"}) #Not including titles but pretty
    #print(active_ticket_information_soup)
    #print(len(active_ticket_information_soup))
    title_href = active_ticket_information_soup[0]
    #print(title_href)
    h4_titles = title_href.find_all("h4")
    #print(h4_titles)
    date_soup_list= active_ticket_information_soup[0].find_all("td", {"class": "info_Date"}) #print(date_soup_list)

    b=[]
    for i in h4_titles:
        links = i.find_all('a')
        #print(links)
        for link in links:
            #making title and url dictionary
            url = link['href']
            b.append({"title":i.text, "url":url})
        for index_no in range(len(b)):
            print(index_no)
            tag_and_date = date_soup_list[index_no] #print(tag_and_date)
            no_tag_date = tag_and_date.text #print(no_tag_date) #print(no_tag_date)
            sixteen_digit_date = re.sub('[^0-9]+', '', no_tag_date)
            length_string = len(sixteen_digit_date)
            first_length = round(length_string / 2)
            first_half = sixteen_digit_date[0:first_length]
            second_half = sixteen_digit_date[first_length:]
            starting_dt = datetime.strptime(first_half, "%Y%m%d")
            end_dt = datetime.strptime(second_half, "%Y%m%d") + timedelta(days=1)
            start_date = starting_dt.strftime("%Y-%m-%d")
            end_date = end_dt.strftime("%Y-%m-%d")
            b[index_no]['start_date'] = start_date
            b[index_no]['end_date'] = end_date
        print(b)
    return b

#if sentence halts after isEnglish() returns specific value(True or False value).
#Therefore, evolved interpark ticket finder has to be made in order to continue interpark ticket finder
def evolved_interpark_ticket_finder(input):
    if not isEnglish(input):
        return interpark_ticket_finder(throw_up_unicode(input))
    else:
        return interpark_ticket_finder(input)

