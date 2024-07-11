
import sys
import json
import yaml
import xml.etree.ElementTree as ET
import argparse

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
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON syntax in file {file_path}: {e}")
        sys.exit(1)

"""

Usprawnienia: write_json()

Obsługa wyjątków: Funkcja write_json zawiera teraz blok try-except, który przechwytuje wszelkie błędy wejścia/wyjścia (IOError) podczas zapisywania pliku.

Kontekst menedżera: Zastosowanie with open(file_path, 'w') as file: zapewnia, że plik zostanie poprawnie zamknięty, nawet jeśli wystąpi błąd.

Lepsze formatowanie: Opcje indent=4 i sort_keys=True w json.dump poprawiają czytelność i przewidywalność zapisanego pliku JSON.

Dodatkowy komunikat: Informacja o sukcesie zapisu danych do pliku została dodana w funkcji write_json.

"""

def write_json(data, file_path):
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4, sort_keys=True)
        print(f"Data successfully written to {file_path}")
    except IOError as e:
        print(f"Error writing to file {file_path}: {e}")
        sys.exit(1)

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

"""

Parsowanie argumentów przekazywanych przy uruchomieniu programu w obecnym kodzie jest podstawowe i działa, ale można to zrobić lepiej i bardziej elegancko przy użyciu biblioteki argparse, która jest standardową biblioteką Pythona do parsowania argumentów wiersza poleceń.

można skorzystać z biblioteki argparse 

dadajemy

import argparse

"""


def main():

    """
    poprzednie rozwiązanie

    if len(sys.argv) != 3:
        print("Usage: program.exe pathFile1.x pathFile2.y")
        sys.exit(1)

    file_in = sys.argv[1]
    file_out = sys.argv[2]
    """

    parser = argparse.ArgumentParser(description="Convert data between XML, JSON, and YAML formats.")
    parser.add_argument('input_file', help="Input file path")
    parser.add_argument('output_file', help="Output file path")

    args = parser.parse_args()

    file_in = args.input_file
    file_out = args.output_file

    try:
        convert(file_in, file_out)
        print(f"Converted {file_in} to {file_out}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()