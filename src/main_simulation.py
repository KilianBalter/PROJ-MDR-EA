import json
import logging

from src.handle_data import handle_data

if __name__ == "__main__":
    try:
        files = ["Test_Event_1.json", "Test_Event_2.json"]
        for file in files:
            with open("../assets/Example MDR Events/" + file) as event_file:
                print(file + ":")
                json_event = json.load(event_file)
                sat_mitigations, vuln_status = handle_data(json_event)

                print(f"Vulnerability status: {vuln_status}")
                if sat_mitigations:
                    print(f"Following mitigations are present: {sat_mitigations}")
                else:
                    print("No mitigations are present")
                print("\n\n")
    except json.decoder.JSONDecodeError:
        logging.error("Error in JSON file. Check for correct JSON syntax!")
    except FileNotFoundError:
        logging.error("File wasn't found. Check for the correct path!")
