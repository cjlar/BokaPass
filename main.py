import time
from selenium import webdriver
import os
import datetime

os.environ['PATH'] += r"C:/Users/Afroanton/Documents/Dev/WebScraper"
def findTime(lastDesiredDate):
    foundTime = False
    while not foundTime:
        browser = webdriver.Chrome()
        pageOverload = False
        browser.get('https://bokapass.nemoq.se/Booking/Booking/Index/Stockholm')
        browser.implicitly_wait(3)
        bokaNytidButton = browser.find_elements_by_name("StartNextButton")
        if (len(bokaNytidButton) == 0):
            print("Something wrong loading the page")
            return
        else:
            bokaNytidButton = bokaNytidButton[0]
            bokaNytidButton.click()
            acceptInfoCheckBox = browser.find_element_by_id("AcceptInformationStorage")
            acceptInfoCheckBox.click()
            nextButton = browser.find_element_by_name("Next")
            nextButton.click()
            boendeButton = browser.find_elements_by_id("ServiceCategoryCustomers_0__ServiceCategoryId")
            if len(boendeButton) == 0:
                print("Something wrong loading the page")
                return
            else:
                boendeButton[0].click()
                browser.find_element_by_name("Next").click()
                while not pageOverload and not foundTime:
                    browser.find_element_by_name("TimeSearchFirstAvailableButton").click()
                    browser.implicitly_wait(10)
                    bookingCell = browser.find_elements_by_class_name("timetable-cells")
                    if len(bookingCell) == 0:
                        pageOverload = True
                        browser.close()
                    else:
                        bookingCell[0].click()
                        bookingTime = browser.find_elements_by_id("timeSelectionText")
                        if len(bookingTime) == 0:
                            print("something went wrong")
                            browser.close()
                            return
                        else:
                            booking = bookingTime[0].text.split()
                            date = booking[0]
                            month = booking[1]
                            datum = browser.find_element_by_id("datepicker").get_attribute("value")
                            date = datum.split("-")
                            bookingDate = datetime.datetime(int(date[0]), int(date[1]), int(date[2]))
                            if bookingDate < lastDesiredDate:
                                foundTime = True
                                nextButton = browser.find_element_by_name("Next").click()
                                print('Time Booked')
                                print(bookingDate)
                            else:
                                time.sleep(7)
    return browser
def fillForm(browser,firstName,lastName,eMail,phoneNummber):
    inputFirstName = browser.find_element_by_id("Customers_0__BookingFieldValues_0__Value")
    inputLastName = browser.find_element_by_id("Customers_0__BookingFieldValues_1__Value")
    inputFirstName.send_keys(firstName)
    inputLastName.send_keys(lastName)
    browser.find_element_by_id("Customers_0__Services_0__IsSelected").click()
    browser.find_element_by_name("Next").click()

    browser.find_element_by_name("Next").click()

    inputEmail = browser.find_element_by_id("EmailAddress")
    inputConfirmEmail = browser.find_element_by_id("ConfirmEmailAddress")
    inputPhone = browser.find_element_by_id("PhoneNumber")
    inputConfirmPhone = browser.find_element_by_id("ConfirmPhoneNumber")

    inputEmail.send_keys(eMail)
    inputConfirmEmail.send_keys(eMail)
    inputPhone.send_keys(phoneNummber)
    inputConfirmPhone.send_keys(phoneNummber)

    browser.find_element_by_id("SelectedContacts_0__IsSelected").click()
    browser.find_element_by_id("SelectedContacts_1__IsSelected").click()

    browser.find_element_by_id("SelectedContacts_2__IsSelected").click()
    browser.find_element_by_id("SelectedContacts_3__IsSelected").click()

    browser.find_element_by_name("Next").click()

def main():
    firstName = input("skriv in förnamn: ")
    lastName = input("skriv in efternamn: ")
    eMail = input("skriv in E-post: ")
    phoneNummber = input("skriv in telefonnummer: ")
    day, month, year = [int(x) for x in input("Enter last desirable date(DD/MM/YYYY): ").split('/')]
    lastDesiredDate = datetime.datetime(year, month, day)
    browser = findTime(lastDesiredDate)
    fillForm(browser,firstName,lastName,eMail,phoneNummber)



    while True:
        a = 1



if __name__ == "__main__":
        main()