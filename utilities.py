import json
import pandas as pd
import os


def dic(inputDict, parentKey=None, parentDict=None):
    if parentDict is None:
        parentDict = {}

    for key, value in inputDict.items():
        if parentKey is not None:
            key = f'{parentKey}_{key}'
        if isinstance(value, list):
            listValue = lst(value, key, parentDict)
            parentDict.update(listValue)
            continue
        elif isinstance(value, dict):
            dictValue = dic(value, key, parentDict)
            parentDict.update(dictValue)
            continue

        elif key in parentDict:  # If key already exists, convert value to list
            existing_value = parentDict[key]
            if not isinstance(existing_value, list):
                parentDict[key] = [existing_value]  # Convert existing value to list
            parentDict[key].append(value)  # Append new value to list
        else:
            parentDict.update({key: value})

    return parentDict

def lst(inputList, parentKey=None, parentDict=None):
    outputDict = {}
    for item in inputList:
        if isinstance(item, dict):
            newItem = dic(item, parentKey, parentDict)
            outputDict.update(newItem)
            continue
        elif isinstance(item, list):
            lst(item)
    return outputDict

def json_to_excel(json_file):
    data = json.load(open(json_file, 'r'))
    dictData = dic(data)

    df = pd.DataFrame(dictData)
    # df = df.transpose()
    output_file = json_file.replace('.json', '.xlsx')

    df.to_excel(output_file, index=False)
    print(f"Excel file saved: {output_file}")

if __name__ == "__main__":
    # Replace with your JSON file path
    json_file = 'output/db0/f24-coi-ch1-shield-down.json'

    json_to_excel(json_file)
