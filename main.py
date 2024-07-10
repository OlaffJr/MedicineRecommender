import requests
from bs4 import BeautifulSoup
import json
from pymongo import MongoClient

def get_medicine_details(link, medicine_name):
    s = requests.Session()
    data = s.get(link).text
    soup = BeautifulSoup(data, 'html.parser')
    price = soup.find('span', class_='final-price')
    description = soup.find_all('div', class_='druginfo_cont')

    data2 = [i.get_text() for i in description]

    return {
        "medicine_name": medicine_name,
        "price": price.get_text() if price else None,
        "description": data2
    }

def get_medicines(link, disease_name):
    s = requests.Session()
    data = s.get(link).text
    soup = BeautifulSoup(data, 'html.parser')
    li_medicine_list = soup.find_all('li', class_='product-item')
    medicinedata = []
    for element in li_medicine_list:
        a_tags = element.find_all('a', href=True)
        for a in a_tags:
            href = a.get('href')
            medicine_details = get_medicine_details(href, element.get_text().strip())
            medicine_details["disease_name"] = disease_name.strip()
            medicinedata.append(medicine_details)
    return medicinedata

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['medicine_database']
collection = db['medicines']

base_url = r"https://www.netmeds.com/prescriptions"

s = requests.Session()
data = s.get(base_url).text

soup = BeautifulSoup(data, 'html.parser')

# Find the <ul> with class "alpha-drug-list"
ul_alpha_drug_list = soup.find_all('ul', class_='alpha-drug-list')

if ul_alpha_drug_list:
    for element in ul_alpha_drug_list:
        child_elements = element.find_all(recursive=False)
        for i in child_elements:
            a_tags = i.find_all('a', href=True)
            for a in a_tags:
                href = a.get('href')
                disease_name = i.get_text().strip()
                output = get_medicines(href, disease_name)
                for temp in output:
                    collection.insert_one(temp)
else:
    print("No <ul> with class 'alpha-drug-list' found.")


