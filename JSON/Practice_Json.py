import json
from datetime import datetime

# Load JSON data
try:
    with open("sample-data.json", 'r', encoding='utf-8') as file:
        data = json.load(file)
except FileNotFoundError:
    print("Error: The file 'sample-data.json' was not found.")
    exit(1)
except json.JSONDecodeError:
    print("Error: Failed to decode JSON from the file.")
    exit(1)

# Check if 'imdata' key exists in the JSON data
if 'imdata' not in data:
    print("Error: 'imdata' key not found in JSON data.")
    exit(1)

arr = data['imdata']

target_days = {0, 2, 4}
filtered_interfaces = {"Mon, Wed, Fri": [], "Other Days": []}

for item in arr:
    attributes = item.get("l1PhysIf", {}).get("attributes", {})
    mod_ts = attributes.get("modTs", "")

    try:
        date_obj = datetime.strptime(mod_ts, "%Y-%m-%dT%H:%M:%S.%f%z")
    except ValueError:
        print(f"Warning: Failed to parse date '{mod_ts}'. Skipping this entry.")
        continue

    category = "Mon, Wed, Fri" if date_obj.weekday() in target_days else "Other Days"
    filtered_interfaces[category].append(attributes)

def print_table(title, interfaces):
    print(f"\n{title}:")
    print("=" * 80)
    print(f"{'DN':<50} {'Description':<20} {'Speed':<10} {'MTU'}")
    print("-" * 80)

    for interface in interfaces:
        print(f"{interface['dn']:<50} {interface.get('descr', 'N/A'):<20} {interface['speed']:<10} {interface['mtu']}")

if filtered_interfaces["Mon, Wed, Fri"]:
    print_table("Interfaces (Mon, Wed, Fri)", filtered_interfaces["Mon, Wed, Fri"])

if filtered_interfaces["Other Days"]:
    print_table("Interfaces (Other Days)", filtered_interfaces["Other Days"])