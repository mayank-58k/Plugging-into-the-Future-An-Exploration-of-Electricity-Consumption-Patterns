from flask import Flask, jsonify
import pandas as pd
import os

app = Flask(__name__)

DATA_FILE = "electricity_data.csv"


def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
    else:
        # dummy dataset if CSV not present
        data = {
            "Year":[2019,2019,2019,2020,2020,2020],
            "Month":["Jan","Feb","Mar","Jan","Feb","Mar"],
            "Region":["North","South","West","North","South","West"],
            "Consumption":[1200,1500,1100,1700,1600,1400]
        }
        df = pd.DataFrame(data)

    return df


def analyze_data():
    df = load_data()

    total_consumption = df["Consumption"].sum()
    avg_consumption = df["Consumption"].mean()
    max_consumption = df["Consumption"].max()

    region_consumption = df.groupby("Region")["Consumption"].sum().to_dict()

    return {
        "total_consumption": int(total_consumption),
        "average_consumption": round(avg_consumption,2),
        "maximum_consumption": int(max_consumption),
        "region_wise": region_consumption
    }


@app.route("/")
def dashboard():

    stats = analyze_data()

    return f"""
    <!DOCTYPE html>
    <html>
    <head>

    <title>Electricity Consumption Dashboard</title>

    <style>

    body {{
        font-family: Arial;
        background:#f4f6f9;
        margin:0;
        padding:0;
    }}

    header {{
        background:#2c3e50;
        color:white;
        padding:20px;
        text-align:center;
    }}

    .container {{
        width:90%;
        margin:auto;
        margin-top:30px;
    }}

    .stats {{
        display:flex;
        gap:20px;
        margin-bottom:30px;
    }}

    .card {{
        background:white;
        padding:20px;
        border-radius:8px;
        box-shadow:0 2px 5px rgba(0,0,0,0.2);
        flex:1;
        text-align:center;
    }}

    .card h3 {{
        margin:0;
        color:#555;
    }}

    .card p {{
        font-size:24px;
        font-weight:bold;
        margin-top:10px;
    }}

    .tableau-section {{
        background:white;
        padding:20px;
        border-radius:8px;
        box-shadow:0 2px 5px rgba(0,0,0,0.2);
    }}

    </style>

    </head>

    <body>

    <header>
    <h1>Electricity Consumption Analysis Dashboard</h1>
    <p>Data Visualization using Tableau + Flask</p>
    </header>

    <div class="container">

        <div class="stats">

            <div class="card">
                <h3>Total Consumption</h3>
                <p>{stats['total_consumption']}</p>
            </div>

            <div class="card">
                <h3>Average Consumption</h3>
                <p>{stats['average_consumption']}</p>
            </div>

            <div class="card">
                <h3>Maximum Consumption</h3>
                <p>{stats['maximum_consumption']}</p>
            </div>

        </div>

        <div class="tableau-section">

        <h2>Electricity Consumption Analysis (2019–2020)</h2>

        <div class='tableauPlaceholder' id='viz'>
            <object class='tableauViz' width='100%' height='800'>
                <param name='host_url' value='https://public.tableau.com/' />
                <param name='embed_code_version' value='3' />
                <param name='name' value='electricity-dashboard/Story1' />
                <param name='tabs' value='no' />
                <param name='toolbar' value='yes' />
            </object>
        </div>

        </div>

    </div>

    <script src="https://public.tableau.com/javascripts/api/viz_v1.js"></script>

    </body>
    </html>
    """


@app.route("/api/stats")
def stats_api():
    return jsonify(analyze_data())


if __name__ == "__main__":
    app.run(debug=True)