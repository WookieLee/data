# data_widget.py

import pandas as pd
import requests
import ipywidgets as widgets
from IPython.display import display, clear_output
from io import StringIO

def download_fiscal_data():
# Dictionary to store data names and corresponding numbers
    file_name_to_number = {
        '중앙관서별총지출추이': '166',
        '정부구매예산': '173',
        '세입/수입 결산 현황': '174',
        '소관별 세입/세출 결산 현황': '177',
        '회계별 세입 결산 현황': '178',
        '회계별 세출 결산 현황': '179',
        '소관별 주요관리대상사업 집행실적': '181',
        '월별 지출집행상황': '183',
        '월별 지출운용상황': '184',
        '일별 지출운용상황': '185',
        '총사업비현황': '186',
        '월별 수입징수상황': '187',
        '월별 수입운용상황': '188',
        '일별 수입운용상황': '189',
        '재정증권 발행 및 상환내역': '190',
        '소관별 재정상태표': '192',
        '채권현재액명세서': '195',
        '세출/지출 결산 현황': '802',
        '소관별 재정운영표': '915',
        '소관별 순자산변동표': '916',
        '세부사업 예산편성현황(총액)': '938',
        '세목 예산편성현황(총액)': '939',
        '세부사업 예산편성현황(총지출)': '940',
        '세목 예산편성현황(총지출)': '941',
        '세부사업 예산편성현황(외화)': '942',
        '세목 예산편성현황(외화)': '943',
        '세출 세부사업 예산편성현황(추경포함)': '944',
        '세출 세목 예산편성현황(추경포함)': '945',
        '예산편성현황(총액)': '946',
        '예산편성현황(총수입)': '947',
        '예산편성현황(외화)': '948',
        '세입 예산편성현황(추경포함)': '949'
    }

    # Base URL for fetching CSV files
    base_url = "https://raw.githubusercontent.com/WookieLee/data/fiscal_data/df_{}.csv"

    # Iterate over the file_name_to_number dictionary
    for data_name, number in file_name_to_number.items():
        url = base_url.format(number)  # Construct the URL for the CSV file
        response = requests.get(url)    # Fetch the CSV file content

        if response.status_code == 200:
            # Read the CSV content into a pandas DataFrame
            df = pd.read_csv(url)

            # Create a variable name dynamically using exec() and assign the DataFrame
            var_name = f"dataframe_{number}"  # Variable name like 'dataframe_166', 'dataframe_173', etc.
            exec(f"{var_name} = df")           # Assign df to the dynamically created variable
            print(f'{data_name} (dataframe_{number}) has been downloaded.')
        else:
            print(f"Failed to fetch data for {data_name} from URL: {url}")
    print('Download complete.')

def fiscal_data_widget():
    # Define the dictionary mapping data names to corresponding numbers
    file_name_to_number = {
        '중앙관서별총지출추이': '166',
        '정부구매예산': '173',
        '세입/수입 결산 현황': '174',
        # Add other key-value pairs here
    }

    # Dropdown for selecting dataframes
    df_dropdown = widgets.Dropdown(description='Dataframe:')

    # Dropdown for selecting years (allowing multiple selection)
    year_dropdown = widgets.SelectMultiple(description='Years:')

    # Dropdown for selecting departments (allowing multiple selection)
    department_dropdown = widgets.SelectMultiple(description='Departments:')

    # Dropdown for selecting specific variables
    variable_dropdown = widgets.SelectMultiple(description='Variables:')

    # Dropdown for selecting keys
    key_dropdown = widgets.SelectMultiple(description='Keys:')

    # Buttons for adding variables and importing data
    add_variable_button = widgets.Button(description='Add variables')
    import_button = widgets.Button(description='Import data')

    # Output widget for displaying the result
    output_widget = widgets.Output()

    # Dictionary to store selected variables from each dataframe
    selected_variables_dict = {}

    # List to store added variables messages
    added_variables_messages = []

    # Predefined list of dataframe names
    dataframe_names = list(file_name_to_number.keys())

    # Function to update dataframe dropdown options based on predefined list of dataframe names
    def update_dataframe_dropdown(change):
        options = {f'{idx + 1} - {df_name}': df_name for idx, df_name in enumerate(dataframe_names)}
        df_dropdown.options = options
        if df_dropdown.value:
            update_variable_dropdown(None)
            update_year_department_dropdowns()
            update_key_dropdown()

    # Rest of the existing code for the widget function...

    # Connect update functions to observe changes in dropdown values
    df_dropdown.observe(update_variable_dropdown, names='value')
    df_dropdown.observe(update_year_department_dropdowns, names='value')
    df_dropdown.observe(update_key_dropdown, names='value')

    # Display widgets
    display(df_dropdown)
    display(year_dropdown)
    display(department_dropdown)
    display(key_dropdown)
    display(variable_dropdown)
    display(add_variable_button)
    display(import_button)
    display(output_widget)

    # Dictionary to store dataframes
    uploaded_dataframes = {}

    for data_name, number in file_name_to_number.items():
        dataframe_name = 'dataframe_' + number
        if dataframe_name in globals():  # Check if the dataframe variable exists
            uploaded_dataframes[data_name] = globals()[dataframe_name]

    # Update dropdown options
    update_dataframe_dropdown(None)
