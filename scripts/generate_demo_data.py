import csv
import json
import random
from pathlib import Path
import xml.etree.ElementTree as ET

out_dir = Path("examples/datasets")
out_dir.mkdir(parents=True, exist_ok=True)

random.seed(42)
countries = ["France", "Germany", "Spain", "Italy", "Portugal", "Belgium", "Netherlands", "Morocco", "Tunisia"]
first_names = ["Alice", "Bob", "Charlie", "Diana", "Ethan", "Fatima", "Hugo", "Ines", "Jules", "Karim", "Lina", "Mehdi", "Nora", "Omar", "Sarah"]
last_names = ["Martin", "Bernard", "Thomas", "Petit", "Robert", "Richard", "Durand", "Dubois", "Moreau", "Laurent", "Simon", "Michel", "Lefevre", "Garcia", "Roux"]

rows = []
for i in range(1, 301):
    fn = random.choice(first_names)
    ln = random.choice(last_names)
    name = f"{fn} {ln}"
    email = f"{fn.lower()}.{ln.lower()}{i}@example.com"
    age = random.randint(18, 65)
    country = random.choice(countries)
    rows.append({"id": i, "name": name, "email": email, "age": age, "country": country})

# CSV
csv_path = out_dir / "users_medium.csv"
with csv_path.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["id", "name", "email", "age", "country"])
    w.writeheader()
    w.writerows(rows)

# JSON
json_path = out_dir / "users_medium.json"
json_path.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")

# XML
xml_path = out_dir / "users_medium.xml"
root = ET.Element("users")
for r in rows:
    user = ET.SubElement(root, "user")
    for k, v in r.items():
        el = ET.SubElement(user, k)
        el.text = str(v)
ET.ElementTree(root).write(xml_path, encoding="utf-8", xml_declaration=True)

print("Generated:")
print(" -", csv_path)
print(" -", json_path)
print(" -", xml_path)
