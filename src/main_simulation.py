import json
import logging
from src.handle_data import handle_data

if __name__ == "__main__":
    try:
        with open("../assets/Example MDR Events/Test_Event_1.json") as event_file:
            event = json.load(event_file)
            handle_data(event)
    except json.decoder.JSONDecodeError:
        logging.error("Error in JSON file. Check for correct JSON syntax!")
    except FileNotFoundError:
        logging.error("File wasn't found. Check for the correct path!")
