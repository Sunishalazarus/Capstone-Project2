from Datass import data2A
from Locatorss import locator2A

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class ValidateOrangeHRM:

    def __init__(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.wait = WebDriverWait(self.driver, 10)

    def boot(self):
        self.driver.get(data2A.Webdata().url)
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

    def login_forgot_password(self):

        self.boot()

        # Username = 7
        # Password = 8
        # Test Results = 11

        # Rows - 2 to 4

        for row in range(2, 3):
            username = data2A.Webdata().readData(row, 7)

            try:

                self.clickButton(locator2A.WebLocators().forgotPasswordLinkLocator)
                self.enterText(locator2A.WebLocators().usernameLocator, username)
                self.clickButton(locator2A.WebLocators().resetButtonLocator)

                try:

                    reset_locator = (By.XPATH, locator2A.WebLocators().resetPasswordLinkLocator)
                    WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(reset_locator))
                    reset_message = self.driver.find_element(*reset_locator).text
                    print("Reset message:", reset_message)
                except TimeoutException:
                    print("No Error message")

                data2A.Webdata().writeData(row, 11, "SUCCESS")

            except NoSuchElementException as e:

                print("An error occurred:", e)


    def header_validation(self):

        self.boot()

        for row in range(3, 4):
            username = data2A.Webdata().readData(row, 7)
            password = data2A.Webdata().readData(row, 8)

            try:
                self.enterText(locator2A.WebLocators().usernameLocator, username)
                self.enterText(locator2A.WebLocators().passwordLocator, password)
                self.clickButton(locator2A.WebLocators().loginButtonLocator)

                try:
                    WebDriverWait(self.driver, 10).until(EC.alert_is_present())
                    alert = self.driver.switch_to.alert
                    alert.accept()
                except TimeoutException:
                    print("No alert to accept.")

                try:
                    title = self.driver.title
                    print("Page Title:", title)

                except Exception as e:
                    print("Failed to fetch page title", e)

                if self.driver.current_url == data2A.Webdata().dashboardURL:

                    self.clickButton(locator2A.WebLocators().adminPageLocator)
                    self.clickButton(locator2A.WebLocators().userManagementLocator)
                    self.clickButton(locator2A.WebLocators().jobLocator)
                    self.clickButton(locator2A.WebLocators().organizationLocator)
                    self.clickButton(locator2A.WebLocators().qualificationsLocator)
                    self.clickButton(locator2A.WebLocators().nationalitiesLocator)
                    self.clickButton(locator2A.WebLocators().corporateLocator)
                    self.clickButton(locator2A.WebLocators().configurationLocator)

                    data2A.Webdata().writeData(row, 11, "SUCCESS")
                    return title

                else:
                    data2A.Webdata().writeData(row, 11, "FAILED")

            except NoSuchElementException as e:

                print("An error occurred:", e)


obj = ValidateOrangeHRM()
obj.login_forgot_password()
obj.header_validation()
obj.quit()


"""
Output-
Reset message: Reset Password link sent successfully
No alert to accept.
Page Title: OrangeHRM
"""