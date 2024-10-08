"""
**Task 1: External user public profile**

This script tests retrieving a user's public profile information from the GitHub API.

* **Objective:**
    * Retrieve the public profile information of a specific user without authentication.
    * Endpoint: https://api.github.com/users/{username}
* **Expected Outcome:**
    * Validate the possible status codes matching endpoint spec.
    * Ensure key public fields are returned.
"""

import requests
import pytest
import json


# Load configuration data from JSON file
with open('config.json', 'r') as file:
    config_data = json.load(file)

# Extract configuration values
BASE_URL = config_data['general']['base_url']
endpoint = config_data['task1']['endpoint']
username = config_data['task1']['username']
items = config_data['task1']['items']  # List of expected keys in the response data


def get_user(username):
    """
    Fetches the public profile information for a given username from the GitHub API.

    Args:
        username (str): The username to retrieve information for.

    Returns:
        requests.Response: The API response object.
    """

    url = f"{BASE_URL}/{endpoint}/{username}"  # Construct the full URL with username
    response = requests.get(url, verify=False)  # Make the GET request (ignoring SSL verification)
    return response


def test_response_200():
    """
    Tests if the API returns a 200 status code (Success) for a valid username.
    """

    response = get_user(username)

    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    data = response.json()
    assert data["login"] == username, "Username should match the requested user " + username


def test_response_404():
    """
    Tests if the API returns a 404 status code (Not Found) for a non-existent user.
    """

    nonexistent_username = "wrong_user_name_09090909332"
    response = get_user(nonexistent_username)

    assert response.status_code == 404, f"Expected status code 404 for non-existent user: {nonexistent_username}"


def test_response_items():
    """
    Tests if the API response contains all the expected key-value pairs (listed in 'items').
    """

    response = get_user(username)

    assert response.status_code == 200,  f"Expected status code 200, but got {response.status_code}"

    data = response.json()

    assert set(items) == set(data.keys()), "The returned ietm list  does not match with expected one"


if __name__ == "__main__":
    pytest.main()