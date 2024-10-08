"""
Task 2: Logged user own profile
● Objective:
○ Retrieve the profile information of the logged-in user using an access token.
○ Endpoint: https://api.github.com/user
● Expected Outcome:
○ Validate the possible status codes matching endpoint spec.
○ Ensure additional user-specific fields (such as private details) are included.

"""

import requests
import pytest
import json

# Get parameters from the configuration file
with open('config.json', 'r') as file:
    config_data = json.load(file)

BASE_URL = config_data['general']['base_url']
endpoint = config_data['task2']['endpoint']
GITHUB_TOKEN = config_data['general']['github_token']
GITHUB_TOKEN_forbidden = config_data['general']['github_token_forbidden']
items = config_data['task2']['items']

headers = {'Authorization': f'token {GITHUB_TOKEN}'}

URL = f"{BASE_URL}/{endpoint}"

def get_user(token):
    """
    Retrieves user information from the given API endpoint using the provided token.

    Args:
        token (str): The authentication token to use for the request.

    Returns:
        requests.Response: The HTTP response object containing the user information.
    """

    headers = {
        "Authorization": f"token {token}"
    }
    response = requests.get(f"{BASE_URL}/{endpoint}", headers=headers, verify=False)
    return response

def test_response_200():
    """
    Tests if the API returns a 200 OK response when using a valid token.
    """

    response = get_user(GITHUB_TOKEN)

    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

def test_response_401():
    """
    Tests if the API returns a 401 Unauthorized response when using an invalid token.
    """

    response = get_user("hello")

    assert response.status_code == 401, f"Expected status code 401, but got {response.status_code}"

def test_response_304():
    """
    Tests if the API returns a 304 Not Modified response when using an ETag header to indicate that the resource hasn't changed.
    """

    response = get_user(GITHUB_TOKEN)
    etag = response.headers.get("ETag")

    response = requests.get(f"{BASE_URL}/{endpoint}", verify=False, headers={**headers, "If-None-Match": etag})

    assert response.status_code == 304, f"Expected status code 304, but got {response.status_code}"

def test_response_403():
    """
    Tests if the API returns a 403 Forbidden response when using a token that lacks necessary permissions.
    """

    response = requests.get(f"{BASE_URL}/{endpoint}", verify=False)
    # TODO: Implement logic to obtain a 403 response.
    assert response.status_code == 403, f"Expected status code 403, but got {response.status_code}"

def test_response_items():
    """
    Tests if the API response contains the expected items in the JSON data.
    """

    response = get_user(GITHUB_TOKEN)

    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    data = response.json()

    assert set(items) == set(data.keys()), "The returned ietm list  does not match with expected one"

if __name__ == "__main__":
    pytest.main()