from dash import Dash, dcc, html, dash_table, Input, Output, State, callback
from dash_iconify import DashIconify

import pandas as pd
import base64
import datetime
import io
import fitz  # PyMuPDF

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        className="upload-container",
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-data-upload'),
    html.Button('Upload File', id='submit-button', className='file-submit-button', n_clicks=0),
])

def parse_csv_excel_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            file_symbol = DashIconify(icon='fa6-solid:file-csv', width=50, height=50, className='file_icon')
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
            file_symbol = DashIconify(icon='vscode-icons:file-type-excel', width=50, height=50, className='file_icon')
        elif 'xlsx' in filename:
            # Assume that the user uploaded an xlsx file
            df = pd.read_excel(io.BytesIO(decoded))
            file_symbol = DashIconify(icon='vscode-icons:file-type-excel', width=50, height=50, className='file_icon')
        else:
            raise ValueError("Unsupported file type")
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        file_symbol,  # Show file type symbol
        html.H5(filename, className="file-name"),
        # html.H6(datetime.datetime.fromtimestamp(date)),
        # dash_table.DataTable(
        #     df.head(),  # Display the first 5 rows
        #     [{'name': i, 'id': i} for i in df.columns]
        # ),
    ])

def parse_pdf_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        doc = fitz.open(stream=decoded, filetype='pdf')
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    pdf_text = ''
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        pdf_text += page.get_text()

    return html.Div([
        DashIconify(icon='vscode-icons:file-type-pdf2', width=50, height=50, className='file_icon'),  # PDF icon
        html.H5(filename, className='file-name'),
        # html.H6(datetime.datetime.fromtimestamp(date)),
        # html.Div(pdf_text),  # Display the extracted text from the PDF
    ])

@app.callback(
    Output('output-data-upload', 'children'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State('upload-data', 'last_modified')
)
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_csv_excel_contents(c, n, d) if ('csv' in n or 'xls' in n or 'xlsx' in n) else
            parse_pdf_contents(c, n, d)
            for c, n, d in zip(list_of_contents, list_of_names, list_of_dates)
        ]
        return children

if __name__ == '__main__':
    app.run_server(debug=True)
