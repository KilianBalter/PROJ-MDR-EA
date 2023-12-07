import requests

def get_JWT_Token(uname, pssword):
    login_url = "win-jtn7m3lf4bq.theagleenforce.local/login"

    payload = {
        "uname": username,
        "pssword": password
    }

    try:
        # Including verify=False to disable SSL certificate verification
        response = requests.post(login_url, data=payload, verify=False)

        if response.status_code == 200:
            jwt_token = response.json().get("token")
            return jwt_token
        else:
            print(f"Error {response.status_code}: Failed to retrieve JWT token")
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example usage
username = "your_username"
password = "your_password"
jwt_token = get_JWT_Token(username, password)

if jwt_token:
    print(f"JWT Token: {jwt_token}")
else:
    print("JWT Token retrieval failed.")
