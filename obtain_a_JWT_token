pip install requests

import requests

def get_JWT_Token(username, password):
    # Define the API endpoint for local login
    login_url = "https://win-jtn7m3lf4bq.theagleenforce.local/login"

    # Define the payload with the username and password
    payload = {
        "username": username,
        "password": password
    }

    try:
        # Perform the local login
        response = requests.post(login_url, data=payload)

        # Check if the login was successful (status code 200)
        if response.status_code == 200:
            # Extract and return the JWT token from the response
            jwt_token = response.json().get("token")
            return jwt_token
        else:
            # Print the error message if login fails
            print(f"Error {response.status_code}: Failed to retrieve JWT token")
            return None

    except Exception as e:
        # Print any other exceptions that might occur
        print(f"An error occurred: {e}")
        return None

# Example usage
username = "your_username"
password = "your_password"
jwt_token = get_JWT_Token(username, password)

# Print the obtained JWT token
if jwt_token:
    print(f"JWT Token: {jwt_token}")
else:
    print("JWT Token retrieval failed.")
