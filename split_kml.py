import os
from pykml import parser
from lxml import etree

def process_folder(folder):
    # Check if folder has a name
    if hasattr(folder, 'name'):
        folder_name = folder.name.text.strip()

        # Create a KML file for the folder, excluding 'Sites' subfolder
        folder_kml = etree.Element("kml")
        for element in folder.getchildren():
            if not (element.tag.endswith('Folder') and hasattr(element, 'name') and element.name.text.strip() == 'Sites'):
                folder_kml.append(element)

        # Save the KML file
        filepath = os.path.expanduser(f'~/Desktop/sggs/{folder_name}.kml')
        with open(filepath, 'w') as file:
            file.write(etree.tostring(folder_kml, pretty_print=True).decode())

        # If there's a 'Sites' subfolder, create a separate KML file for it
        for subfolder in folder.Folder:
            if hasattr(subfolder, 'name') and subfolder.name.text.strip() == 'Sites':
                subfolder_kml = etree.Element("kml")
                subfolder_kml.append(subfolder)

                # Save the KML file
                filename = f"{folder_name}_Sites"
                filepath = os.path.expanduser(f'~/Desktop/sggs/{filename}.kml')
                with open(filepath, 'w') as file:
                    file.write(etree.tostring(subfolder_kml, pretty_print=True).decode())

# Load the KML file
kml_file_path = os.path.expanduser('~/Desktop/sggs/doc.kml')

with open(kml_file_path, 'r') as kml_file:
    doc = parser.parse(kml_file).getroot()

# Get the first 'Folder' element (should be 'SG.GS') and process its subfolders
sggs_folder = doc.Document.Folder
for subfolder in sggs_folder.Folder:
    process_folder(subfolder)
