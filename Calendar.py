from bs4 import BeautifulSoup
import re
import time
import telegram_message


def open_day(driver):
    open_days_list = []
    
    soup_level = BeautifulSoup(driver.page_source, 'html.parser')
    month = soup_level.find_all('tbody') #, attrs = {'class':'fc-week fc-first'})
    
    days = re.findall(r'<td class=\"fc-day fc-(.*?)>', str(month[0]))
    #print(len(days))
    for i in range(len(days)):
        #print(days[i])
        date = re.search(r'\"(\d.+?)\"', days[i])
        try:
            style = re.search(r'\((\d.+)\)', days[i])
            if  style.group()== '(255, 106, 106)':
                print("Close Day")
                print("Date: %s" %(date.group()))
            elif style.group()== '(188, 237, 145)':
                print("Open Day")
                open_days_list.append(date.group())
                print("Date: %s" %(date.group()))
            #print("--------")
            #print("Date: %s and Color-day: %s" %(date.group(), style.group()))
        except:
            pass
            #print("Date: %s" %(date.group()))
    return open_days_list
        
        
        
def select_day(driver, open_days, desired_date):
    time.sleep(5)
    status = False
    for date in open_days:
        if date == desired_date:
            driver.find_element_by_xpath("//*[contains(text(), '14')]").click()
            time.sleep(3)
            soup_level = BeautifulSoup(driver.page_source, 'html.parser')
            hours = soup_level.find_all('input', attrs = {'name':'selectedTimeBand'})
            print(hours)                                       
            print("Date selected")
            status = True
    return status

     
def calendar_update(driver, location_name):
    try:
        open_days = open_day(driver)
        telegram_message.message_sender(open_days, location_name)
        time.sleep(30)
    
        driver.find_element_by_xpath("//*[contains(text(), '›')]").click()
        open_days = open_day(driver)
        telegram_message.message_sender(open_days, location_name)
        time.sleep(30)
        
        driver.find_element_by_xpath("//*[contains(text(), '‹')]").click()
        
        status = True
        return status
    
    except:
        status = False
        return status
