from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from elements import LoginPageUserName, LoginPagePassword
from locators import LoginPageLocator, MainPageLocator, TagPageLocator, LocationPageLocator, UserPageLocators


class BasePage(object):
    def __init__(self, driver):
        self.driver = driver

    def _click(self, element):
        obj = self._get_element(element)
        obj.click()

    def _get_element(self, element):
        if type(element) is WebElement:
            return element
        try:
            WebDriverWait(self.driver, 30).until(
                lambda driver: self.driver.find_element(*element)
            )
        finally:
            WebDriverWait(self.driver, 15).until(
                lambda driver: self.driver.find_element(*element)
            )
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(element))
        return self.driver.find_element(*element)

    def _get_elements(self, element):
        try:
            WebDriverWait(self.driver, 25).until(
                lambda driver: self.driver.find_elements(*element)
            )
        finally:
            WebDriverWait(self.driver, 5).until(
                lambda driver: self.driver.find_elements(*element)
            )
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(element))
        return self.driver.find_elements(*element)

    def _get_child_element(self, parent, child):
        try:
            WebDriverWait(self.driver, 30).until(
                lambda driver: parent.find_element(*child)
            )
        finally:
            WebDriverWait(self.driver, 15).until(
                lambda driverl: parent.find_element(*child)
            )
        return parent.find_element(*child)

    def _get_child_elements(self, parent, child):
        try:
            WebDriverWait(self.driver, 30).until(
                lambda driver: parent.find_elements(*child)
            )
        finally:
            WebDriverWait(self.driver, 15).until(
                lambda driverl: parent.find_elements(*child)
            )
        return parent.find_elements(*child)

    def _get_text(self, element):
        obj = self._get_element(element)
        value = obj.get_attribute("value")
        text = obj.text
        if value:
            return value
        return text

    def _get_href(self, element):
        return self._get_element(element).get_attribute("href")

    def _get_handler(self):
        return self.driver.current_window_handle()

    def open_in_new_window(self, url):
        script = "$(window.open('%s'))" % url
        self.driver.execute_script(script)

    def check_elements(self, obj):
        result = self.driver.find_elements(*obj)
        return result


class LoginPage(BasePage):
    username = LoginPageUserName()
    password = LoginPagePassword()

    def login(self, username, password):
        self.username = username
        self.password = password
        self._click(LoginPageLocator.BUTTON)


class MainPage(BasePage):
    def click_view_all(self):
        buttons = self._get_elements(MainPageLocator.VIEW_ALL)
        for button in buttons:
            self._click(button)

    def get_links(self):
        body = self._get_element(MainPageLocator.BODY)
        aa = self._get_child_elements(body, MainPageLocator.LINKS)
        ee = self._get_elements(MainPageLocator.LINKS)
        return [self._get_href(x) for x in ee]

    def get_window_handler(self):
        return self.driver.current_window_handle()


class UserPage(BasePage):
    def random_click(self):
        pass

    def get_photo(self):
        return self._get_elements(UserPageLocators.PHOTOS)

    def like(self):
        self._click(TagPageLocator.LIKE)

    def close(self):
        self._click(TagPageLocator.CLOSE)


class TagPage(BasePage):
    def get_recent_photo(self):
        return self._get_elements(TagPageLocator.MOST_RECENT)

    def like(self):
        self._click(TagPageLocator.LIKE)

    def close(self):
        self._click(TagPageLocator.CLOSE)


class LocationPage(BasePage):
    def get_photo(self):
        return self._get_elements(LocationPageLocator.PHOTO)

    def like(self):
        self._click(TagPageLocator.LIKE)

    def close(self):
        self._click(TagPageLocator.CLOSE)