from selenium.webdriver.support.ui import WebDriverWait

from locators import LoginPageLocator


class BasePageElement(object):

    def __get__(self, instance, owner):
        driver = instance.driver
        WebDriverWait(driver, 30).until(
            lambda driver: driver.find_element(*self.locator)
        )
        element = driver.find_element(*self.locator)
        return element.get_attribute("value")

    def __set__(self, instance, value):
        driver = instance.driver
        WebDriverWait(driver, 30).until(
            lambda driver: driver.find_element(*self.locator)
        )
        driver.find_element(*self.locator).send_keys(value)


class LoginPageUserName(BasePageElement):
    locator = LoginPageLocator.USERNAME


class LoginPagePassword(BasePageElement):
    locator = LoginPageLocator.PASSWORD