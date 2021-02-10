import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px


# ############ Create custom components ############
def build_component(class_name, component=html.Div):
    def component_func(*args, className="", **kwargs):
        return component(*args, className=class_name + " " + className, **kwargs)

    return component_func


def Col(*args, width, **kwargs):
    class_name = f"col s{width}"
    return html.Div(*args, className=class_name, **kwargs)


def CustomSlider(id, min, max, label, **kwargs):
    mid = int((min + max) / 2)
    kwargs["value"] = kwargs.get("value", mid)
    return html.Div(
        [
            html.P(label),
            html.Br(),
            dcc.Slider(
                id=id,
                min=min,
                max=max,
                marks={i: str(i) for i in [min, mid, max]},
                tooltip={"always_visible": False},
                **kwargs,
            ),
        ]
    )


Row = build_component("row")
Card = build_component("card")
CardTitle = build_component("card-title")
CardContent = build_component("card-content")
CardAction = build_component("card-action")


# ############ Load Data ############
df = px.data.tips()
days = df.day.unique()

# ############ Initialize app ############
app = dash.Dash(
    __name__,
    external_stylesheets=[
        "https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css"
    ],
    external_scripts=[
        "https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"
    ],
)
server = app.server  # gunicorn needs this for deployment


# ############ Define components and layouts ############
controls = [
    CustomSlider(id="wind-direction", min=250, max=290, label="Wind Direction"),
    CustomSlider(id="yaw-angle", min=250, max=290, label="Yaw angle T1"),
    CustomSlider(id="x-plane", min=0, max=3000, label="X Normal Plane Intercept"),
    CustomSlider(id="y-plane", min=-100, max=100, label="Y Normal Plane Intercept"),
]


navbar = html.Nav(
    html.Div(
        className="nav-wrapper teal",
        children=[
            html.Img(
                src=app.get_asset_url("dash-logo.png"),
                style={"float": "right", "height": "100%", "padding-right": "15px"},
            ),
            html.A(
                "Floris Demo",
                className="brand-logo",
                href="https://plotly.com/dash/",
                style={"padding-left": "15px"},
            ),
        ],
    )
)


left_section = Card(
    CardContent(
        [
            CardTitle("Results with GCH"),
        ]
    )
)

right_section = Card(CardContent([CardTitle("Results without GCH")]))

app.layout = html.Div(
    # className="container",
    style={"--slider_active": "teal"},
    children=[
        navbar,
        html.Br(),
        Row(
            Col(
                width=12,
                children=Card(CardContent(Row([Col(c, width=3) for c in controls]))),
            )
        ),
        Row(
            [
                Col(width=6, children=left_section),
                Col(width=6, children=right_section),
            ]
        ),
    ],
)


if __name__ == "__main__":
    app.run_server(debug=True)
