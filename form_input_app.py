from dash import Dash, dash_table, html, Input, Output, ctx, dcc, callback, State
import dash_mantine_components as dmc
import pandas as pd

# list of columns:
# Date, Time, Motor Name/Motor Size, Serial Number, Status Start, Status End

# create a dropdown for Status Column
status_data = {
    "status-start": ["IM", "WOP", "RTG", "OJ", "STB"],
    "status-end": ["IM", "WOP", "RTG", "OJ", "STB"],
}

new_order_line = {
    "date": "",
    "time": "",
    "motor_name_size": "",
    "serial_number": "",
    "status_start": "",
    "status_end": "",
}
# date
# time
# motor-name-size
# serial-number
# status-start
# status-end

df_status = pd.DataFrame(status_data)
df_new_order_line = pd.DataFrame(new_order_line, index=range(5))

app = Dash(__name__)

title = html.H4("Order Entry Table", style={"textAlign": "center", "margin": 30})
add_button = html.Button("Add Rows", n_clicks=0, id="add-btn")

table = dash_table.DataTable(
    id="table",
    columns=[
        {
            "name": "Date",
            "id": "date",
            "editable": True,
            # "type": "datetime",  # Set column type to datetime
        },
        {
            "name": "Time",
            "id": "time",
            "editable": True,
            # "type": "datetime",  # Set column type to time
        },
        {
            "name": "Motor Name/Motor Size",
            "id": "motor_name_size",
            "editable": True,
        },
        {
            "name": "Serial Number",
            "id": "serial_number",
            "editable": True,
        },
        {
            "name": "Status Start",
            "id": "status_start",
            "editable": True,
            "presentation": "dropdown",  # Set dropdown presentation
        },
        {
            "name": "Status End",
            "id": "status_end",
            "editable": True,
            "presentation": "dropdown",  # Set dropdown presentation
        },
    ],
    data=df_new_order_line.to_dict("records"),
    row_deletable=True,
    dropdown={
        "status_start": {
            "options": [{"label": i, "value": i} for i in df_status["status-start"]]
        },
        "status_end": {
            "options": [{"label": i, "value": i} for i in df_status["status-end"]]
        },
    },
)

add_item_button = html.Button("(+) Add Items to Database)", n_clicks=0, id="add-item-btn", style={"position": "relative", "left": 1670})

app.layout = html.Div([title, add_button, table, dcc.Store(id='previous-data'), add_item_button], style={"margin": 30})


@app.callback(
    Output("table", "data"),
    Input("add-btn", "n_clicks"),
    Input("table", "data"),
    prevent_initial_call=True,
)
def add_row(n_clicks, rows):
    df_order = pd.DataFrame(rows)

    # add a new line
    if ctx.triggered_id == "add-btn":
        df_order = pd.concat([df_order, df_new_order_line], ignore_index=True)

    return df_order.to_dict("records")


if __name__ == "__main__":
    app.run_server(debug=True)
