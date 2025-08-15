import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn
class Frontend:
    def __init__(self):
        """Initialize the Frontend class."""
        pass

    def plotLanguageCommitPie(self, data):
        if not data:
            print("Error: No data provided for pie chart")
            return
        categories = [item['category'] for item in data]
        percentages = [item['percentage'] for item in data]
        plt.style.use('ggplot')  
        plt.figure(figsize=(8, 8))
        colors = ['#0366d6', '#28a745', '#d73a49', '#f66a0a', '#6f42c1', "#bbbe0f", "#72dd30"]  
        plt.pie(percentages, labels=categories, autopct='%1.1f%%', startangle=140, colors=colors, textprops={'fontsize': 14})
        plt.title("")
        plt.axis('equal')
        plt.savefig('language_commits_pie.png', dpi=300, bbox_inches='tight')  
        print("Pie chart saved as 'language_commits_pie.png'")
        plt.close()

    def plotRepoBarCharts(self, analyzer, top_n=10):
        if not analyzer or not analyzer.repos:
            print("Error: No valid analyzer or repository data provided for bar charts")
            return
        fields = [
            ('commits', 'Commits', 'Commits'),
            ('stars', 'Stars', 'Stars'),
            ('contributors', 'Contributors', 'Contributors')
        ]
        plt.style.use('ggplot')
        for field, title_suffix, ylabel in fields:
            try:
                sorted_repos = analyzer.rankByField(field)[:top_n]
                if not sorted_repos:
                    print(f"No valid data for {field} bar chart")
                    continue
                names = [repo['name'].replace(' / ', '/') for repo in sorted_repos]
                values = [int(repo[field]) for repo in sorted_repos]
                plt.figure(figsize=(12, 6))
                plt.bar(names, values, color='#0366d6')
                plt.title("")
                plt.xlabel('Repository', fontsize=12)
                plt.ylabel(ylabel, fontsize=12)
                plt.xticks(rotation=45, ha='right', fontsize=10)
                plt.tight_layout()
                plt.savefig(f'repo_{field}_bar.png', dpi=300, bbox_inches='tight')
                print(f"Bar chart for {field} saved as 'repo_{field}_bar.png'")
                plt.close()
            except ValueError as e:
                print(f"Error generating bar chart for {field}: {e}")
