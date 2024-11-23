import data
import requests
import pandas as pd
import io
import openai
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
# URL na stiahnutie dát o potvrdených prípadoch COVID-19
url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"

# Poslanie GET požiadavky na stiahnutie súboru
response = requests.get(url)

if response.status_code == 200:
    # Načítanie dát do DataFrame
    data = pd.read_csv(io.StringIO(response.text))

    # Zobrazenie prvých 5 riadkov dát
    print(data.head())

    # Uistíme sa, že všetky dátové stĺpce, ktoré majú byť numerické, sú konvertované na čísla (float)
    # Predpokladáme, že stĺpce od 4. stĺpca obsahujú počet potvrdených prípadov
    for col in data.columns[4:]:
        data[col] = pd.to_numeric(data[col], errors='coerce')  # Prevod na číslo, chyby sa nastavia na NaN

    # Sčíta všetky prípady pre každú krajinu (počítame od 5. stĺpca)
    total_cases = data.iloc[:, 4:].sum(axis=0)

    # Vytvorenie textu pre analýzu
    country_data = "\n".join([f"{data.columns[i]}: {total_cases[i]}" for i in range(len(total_cases))])

    # Príprava textu pre OpenAI na analýzu
    analysis_request = f"Analyze the following data on confirmed COVID-19 cases across countries:\n{country_data}"

    # Použitie OpenAI na analýzu týchto údajov
    response_openai = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": analysis_request}
        ],
        max_tokens=500
    )

    # Výstup analýzy
    print("OpenAI Analýza:")
    print(response_openai['choices'][0]['message']['content'].strip())

else:
    print(f"Chyba pri načítaní údajov: {response.status_code}")