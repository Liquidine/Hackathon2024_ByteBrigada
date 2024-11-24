from openai import OpenAI
import pandas as pd
from flask import Flask, request, render_template


df = pd.read_csv('../../../../OneDrive/Počítač/SYB66_1_202310_Population, Surface Area and Density (1).csv', delimiter=',', skiprows=2)  # Preskočíme 2 prvé riadky
#df = pd.read_csv('C:\Users\molna\PycharmProjects\hackathon-2024\Hackathon2024_ByteBrigada\src\SYB66_1_202310_Population, Surface Area and Density (1).csv', delimiter=',', skiprows=2)  # Preskočíme 2 prvé riadky

df.columns = ["ID", "Region/Country/Area", "Year", "Series", "Value", "Footnotes", "Source"]
df["Value"] = df["Value"].replace(',', '', regex=True).astype(float)


average_values = df.groupby("Region/Country/Area")["Value"].mean()


asia_data = df[df["Region/Country/Area"] == "Asia"]


asia_data.to_csv("asia_data_cleaned.csv", index=False)


client = OpenAI()
def ask_ai(question, data):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a data analyst assistant. Answer user questions concisely based on the provided data."},
            {"role": "user", "content": f"Here is the data: {df}. {question}"}
        ],
    )

    answer = response.choices[0].message
    return answer

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ask', methods=['POST'])
def ask():
    question = request.form['question']
    answer = ask_ai(question, df)
    print("\nGenerated Code:")
    print(answer)
    return render_template('index.html', question=question, answer=answer)


if __name__ == '__main__':
    app.run(debug=True)

