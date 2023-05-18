import requests
import os
import json
import pandas as pd
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI
from pandasai.llm.open_assistant import OpenAssistant

def FindAlternateGroups(url):
    
    num = 1
    url = url.rsplit("=", 1)
    url = url[0]+ '='
    extracted_data = []
    while True:
      try:
        # Send GET request to the URL
        response = requests.get(url+ str(num))
        num= int(num)+1
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = json.loads(response.text)
        
            # Extract the desired information from the data
            for product in data['products']:
                extracted_data.append({
                    'title': product['title'],
                    'id': product['id'] ,
                    'handle': product['handle'],
                    'vendor': product['vendor'],
                    'product_type': product['product_type'],
                    'tags':product['tags'],
                    'variants': product['variants'] 
                })
        else:
            print("Request failed with status code:", response.status_code)
            break
      
      except Exception as e:
          break
    
    # Convert the extracted data to JSON format
    json_data = json.dumps(extracted_data, indent=4)

    df = pd.read_json(json_data, orient='columns')
    
    df['variants_url']=""
    for j in range(len(df)):
      df['variants_url'][j] = ['https://www.boysnextdoor-apparel.co/products/'+ df['handle'][j]+ '?variant=' + str(df.iloc[j]['variants'][i]['id']) for i in range(len(df.iloc[j]['variants']))]
        
    df.drop(['variants'],axis = 1,inplace=True)
    
    # Group URLs by Product Category
    grouped_urls = df.groupby('product_type')['variants_url'].apply(list).to_dict()

    # Convert to JSON format
    json_output = json.dumps(grouped_urls, indent =4)

    return json_output

