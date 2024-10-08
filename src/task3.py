"""
Task 3: List repositories
● Objective:
○ Retrieve a list of public repositories for a user.
○ Endpoint: https://api.github.com/users/{username}/repos
● Expected Outcome:
○ Validate the possible status codes matching endpoint spec.
○ Ensure key fields are returned.
"""


import requests
import pytest
import json

# Load configuration settings from a JSON file
with open('config.json', 'r') as file:
    config_data = json.load(file)

# Extract relevant configuration values
BASE_URL = config_data['general']['base_url']  # Base URL for API requests
endpoint_1 = config_data['task3']['endpoint_1']  # First endpoint component
endpoint_2 = config_data['task3']['endpoint_2']  # Second endpoint component
username = config_data['task3']['username']  # Valid username
wrong_username = config_data['task3']['wrong_username']  # Invalid username
items = config_data['task3']['items']  # Expected items in the response

# Construct the full URL for API requests


def get_user_repos(username):
    """
    Retrieves user repositories from the specified API endpoint.

    Args:
        username (str): The username.

    Returns:
        requests.Response: The HTTP response object.
    """

    response = requests.get(f"{BASE_URL}/{endpoint_1}/{username}/{endpoint_2}", verify=False)
    return response

# Test cases for validating the user endpoint response

def test_response_200():
    """
    Tests if the response code is 200 for a valid username.
    """

    response = get_user_repos(username)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

def test_response_404():
    """
    Tests if the response code is 404 for an invalid username.
    """

    response = get_user_repos(wrong_username)
    assert response.status_code == 404, f"Expected status code 404, but got {response.status_code}"

def test_response_items():
    """
    Tests if the response contains the expected items for a valid username.
    """

    response = get_user_repos(username)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    # Parse the JSON response
    data = response.json()
    data = data[0]  # Assuming the first element contains the relevant data

    # Check if all expected items are present in the response
    assert set(items) == set(data.keys()), "The returned item list  does not match with expected one"

if __name__ == "__main__":
    pytest.main()