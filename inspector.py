from bs4 import BeautifulSoup
from selenium import webdriver
from lxml import etree

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

    print("{} by {}: {} issues, {} PRs, {} stars, {} watchers, {} forks, languages {}".format(repo_name, author, issues, pull_requests, stars, watchers, forks, languages))



get_github_info("https://github.com/CodeYourFuture/node-challenge-chat-server")

