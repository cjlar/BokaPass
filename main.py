import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import os
import datetime


# os.environ['PATH'] += "Add chromedriver path here if needed"
def findTime(lastDesiredDate, firstDesiredDate, sections, numberOfPeople):
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
            select = Select(browser.find_element_by_id("NumberOfPeople"))
            select.select_by_visible_text(str(numberOfPeople))
            acceptInfoCheckBox = browser.find_element_by_id("AcceptInformationStorage")
            acceptInfoCheckBox.click()
            nextButton = browser.find_element_by_name("Next")
            nextButton.click()
            for i in range(0, numberOfPeople):
                boendeId = "ServiceCategoryCustomers_{}__ServiceCategoryId".format(i)
                print("boendeId is {}".format(i))
                boendeButton = browser.find_elements_by_id(boendeId)
                boendeButton[0].click()
            if len(boendeButton) == 0:
                print("Something wrong loading the page")
                return
            else:
                browser.find_element_by_name("Next").click()
                while not pageOverload and not foundTime:
                    browser.find_element_by_name("TimeSearchFirstAvailableButton").click()
                    browser.implicitly_wait(3)
                    bookingCell = browser.find_elements_by_class_name("timetable-cells")
                    if len(bookingCell) == 0:
                        pageOverload = True
                        browser.close()
                    else:
                        bookingCell[0].click()
                        bookingTime = browser.find_elements_by_id("timeSelectionText")
                        sectionText = browser.find_elements_by_id("sectionSelectionText")
                        if len(bookingTime) == 0:
                            print("something went wrong")
                            browser.close()
                            return
                        else:
                            booking = bookingTime[0].text.split()
                            place = sectionText[0].text
                            date = booking[0]
                            month = booking[1]
                            datum = browser.find_element_by_id("datepicker").get_attribute("value")
                            date = datum.split("-")
                            bookingDate = datetime.datetime(int(date[0]), int(date[1]), int(date[2]))
                            if bookingDate < lastDesiredDate and bookingDate > firstDesiredDate and list_contains(sections, place):
                                foundTime = True
                                nextButton = browser.find_element_by_name("Next").click()
                                browser.implicitly_wait(3)

                                print('Time Booked')
                                print(bookingDate)
                            else:
                                try:
                                    error = browser.find_elements_by_css_selector("validation-summary-errors")[0].text
                                    if error.contains("en stund"):
                                        print("aborting")
                                        return
                                except Exception as e:
                                    print("Exception")
                                    print(e)
                                    time.sleep(1)
    return browser
def fillCustomerForm(browser,firstName,lastName, index):
    inputFirstName = browser.find_element_by_id("Customers_{}__BookingFieldValues_0__Value".format(index))
    inputLastName = browser.find_element_by_id("Customers_{}__BookingFieldValues_1__Value".format(index))
    inputFirstName.send_keys(firstName)
    inputLastName.send_keys(lastName)
    browser.find_element_by_id("Customers_{}__Services_0__IsSelected".format(index)).click()
    
def fillContactForm(browser,eMail,phoneNummber):
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


def list_contains(lst, string):
   for v in lst:
      if string in v:
         return True
   return False

def main():
    firstNames = input("First Names (split by comma): ").split(',')
    lastNames = input("Last Names (split by comma): ").split(',')
    assert(len(firstNames) == len(lastNames))
    eMail = input("skriv in E-post: ")
    phoneNummber = input("skriv in telefonnummer: ")
    day, month, year = [int(x) for x in input("Enter last desirable date(DD/MM/YYYY): ").split('/')]
    firstday, firstmonth, firstYear = [int(x) for x in input("Enter first desirable date(DD/MM/YYYY): ").split('/')]
    lastDesiredDate = datetime.datetime(year, month, day)
    firstDesiredDate = datetime.datetime(firstYear, firstmonth, firstday)
    numberOfPeople = int(input("How many persons?: "))
    assert(len(firstNames) == numberOfPeople)
    sections = ["Globen", "Solna", "Sthlm City"]
    browser = findTime(lastDesiredDate, firstDesiredDate, sections, numberOfPeople)
    for i in range(0,len(firstNames)):
        fillCustomerForm(browser,firstNames[i],lastNames[i], i)
    fillContactForm(browser, eMail, phoneNummber)



    while True:
        a = 1



if __name__ == "__main__":
        main()