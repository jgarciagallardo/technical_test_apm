"""
Task 7: Implement testing workflows
Objective: Create workflows that demonstrate the ability to chain multiple API interactions,
including both successful and failed requests. The goal is to simulate real-world usage patterns
and validate how different API endpoints work together.

Example Workflow:

1. Step 1: Try to retrieve the user's profile without a Bearer token and validate that access
is denied (e.g., 401 Unauthorized).
2. Step 2: Set the Bearer token and retry fetching the profile, this time validating that
access is granted (e.g., 200 OK).
3. Step 3: Update a field in the logged-in user’s profile, such as the bio or name.
4. Step 4: Retrieve the profile again and validate that the field has been successfully
updated.
5. Step 5: Obtain the list of repositories for the logged-in user (both public and private).
Ensure that the repositories are listed correctly.
6. Step 6: Attempt to list commits for a non-existent repository and validate that the
appropriate error is returned (e.g., 404 Not Found).
7. Step 7: List commits from the first repository of the logged-in user and validate the key
fields (sha, author, message, date) in the response.
8. Step 8: List commits from the last repository of the logged-in user, again validating key
fields.

Expected Outcome:
● Ensure status codes are validated at every step.
● Verify that the appropriate error handling is in place for failed requests.
● Validate the correct sequence of operations and responses, ensuring proper flow
through the API endpoints.
● Ensure that each request and response in the workflow behaves as expected according
to the GitHub API documentation.
"""
import requests
import pytest
import json


#get parameters
with open('config.json', 'r') as file:
    config_data = json.load(file)

BASE_URL = config_data['general'][ 'base_url']
GITHUB_TOKEN = config_data['general']['github_token']

user_new_name =config_data["task7"]["user_new_name"]
user_new_bio =config_data["task7"]["user_new_bio"]
user_new_blog =config_data["task7"]["user_new_blog"]

step_6_user_name = config_data["task7"]["step_6_user_name"]
step_6_wrong_repo_name = config_data["task7"]["step_6_wrong_repo_name"]

step_5_repo_list = config_data["task7"]["step_5_repo_list"]

step_7_items = config_data["task7"]["step_7_item_list"]
step_7_first_repo_name = config_data["task7"]["step_7_first_repo_name"]

step_8_items = config_data["task7"]["step_8_item_list"]
step_8_last_repo_name = config_data["task7"]["step_8_last_repo_name"]

headers = {"Authorization": f"token {GITHUB_TOKEN}","Accept": "application/vnd.github.v3+json" }

def key_in_dictionary(input_dict, key):
    """
    Checks if a key is in the given dictionary or its sub-dictionaries.

    Args:
    input_dict: The dictionary to search.
    key: key name

    Returns:
    True key exists, False otherwise
    """

    return_value = False

    #browse dictionary item
    for dict_key , value in input_dict.items():
        if dict_key == key:
            # key found
            return_value = True
        else:
            # if element is dictionary we search recursive
            if type(value) is dict:
                return_value =  return_value or key_in_dictionary( value , key )

    return return_value


def test_step1():
    """
    Step 1 : Try to retrieve the user's profile without a Bearer token and validate that access
    is denied (e.g., 401 Unauthorized).
    """
    response = requests.get(f"{BASE_URL}/user", verify=False)
    assert response.status_code == 401, f"Expected status code 401, but got {response.status_code}"

def test_step2():
    """
    Step 2: Set the Bearer token and retry fetching the profile, this time validating that
    access is granted (e.g., 200 OK).
    """
    response = requests.get(f"{BASE_URL}/user", headers=headers,verify=False)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

def test_step3():
    """
    Step 3: Update a field in the logged-in user’s profile, such as the bio or name.
    """
    # Update user metadata
    update_data = {
        "name": user_new_name,
        "bio": user_new_bio,
        "blog": user_new_blog
    }
    response = requests.patch(f"{BASE_URL}/user", headers=headers, json=update_data, verify=False)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

def test_step4():
    """
    Step 4: Retrieve the profile again and validate that the field has been successfully
    updated.
    """
    # Verify the updates
    response = requests.get(f"{BASE_URL}/user", headers=headers, verify=False)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    user_data = response.json()
    assert user_data["name"] == user_new_name,  f"Name not updated"
    assert user_data["bio"] == user_new_bio,  f"Bio not updated"
    assert user_data["blog"] == user_new_blog,  f"Blog not updated"

def test_step5():
    """
    Step 5: Obtain the list of repositories for the logged-in user (both public and private).
    Ensure that the repositories are listed correctly.
    """
    response = requests.get(f"{BASE_URL}/user/repos", headers=headers, verify=False)
    data = response.json()

    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    # add response repos to list
    response_repos =[]
    for item in data:
        response_repos.append(item["name"])

    assert set(response_repos)==set(step_5_repo_list), "The returned repo list  does not match with expected one"

def test_step6():
    """
    Step 6: Attempt to list commits for a non-existent repository and validate that the
    appropriate error is returned (e.g., 404 Not Found).
    """
    response = requests.get(f"{BASE_URL}/repos/{step_6_user_name}/{step_6_wrong_repo_name}/commits", headers=headers, verify=False)

    assert response.status_code == 404, f"Expected status code 404, but got {response.status_code}"

def test_step7():
    """
    Step 7: List commits from the first repository of the logged-in user and validate the key
    fields (sha, author, message, date) in the response.
    """
    response = requests.get(f"{BASE_URL}/user/repos", headers=headers, verify=False)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    data = response.json()

    # get first repo name
    repo_name = data[0]["name"]

    assert repo_name == step_7_first_repo_name, "Commit returned wrong repo name as first repo"

    #get owner
    owner = data[0]["owner"]["login"]

    #get commits
    response = requests.get(f"{BASE_URL}/repos/{owner}/{repo_name}/commits", headers=headers, verify=False)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    for commit in response.json():
        for item in step_7_items:
            assert key_in_dictionary( commit , item), "Item " + item + " not in commit response "

def test_step8():
    """
    Step 8: List commits from the last repository of the logged-in user, again validating key
    fields
    """
    #get last repo name
    response = requests.get(f"{BASE_URL}/user/repos", headers=headers, verify=False)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    data = response.json()

    # get first repo name
    commit_response_length = len(data)
    repo_name = data[commit_response_length - 1]["name"]

    # get owner
    owner = data[0]["owner"]["login"]

    assert repo_name == step_8_last_repo_name, "Commit returned wrong repo name as last repo"

    # get commits
    response = requests.get(f"{BASE_URL}/repos/{owner}/{repo_name}/commits", headers=headers, verify=False)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    for commit in response.json():
        for item in step_8_items:
            assert key_in_dictionary(commit, item), "Item " + item + " not in commit response "


if __name__ == "__main__":
    pytest.main()