"""
Task 6: Update logged user metadata
Objective: Update the metadata of the logged-in user using an access token. This task tests
the ability to modify user information and ensure that the updates are reflected accurately.
Endpoint: https://api.github.com/user
Expected Outcome:
● Validate the possible status codes matching endpoint spec.
● Ensure that user-specific fields, such as name, bio, or blog, can be updated.
● Ensure the updated fields are reflected in subsequent requests for the user profile.
● Verify that an unauthorized request (missing or invalid token) results in the appropriate
error status code
"""

import requests
import pytest
import json

# Load configuration settings from a JSON file
with open('config.json', 'r') as file:
    config_data = json.load(file)

# Extract necessary configuration values
BASE_URL = config_data['general']['base_url']
endpoint = config_data["task6"]["endpoint"]
GITHUB_TOKEN = config_data['general']['github_token']

user_new_name = config_data["task6"]["user_new_name"]
user_new_bio = config_data["task6"]["user_new_bio"]
user_new_blog = config_data["task6"]["user_new_blog"]


# Set up headers for API requests
headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}

# Function to retrieve user data from the GitHub API
def get_user(token):
    """
    Retrieves user data from the GitHub API using the provided token.

    Args:
        token (str): The GitHub access token.

    Returns:
        requests.Response: The HTTP response object.
    """

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(f"{BASE_URL}/{endpoint}", headers=headers, verify=False)
    return response

# Test cases for different HTTP status codes

def test_response_200():
    """Tests if the API returns a 200 status code."""

    response = get_user(GITHUB_TOKEN)

    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

def test_response_401():
    """Tests if the API returns a 401 status code for an unauthorized request."""

    response = get_user("hello")  # Invalid token

    assert response.status_code == 401, f"Expected status code 401, but got {response.status_code}"

def test_response_304():
    """Tests if the API returns a 304 status code for a not modified response."""

    # Get the initial ETag
    response = get_user(GITHUB_TOKEN)
    etag = response.headers.get("ETag")

    # Send a request with the ETag
    response = requests.get(f"{BASE_URL}/{endpoint}", verify=False, headers={**headers, "If-None-Match": etag})

    assert response.status_code == 304, f"Expected status code 304, but got {response.status_code}"

def test_response_403():
    """Tests if the API returns a 403 status code for a forbidden request."""

    response = requests.get(f"{BASE_URL}/{endpoint}", verify=False)
    # TODO: Add logic to trigger a 403 response

    assert response.status_code == 403, f"Expected status code 403, but got {response.status_code}"

# Test case for updating user metadata

def test_update_user_metadata():
    """Tests if user metadata can be successfully updated."""

    # Update user metadata
    update_data = {
        "name": user_new_name,
        "bio": user_new_bio,
        "blog": user_new_blog
    }
    response = requests.patch(f"{BASE_URL}/{endpoint}", headers=headers, json=update_data, verify=False)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    # Verify the updates
    response = requests.get(f"{BASE_URL}/{endpoint}", headers=headers, verify=False)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    user_data = response.json()
    assert user_data["name"] == user_new_name
    assert user_data["bio"] == user_new_bio
    assert user_data["blog"] == user_new_blog

# Test case for an unauthorized request

def test_unauthorized_request():
    """Tests if the API returns a 401 status code for an unauthorized request."""

    # Attempt to update user metadata without a token
    update_data = {
        "name": "Unauthorized Name"
    }
    response = requests.patch(f"{BASE_URL}/{endpoint}", json=update_data, verify=False)
    assert response.status_code == 401, f"Expected status code 401, but got {response.status_code}"

# Run the tests
if __name__ == "__main__":
    pytest.main()