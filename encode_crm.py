# IMPORTING ALL LIBRARIES
from faker import Faker
import pandas as pd
import random
from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client

# ASSIGNING LEAD SCORE
def lead_score_calc(industry, location, revenue, interest):
    score = 0
    if industry in ["Tech", "Finance"]:
        score += 20
    if location in ["Delhi", "Bangalore", "Gwahati"]:
        score += 10
    if revenue > 500000:
        score += 15
    if interest == "Yes":
        score += 10
    else:
        score -= 20
    return score

# ASSIGNING STATUS TO PRIORITIZE THE TARGET AUDIENCE FOR CALLS
def assign_status(score):
    if score >= 50:
        status = "Hot"
    elif score > 30:
        status = "Warm"
    else:
        status = "Cold"
    return status

# CREATING A FAKE DATABASE
fake = Faker('en_IN')

def gen_crm_data(num):
    industries = ["Tech", "Healthcare", "Retail", "Finance", "Manufacturing"]
    locations = ["Delhi", "Bangalore", "Mumbai", "Guwahati", "Chennai", "Hyderabad"]
    interests = ["Yes", "No"]

    data = []

    for i in range(num):
        industry = random.choice(industries)
        location = random.choice(locations)
        interest = random.choice(interests)
        revenue = round(random.uniform(50000,1000000),2)

        score = lead_score_calc(industry, location, revenue, interest)

        status = assign_status(score)

        data.append({
            "Customer ID": fake.uuid4(),
            "Customer Name": fake.name(),
            "Email": fake.email(),
            "Phone No.": fake.phone_number(),
            "Company": fake.company(),
            "Industry": industry,
            "Location": location,
            "Annual Revenue": revenue,
            "Interest": interest,
            "Lead Score": score,
            "Status": status
        })

    return data

data = gen_crm_data(2000)
df = pd.DataFrame(data)
df.to_csv("CRM_Data.csv")

print(df.head())
