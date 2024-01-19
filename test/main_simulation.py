import json
import logging
import sys

from src.handle_data import handle_data

if __name__ == "__main__":
    try:
        files = ["Test_Event_1.json", "Test_Event_2.json", "Test_Event_3.json"]
        for file in files:
            with open("../assets/Example MDR Events/" + file) as event_file:
                print(file + ":")
                json_event = json.load(event_file)
                modified_event = handle_data(json_event)

                print(f"Vulnerability status: {modified_event['hardening_info']['vulnerability_status']}\n")
                sat_mitigations = modified_event['hardening_info']['satisfied_mitigations']
                part_mitigations = modified_event['hardening_info']['partial_mitigations']
                unsat_mitigations = modified_event['hardening_info']['unsatisfied_mitigations']
                error_message = modified_event['hardening_info']['error_message']
                print(f"Following mitigations are present: \n{json.dumps(sat_mitigations, indent=2)}\n")
                print(f"Following partial mitigations are present: \n{json.dumps(part_mitigations, indent=2)}\n")
                print(f"Following mitigations are not present: \n{json.dumps(unsat_mitigations, indent=2)}\n")
                print(f"Error message: {error_message}\n")
                print("\n\n")
    except json.decoder.JSONDecodeError:
        logging.error("Error in JSON file. Check for correct JSON syntax!")
    except FileNotFoundError:
        logging.error("File wasn't found. Check for the correct path!")
    except Exception:
        print("Unexpected error:", sys.exc_info()[0])
