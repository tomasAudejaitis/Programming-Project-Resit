from bs4 import BeautifulSoup
from github import Github
import requests
import time
import json

class Gather:
    def __init__(self, github_token):
        """Initialize token."""
        self.g = Github(github_token)
        self.repos = []
        self.contributors_data = []
    
    def scrape_trending(self):
        """Scrape  trending page and fetch  data. Populates list."""
        url = 'https://github.com/trending'
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f"Failed to fetch trending page: HTTP {response.status_code}")
            return False
        
        soup = BeautifulSoup(response.text, 'html.parser')
        repo_list = soup.find_all('article', class_='Box-row')
        print(f"Found {len(repo_list)} repositories on trending page")
        
        if not repo_list:
            print("No repos found. Check if the 'Box-row' class has changed.")
            return False
        
        self.repos = []  # Clear any existing data
        for repo in repo_list:
            name_elem = repo.find('h2', class_='h3 lh-condensed')
            if not name_elem:
                print("No name  found for a repository, skipping...")
                continue
            name = name_elem.text.strip().replace('\n', '').replace(' ', '').replace('/', ' / ')
            repo_name = name.replace(' / ', '/')
            star_elem = repo.find('a', class_='Link--muted', href=lambda x: x and '/stargazers' in x)
            star_count = star_elem.text.strip().replace(',', '') if star_elem else '0'
            fork_elem = repo.find('a', class_='Link--muted', href=lambda x: x and '/forks' in x)
            fork_count = fork_elem.text.strip().replace(',', '') if fork_elem else '0'
            lang_elem = repo.find('span', itemprop='programmingLanguage')
            language = lang_elem.text.strip() if lang_elem else 'Unknown'
            try:
                repo_data = self.g.get_repo(repo_name)
                commits_count = repo_data.get_commits().totalCount
                contributors_count = repo_data.get_contributors().totalCount
            except Exception as e:
                print(f"Error fetching  data for {repo_name}: {e}")
                commits_count = contributors_count = 'N/A'
            self.repos.append({
                'name': name,
                'stars': star_count,
                'forks': fork_count,
                'language': language,
                'commits': commits_count,
                'contributors': contributors_count
            })
            time.sleep(0.05)  # Respect API rate limits
        return True
    def scrape_contributors(self):
        """Scrape trending page and get only the first 20 contributors """
        url = 'https://github.com/trending'
        headers = {'User-Agent': 'Mozilla/5.0'}
        print("Fetching trending page for contributors...")
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"Failed to fetch trending page: HTTP {response.status_code}")
            return False

        soup = BeautifulSoup(response.text, 'html.parser')
        repo_list = soup.find_all('article', class_='Box-row')
        print(f"Found {len(repo_list)} repositories on trending page")

        if not repo_list:
            print("No repositories found. Check if the 'Box-row' class has changed.")
            return False

        self.contributors_data = []  # Clear any existing contributor data
        for i, repo in enumerate(repo_list):
            print(f"Processing repository {i+1}/{len(repo_list)} for contributors...")
            name_elem = repo.find('h2', class_='h3 lh-condensed')
            if not name_elem:
                print("No name element found for a repository, skipping...")
                continue
            name = name_elem.text.strip().replace('\n', '').replace(' ', '').replace('/', ' / ')
            repo_name = name.replace(' / ', '/')
            print(f"Repository name: {repo_name}")

            try:
                repo_data = self.g.get_repo(repo_name)
                contributors_info = []
                print(f"Fetching up to 20 contributors for {repo_name}...")
                # Limit to first 20 contributors 
                for j, contributor in enumerate(repo_data.get_contributors()):
                    if j >= 20: 
                        print(f"Reached limit of 20 contributors for {repo_name}")
                        break
                    print(f"Processing contributor {j+1}/20: {contributor.login}...")
                    try:
                        commits = repo_data.get_commits(author=contributor.login)
                        commit_count = commits.totalCount
                        contributors_info.append({
                            'username': contributor.login,
                            'commit_count': commit_count
                        })
                        print(f"Added {contributor.login} with {commit_count} commits")
                    except Exception as e:
                        print(f"Error fetching commits for {contributor.login}: {e}")
                        contributors_info.append({
                            'username': contributor.login,
                            'commit_count': 'N/A'
                        })
                print(f"Collected {len(contributors_info)} contributors for {repo_name}")
                self.contributors_data.append({
                    'repo_name': name,
                    'contributors': contributors_info
                })
            except Exception as e:
                print(f"Error fetching API data for {repo_name}: {e}")
                self.contributors_data.append({
                    'repo_name': name,
                    'contributors': []
                })
            time.sleep(0.05)  
        return True
    
    def save_contributors_to_file(self, filename):
        """Save  to a JSON file."""
        # print(f"Attempting to save contributors to {filename}")
        # print(f"Contributors data: {self.contributors_data}")
        if not self.contributors_data:
            print("No contributor data to save")
            return False
        try:
            with open(filename, 'w') as f:
                json.dump(self.contributors_data, f, indent=4)
            print(f"Saved contributor data to {filename} in JSON format")
            return True
        except Exception as e:
            print(f"Error saving to {filename}: {e}")
            return False


    def get_repos(self):
        """Return repositories."""
        return self.repos
    
    def get_repo_by_name(self, name):
        """Return a specific repository by name, if it exists."""
        for repo in self.repos:
            if repo['name'] == name:
                return repo
        return None
    
    def get_repos_by_language(self, language):
        """Return repositories by language."""
        return [repo for repo in self.repos if repo['language'].lower() == language.lower()]
    
    def get_rate_limit(self):
        """Return API rate limit status."""
        return self.g.get_rate_limit()
    
    def save_to_file(self, filename):
        """Save repo to a JSON file."""
        if not self.repos:
            print("No repository data to save")
            return False
        
        try:
            with open(filename, 'w') as f:
                json.dump(self.repos, f, indent=4)
            print(f"Saved data to {filename} in JSON format")
            return True
        except Exception as e:
            print(f"Error saving to {filename}: {e}")
            return False
