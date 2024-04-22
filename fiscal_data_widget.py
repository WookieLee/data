# -*- coding: utf-8 -*-
import pandas as pd
import ipywidgets as widgets
from IPython.display import display, clear_output
import requests
from io import StringIO

def fiscal_data_widget():

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

    # Function to update variable dropdown options based on selected dataframe
    def update_variable_dropdown(change):
        selected_df = df_dropdown.value
        df = uploaded_dataframes[selected_df]
        variable_dropdown.options = df.columns.tolist()

    # Function to update year and department dropdown options based on selected dataframe
    def update_year_department_dropdowns(change=None):
        selected_df = df_dropdown.value
        df = uploaded_dataframes[selected_df]
        all_years = sorted(df['회계연도'].unique().tolist())
        all_departments = sorted(df['소관명'].unique().tolist())
        year_dropdown.options = all_years
        department_dropdown.options = all_departments

    # Function to update key dropdown options based on selected dataframe
    def update_key_dropdown(change=None):
        selected_df = df_dropdown.value
        df = uploaded_dataframes[selected_df]
        key_dropdown.options = df.columns.tolist()

    # Function to add selected variables to the list
    def add_variables(button):
        selected_df = df_dropdown.value
        selected_variables = variable_dropdown.value
        selected_variables_dict[selected_df] = selected_variables
        added_variables_messages.append(f"Variables added for {selected_df}: {selected_variables}")
        with output_widget:
            clear_output(wait=True)
            for message in added_variables_messages:
                print(message)

    # Function to import selected variables and create the output dataframe
    def import_data(button):
        global output_dataframe
        years = year_dropdown.value
        departments = department_dropdown.value
        selected_keys = key_dropdown.value

        selected_dataframes = []

        for df_name, df in uploaded_dataframes.items():
            if df_name in selected_variables_dict:
                selected_variables = selected_variables_dict[df_name]
                filtered_df = df[(df['회계연도'].isin(years)) & (df['소관명'].isin(departments))]
                selected_df = filtered_df[[*selected_keys, *selected_variables]]
                selected_df.columns = [*selected_keys, *selected_variables]
                selected_dataframes.append(selected_df)

        merged_df = selected_dataframes[0]
        for df in selected_dataframes[1:]:
            merged_df = pd.merge(merged_df, df, on=selected_keys, how='outer')

        output_dataframe = merged_df.reset_index(drop=True)
        with output_widget:
            clear_output(wait=True)
            display(output_dataframe)

    # Event handlers for buttons
    add_variable_button.on_click(add_variables)
    import_button.on_click(import_data)

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