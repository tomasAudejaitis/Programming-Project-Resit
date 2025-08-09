import os
from Gather import Gather
from analyzer import RepoAnalyzer

if __name__ == "__main__":
    # Load GitHub token from environment variable
    github_token = os.getenv('GITHUB_TOKEN') or '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'
    
    # Create Gather instance and scrape data
    gather = Gather(github_token)
    if gather.scrape_trending():
        # Save data to JSON file
        gather.save_to_file('data.json')
        gather.scrape_contributors()
        gather.save_contributors_to_file("contributorData.json")
    #    gather.save_contributors_to_file('contributorData.json')
        
        # Create RepoAnalyzer instance and execute analysis
        analyzer = RepoAnalyzer(filename='data.json')
        analyzer.execute()
        analyzer.percentageByCategory('language', 'commits')
    else:
        print("Failed to scrape trending repositories")