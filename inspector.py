from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from lxml import etree
from time import sleep
import argparse
import sys

def get_github_info(url):
    driver = webdriver.Chrome()
    driver.get(url)
    content = driver.page_source.encode("utf-8").strip()
    github_soup = BeautifulSoup(content, 'html.parser')
    dom = etree.HTML(str(github_soup))
    
    repo_name = dom.xpath('//strong[@itemprop="name"]/a')[0].text
    author = dom.xpath('//a[@rel="author"]')[0].text
    issues = dom.xpath('//span[@id="issues-repo-tab-count"]')[0].text
    pull_requests = dom.xpath('//span[@id="pull-requests-repo-tab-count"]')[0].text
    stars = dom.xpath('//svg[@class="octicon octicon-star mr-2"]/following-sibling::strong')[0].text
    watchers = dom.xpath('//svg[@class="octicon octicon-eye mr-2"]/following-sibling::strong')[0].text
    forks = dom.xpath('//svg[@class="octicon octicon-repo-forked mr-2"]/following-sibling::strong')[0].text
    languages = []
    languages_list = dom.xpath('//div[h2/text()="Languages"]/ul//span[contains(@class,"text-bold")]')
    for item in languages_list:
        languages.append(item.text)

    #fork_icon = github_soup.find_all('svg', {"class":"octicon octicon-repo-forked mr-2"})[1]
    #forks = fork_icon.find_next_sibling("strong").text.strip()
    return {
        'repo_name': repo_name,
        'author': author,
        'issues': issues,
        'pull_requests': pull_requests,
        'stars': stars,
        'watchers': watchers,
        'forks': forks,
        'languages': languages
    }

def ig_login(driver, username, password):
    sleep(2)
    driver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
    sleep(3)

    cookie_button = driver.find_element(By.XPATH, "//div[@role='dialog']//button[@tabindex='0']")
    cookie_button.click()
    username_el = driver.find_element(By.NAME, 'username')
    username_el.send_keys(username)
    password_el = driver.find_element(By.NAME, 'password')
    password_el.send_keys(password)

    #instead of searching for the Button (Log In) you can simply press enter when you already selected the password or the username input element.
    submit = driver.find_element(By.TAG_NAME, 'form')
    sleep(10)
    submit.submit()
    sleep(10)
    # not now
    save_login_info_button= driver.find_element(By.XPATH, "//button[text()='Not Now']")
    save_login_info_button.click()
    sleep(2)

def scroll(driver, timeout):
    scroll_pause_time = timeout

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    sleep(scroll_pause_time)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        # If heights are the same it will exit the function
        return
    last_height = new_height


def ig_get_posts_for_hashtag(driver, hashtag, min_images_required):
    driver.get('https://www.instagram.com/explore/tags/' + hashtag) # Load the page at the given url with the #Hashtag
    sleep(15)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # Scrolls to the ZERO position (horizontal)

    posts = set()
    while len(posts) < min_images_required:
        old_count = len(posts)
        data = BeautifulSoup(driver.page_source, 'html.parser')
        dom = etree.HTML(str(data))
        links = dom.xpath('//a[starts-with(@href, "/p/")]')
        for link in links:
            page_url = link.attrib['href']
            posts.add(page_url)
        scroll(driver, 3)
        if old_count == len(posts): # No new images loaded - exit
            break
    print(len(posts), " Images Found")
    return list(posts)

def ig_get_post_info(driver, post_url):
    driver.get('https://www.instagram.com' + post_url) # Load the page at the given url with the #Hashtag
    sleep(10)
    cookie_button = driver.find_element(By.XPATH, "//div[@role='dialog']//button[@tabindex='0']")
    cookie_button.click()
    content = driver.page_source.encode("utf-8").strip()
    data = BeautifulSoup(content, 'html.parser')
    dom = etree.HTML(str(data))
    author = dom.xpath('//header//a')[0].text
    post_text = dom.xpath('//h2/following-sibling::div//span/text()')
    print(post_text)
    #print(etree.tostring(post_text, pretty_print = True))

    post_tags = dom.xpath('//a[starts-with(text(), "#")]')
    tags = []
    for item in post_tags:
        tags.append(item.text)
    print("Author {}, Text {}, Tags {} ".format(author, post_text, tags))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', help='Github repo URL')
    args = parser.parse_args()
    github_url = args.url
    if github_url:
        sys.stdout.write(str(get_github_info(github_url)))

if __name__ == '__main__':
    main()

# repo_data = get_github_info("https://github.com/CodeYourFuture/node-challenge-chat-server")
# print(repo_data)

# driver = webdriver.Chrome()
# ig_login(driver, "username", "password")
# hashtag = 'disneymerch' # This assigns the #hashtag that will be searched for in Instagram
# posts = ig_get_posts_for_hashtag(driver, hashtag, 20)
# print(posts)
# ig_get_post_info(driver, '/p/CleF8YIuiHH/')
