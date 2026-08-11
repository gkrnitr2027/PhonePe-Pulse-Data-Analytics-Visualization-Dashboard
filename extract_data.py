import os
import json
import pandas as pd

base_path = os.path.join("pulse", "data")

def clean_name(text):
    return text.replace("-", " ").title().strip() if text else text

def extract_all_dynamic():
    agg_trans, agg_user = [], []
    map_trans, map_user = [], []
    top_trans, top_user = [], []

    print("Scanning PhonePe Pulse repository for JSON files... This might take a minute.")

    # os.walk scans every single folder and subfolder automatically
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                
                # We only want State-level data, so we check if 'state' is in the folder path
                if 'state' in file_path.lower():
                    # Extract the State, Year, and Quarter directly from the file path
                    path_parts = file_path.replace("\\", "/").split("/")
                    
                    try:
                        # In the structure .../state/maharashtra/2022/1.json
                        state_name = clean_name(path_parts[-3]) 
                        year = int(path_parts[-2])
                        quarter = int(file.replace(".json", ""))
                        
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            
                        if not data or data.get('data') is None:
                            continue
                            
                        payload = data['data']
                        
                        # 1. Aggregated Transactions
                        if payload.get('transactionData'):
                            for item in payload['transactionData']:
                                agg_trans.append({
                                    'State': state_name, 'Year': year, 'Quarter': quarter,
                                    'Transaction_Type': item.get('name', ''),
                                    'Transaction_Count': item['paymentInstruments'][0].get('count', 0),
                                    'Transaction_Amount': item['paymentInstruments'][0].get('amount', 0.0)
                                })
                                
                                
                        # 5 & 6. Top Transactions & Top Users
                        for entity in ['districts', 'pincodes']:
                            if payload.get(entity):
                                for item in payload[entity]:
                                    # Top Transactions
                                    if item.get('metric'):
                                        top_trans.append({
                                            'State': state_name, 'Year': year, 'Quarter': quarter,
                                            'Entity_Type': entity.capitalize(),
                                            'Entity_Name': str(item.get('entityName') or item.get('name', '')),
                                            'Transaction_Count': item['metric'].get('count', 0),
                                            'Transaction_Amount': item['metric'].get('amount', 0.0)
                                        })
                                        
                    except Exception as e:
                        # Skip if there's an unexpected file structure
                        pass

    # Save to CSV
    pd.DataFrame(agg_trans).to_csv("aggregated_transactions.csv", index=False)
    pd.DataFrame(top_trans).to_csv("top_transactions.csv", index=False)

    print("\n" + "="*50)
    print("SUCCESS! Data Extracted:")
    print(f"- aggregated_transactions.csv : {len(agg_trans)} rows")
    print(f"- top_transactions.csv        : {len(top_trans)} rows")
    print("="*50)

if __name__ == "__main__":
    extract_all_dynamic()