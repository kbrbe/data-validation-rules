# Initial version from Hannes Lowagie
#
import csv
import yaml

def generate_yaml_from_csv(input_csv, output_yaml):
    with open(input_csv, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        
        yaml_data = {
            "format": "MARC",
            "fields": []
        }
        
        for row in reader:
            if row.get('IncludeInAP?', '').strip().lower() == 'yes':
                field_entry = {
                    "name": row['MARC21field'],
                    "path": row['MARC21field'],
                    "rules": []
                }      
                remarks = row.get("Remarks", "").strip()           
                if row.get("Pattern") and row["Pattern"].startswith("not(") and row["Pattern"].endswith(")"):
                    pattern_content = row["Pattern"][4:-1]  # Extract the pattern inside 'not()'

                    rule_entry = {
                        "id": f"{row['MARC21field']}.pattern",
                        "description": remarks if remarks else f"Invalid pattern: {pattern_content}",  # Use remarks if available
                        "debug": False,
                        "not": [{"pattern": pattern_content}],
                    }
                    field_entry["rules"].append(rule_entry)

                # Handle standard pattern rules
                elif row.get("Pattern"):
                    field_entry["rules"].append({
                        "id": f"{row['MARC21field']}.pattern",
                        "pattern": row["Pattern"],
                        "description": remarks if remarks else f"Follow pattern"
                    })

                # Handle 'Obligatory' (minCount=1)
                if row.get("Obligatory", "").strip().lower() == "yes":
                    field_entry["rules"].append({
                        "id": f"{row['MARC21field']}.minCount",
                        "minCount": 1,
                        "description": f"Obligatory field"
                    })

                # Handle 'Repeatable' (maxCount=1 if 'no')
                if row.get("Repeatable", "").strip().lower() == "no":
                    field_entry["rules"].append({
                        "id": f"{row['MARC21field']}.maxCount",
                        "maxCount": 1,
                        "description": f"Not repeatable"
                    })

                # Add the field entry to the fields list
                yaml_data["fields"].append(field_entry)
    
    # Write the YAML file
    with open(output_yaml, mode='w', encoding='utf-8') as yamlfile:
        yaml.dump(yaml_data, yamlfile, allow_unicode=True, sort_keys=False)

# File paths
input_csv = "rdam.csv"  
output_yaml = "shacl4bib.yaml" 

# Generate the YAML file
generate_yaml_from_csv(input_csv, output_yaml)
