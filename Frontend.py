import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

class Frontend:
    def __init__(self):
        """Initialize the Frontend class."""
        pass

    def plotLanguageCommitPie(self, data):
        """Generate a pie chart for percentage of commits by programming language."""
        if not data:
            print("Error: No data provided for pie chart")
            return

        # Extract categories and percentages
        categories = [item['category'] for item in data]
        percentages = [item['percentage'] for item in data]

        # Create pie chart
        plt.figure(figsize=(8, 8))
        plt.pie(percentages, labels=categories, autopct='%1.1f%%', startangle=140)
        plt.title('Percentage of Commits by Programming Language')
        plt.axis('equal')  # Equal aspect ratio ensures pie chart is circular
        plt.savefig('language_commits_pie.png')  # Save the chart
        print("Pie chart saved as 'language_commits_pie.png'")
        #plt.show()
        plt.close()  # Close the plot to free memory

    def plotRepoBarCharts(self, analyzer, top_n=10):
        """Generate bar charts for repositories by commits, stars, and contributors."""
        if not analyzer or not analyzer.repos:
            print("Error: No valid analyzer or repository data provided for bar charts")
            return

        # Define fields to plot
        fields = [
            ('commits', 'Number of Commits', 'Commits'),
            ('stars', 'Number of Stars', 'Stars'),
            ('contributors', 'Number of Contributors', 'Contributors')
        ]

        for field, title_suffix, ylabel in fields:
            try:
                # Get sorted repositories by the field
                sorted_repos = analyzer.rankByField(field)[:top_n]
                if not sorted_repos:
                    print(f"No valid data for {field} bar chart")
                    continue

                # Extract names and values
                names = [repo['name'].replace(' / ', '/') for repo in sorted_repos]
                values = [int(repo[field]) for repo in sorted_repos]

                # Create bar chart
                plt.figure(figsize=(12, 6))
                plt.bar(names, values, color='skyblue')
                plt.title(f'Top {top_n} Repositories by {title_suffix}')
                plt.xlabel('Repository')
                plt.ylabel(ylabel)
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()

                # Save the chart
                filename = f'repo_{field}_bar.png'
                plt.savefig(filename)
                print(f"Bar chart for {field} saved as '{filename}'")
                plt.close()

            except ValueError as e:
                print(f"Error generating bar chart for {field}: {e}")
            except Exception as e:
                print(f"Unexpected error for {field} bar chart: {e}")