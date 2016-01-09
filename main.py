MAX_NUMBER = 10
USER = "username"
PASSWORD = "password"
import re
import random

from selenium import webdriver
from pymongo import MongoClient

from locators import UserPageLocators
import page


client = MongoClient('localhost', 27017)
db = client.instadb
collection = db.parse_links


def login(driver):
    login_page = page.LoginPage(driver)
    login_page.login(USER, PASSWORD)


def get_valid_links(driver):
    main_page = page.MainPage(driver)
    main_page.click_view_all()
    all = [x for x in list(set(main_page.get_links())) if "com/p/-" not in x]
    return get_tag_links(all) + get_user_links(all) + get_locations_links(all)


def like(driver, selection):
    if driver is None or selection is None:
        return 0
    for num in selection:
        driver._click(photos[num])
        driver.like()
        driver.close()


def save_to_db(links):
    if collection.find({"_id": 1}, {"_id": 1}).limit(1).count():
        collection.update({"_id": 1}, {"$addToSet": {"links": {"$each": links}}})
    else:
        collection.insert_one({"_id": 1, "links": links})


def remove_from_db(link):
    collection.update({"_id": 1}, {"$pull": {"links": link}}, {"multi": True})


def get_tag_links(links):
    return [x for x in links if is_tag_link(x)]


def get_user_links(links):
    return [x for x in links if is_user_link(x)]


def get_locations_links(links):
    return [x for x in links if is_location_link(x)]


def is_user_link(link):
    m = re.compile(r"https://www.instagram.com/(\w+)/")
    return bool(m.match(link))


def is_tag_link(link):
    return "/explore/tags/" in link


def is_location_link(link):
    return "/explore/locations/" in link


if __name__ == '__main__':
    driver = webdriver.Firefox()
    driver.get("https://www.instagram.com/")
    login(driver)
    if not collection.find({"links.500": {"$exists": True}}).limit(1).count():
        all_links = get_valid_links(driver)
        random.shuffle(all_links)
        save_to_db(all_links)

    main_window = driver.current_window_handle
    asa = list(collection.find({"_id": 1}, {"links": 1, "_id": 0}))[0]["links"]
    for i in xrange(MAX_NUMBER / 2):
        link = random.choice(asa)
        photo_page = None
        selection = None
        if is_tag_link(link):
            photo_page = page.TagPage(driver)
            photo_page.open_in_new_window(link)
            driver.switch_to_window(driver.window_handles[-1])
            photos = photo_page.get_recent_photo()
            selection = random.sample(xrange(len(photos)), 2)

        elif is_location_link(link):
            photo_page = page.LocationPage(driver)
            photo_page.open_in_new_window(link)
            driver.switch_to_window(driver.window_handles[-1])
            photos = photo_page.get_photo()
            selection = random.sample(xrange(len(photos)), 2)

        elif is_user_link(link):
            photo_page = page.UserPage(driver)
            photo_page.open_in_new_window(link)
            driver.switch_to_window(driver.window_handles[-1])
            if len(photo_page.check_elements(UserPageLocators.PHOTOS)) == 0:
                driver.close()
                driver.switch_to_window(main_window)
                collection.update({"_id": 1}, {"$pull": {"links": link}})
                continue
            photos = photo_page.get_photo()
            selection = random.sample(xrange(len(photos) - 1), 2)
        like(photo_page, selection)
        driver.close()
        driver.switch_to_window(main_window)
        collection.update({"_id": 1}, {"$pull": {"links": link}})

    driver.delete_all_cookies()
    driver.close()

