import requests

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
mdr_name_input = "YourMDRName"
systems_input = [
    {"mdr_name": "System1MDR", "ea_system_id": "EA123"},
    {"mdr_name": "System2MDR", "ea_system_id": "EA456"},
  
]

# Call the function
ea_system_id = get_system_id(mdr_name_input, systems_input)

# Print the result
if ea_system_id is not None:
    print(f"EA System ID for {mdr_name_input}: {ea_system_id}")
else:
    print(f"No matching system found for {mdr_name_input}")
