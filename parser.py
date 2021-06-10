import csv
import json
import numpy as np
import pandas as pd



typeDictionary = { #maps data types in file to python data types
    'BIT':'bool',
    'REAL32':'float32',
    'REAL64':'float64',
    'INT16':'int16',
}
"""
Function to read all information from the text file
Parameters:
filename (str): name of text file

Returns:
data : dataframe with required data
properties : file properties for JSON  
"""
def read_file():
    filepath = input("Enter file path: ")
    data = read_data(filepath)
    properties = read_file_properties(filepath)
    return data, properties

"""Reads the file properties for JSON """
def read_file_properties(filename):
    properties = {}#'file name':'','start date':'','start time':'','end date':'','end time':'' }
    with open(filename) as file:
        reader = csv.reader(file,delimiter='\t')
        line_count = 0
        for row in reader:
            if line_count==0:
                properties['file name'] = row[1]
            if line_count == 2:
                properties['start date'] = row[2]
                properties['start time'] = row[3]
            if line_count == 3:
                properties['end date'] = row[2]
                properties['end time'] = row[3]
                break
            line_count += 1
    return properties
    
"""Reads data from text file with correct datatype"""
def read_data(filename):
    skiprows = list(range(0,6))+list(range(7,21))
    datatypes = pd.read_csv(filename, delim_whitespace=True, skiprows=skiprows , nrows=1, dtype='string') #read in data types of each column
    datatypes = datatypes.iloc[:,1::2] #delete extra Name columns
    datatypes.iloc[0,:] = [typeDictionary[type] for type in datatypes.iloc[0,:]] #convert data types to proper names using typeDictionary
    datatypes = datatypes.iloc[0,:].to_dict() #converts to series then to dictionary

    skiprows = list(range(0,6))+list(range(7,28))

    data = pd.read_csv('test_dataset_1.txt' , delim_whitespace=True , skiprows=skiprows,  skipfooter=1, dtype=datatypes)
    data = pd.merge(data.iloc[:,0],data.iloc[:,1::2],left_index=True, right_index=True) #delete all extra time columns
    data = data.rename(columns={'Name':'Time'}) #rename time column to have proper header
    return data

"""Creates JSON"""
def create_JSON(data, properties):
    properties['mean'] = data.iloc[:,1:-1].mean(axis=0).to_dict() #calculates mean, not including the time column
    json_data = json.dumps(properties, indent=4)
    return json_data

"""
returns:
data : pandas dataframe 
json_data : json with file and mean information
"""
def main():
    
    (data,properties) = read_file()
    json_data = create_JSON(data,properties)
    return data, json_data

if __name__ == "__main__":
    main()
