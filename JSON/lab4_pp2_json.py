import json
from datetime import datetime

with open("sample-data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

target_days = {0, 2}
filtered_interfaces = {"Mon, Wed": [], "Other Days": []}

for item in data["imdata"]:
    attributes = item["l1PhysIf"]["attributes"]
    mod_ts = attributes.get("modTs", "")

    try:
        date_obj = datetime.strptime(mod_ts, "%Y-%m-%dT%H:%M:%S.%f%z")
    except ValueError:
        continue

    category = "Mon, Wed" if date_obj.weekday() in target_days else "Other Days"
    filtered_interfaces[category].append(attributes)

def print_table(title, interfaces):
    print(f"\n{title}:")
    print("=" * 80)
    print(f"{'DN':<50} {'Description':<20} {'Speed':<10} {'MTU'}")
    print("-" * 80)

    for interface in interfaces:
        print(f"{interface['dn']:<50} {interface.get('descr', 'N/A'):<20} {interface['speed']:<10} {interface['mtu']}")

print_table("Interfaces (Mon, Wed)", filtered_interfaces["Mon, Wed"])
print_table("Interfaces (Other Days)", filtered_interfaces["Other Days"])c