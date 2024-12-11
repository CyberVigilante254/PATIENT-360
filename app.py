import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import numpy as np

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "Patient 360"

# Mock Data
patients = pd.DataFrame({
    "Patient ID": [f"P{i:03d}" for i in range(1, 21)],
    "Readmission Risk": np.random.uniform(0, 100, 20),
    "Cost Analysis": np.random.uniform(5000, 20000, 20),
    "Claims Status": np.random.choice(["Approved", "Flagged", "Denied"], 20)
})

provider_ranking = pd.DataFrame({
    "Provider": [f"Provider {i}" for i in range(1, 11)],
    "Efficiency Score": np.random.uniform(70, 100, 10)
})

# Layout Colors
colors = {
    "background": "#A8DADC",
    "card": "#FFFFFF",
    "text": "#1D3557",
    "accent": "#457B9D"
}

# App Layout
app.layout = html.Div(style={"backgroundColor": colors["background"], "padding": "20px"}, children=[
    html.H1("Patient 360 Dashboard", style={"color": colors["text"], "textAlign": "center"}),

    # Overview Section
    html.Div(style={"display": "flex", "gap": "20px", "justifyContent": "center"}, children=[
        html.Div(style={"backgroundColor": colors["card"], "padding": "20px", "borderRadius": "10px"}, children=[
            html.H4("Total Patients", style={"color": colors["accent"]}),
            html.P(f"{len(patients)}", style={"fontSize": "24px", "color": colors["text"]})
        ]),
        html.Div(style={"backgroundColor": colors["card"], "padding": "20px", "borderRadius": "10px"}, children=[
            html.H4("Avg. Readmission Risk", style={"color": colors["accent"]}),
            html.P(f"{patients['Readmission Risk'].mean():.2f}%", style={"fontSize": "24px", "color": colors["text"]})
        ]),
        html.Div(style={"backgroundColor": colors["card"], "padding": "20px", "borderRadius": "10px"}, children=[
            html.H4("Flagged Claims", style={"color": colors["accent"]}),
            html.P(f"{(patients['Claims Status'] == 'Flagged').sum()}", style={"fontSize": "24px", "color": colors["text"]})
        ]),
    ]),

    html.Hr(style={"margin": "40px 0"}),

    # Readmission Risk Section
    html.Div(children=[
        html.H3("Readmission Risk Analysis", style={"color": colors["text"]}),
        dcc.Graph(
            figure=px.bar(patients, x="Patient ID", y="Readmission Risk", color="Readmission Risk",
                          color_continuous_scale="tealgrn", title="Patient Readmission Risk",
                          labels={'Readmission Risk': 'Risk (%)'})
        )
    ]),

    html.Hr(style={"margin": "40px 0"}),

    # Cost Analysis Section
    html.Div(children=[
        html.H3("Cost Analysis", style={"color": colors["text"]}),
        dcc.Graph(
            figure=px.histogram(patients, x="Cost Analysis", nbins=10, title="Cost Distribution",
                                 color_discrete_sequence=[colors["accent"]],
                                 labels={'Cost Analysis': 'Cost ($)'})
        )
    ]),

    html.Hr(style={"margin": "40px 0"}),

    # Provider Ranking Section
    html.Div(children=[
        html.H3("Provider Efficiency Rankings", style={"color": colors["text"]}),
        dcc.Graph(
            figure=px.bar(provider_ranking, x="Efficiency Score", y="Provider", orientation="h",
                          color="Efficiency Score", color_continuous_scale="tealgrn",
                          title="Top Providers by Efficiency Score",
                          labels={'Efficiency Score': 'Efficiency Score'})
        )
    ]),

    # Insights Section
    html.Div(children=[
        html.H3("Insights and Recommendations", style={"color": colors["text"]}),
        html.P("1. High readmission risk patients should be monitored closely to prevent unnecessary hospitalizations.",
                style={"color": colors["text"]}),
        html.P("2. Claims flagged for review may indicate potential issues that need addressing to improve approval rates.",
                style={"color": colors["text"]}),
        html.P("3. Providers with higher efficiency scores are likely delivering better value care; consider referrals to these providers.",
                style={"color": colors["text"]}),
    ], style={"marginTop": "40px"})
])

# Run App
if __name__ == "__main__":
    app.run_server(debug=True)
