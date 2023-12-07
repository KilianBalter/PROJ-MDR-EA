import requests
import src.obtain_a_JWT_token as Jwt
import receive_list_of_systems_from_ea as Los

def get_system_id(mdr_name, systems):
    # Iterate through the list of systems
    for system in systems:
        # Check if the MDR name matches
        if system.get('mdr_name') == mdr_name:
            # Return the EA system ID
            return system.get('ea_system_id')

    # If MDR name is not found, return None or raise an exception based on your use case
    return None

# Example usage:

# Get the JWT token
jwt_token = Jwt.get_jwt_token("your_username", "your_password").json()

# Get the list of systems from the EA API
systems_response = Los.get_list_of_systems_from_ea(jwt_token)

# Check if the request was successful
if systems_response.status_code == 200:
    # Convert the JSON response to a list of systems
    systems = systems_response.json()

    mdr_name_input = "YourMDRName"

    # Call the function
    ea_system_id = get_system_id(mdr_name_input, systems)

    # Print the result
    if ea_system_id is not None:
        print(f"EA System ID for {mdr_name_input}: {ea_system_id}")
    else:
        print(f"No matching system found for {mdr_name_input}")
else:
    print(f"Error getting systems: {systems_response.status_code} - {systems_response.text}")
