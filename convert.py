
import sys
import json
import yaml
import xml.etree.ElementTree as ET

def read_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    return elem_to_dict(root)

def elem_to_dict(elem):
    data = {elem.tag: {} if elem.attrib else None}
    children = list(elem)
    if children:
        dd = {}
        for dc in map(elem_to_dict, children):
            for k, v in dc.items():
                if k in dd:
                    if isinstance(dd[k], list):
                        dd[k].append(v)
                    else:
                        dd[k] = [dd[k], v]
                else:
                    dd[k] = v
        data = {elem.tag: dd}
    if elem.attrib:
        data[elem.tag].update((k, v) for k, v in elem.attrib.items())
    if elem.text:
        text = elem.text.strip()
        if children or elem.attrib:
            if text:
                data[elem.tag]['text'] = text
        else:
            data[elem.tag] = text
    return data

def write_xml(data, file_path):
    def build_elem(elem, data):
        for key, val in data.items():
            if isinstance(val, dict):
                sub_elem = ET.SubElement(elem, key)
                build_elem(sub_elem, val)
            else:
                elem.set(key, val)
    root_tag = next(iter(data))
    root_data = data[root_tag]
    root = ET.Element(root_tag)
    build_elem(root, root_data)
    tree = ET.ElementTree(root)
    tree.write(file_path)

def read_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def write_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def read_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def write_yaml(data, file_path):
    with open(file_path, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)

def convert(file_in, file_out):
    if file_in.endswith('.xml'):
        data = read_xml(file_in)
    elif file_in.endswith('.json'):
        data = read_json(file_in)
    elif file_in.endswith('.yaml') or file_in.endswith('.yml'):
        data = read_yaml(file_in)
    else:
        raise ValueError("Unsupported input file format")

    if file_out.endswith('.xml'):
        write_xml(data, file_out)
    elif file_out.endswith('.json'):
        write_json(data, file_out)
    elif file_out.endswith('.yaml') or file_out.endswith('.yml'):
        write_yaml(data, file_out)
    else:
        raise ValueError("Unsupported output file format")

def main():
    if len(sys.argv) != 3:
        print("Usage: program.exe pathFile1.x pathFile2.y")
        sys.exit(1)

    file_in = sys.argv[1]
    file_out = sys.argv[2]

    try:
        convert(file_in, file_out)
        print(f"Converted {file_in} to {file_out}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()