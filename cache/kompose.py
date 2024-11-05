import yaml
import sys

filename = sys.argv[1]
# Load the YAML file
with open(filename, 'r') as file:
    data = yaml.safe_load(file)

# Modify the volumeMounts to include subPath
for container in data['spec']['template']['spec']['containers']:
    for volume_mount in container.get('volumeMounts', []):
        volume_mount['subPath'] = volume_mount['name']

# Save the modified YAML back to a file
with open(filename, 'w') as file:
    yaml.safe_dump(data, file, default_flow_style=False)
