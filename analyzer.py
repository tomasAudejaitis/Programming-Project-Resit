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
        # self.print_summary()
        # self.print_most_starred()
        # self.print_python_repos()
        
    def get_average_contributors(self):
        """Return the average number of contributors across all repositories."""
        valid_contributors = [int(repo['contributors']) for repo in self.repos if repo['contributors'] != 'N/A']
        if not valid_contributors:
            return None
        return sum(valid_contributors) / len(valid_contributors)
    
    def rankByField(self, rank):
        """Return repositories ranked by the specified numeric field in descending order."""
        # Check if the field exists in at least one repository
        if not any(rank in repo for repo in self.repos):
            raise ValueError(f"Incompatible ranking field: {rank} does not exist in repository data")
        
        # Filter out repositories with 'N/A' for the field
        valid_repos = [repo for repo in self.repos if repo[rank] != 'N/A']
        if not valid_repos:
            raise ValueError(f"No valid {rank} data available")
        
        # Sort by numeric value
        try:
            sorted_repos = sorted(valid_repos, key=lambda x: int(x[rank]), reverse=True)
            return sorted_repos
        except ValueError:
            raise ValueError(f"Incompatible ranking field: {rank} values are not numeric")
    
    def percentageByCategory(self, category_field, value_field):
        
        # Check if fields exist in at least one repository
        if not any(category_field in repo for repo in self.repos):
            raise ValueError(f"Incompatible category field: {category_field} does not exist in repository data")
        if not any(value_field in repo for repo in self.repos):
            raise ValueError(f"Incompatible value field: {value_field} does not exist in repository data")
        
        # Filter repositories with valid (non-'N/A') values for value_field
        valid_repos = [repo for repo in self.repos if repo[value_field] != 'N/A']
        if not valid_repos:
            raise ValueError(f"No valid {value_field} data available")
        
        # Sum values by category
        category_sums = {}
        try:
            for repo in valid_repos:
                category = repo[category_field]
                value = int(repo[value_field])
                category_sums[category] = category_sums.get(category, 0) + value
        except ValueError:
            raise ValueError(f"Incompatible value field: {value_field} values are not numeric")
        
        # Calculate total and percentages
        total_value = sum(category_sums.values())
        if total_value == 0:
            raise ValueError(f"Total {value_field} is zero, cannot calculate percentages")
        
        # Create result list
        result = [
            {
                'category': category,
                'total': total,
                'percentage': (total / total_value) * 100
            }
            for category, total in sorted(category_sums.items(), key=lambda x: x[1], reverse=True)
        ]
        return result

