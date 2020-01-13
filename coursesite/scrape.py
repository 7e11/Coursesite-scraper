from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time
import json
import urllib.parse
import re



def get_authenticated_firefox():
    desired = DesiredCapabilities.FIREFOX
    desired['loggingPrefs'] = {'browser': 'ALL'}
    driver = webdriver.Firefox(executable_path='../geckodriver.exe', desired_capabilities=desired)
    authenticate_driver(driver)
    return driver


def authenticate_driver(driver):
    # Initialization
    url_login_button = r'https://coursesite.lehigh.edu/auth/saml/login.php'
    url_login = r'https://coursesite.lehigh.edu/auth/saml/index.php?wantsurl=https%3A%2F%2Fcoursesite.lehigh.edu%2F'
    # Disabled this wait because it makes crawling slow when elements can sometimes exist, sometimes not.
    # Use explicit waits instead.
    # driver.implicitly_wait(5)   # Wait up to 5 seconds for stuff to exist
    with open('./credentials.txt', 'r') as credential_file:
        username = credential_file.readline().rstrip()
        password = credential_file.readline().rstrip()

    # Logging in (Button page)
    driver.get(url_login_button)
    driver.find_element_by_class_name('lu-login-button').click()
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'username')))
    except TimeoutException:
        # Maybe it just logs us in again without asking for credentials?
        if driver.find_elements_by_xpath(r'''//header[@id='page-header']'''):
            print('authenticated without username and password (?)')
            return
        else:
            raise Exception

    # Logging in (username & password page)
    driver.find_element_by_id('username').send_keys(username)
    driver.find_element_by_id('password').send_keys(password)
    driver.find_element_by_id('regularsubmit').click()

    # See https://selenium-python.readthedocs.io/waits.html
    # Wait until the page header is visible.
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, r'''//header[@id='page-header']''')))
    # //header[@id='page-header']


def session_from_driver(driver):
    '''
    Copies cookies from a webdriver to a new requests session
    :param driver: A selenium webdriver
    :return: A requests session
    '''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
    }
    s = requests.session()
    s.headers.update(headers)
    s.cookies.update({c['name']: c['value'] for c in driver.get_cookies()})
    return s


def parse_valid_user_page(user_id, driver):
    # Scrape name
    name = driver.find_element_by_xpath(r'''//div[@class='page-header-headings']/h1''').text

    # Scraping the image info
    image_element = driver.find_element_by_xpath(r'''//div[@class='page-header-image']/a/img''')
    image_title = image_element.get_attribute('title')
    image_link = image_element.get_attribute('src')
    is_default_image = 'defaultuserpic' in image_element.get_attribute('class')

    # Scraping User Description (May not exist)
    try:
        description = driver.find_element_by_xpath(r'''//div[@class='description']''').text
    except NoSuchElementException:
        description = ''

    #   Scraping the profile tree:
    profile_tree = driver.find_element_by_xpath(r'''//div[@class='profile_tree']''')
    # Scraping User Details (May not exist. Thats OK though, because the selenium array will just be empty. no nodes.)
    user_details = {}
    user_detail_content_nodes = profile_tree.find_elements_by_xpath(
        r'''//*[text()='User details']/following-sibling::ul/li[@class='contentnode']''')
    # If the
    # A variable number of arguments, many of different types can exist:
    for node in user_detail_content_nodes:
        key = node.find_element_by_xpath(r'''dl/dt''').text
        val = node.find_element_by_xpath(r'''dl/dd''').text
        user_details[key] = val

    # TODO: Scraping User Badges (May not exist)
    badges = []
    badges_a = profile_tree.find_elements_by_xpath(r'''//*[@class='badges']/li/a''')
    for a in badges_a:
        badge_link = a.get_attribute('href')
        badge_image_link = a.find_element_by_class_name('badge-image').get_attribute('src')
        badge_name = a.find_element_by_class_name('badge-name').text
        badges.append({'badge_name': badge_name, 'badge_link': badge_link, 'badge_image_link': badge_image_link})

    # Create our user dictionary
    user = {'id': user_id, 'name': name, 'image_title': image_title, 'image_link': image_link,
            'is_default_image': is_default_image, 'description': description, 'user_details': user_details,
            'badges': badges, 'account_status': 'valid'}
    return user

def scrape_single_user(user_id, driver):
    # The page doesn't use AJAX to load, so we don't need any waits.
    driver.get(r'https://coursesite.lehigh.edu/user/profile.php?id=' + str(user_id))

    # Our session expires every hour, so check if we're back at the login screen.
    if 'Log in' in driver.title:
        print('authenticating')
        authenticate_driver(driver)
        driver.get(r'https://coursesite.lehigh.edu/user/profile.php?id=' + str(user_id))

    # Check if it's an invalid user (or a deleted user)
    if '' == driver.title:
        user = {'id': user_id, 'account_status': 'invalid'}
    # Check if it's a private (?) user. Not sure what this means.
    elif 'Home: User' == driver.title:
        user = {'id': user_id, 'account_status': 'accessdenied'}
    # Check if it's some other kind of error (unexpected)
    elif 'Public profile' not in driver.title:
        user = {'id': user_id, 'account_status': 'other'}
        print(user)
    # Otherwise it's a valid user page
    else:
        user = parse_valid_user_page(user_id, driver)
        print(user)

    return user

def scrape_all_users(driver):
    users = []
    for user_id in range(66_001, 90_000):
        users.append(scrape_single_user(user_id, driver))

        if user_id % 1 == 0:
            with open('users66001.json', 'w') as outfile:
                json.dump(users, outfile)

        # This is for rate limiting.
        time.sleep(0.5)

    with open('users66001.json', 'w') as outfile:
        json.dump(users, outfile)


def scrape_classes(driver):
    authenticate_driver(driver)
    driver.get(r'https://coursesite.lehigh.edu/')
    classes = []
    class_links = driver.find_elements_by_xpath(r'''//p[starts-with(@id, 'expandable_branch')]/a''')
    for a in class_links:
        class_link = a.get_attribute('href')
        class_title = a.get_attribute('title')
        class_text = a.text
        class_id = int(class_link.split('?id=')[1])
        # https://coursesite.lehigh.edu/course/view.php?id=135711
        # Has a user page of:
        # https://coursesite.lehigh.edu/user/index.php?id=135711
        class_participants_link = 'https://coursesite.lehigh.edu/user/index.php?id=' + str(class_id) + '&perpage=10000'
        classes.append({'class_id': class_id, 'class_title': class_title, 'class_text': class_text, 'class_link': class_link, 'class_participants_link': class_participants_link})

    # Now get the participants:
    for c in classes:
        if c['class_id'] == 70682 or c['class_id'] == 75536:
            # Skip getting participants for the compliance course and LUAlly
            c['participants'] = []
        else:
            c['participants'] = scrape_participants(c['class_participants_link'], driver)


    print(classes)
    with open('classes.json', 'w') as outfile:
        json.dump(classes, outfile)



def scrape_participants(link, driver):
    driver.get(link)
    table = driver.find_element_by_xpath(r'''//table[@id='participants']''')
    columns = [th.text for th in table.find_elements_by_xpath(r'''thead/tr/th''')]
    print(columns)
    rows = table.find_elements_by_xpath(r'''tbody/tr[@class='']''')
    # Lots of invisible, empty rows are added at the bottom, with class 'emptyrow'. Want to avoid those.
    participants = []
    for r in rows:
        # Do the ID first
        user_link = r.find_element_by_xpath(r'''td/a''').get_attribute('href')
        query_string = urllib.parse.urlparse(user_link).query
        user_id = int(urllib.parse.parse_qs(query_string)['id'][0])

        # Do the entires
        entries = r.find_elements_by_xpath(r'''td''')
        participant = {'user_id': user_id, **dict(zip(columns, [td.text for td in entries]))}
        participants.append(participant)
    print(participants)
    return participants


if __name__ == '__main__':
    # with get_authenticated_firefox() as driver:
    #     scrape_all_users(driver)
    # with webdriver.Firefox(executable_path='../geckodriver.exe') as driver:
    driver = webdriver.Firefox(executable_path='../geckodriver.exe')
    scrape_all_users(driver)
    # scrape_classes(driver)