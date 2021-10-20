from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import (
    TimeoutException,
    ElementClickInterceptedException,
    StaleElementReferenceException,
    ElementNotInteractableException
)
import re


# Здесь следует указать путь к веб драйверу используемого браузера.
PATH_TO_DRIVER = r'D:\chromedriver\chromedriver.exe'
FIRST_PAGE_URL = (
        'https://market.yandex.ru/catalog--smartfony/54726/list' +
        '?show-reviews=1&cpa=0&onstock=0&hid=91491&local-offers-first=0'
)


def main():
    driver = get_driver()
    open_first_page(driver)
    is_last_page = False
    while not is_last_page:
        parse_from_current_page(driver)
        is_last_page = open_next_page(driver)
    driver.close()


def get_driver():
    return webdriver.Chrome(PATH_TO_DRIVER)


def open_first_page(driver):
    driver.get(FIRST_PAGE_URL)


def parse_from_current_page(driver):
    while True:
        try:
            links_to_reviews = get_links_to_reviews(driver)
            for link in links_to_reviews:
                link.click()
                driver.switch_to.window(driver.window_handles[1])
                parse_reviews(driver)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
            return
        except ElementClickInterceptedException:
            print('ElementClickInterceptedException in parse_from_current_page')
            continue
        except StaleElementReferenceException:
            print('StaleElementReferenceException in parse_from_current_page')
            continue


def get_links_to_reviews(driver):
    while True:
        try:
            links_to_reviews_located = expected_conditions.presence_of_all_elements_located(
                (By.LINK_TEXT, 'Читать все отзывы')
            )
            wait = WebDriverWait(driver, 120)
            links_to_reviews = wait.until(links_to_reviews_located)
            return links_to_reviews
        except TimeoutException:
            print('TimeoutException in get_links_to_reviews')
            continue


def parse_reviews(driver):
    is_last_reviews_page = False
    while not is_last_reviews_page:
        parse_reviews_on_current_page(driver)
        is_last_reviews_page = open_next_page(driver)
    return


def parse_reviews_on_current_page(driver):
    while True:
        try:
            reviews_located = expected_conditions.presence_of_all_elements_located(
                (By.XPATH, '//div[@data-zone-name="product-review"]')
            )
            wait = WebDriverWait(driver, 120)
            reviews = wait.until(reviews_located)
            for review in reviews:
                parse_review(review)
            return
        except TimeoutException:
            print('TimeoutException in parse_reviews')
            continue
        except StaleElementReferenceException:
            print('StaleElementReferenceException in parse_reviews_on_current_page')
            continue


def parse_review(review):
    rating = review.find_element_by_xpath('descendant::div[@data-rate]').get_attribute('data-rate')
    text_elements = review.find_elements_by_xpath('descendant::dd')[1:4]
    text_joined = ' '.join(element.text for element in text_elements)
    text_clean = re.sub('[\n\r]', ' ', text_joined).strip()
    with open('data_ym_raw.tsv', 'a', encoding='utf-8') as f:
        f.write(text_clean + '\t' + rating + '\n')


def open_next_page(driver):
    while True:
        try:
            next_page_button_located = expected_conditions.presence_of_element_located(
                (By.XPATH, '//a[@aria-label="Следующая страница"]')
            )
            wait = WebDriverWait(driver, 30)
            next_page_button = wait.until(next_page_button_located)
            next_page_button.click()
            return False
        except TimeoutException:
            print('TimeoutException in open_next_page')
            return True
        except ElementClickInterceptedException:
            print('ElementClickInterceptedException in open_next_page')
            continue
        except StaleElementReferenceException:
            print('StaleElementReferenceException in open_next_page')
            continue
        except ElementNotInteractableException:
            print('ElementNotInteractableException in open_next_page')
            continue


main()
