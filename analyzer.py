import json
import os


class RepoAnalyzer:
    def __init__(self, filename='data.json'): 
        """Initialize by loading repository data from a JSON file."""
        self.repos = []
        self.filename = filename
        
        if os.path.exists(filename):
            try:
                with open(filename, 'r') as f:
                    self.repos = json.load(f)
                print(f"Loaded {len(self.repos)} repositories from {filename}")
            except Exception as e:
                print(f"Error loading {filename}: {e}")
        else:
            print(f"File {filename} does not exist")           
        if not self.repos:
            print("No repositories to analyze")
            raise ValueError(f"No valid data available")


    def execute(self):
        """Execute analysis tasks."""
        
        
    def getAverageContributors(self):
        """Return the average number of contributors across all repositories."""
        valid_contributors = [int(repo['contributors']) for repo in self.repos if repo['contributors'] != 'N/A']
        if not valid_contributors:
            return None
        return sum(valid_contributors) / len(valid_contributors)
    
    def rankByField(self, rank):
        #Return repos ranked by the specified numeric field in descending order.

        valid_repos = [repo for repo in self.repos if repo[rank] != 'N/A']    
        sorted_repos = sorted(valid_repos, key=lambda x: int(x[rank]), reverse=True)
        return sorted_repos
        
    
    def percentageByCategory(self, category_field, value_field):
        valid_repos = [repo for repo in self.repos if repo[value_field] != 'N/A']
        if not valid_repos:
            raise ValueError(f"No json data for {value_field} available")      
        category_sums = {}
        for repo in valid_repos:
            category = repo[category_field]
            value = int(repo[value_field])
            category_sums[category] = category_sums.get(category, 0) + value
        total_value = sum(category_sums.values())
        result = [
            {
                'category': category,
                'total': total,
                'percentage': (total / total_value) * 100
            }
            for category, total in sorted(category_sums.items(), key=lambda x: x[1], reverse=True)
        ]
        return result
    def rankTopContributors(self, contributors_filename='contributorData.json'):
        """Return the top 20 contributors across all repositories ranked by commit count."""
        with open(contributors_filename, 'r') as f:
                contributors_data = json.load(f)
        all_contributors = []
        for repo in contributors_data:
            repo_name = repo['repo_name']
            for contributor in repo['contributors']:
                if contributor['commit_count'] != 'N/A':
                    all_contributors.append({
                        'username': contributor['username'],
                        'repo_name': repo_name,
                        'commit_count': int(contributor['commit_count'])
                    })
        sorted_contributors = sorted(all_contributors, key=lambda x: x['commit_count'], reverse=True)[:20]
        
        medal = {1:'🥇', 2: '🥈',3:'🥉' }
        for i, contributor in enumerate(sorted_contributors, 1):
            if i <4:
                contributor['ranking'] = medal.get(i)
            else:
                suffix = 'th'
                contributor['ranking'] = f"{i}{suffix}"       
        return sorted_contributors
