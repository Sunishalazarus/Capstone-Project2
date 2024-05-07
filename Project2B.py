from Datass import data2B
from Locatorss import locator2B

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


class ValidateOrangeHRM1:

    def __init__(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.wait = WebDriverWait(self.driver, 10)

    def boot(self):
        self.driver.get(data2B.Webdata().url)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)

    def quit(self):
        self.driver.quit()

    def enterText(self, locator, textValue):
        element = self.wait.until(EC.visibility_of_element_located((By.NAME, locator)))
        element.clear()
        element.send_keys(textValue)

    def clickButton(self, locator):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, locator))).click()

    def mainMenu_validation(self):

        self.boot()

        username = data2B.Webdata().readData(4, 7)
        password = data2B.Webdata().readData(4, 8)

        try:
            self.enterText(locator2B.WebLocators().usernameLocator, username)
            self.enterText(locator2B.WebLocators().passwordLocator, password)
            self.clickButton(locator2B.WebLocators().loginButtonLocator)

            try:
                WebDriverWait(self.driver, 10).until(EC.alert_is_present())
                alert = self.driver.switch_to.alert
                alert.accept()
            except TimeoutException:
                print("No alert to accept.")

            if self.driver.current_url == data2B.Webdata().dashboardURL:
                self.clickButton(locator2B.WebLocators().adminPageLocator)
                self.clickButton(locator2B.WebLocators().pimLocator)
                self.clickButton(locator2B.WebLocators().leaveLocator)
                self.clickButton(locator2B.WebLocators().timeLocator)
                self.clickButton(locator2B.WebLocators().recruitmentLocator)
                self.clickButton(locator2B.WebLocators().myInfoLocator)
                self.clickButton(locator2B.WebLocators().performanceLocator)
                self.clickButton(locator2B.WebLocators().dashboardLocator)
                self.clickButton(locator2B.WebLocators().directoryLocator)
                self.clickButton(locator2B.WebLocators().claimLocator)
                self.clickButton(locator2B.WebLocators().buzzLocator)
                data2B.Webdata().writeData(4, 11, "SUCCESS")

            else:
                data2B.Webdata().writeData(4, 11, "FAILED")

        except NoSuchElementException as e:

            print("An error occurred:", e)

obj = ValidateOrangeHRM1()
obj.mainMenu_validation()
obj.quit()

"""
Output-
No alert to accept.
"""