import uuid
import pandas as pd
import plotly.express as px
from dash_iconify import DashIconify
from dash_extensions.enrich import (
    Output,
    Input,
    State,
    html,
    DashProxy,
    LogTransform,
    DashLogger,
    LogConfig,
    get_notification_log_writers,
)
from flask_instance import (
    server,
)  # This was created to wrap several Flask applications into one

from dash import dcc, no_update
import base64
import io
import traceback
import dash_mantine_components as dmc

sample_data_path = "static/population_final.csv"


def setup_custom_notifications_log_config():
    log_id = "notifications_provider"
    log_output = Output(log_id, "children")

    def notification_layout_transform(layout):
        layout.append(html.Div(id=log_id))
        return [dmc.NotificationsProvider(layout, position="top-right")]

    return LogConfig(
        log_output, get_notification_log_writers(), notification_layout_transform
    )


def serve_layout():
    session_id = str(uuid.uuid4())

    return html.Div(
        [
            dmc.Modal(
                id="modal-inside",
                title="CSV Visualizer",
                overflow="inside",
                zIndex=10000,
                size="lg",
                children=[
                    dmc.Text(
                        "CSV visualizer application allows you to upload a CSV file and visualize it."
                    ),
                    dmc.Text(
                        "It accepts CSV and simple Excel files. It is possible to select the columns for the x and y axis, as well as the line style and color."
                    ),
                    dmc.Text(
                        "The app is designed to be simple and easy to use. Excel files with multiple sheets are not supported. The app is not designed to handle large files."
                    ),
                    dmc.Text(
                        "Excel files should contain first row as header as column names."
                    ),
                    dmc.Text(
                        "If you click to 'Load population data' button, it will load public pupulation data for many countries. Data is taken from https://data.worldbank.org/"
                    ),
                    dmc.Text(
                        "If you have any suggestions or questions, please feel free to contact me."
                    ),
                    dmc.Text("Email: ashkhen09300@gmail.com"),
                    dmc.Text("Enjoy the app!"),
                ],
            ),
            html.Div(
                [
                    dcc.Store(data=[], id="session_ids"),
                    dcc.Store(data=session_id, id="session_id"),
                    dcc.Store(id="df"),
                    html.H1(
                        children="CSV Visualizer",
                        style={
                            "textAlign": "center",
                            "margin-top": "3rem",
                            "margin-bottom": "0.5rem",
                        },
                    ),
                    dcc.Graph(
                        id="line-chart",
                        figure=px.line(),
                        style={
                            "height": "80vh",
                        },
                    ),
                ],
                style={
                    "backgroundColor": "#272a31",
                    "color": "white",
                    "width": "65%",
                    "height": "100vh",
                    "display": "inline-block",
                    "verticalAlign": "top",
                },
            ),
            html.Div(
                [
                    html.Div(
                        dmc.Button(
                            "INFO",
                            id="modal-inside-button",
                            leftIcon=DashIconify(icon="ic:round-info", width="3rem"),
                            size="sm",
                            color="white",
                            variant="outline",
                            style={"margin-bottom": "2rem"},
                        ),
                        style={"textAlign": "right", "margin-top": "1rem"},
                    ),
                    html.Div(
                        dmc.Button(
                            "Load population data",
                            id="loading-button",
                            leftIcon=DashIconify(
                                icon="line-md:downloading-loop", width="3rem"
                            ),
                            size="sm",
                            color="white",
                            variant="outline",
                            style={"margin-bottom": "2rem"},
                        ),
                        style={"textAlign": "right", "margin-top": "1rem"},
                    ),
                    dcc.Upload(
                        id="upload-data",
                        children=html.Div(
                            [
                                "Drag and Drop or ",
                                html.A(children="Select File"),
                            ]
                        ),
                        style={
                            "color": "silver",
                            "borderWidth": "1px",
                            "borderStyle": "dashed",
                            "borderRadius": "15px",
                            "textAlign": "center",
                            "padding": "5rem 0",
                            "margin-bottom": "2rem",
                            "margin-top": "10rem",
                        },
                    ),
                    dcc.Dropdown(
                        id="dropdown-y",
                        style={
                            "width": "100%",
                            "font-size": "15px",
                            "color": "white",
                            "margin-bottom": "2rem",
                        },
                    ),
                    dcc.Dropdown(
                        id="dropdown-x",
                        style={
                            "width": "100%",
                            "font-size": "15px",
                            "color": "white",
                            "margin-bottom": "2rem",
                        },
                    ),
                    dcc.RadioItems(
                        id="line-style",
                        options=[
                            {"label": "Solid", "value": "solid"},
                            {"label": "Scatter", "value": "dash"},
                        ],
                        value="solid",
                        labelStyle={"display": "inline-block"},
                        style={
                            "margin-bottom": "2rem",
                        },
                    ),
                    dmc.ColorPicker(
                        id="color-picker",
                        format="rgba",
                        value="rgba(41, 96, 214, 1)",
                        style={
                            "width": "100%",
                            "font-size": "15px",
                            "color": "white",
                            "margin-bottom": "2rem",
                        },
                    ),
                ],
                style={
                    "display": "inline-block",
                    "verticalAlign": "top",
                    "width": "35%",
                    "height": "100%",
                    "padding": "2rem",
                    "boxSizing": "border-box",
                },
            ),
        ],
        style={
            "backgroundColor": "#43454a",
        },
    )


if __name__ == "__main__":
    URL_BASE_PATHNAME = None
else:
    URL_BASE_PATHNAME = "/apps/csv/"

app = DashProxy(
    __name__,
    transforms=[LogTransform(setup_custom_notifications_log_config())],
    server=server,
    url_base_pathname=URL_BASE_PATHNAME,
)
app.title = "CSV Visualizer"

app.layout = serve_layout


@app.callback(
    [
        Output("dropdown-x", "options"),
        Output("dropdown-y", "options"),
        Output("dropdown-x", "value"),
        Output("dropdown-y", "value"),
        Output("df", "data"),
    ],
    Input("loading-button", "n_clicks"),
    prevent_initial_call=True,
)
def load_sample_data(n_clicks):
    df = pd.read_csv(sample_data_path, sep="[;]")
    options_x = [{"label": col, "value": col} for col in df.columns]
    options_y = [{"label": col, "value": col} for col in df.columns]
    value_x = options_x[0]["value"]
    value_y = options_y[1]["value"]

    return options_x, options_y, value_x, value_y, df.to_json()


@app.callback(
    [
        Output("line-chart", "figure"),
        Output("session_ids", "data"),
    ],
    [
        Input("dropdown-x", "value"),
        Input("dropdown-y", "value"),
        Input("color-picker", "value"),
        Input("line-style", "value"),
    ],
    [State("session_id", "data"), State("session_ids", "data"), State("df", "data")],
    log=True,
)
def update_chart(
    selected_x,
    selected_y,
    selected_color,
    line_style,
    session_id,
    session_ids,
    df,
    dash_logger: DashLogger,
):
    if session_id not in session_ids:
        # Only show info notifications during first visit.
        # Keep in mind that the refresh of the page will be treated as a new session.
        session_ids.append(session_id)
        dash_logger.info(
            "Welcome to the CSV Visualizer App!",
            autoClose=5000,
            title=None,
            icon=DashIconify(icon="ic:round-celebration", width="3rem"),
        )
        dash_logger.info(
            "Please be informed, that we don't keep any data from you in our system.",
            autoClose=8000,
            title=None,
            icon=DashIconify(icon="ic:round-info", width="3rem"),
        )
    max_value_x = 1  # Default value for max_value_x
    max_value_y = 1  # Default value for max_value_y

    if df is not None:
        try:
            df = pd.read_json(io.StringIO(df))
            if selected_x in df.columns:
                max_value_x = df[selected_x].max()
            if selected_y in df.columns:
                max_value_y = df[selected_y].max()
        except Exception as e:
            dash_logger.error(f"Error loading data: {e}")
    fig_update = px.line()
    figure_design(fig_update, max_value_x, max_value_y)
    if selected_x is None:
        return fig_update, session_ids

    if line_style == "solid":  # If 'solid' style selected, plot line chart
        fig_update = px.line(df, x=selected_x, y=selected_y, line_shape="spline")
        fig_update.update_traces(line=dict(color=selected_color, dash=line_style))
    else:  # Otherwise, plot scatter plot
        fig_update = px.scatter(df, x=selected_x, y=selected_y)
        fig_update.update_traces(marker=dict(color=selected_color))

    figure_design(fig_update, max_value_x, max_value_y)
    return fig_update, session_ids


@app.callback(
    [
        Output("dropdown-x", "options"),
        Output("dropdown-y", "options"),
        Output("dropdown-x", "value"),
        Output("dropdown-y", "value"),
        Output("df", "data"),
    ],
    Input("upload-data", "contents"),
    State("upload-data", "filename"),
    prevent_initial_call=True,
    log=True,
)
def upload_file(content, filename, dash_logger: DashLogger):
    _, encoded_content = content.split(",")
    decoded = base64.b64decode(encoded_content)
    try:
        if "csv" in filename:
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")), sep="[;]")
        elif "xls" in filename:
            df = pd.read_excel(io.BytesIO(decoded), header=0)
        else:
            dash_logger.error(
                "Only CSV and simple Excel files are allowed.", autoClose=5000
            )
            return no_update, no_update, no_update, no_update, no_update

        options_x = [{"label": col, "value": col} for col in df.columns]
        options_y = [{"label": col, "value": col} for col in df.columns]
        value_x = options_x[0]["value"]
        value_y = options_y[1]["value"]
        return options_x, options_y, value_x, value_y, df.to_json()
    except Exception:
        traceback.print_exc()
        dash_logger.error(f"Unable to process {filename} file", autoClose=5000)
        return no_update, no_update, no_update, no_update, no_update


def figure_design(fig, max_value_x, max_value_y):
    fig.update_layout(
        plot_bgcolor="#272a31",
        paper_bgcolor="#272a31",
        font_color="white",
        xaxis=dict(
            gridcolor="grey",
            linecolor="white",
            zeroline=False,
        ),
        yaxis=dict(
            gridcolor="grey",
            linecolor="white",
            zeroline=False,
            showgrid=True,
        ),
    )


def toggle_modal(n_clicks, opened):
    return not opened


app.callback(
    Output("modal-inside", "opened"),
    Input("modal-inside-button", "n_clicks"),
    State("modal-inside", "opened"),
    prevent_initial_call=True,
)(toggle_modal)

if __name__ == "__main__":
    app.run_server(debug=False)
