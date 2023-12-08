import json
import logging
import handle_data

if __name__ == "__main__":
    try:
        with open("../assets/Example MDR Events/MDR_Event_1.json") as json_file:
            data = json.load(json_file)
            print(handle_data.handle_data(data))
    except json.decoder.JSONDecodeError:
        logging.error("Error in JSON file. Check for correct JSON syntax!")
    except FileNotFoundError:
        logging.error("File wasn't found. Check for the correct path!")
