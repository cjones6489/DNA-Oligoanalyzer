import requests
import json
import pandas as pd
import numpy as np

# List of keys returned by API 
params_list = ['sequence', 'thermo', 'deltaS', 'deltaG', 'deltaH']

# Create empty dataframe for returned sequence parameters
DNA_params_df = pd.DataFrame(columns=params_list)

# Read in excel file
sequence_df = pd.read_csv('nupack_automation/hp6_4_base_matches.csv', header=None)
sequence_arr = sequence_df[0].to_numpy() # convert to numpy array

# Iterate over all sequences in list and append values to dataframe
for sequence in sequence_arr:
  print(f'Sequence={sequence}&NaConc=125&FoldingTemp=25&MgConc=0.3&NucleotideType=DNA')

  url = "https://www.idtdna.com/Restapi/v1/OligoAnalyzer/Hairpin"

  payload = f'Sequence={sequence}&NaConc=125&FoldingTemp=25&MgConc=0.3&NucleotideType=DNA'
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': 'Bearer 4dae531585b1f4762e8a8728cc0ea534',
    'Cookie': 'ARRWestffinity=ba40cc5de3760d56c7d5bda31309fd0f34ac4ddd6a11aaa1f1aa3943af5c5db2'
  }

  response = requests.request("POST", url, headers=headers, data = payload)

  print(response.text.encode('utf8'))
  print(response.json()[0]['sequence'])


  sequence_params = pd.Series([response.json()[0][param] for param in params_list], index=DNA_params_df.columns)
  
  DNA_params_df = DNA_params_df.append(sequence_params, ignore_index=True)

DNA_params_df.to_csv('hp6_4_base_params.csv', index=False)