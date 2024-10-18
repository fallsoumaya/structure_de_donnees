import json
import yaml 
import pandas as pd
import xmltodict


def serialize_json(obj):
    try:
        return json.dumps(obj, indent=4, sort_keys=True)
    except json.JSONDecodeError as e:
        return e


def deserialize_json(obj):
    try:
        return json.loads(obj)
    except json.JSONDecodeError as e:
        return e
    

def serialize_yaml(obj):
    try:
        return yaml.dump(obj)
    except yaml.YAMLError as e:
        return e
    
    
def deserialize_yaml(obj):
    try:
        return yaml.loads(obj)
    except yaml.YAMLError as e:
        return e
    

def depuis_csv(file):
    try:
        df = pd.read_csv(file)
        return df.to_dict('records') 
    except pd.errors.EmptyDataError as e:
        return e

    
def vers_csv(obj):
    try:
        df = pd.DataFrame(obj)
        return df.to_csv()
    except pd.errors.EmptyDataError as e:
        return e
    

def depuis_xml(obj):
    try:
        return xmltodict.parse(obj)
    except xmltodict.expat.ExpatError as e:
        return e

def vers_xml(obj):
    try:
        if isinstance(obj, list):
            # If obj is a list, wrap each item with a root element and return as a list of XML documents
            xml_docs = []
            for i, item in enumerate(obj):
                xml_docs.append(xmltodict.unparse({f'root_{i}': item}))
            return xml_docs
        elif isinstance(obj, dict):
            # If obj is a dictionary, check if it has exactly one root element
            if len(obj) == 1:
                root_name = list(obj.keys())[0]
                return xmltodict.unparse({root_name: obj[root_name]})
            else:
                # If obj has more than one root element, wrap each root element and return as a list of XML documents
                xml_docs = []
                for i, (key, value) in enumerate(obj.items()):
                    xml_docs.append(xmltodict.unparse({key: value}))
                return xml_docs
        else:
            # If obj is not a list or dictionary, raise an error
            raise ValueError('Invalid input format. Input must be a list or dictionary.')
    except xmltodict.expat.ExpatError as e:
        return str(e)



    
def deserialize(extension:str, object):
      match extension:
            case "json":
                 return deserialize_json(object)
            case "csv":
                  return depuis_csv(object)
            case "xml":
               return depuis_xml(object)
            case "yaml":
                return deserialize_yaml(object)
            case _:
                  raise ValueError('Fichier Non Pris en Charge')

def serialize(extension:str, object):
      match extension:
            case "json":
                 return serialize_json(object)
            case "csv":
                  return vers_csv(object)
            case "xml":
               return vers_xml(object)
            case "yaml":
                return serialize_yaml(object)
            case _:
                  raise('Fichier Non Pris en Charge')
def app(imported_path_element: str, exported_path_element: str):
    extension = imported_path_element.split(".")[-1]
    with open(imported_path_element, 'r') as f:
        obj = deserialize(extension, f)
        print(obj)
        data = {
            "json": serialize("json", obj),
            "csv": serialize("csv", obj),
            "xml": serialize("xml", obj),
            "yaml": serialize("yaml", obj)
        }
        del data[extension]
        key = list(data.keys())
        print("\nChoose a format for the exported file:\n")
        for i, k in enumerate(key):
            print(f"{i+1}. {k}\n")
        while True:
            try:
                choice = int(input(f"Insert your choice (1-{len(key)}): "))
                if 0 < choice < len(key) + 1:
                    break
                else:
                    print(f"\nInsert a value between (1-{len(key)})\n")
            except ValueError:
                print("Invalid input! Please enter a number.")

        selected_format = key[choice - 1]
        name = str(input('\nchoose a name for the file:\t'))
        exported_filename = f"{exported_path_element}/{name}.{selected_format}"
        with open(exported_filename, 'w') as file:
            file.write(data[selected_format])

            

