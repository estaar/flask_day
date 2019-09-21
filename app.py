from flask import Flask
import requests
import pandas as pd

app = Flask(__name__)
def get_data():
    a = requests.get("https://opendata.arcgis.com/datasets/ea875858ec11462ab4e8a2ef5dc2c4ce_0.geojson")

    data = a.json()

    b = data["features"]

    pandas_list = []
    for x in b:
        pandas_list.append(x["properties"])

    df = pd.DataFrame(pandas_list)

    df2 = df["Year_and_Quarter"].str.split(" ", expand=True)
    df2.columns = ["Year", "Quarter"]

    df3 = df.join(df2, how="left")
    df3.drop("OBJECTID", axis=1, inplace=True)

    return df3

@app.route('/ex1')
def hello_world():
    df3 = get_data()
    df4 = df3.groupby(['Year', 'Sector']).sum()
    return df4.to_html()
@app.route('/ex2')
def hello_worl():
    df3 = get_data()
    df4 = df3.groupby(['Sector', 'Year']).sum()
    table = pd.pivot_table(df4, values="Kshs_Million", index=["Sector"], columns=["Year"])
    return table.to_html()


if __name__ == '__main__':
    app.run(debug=True)
