import requests
from bs4 import BeautifulSoup
from github import Github
import time

#my github token to use github api/other set up
g = Github('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')  

url = 'https://github.com/trending'

# Send a GET request to fetch the page
headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')


repo_list = soup.find_all('article', class_='Box-row')

repos = []
for repo in repo_list:
    # Extract different elements via webscraping: repository name
    name_elem = repo.find('h2', class_='h3 lh-condensed')
    name = name_elem.text.strip().replace('\n', '').replace(' ', '').replace('/', ' / ')
    repo_name = name.replace(' / ', '/')

    # Star count
    star_elem = repo.find('a', class_='Link--muted', href=lambda x: x and '/stargazers' in x)
    star_count = star_elem.text.strip().replace(',', '') if star_elem else '0'

    # fork count
    fork_elem = repo.find('a', class_='Link--muted', href=lambda x: x and '/forks' in x)
    fork_count = fork_elem.text.strip().replace(',', '') if fork_elem else '0'

    # language
    lang_elem = repo.find('span', itemprop='programmingLanguage')
    language = lang_elem.text.strip() if lang_elem else 'Unknown'

    # Extract different elements via GitHub API: commits and contributors 
    try:
        repo_data = g.get_repo(repo_name)
        commits_count = repo_data.get_commits().totalCount
        contributors_count = repo_data.get_contributors().totalCount
    except Exception as e:
        print(f"Error fetching API data for {repo_name}: {e}")
        commits_count = contributors_count = 'N/A'

    # Only keep desired fields in repos[]
    repos.append({
        'name': name,
        'stars': star_count,
        'forks': fork_count,
        'language': language,
        'commits': commits_count,
        'contributors': contributors_count
    }) 
    # delay tonot exceed API rate limits
    time.sleep(0.5)

    

# Printing data as test
for repo in repos:
    print(repo)






