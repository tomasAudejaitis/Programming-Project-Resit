import os
from Gather import Gather
from analyzer import RepoAnalyzer
from Frontend import Frontend

if __name__ == "__main__":
    
    github_token = os.getenv('GITHUB_TOKEN') 
    
   
    gather = Gather(github_token)
    gather.scrape_trending()
    gather.save_to_file('data.json')
    gather.scrape_contributors()
    gather.save_contributors_to_file("contributorData.json")
    gather.save_contributors_to_file('contributorData.json')
        
       
    analyzer = RepoAnalyzer(filename='data.json')
    analyzer.execute()

    commit_data = analyzer.percentageByCategory('language','commits')   
    gather.saveRankedContributorsToJson(analyzer, 'rankedContributorData.json', 'contributorData.json')
    frontend= Frontend()
    frontend.plotLanguageCommitPie(commit_data)
    frontend.plotRepoBarCharts(analyzer, top_n=10)

        
