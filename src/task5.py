"""
Task 5: List Commits of a repository
● Objective:
○ Retrieve the list of commits for a public repository without authentication.
○ Endpoint: https://api.github.com/repos/{owner}/{repo}/commits
● Expected Outcome:
○ Validate the possible status codes matching endpoint spec.
○ Validate all commits are listed, with proper handling of pagination if needed.
○ Validate the list of commits includes fields such as sha, author, message, and
date.
"""

import requests
import pytest
import json

# Get parameters from config file
with open('config.json', 'r') as file:
    config_data = json.load(file)

BASE_URL = config_data['general']['base_url']
endpoint_1 = config_data['task5']['endpoint_1']
endpoint_2 = config_data['task5']['endpoint_2']
owner = config_data['task5']['owner']
repo = config_data['task5']['repo']

# Function to retrieve repository data
def get_repo(owner, repo):
    """
    Retrieves repository data from the specified endpoint.

    Args:
        owner (str): The owner of the repository.
        repo (str): The name of the repository.

    Returns:
        requests.Response: The HTTP response object.
    """

    response = requests.get(f"{BASE_URL}/{endpoint_1}/{owner}/{repo}/{endpoint_2}", verify=False)
    return response

# Test cases for different HTTP status codes
def test_response_200():
    """
    Tests if the endpoint returns a 200 OK status code for a valid repository.
    """

    response = get_repo(owner, repo)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

def test_response_404_bad_owner():
    """
    Tests if the endpoint returns a 404 Not Found status code for an invalid owner.
    """

    response = get_repo("Manolito_023412342134", repo)
    assert response.status_code == 404, f"Expected status code 404, but got {response.status_code}"

def test_response_404_bad_repo():
    """
    Tests if the endpoint returns a 400 Bad Request status code for an invalid repository.
    """

    response = get_repo(owner, "repo")
    assert response.status_code == 404, f"Expected status code 400, but got {response.status_code}"

# Test cases for pagination
def test_pagination_no_pagination():
    """
    Tests if the endpoint returns results without pagination.
    """

    response = requests.get(f"{BASE_URL}/{endpoint_1}/{owner}/{repo}/{endpoint_2}", verify=False)
    assert response.status_code == 200
    assert "pagination" not in response.json()

def test_pagination():
    """
    Tests if the endpoint returns results with pagination.
    """

    params = {'per_page': 2}
    response = requests.get(f"{BASE_URL}/{endpoint_1}/{owner}/{repo}/{endpoint_2}", params=params, verify=False)

    # Validate status code
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    # Validate pagination
    commits = response.json()
    assert len(commits) == 2, f"Expected 2 commits, but got {len(commits)}"

    # Check for 'Link' header for pagination
    assert 'Link' in response.headers, "Missing 'Link' header for pagination"

if __name__ == "__main__":
    pytest.main()