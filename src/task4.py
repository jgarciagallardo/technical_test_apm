"""
Task 4: List repositories for logged user
● Objective:
○ Retrieve a list of repositories (both public and private) for the logged-in user.
○ Endpoint: https://api.github.com/user/repos
● Expected Outcome:
○ Validate the possible status codes matching endpoint spec.
○ Validate that both public and private repositories are listed.
○ Ensure key fields are returned.
"""

import requests
import pytest
import json

# Get parameters from the config file
with open('config.json', 'r') as file:
    config_data = json.load(file)

BASE_URL = config_data['general']['base_url']
endpoint = config_data['task4']['endpoint']
GITHUB_TOKEN = config_data['general']['github_token']
GITHUB_TOKEN_forbidden = config_data['general']['github_token_forbidden']
items = config_data['task4']['items']

headers = {'Authorization': f'token {GITHUB_TOKEN}'}

def get_user(token):
    """
    Retrieves user data from the specified endpoint using the provided token.

    Args:
        token (str): The authentication token to use.

    Returns:
        requests.Response: The HTTP response object.
    """

    headers = {
        "Authorization": f"token {token}"
    }
    response = requests.get(f"{BASE_URL}/{endpoint}", headers=headers, verify=False)
    return response

# Tests for validating the user endpoint

def test_response_200():
    """
    Tests if the endpoint returns a 200 OK status code with a valid token.
    """

    response = get_user(GITHUB_TOKEN)

    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

def test_response_401():
    """
    Tests if the endpoint returns a 401 Unauthorized status code with an invalid token.
    """

    response = get_user("hello")

    assert response.status_code == 401, f"Expected status code 401, but got {response.status_code}"

def test_response_304():
    """
    Tests if the endpoint returns a 304 Not Modified status code when using an ETag.
    """

    # Get the ETag from a preliminary request
    response = get_user(GITHUB_TOKEN)
    etag = response.headers.get("ETag")

    # Send a subsequent request with the ETag
    response = requests.get(f"{BASE_URL}/{endpoint}", verify=False, headers={**headers, "If-None-Match": etag})

    assert response.status_code == 304, f"Expected status code 304, but got {response.status_code}"

def test_response_403():
    """
    Tests if the endpoint returns a 403 Forbidden status code when using a forbidden token.
    """

    response = requests.get(f"{BASE_URL}/{endpoint}", verify=False, headers={'Authorization': f'token {GITHUB_TOKEN_forbidden}'})

    assert response.status_code == 403, f"Expected status code 403, but got {response.status_code}"

def test_response_items():
    """
    Tests if the endpoint returns the expected items in the response data.
    """

    response = get_user(GITHUB_TOKEN)

    # Verify the status code and extract the data
    assert response.status_code == 200
    data = response.json()[0]

    # Check if all expected items are present in the data
    assert set(items) == set(data.keys()), "The returned ietm list  does not match with expected one"

if __name__ == "__main__":
    pytest.main()