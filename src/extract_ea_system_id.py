def get_ea_system_id_from_list_of_systems(server_list, mdr_name):
    # Check if either server_list or mdr_name is None, and return None if true
    if server_list is None or mdr_name is None:
        return None
    
    # Iterate through the server_list
    for server in server_list:
        # Check if the lowercase name of the current server matches the lowercase mdr_name
        if server['name'].lower() == mdr_name.lower():
            # Return the ID of the matching server
            return server['id']
    
    # If no matching server is found, return None
    return None
