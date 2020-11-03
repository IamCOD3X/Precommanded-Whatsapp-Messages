import schedule
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

try:
    import autoit
except ModuleNotFoundError:
    pass
import time
import datetime
import os
import argparse
import platform

if platform.system() == 'Darwin':
    # MACOS Path
    chrome_default_path = os.getcwd() + '/driver/chromedriver'
else:
    # Windows Path
    chrome_default_path = os.getcwd() + '/driver/chromedriver.exe'
parser = argparse.ArgumentParser(description='PyWhatsapp Guide')
parser.add_argument('--chrome_driver_path', action='store', type=str, default=chrome_default_path,
                    help='chromedriver executable path (MAC and Windows path would be different)')
parser.add_argument('--message', action='store', type=str, default='', help='Enter the msg you want to send')
parser.add_argument('--remove_cache', action='store', type=str, default='False',
                    help='Remove Cache | Scan QR again or Not')
parser.add_argument('--import_contact', action='store', type=str, default='False',
                    help='Import contacts.txt or not (True/False)')
parser.add_argument('--enable_headless', action='store', type=str, default='False',
                    help='Enable Headless Driver (True/False)')
args = parser.parse_args()

if args.remove_cache == 'True':
    os.system('rm -rf User_Data/*')
browser = None
Contact = None
message = None if args.message == '' else args.message
Link = "https://web.whatsapp.com/"
wait = None
unsaved_Contacts = None
def input_contacts():
    global Contact, unsaved_Contacts
    # List of Contacts
    Contact = []
    unsaved_Contacts = []
    while True:
        # Enter your choice 1 or 2
        print("PLEASE CHOOSE ONE OF THE OPTIONS:\n")
        print("1.Message to Saved Contact number:")
        print("2.Message to Unsaved Contact number:\n")
        x = int(input("Enter your choice(1 or 2):\n"))
        print()
        if x == 1:
            int(input('Enter number of Contacts you want to add->'))
            print()
            inp = str(input("Enter contact name->"))
            inp = '"' + inp + '"'
            # print (inp)
            Contact.append(inp)
        elif x == 2:
            int(input('Enter number of unsaved Contacts to add->'))
            print() 
            inp = str(input(
                "Enter unsaved contact number with country code(interger):\n\nValid input: 91943xxxxx12\nInvalid input: +91943xxxxx12\n\n"))
            # print (inp)
            unsaved_Contacts.append(inp)   
        break 
    if len(Contact) != 0:
        print("\nSaved contacts entered list->", Contact)
    if len(unsaved_Contacts) != 0:
        print("Unsaved numbers entered list->", unsaved_Contacts)


def input_message():
    global message
    
    print(
        "Enter the message and use the symbol '/' to end the message:\nFor example: Hi,Good Morning/\n\nYour message: ")
    message = []
    done = False

    while not done:
        temp = input()
        if len(temp) != 0 and temp[-1] == "/":
            done = True
            message.append(temp[:-1])
        else:
            message.append(temp)
    message = "\n".join(message)
    print(message)


def whatsapp_login(chrome_path, headless):
    global wait, browser, Link
    chrome_options = Options()
    chrome_options.add_argument('--user-data-dir=./User_Data')
    if headless == 'True':
        chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(executable_path=chrome_path, options=chrome_options)
    wait = WebDriverWait(browser, 600)
    browser.get(Link)
    browser.maximize_window()
    print("QR scanned")


def send_message(target):
    global message, wait, browser, n
    try:
        x_arg = '//span[contains(@title,' + target + ')]'
        ct = 0
        while ct != 5:
            try:
                group_title = wait.until(EC.presence_of_element_located((By.XPATH, x_arg)))
                group_title.click()
                break
            except Exception as e:
                print("Retry Send Message Exception", e)
                ct += 1
                time.sleep(3)
        input_box = browser.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
        # Remove [n] and [for] loop to send msg using scheduler
        n=int(input("Enter how many times you want to sent you message: "))      
        for ch in range(n):    
            input_box.send_keys(message)
            input_box.send_keys(Keys.ENTER)
            time.sleep(1) 
        for ch in message:
            if ch == "\n":
                ActionChains(browser).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.ENTER).key_up(
                    Keys.SHIFT).key_up(Keys.BACKSPACE).perform()
            else:
                input_box.send_keys(ch)
        input_box.send_keys(Keys.ENTER)
        print("Message sent successfully")
        time.sleep(1)
    except NoSuchElementException as e:
        print("send message exception: ", e)
        return
       

def send_unsaved_contact_message():
    global message
    try:
        time.sleep(10)
        browser.implicitly_wait(10)
        input_box = browser.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
        n=int(input("Enter how many times you want to sent you message: "))      
        for ch in range(n-1):    
            input_box.send_keys(message)
            input_box.send_keys(Keys.ENTER)
            time.sleep(1) 
        for ch in message:
            if ch == "\n":
                ActionChains(browser).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.ENTER).key_up(
                    Keys.SHIFT).key_up(Keys.BACKSPACE).perform()
            else:
                input_box.send_keys(ch)
        input_box.send_keys(Keys.ENTER)
        print("Message sent successfully")
    except Exception as e:
        print("Failed to send message exception: ", e)
        return


def import_contacts():
    global Contact, unsaved_Contacts
    Contact = []
    unsaved_Contacts = []
    fp = open("contacts.txt", "r")
    while True:
        line = fp.readline()
        con = ' '.join(line.split())
        if con and con.isdigit():
            unsaved_Contacts.append(int(con))
        elif con:
            Contact.append(con)
        if not line:
            break


def sender():
    global Contact,unsaved_Contacts
    print(Contact, unsaved_Contacts)
    for i in Contact:
        send_message(i)
        print("Message sent to ", i)
    time.sleep(5)
    if len(unsaved_Contacts) > 0:
        for i in unsaved_Contacts:
            link = "https://web.whatsapp.com/send?phone={}&text&source&data&app_absent".format(i)
            # driver  = webdriver.Chrome()
            browser.get(link)
            print("Sending message to", i)
            send_unsaved_contact_message()
            time.sleep(7)
# To schedule your msgs



def scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)
if __name__ == "__main__":
    print("Web Page Open")
    if not Contact and not unsaved_Contacts:
        # Append more contact as input to send messages
        input_contacts()
    if message == None:
        # Enter the message you want to send
        input_message()
    isSchedule = input('Do you want to schedule your Message(y/n):')
    if (isSchedule == "y"):
        jobtime = input('input time in 24 hour (HH:MM) format - ')
    # Let us login and Scan
    print("SCAN YOUR QR CODE FOR WHATSAPP WEB")
    whatsapp_login(args.chrome_driver_path, args.enable_headless)
    # Scheduling works below.
    if isSchedule == "y":
        schedule.every().day.at(jobtime).do(sender)
        time.sleep()
    else:
        sender()
        print("Task Completed")
    # Messages are scheduled to send  
    scheduler()  
