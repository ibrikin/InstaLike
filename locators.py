from selenium.webdriver.common.by import By


class LoginPageLocator(object):
    USERNAME = (By.XPATH, ".//*[@name='username']")
    PASSWORD = (By.XPATH, ".//*[@name='password']")
    BUTTON = (By.XPATH, ".//*/form/button")


class MainPageLocator(object):

    BODY = (By.XPATH, ".//body/span/section/main/section")
    LINKS = (By.XPATH, ".//*/article//a")
    VIEW_ALL = (By.XPATH, ".//*/article//li/button")

class TagPageLocator(object):

    MOST_RECENT = (By.CSS_SELECTOR, "article>div+h2+div>div>div>a")
    LIKE = (By.CSS_SELECTOR, "section+ul+section>a")
    CLOSE = (By.CSS_SELECTOR, "body>div>div>button")

class LocationPageLocator(object):

    PHOTO = (By.CSS_SELECTOR, "article>div+h2+div>div>div>a")

class UserPageLocators(object):

    PHOTOS = (By.CSS_SELECTOR, "article>div  div>div>a")