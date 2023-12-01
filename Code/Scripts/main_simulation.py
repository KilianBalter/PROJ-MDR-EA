import json

import handle_data

if __name__ == "__main__":
    with open("../../Assets/Example MDR Events/MDR_Event_4.json") as json_file:
        data = json.load(json_file)
        print(handle_data.handle_data(data))
