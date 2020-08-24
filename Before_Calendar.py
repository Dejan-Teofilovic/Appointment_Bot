


import time
from selenium.webdriver.support.ui import Select

def before_calendar(bot, driver, location_name): 
    try:
        time.sleep(2)
        driver.find_element_by_class_name("inactive-link").click()
        
        time.sleep(2)
        center = Select(driver.find_element_by_id('LocationId'))   # 261: Ankara -- 262: Istanbul
        location_name = location_name.lower()
        location_name = location_name.title()
        if location_name == "Istanbul":
            location_id = "262"
        else:
            location_id = "261"
        center.select_by_value(location_id)
        time.sleep(2)
        number_applicant = Select(driver.find_element_by_id('NoOfApplicantId'))   # 261: Ankara -- 262: Istanbul
        number_applicant.select_by_value('1')
        time.sleep(2)
        category = Select(driver.find_element_by_id('VisaCategoryId'))   # 665: Biometric Entrolment
        category.select_by_value('665')
        time.sleep(4)
        driver.find_element_by_id("IAgree").click()
        time.sleep(3)
        driver.find_element_by_class_name("frm-button").click()    
    
        time.sleep(2)
        driver.find_element_by_class_name("submitbtn").click()

        time.sleep(2)
        birdthday = driver.find_element_by_id("DateOfBirth")
        birdthday.send_keys("USER'S BIRDTHDAY")    
        time.sleep(2)
        driver.find_element_by_id("submitbuttonId").click()

        time.sleep(2)
        driver.find_element_by_class_name("submitbtn").click()
        status = True
        return status, driver

    except:
        status = False
        return status, driver





