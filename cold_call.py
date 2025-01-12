# IMPORTING LIBRARIES
import requests
import pandas as pd

# API DETAILS
sid = "xyz6711"
api_key = "51a8676db4775e4f8c5464438137100a00873030bfa29e93"
caller_id = "09513886363"
token = "4217c68483647079f8ff5fd01d93a68bc198d0d9f5a64450"

# DATA LOADING TO GET PHONE NUMBERS ON BASIS OF STATUS
data = pd.read_csv("CRM_Data.csv")
stat_priority = {"Hot":1, "Warm":2, "Cold":3}

data["Priority"] = data["Status"].map(stat_priority)
final_data = data.sort_values(by="Priority")

#MAKING THE CALL
def call(ph, name, status):
    url = f"https://api.exotel.com/v1/Accounts/{sid}/Calls/connect"

    # PAYLOAD 
    payload = {
        "From": caller_id,
        "To": ph,
        "CallerId": caller_id,
        "Url": "",
        "Priority": "normal"
    }
    response = requests.post(url, data = payload, auth = (api_key,token))
    if response.status_code == 200:
        print(f"Call to {name}({ph}) successfully initiated! Status of Client : {status}")
    else:
        print(f"Failed to initiate call to {name}(ph)!! Status of client : {status}")
        print("Response Code:", response.status_code)
        print("Response Text:", response.text)

for index, row in final_data.iterrows():
    name = row["Customer Name"]
    phone = row["Phone No."]
    status = row["Status"]

    initiate = call(phone, name , status)
    time.sleep(2)

print("All calls completed!")