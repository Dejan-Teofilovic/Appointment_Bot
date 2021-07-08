
from telebot import types
import telebot, time
from Before_Calendar import before_calendar
from selenium import webdriver
from Gmail import gmail_ckeck
from bs4 import BeautifulSoup


bot = telebot.TeleBot("...")  # Insert your bot's TOKEN here
driver = webdriver.Chrome(".../chromedriver")  # Address browser driver (smth.exe)
otp_automate = True  # It is defined to specify the OTP extraction's method

all_users = {}

class User:
    def __init__(self, chat_id):
        self.user_id = chat_id
        self.account_password = ""
        self.email = ""
        self.gmail_password = ""
        self.location = ""
        self.birthday = ""

#----------------------------------------------------------------------1--------------------------------------------------
@bot.message_handler(commands=['start'])  # Whenever user inputs /start, this function is called.
def send_welcome(message):
    
    welcome = "Hello *{}*.\n\n".format(message.from_user.first_name) + "I'm Here to Help You in Booking a Biometric Appointment!\n\n" + "Please Press *Booking Appointment* to Start the Process.\n"    
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton(text='Booking Appointment', callback_data='action'))
    bot.send_message(chat_id=message.chat.id, text = welcome, reply_markup = markup, parse_mode = 'Markdown')

#----------------------------------------------------------------------2--------------------------------------------------
@bot.callback_query_handler(func=lambda query: query.data == "action")
def vac_callback(query):
    
    bot.answer_callback_query(callback_query_id = query.id, text = 'You selected Booking Appointment')
    location_text = "Please choose your desire VAC."
    markup = types.InlineKeyboardMarkup(row_width=2)  # Two inline button in one row
    markup.add(types.InlineKeyboardButton(text='Ankara', callback_data='ankara'), types.InlineKeyboardButton(text='Istanbul', callback_data='istanbul'))
    bot.send_message(chat_id=query.message.chat.id, text = location_text, reply_markup = markup, parse_mode = 'Markdown')

#--------------------------------------------------------------------3----------------------------------------------------
@bot.callback_query_handler(func=lambda query: query.data == "ankara")
def ankara_callback(query):
    
    global all_users
    
    bot.answer_callback_query(callback_query_id = query.id, text = 'You selected Ankara')
    user = User(query.message.chat.id)
    user.location = "Ankara"
    all_users[query.message.chat.id] = user
    login_callback(query.message)
    time.sleep(2)

#-----------------------------------------------------------------3-------------------------------------------------------
@bot.callback_query_handler(func=lambda query: query.data == "istanbul")
def istanbul_callback(query):
    
    global all_users
    
    bot.answer_callback_query(callback_query_id = query.id, text = 'You selected Istanbul')
    user = User(query.message.chat.id)
    user.location = "Istanbul"
    all_users[query.message.chat.id] = user
    login_callback(query.message)

#-----------------------------------------------------------------4-------------------------------------------------------
def login_callback(message):
    
    time.sleep(2)    
    login_info_text = "*Please insert your *Username*, *Password*, *Birthday* in each row*\n\n" + "1) Username\n" + "2) Password\n" + "3) Birdthday"
    msg = bot.send_message(chat_id=message.chat.id, text = login_info_text, parse_mode = 'Markdown')
    time.sleep(10)
    bot.register_next_step_handler(msg, login_info_checker)
    
#-----------------------------------------------------------------5-------------------------------------------------------    
def login_info_checker(message):
    
    global all_users
    
    user = all_users[message.chat.id]
    login_data = message.text.splitlines()
    
    if len(login_data) < 3:
        warning = "Please inser your *Username*, *Password*, *Birthday* in correct form"
        bot.send_message(chat_id=message.chat.id, text = warning, parse_mode = 'Markdown')
        bot.register_next_step_handler(message, login_info_checker)
        return 
    else:
        email_parts = login_data[0].split("@")
        gmail = email_parts[1].split(".")[0]
        user.account_password = login_data[1]
        user.birthday = login_data[2]
        user.email = login_data[0]
        all_users[message.chat.id] = user
        
        if gmail == "gmail":
            otp_method = "Do you allow me to check your Gmail automatically for OTP?\n\n" + "*Notice: I never save your passwords. This is just for an automated booking process*"
            markup = types.InlineKeyboardMarkup(row_width=2)
            markup.add(types.InlineKeyboardButton(text='Yes', callback_data='otp_yes'), types.InlineKeyboardButton(text='No', callback_data='otp_no'))
            bot.send_message(chat_id=message.chat.id, text = otp_method, reply_markup = markup, parse_mode = 'Markdown')
        else:
            global otp_automate
            
            otp_automate = False
            booking(message)

#--------------------------------------------------------------6----------------------------------------------------------
@bot.callback_query_handler(func=lambda query: query.data == "otp_yes")
def gmail1_callback(query):
    
    password_text = "Please insert your gmail password."
    bot.send_message(chat_id= query.message.chat.id, text = password_text, parse_mode = 'Markdown')
    get_gmail_password(query.message)

#-------------------------------------------------------------6-----------------------------------------------------------
@bot.callback_query_handler(func=lambda query: query.data == "otp_no")
def gmail2_callback(query):
    
    global otp_automate
    
    otp_automate = False
    bot.send_message(chat_id=query.message.chat.id, text = "Trying for login...", parse_mode = 'Markdown')
    booking(query.message)
 
#------------------------------------------------------------7------------------------------------------------------------
def get_gmail_password(message):
    
    global all_users
    
    user = all_users[message.chat.id]
    user.gmail_password = message.text
    all_users[message.chat.id] = user
    time.sleep(7)
    bot.send_message(chat_id=message.chat.id, text = "Trying for login...", parse_mode = 'Markdown')
    booking(message)

#-------------------------------------------------------------8-----------------------------------------------------------
@bot.message_handler(commands=['restart'])
def booking(message):
    get_captcha(message)

#------------------------------------------------------------9------------------------------------------------------------
def get_captcha(message):
    
    global driver
    
    driver.get("https://www.vfsglobal.ca/IRCC-AppointmentWave1/Account/RegisteredLogin?q=shSA0YnE4pLF9Xzwon/x/CQ1P0LBKn66dLdNUfueK+wgQK15FNs3yVpXjESPsPIkYqDL56on8vfAnBfe7K1ejg==")
    img = driver.find_element_by_id("CaptchaImage").screenshot_as_png
    msg = bot.send_photo(message.chat.id, img, caption="Please insert captcha number")
    time.sleep(10)
    bot.register_next_step_handler(msg, update_captcha)
    

#------------------------------------------------------------10------------------------------------------------------------
def update_captcha(message):
    
    global all_users
    global driver
    
    time.sleep(2)
    status = True    
    user = all_users[message.chat.id]
    account_email = user.email
    account_password = user.account_password
    if message.text.upper() == "R": # If captcha is not readble --> R: Refresh
        get_captcha(message)
        return
    username = driver.find_element_by_id("EmailId")
    username.send_keys(account_email)
    
    password = driver.find_element_by_id("Password")
    password.send_keys(account_password)
    
    captcha_ = driver.find_element_by_id("CaptchaInputText")
    captcha_.send_keys(message.text.upper())
    
    time.sleep(1)
    driver.find_element_by_class_name("submitbtn").click()
    
    while status:  # Loop for login
        try:
            time.sleep(3)
            driver.find_element_by_class_name("inactive-link")  # Bot successfully logged in
            bot.send_message(chat_id= message.chat.id, text = "Successful Login...", parse_mode = 'Markdown')
            status = False
        except:
            try:  # Here, the account was locked
                login_error = BeautifulSoup(driver.page_source, 'html.parser')
                login_error.find_all('div', attrs = {'class':'validation-summary-errors'})  # check if there is an error with bs4
                text = "Account has been locked for 2 minutes! Please wait..."
                bot.send_message(chat_id= message.chat.id, text = text, parse_mode = 'Markdown')
                time.sleep(90)  # sleep for 90 seconds
                get_captcha(message)   # request captcha again
                return
            except:   # Here, login was failed because of other reasons
                bot.send_message(chat_id= message.chat.id, text = "Error in Login. Trying again...", parse_mode = 'Markdown')
                time.sleep(5)
                get_captcha(message)   # request captcha again
                return 
            
    user = all_users[message.chat.id] 
    status, driver = before_calendar(bot, driver, user.location)
    if not status:
        booking(message)
        return
    else:
        otp(message)

#---------------------------------------------------------------11---------------------------------------------------------
def otp(message):
    
    global otp_automate
    global all_users
    
    if not otp_automate:
        text = "OTP was sent to your email. Please check your email and insert OTP in below."
        msg = bot.send_message(chat_id=message.chat.id, text = text, parse_mode = 'Markdown')
        time.sleep(120)
        bot.register_next_step_handler(msg, get_user_otp)
    else:
        bot.send_message(chat_id=message.chat.id, text = "Getting OTP...", parse_mode = 'Markdown')
        user = all_users[message.chat.id]
        account_email = user.email
        email_password = user.gmail_password
        
        time.sleep(30)
        
        start = time.time()
        user_opt = gmail_ckeck(account_email, email_password)
        end = time.time()

        while (end - start) > 160:  # Here, OTP exceeded its time limit
            text = "OPT was expired!! Trying again for new OTP. Please wait..."
            bot.send_message(chat_id=message.chat.id, text = text, parse_mode = 'Markdown')
            driver.find_element_by_id("txtbox").click()  # Re-generate OTP
            time.sleep(30)
            start = time.time()
            user_opt = gmail_ckeck(account_email, email_password)
            end = time.time()
        
        opt_number = driver.find_element_by_id("OTPe")
        opt_number.send_keys(user_opt[0])
        driver.find_element_by_id("txtsub").click()
        
        try:   # Some unindendent errors!!
            opt_error = BeautifulSoup(driver.page_source, 'html.parser')
            opt_error.find_all('div', attrs = {'style':'color: red; padding: 20px;'})
            bot.send_message(chat_id=message.chat.id, text = "Error in OTP! Regenerating...", parse_mode = 'Markdown')
            driver.find_element_by_id("txtbox").click()  # Re-generate OTP
            
            time.sleep(60)
            
            start = time.time()
            user_opt = gmail_ckeck(account_email, email_password)
            end = time.time()
            
            while (end - start) > 160:
                text = "OPT was expired!! Trying again for new OTP. Please wait..."
                bot.send_message(chat_id=message.chat.id, text = text, parse_mode = 'Markdown')
                driver.find_element_by_id("txtbox").click()  # Re-generate OTP
                time.sleep(90)
                start = time.time()
                user_opt = gmail_ckeck(account_email, email_password)   # Calls gmail_check function for automatic checking
                end = time.time()
                
            opt_number = driver.find_element_by_id("OTPe")
            opt_number.send_keys(user_opt[0])
            driver.find_element_by_id("txtsub").click()
            time.sleep(5)
            
            try:   # We passed successfully OTP step
                driver.find_element_by_xpath("//*[contains(text(), '15')]").click()
                text = "I reached Calendar. Please insert your date like example below./n/nExample: *2020-09-25*."
                msg = bot.send_message(chat_id=message.chat.id, text = text, parse_mode = 'Markdown')   # Gets desired date
                time.sleep(10)
                bot.register_next_step_handler(msg, select_day)
            except:
                text = "Ooops... I am trying again for new OTP./n/nPlease wait..."
                bot.send_message(chat_id=message.chat.id, text = text, parse_mode = 'Markdown')
                driver.find_element_by_id("txtbox").click()
                otp(message)
                
        except:
            text = "I reached Calendar. Please insert your date like example below./n/nExample: *2020-09-25*."
            msg = bot.send_message(chat_id=message.chat.id, text = text, parse_mode = 'Markdown')  # Gets desired date
            time.sleep(10)
            bot.register_next_step_handler(msg, select_day)
            time.sleep(2)

#------------------------------------------------------------------12------------------------------------------------------
def get_user_otp(message):
    
    global driver
    
    try:
        user_opt = message.text
        opt_number = driver.find_element_by_id("OTPe")
        opt_number.send_keys(user_opt)
        driver.find_element_by_id("txtsub").click()
            
        driver.find_element_by_xpath("//*[contains(text(), '15')]").click()
        text = "I reached Calendar. Please insert your date like example below./n/nExample: *2020-09-25*."
        msg = bot.send_message(chat_id=message.chat.id, text = text, parse_mode = 'Markdown')
        bot.register_next_step_handler(msg, select_day)
            
    except:
        driver.find_element_by_id("txtbox").click()  # Re-generate OTP
        time.sleep(30)
        text = "Got a problem with inserted OTP./n/n New OTP was sent. Please check your email and insert new one..."
        msg = bot.send_message(chat_id=message.chat.id, text = text, parse_mode = 'Markdown')
        time.sleep(30)
        bot.register_next_step_handler(msg, get_user_otp)
        return

#----------------------------------------------------------------13--------------------------------------------------------
def select_day(message):
    global driver
    date = message.text
    if len(date) < 10:
        text = "Warning: *Wrong date format!*./n/nPlease insert your date *EXACTLY* like example./n/nExample: *2020-09-25*. "
        msg = bot.send_message(chat_id=message.chat.id, text = text, parse_mode = 'Markdown')
        time.sleep(10)
        bot.register_next_step_handler(msg, select_day)
        return
    else:
        date = date[8:]
        driver.find_element_by_xpath("//*[contains(text(), date)]").click()
        
        time.sleep(3)
    try:
        soup_level = BeautifulSoup(driver.page_source, 'html.parser')
        hours = soup_level.find_all('input', attrs = {'name':'selectedTimeBand'}) 
        bot.send_message(chat_id=message.chat.id, text = hours, parse_mode = 'Markdown')
    except:
        bot.send_message(chat_id=message.chat.id, text = "Sorry...Date is not available", parse_mode = 'Markdown')
                                         
#------------------------------------------------------------------------------------------------------------------------
@bot.message_handler(commands=['stop'])
def stop_process(message):
    
    global driver
    
    driver.close()        

##----------------------------------------------------------
# Run     
bot.polling()










