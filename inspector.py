from bs4 import BeautifulSoup
from selenium import webdriver

def get_github_info(url):
    driver = webdriver.Chrome()
    driver.get(url)
    content = driver.page_source.encode("utf-8").strip()
    github_soup = BeautifulSoup(content, 'html.parser')

    name_container = github_soup.find('strong', {"itemprop":"name"})
    repo_name = name_container.find('a').text.strip()

    author = github_soup.find('a', {"rel":"author"}).text.strip()

    issues = github_soup.find('span', {"id":"issues-repo-tab-count"}).text.strip()
    
    pull_requests = github_soup.find('span', {"id":"pull-requests-repo-tab-count"}).text.strip()
    
    star_icon = github_soup.find('svg', {"class":"octicon octicon-star mr-2"})
    stars = star_icon.find_next_sibling("strong").text.strip()
    
    watch_icon = github_soup.find('svg', {"class":"octicon octicon-eye mr-2"})
    watchers = watch_icon.find_next_sibling("strong").text.strip()
    
    fork_icon = github_soup.find_all('svg', {"class":"octicon octicon-repo-forked mr-2"})[1]
    forks = fork_icon.find_next_sibling("strong").text.strip()
    
    print("{} by {}: {} issues, {} PRs, {} stars, {} watchers, {} forks".format(repo_name, author, issues, pull_requests, stars, watchers, forks))



get_github_info("https://github.com/CodeYourFuture/node-challenge-chat-server")