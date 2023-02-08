import PySimpleGUI as sg
import pandas as pd
import os

# 2/3/23 The purpose of this program is to keep track of all the software I purchase.
# 2/7/23 compiled program

# Create an app using py2app
# pip install py2app
# % py2applet --make-setup  purchased_software.py   (create a setup file needed for compliation)
# % python3 setup.py py2app -A  (create the app in test mode
# If errors, debug as per instructions in Python Coding Angela Yu.docx
# % python3 setup.py py2app  (create a portable .app)


# Create empty dataframe.  This is a one time event.  The data frame will be saved as a .pkl file.

# df = pd.DataFrame(columns=['software', 'where_purchased', 'vendor_name', 'date_purch', 'cost', 'free', 'one_time', 'annual', 'notes'])

# Populate the first row of the dataframe with test data, this is a one time event for testing and development
# data = {'software': 'Microsoft Office',
#         'where_purchased': 'Online',
#         'vendor_name': 'Microsoft Corporation',
#         'date_purch': '02/03/2023',
#         'cost': 149.99,
#         'free': False,
#         'one_time': True,
#         'annual': False,
#         'notes': 'Purchased for personal use'}
# df = pd.DataFrame([data], columns=['software', 'where_purchased', 'vendor_name', 'date_purch', 'cost', 'free', 'one_time', 'annual', 'notes'])
# record_no = df.iloc[0]  #  record-no is the entire row, all columns
# df.to_pickle('software.pkl')

software_file = '/Users/michaelpauken/PythonActiveProjects/PurchasedSoftware2/software.pkl'
df = pd.read_pickle(software_file)  # create dataframe of software products from pickle file


def search(search_arg):
    my_list1 = []
    my_list2 = []
    count_list_items = 0  # used to determine if there were any matches during search
    # Search all fields(Name, UserID, Password, Notes) for a specific set of characters
    for index, row in df.iterrows():
        if search_arg in row.software.lower() or search_arg in row.where_purchased.lower() or search_arg in row.date_purch \
                or search_arg in row.notes.lower() or search_arg in row.vendor_name.lower():
            count_list_items += 1

            # Write each account info to listbox
            software = row.software
            vendor_name = row.vendor_name

            my_list1.append(f" {'   '} {index} {' ' * 11} {software}\n")
            my_list2.append(f'{"   "}vendor_name')

    # ['software', 'where_purchased', 'vendor_name', 'date_purch', 'cost', 'free', 'one_time', 'annual', 'notes']
    if count_list_items > 0:
        window['-LBOX1-'].update(values=my_list1)
        window['-LBOX2-'].update(values=my_list2)
    else:
        sg.popup('No Record Found', any_key_closes=True, background_color='red', font=('Helvetica 16'),
                 location=(1000, 90))
    return


def list_changed(item):  # User method
    # df = 'software', 'where_purchased', 'vendor_name', 'date_purch', 'cost', 'free', 'one_time', 'annual', 'notes']
    software = df.at[item, 'software']
    where_purchased = df.at[item, 'where_purchased']
    vendor_name = df.at[item, 'vendor_name']
    date_purch = df.at[item, 'date_purch']
    cost = df.at[item, 'cost']
    free = df.at[item, 'free']
    one_time = df.at[item, 'one_time']
    annual = df.at[item, 'annual']
    notes = df.at[item, 'notes']

    # keys = '-SOFTWARE NAME-‘, '-WHERE-‘, '-VENDOR-‘, '-DATE-', '-COST-‘, '-FREE-‘, '-ONETIME-‘, '-ANNUAL-‘, '-NOTES-'
    window['-SOFTWARE NAME-'].update(software)
    window['-WHERE-'].update(where_purchased)
    window['-VENDOR-'].update(vendor_name)
    window['-DATE-'].update(date_purch)
    window['-COST-'].update(cost)

     # The only way you can select a radio button in PysimpleGUI is to us the word True or False to update.  If
     # you use a variable, even though the variable is type bool, the update will not work.
    if free == True:
        window['-FREE-'].update(True)
    if one_time == True:
        window['-ONETIME-'].update(True)
    if annual == True:
        window['-ANNUAL-'].update(True)

    window['-NOTES-'].update(notes)
    return


def add_record():
    global df
    software = window['-SOFTWARE NAME-'].get()
    where_purchased = window['-WHERE-'].get()
    vendor_name = window['-VENDOR-'].get()
    date_purch = window['-DATE-'].get()
    cost = window['-COST-'].get()
    free = window['-FREE-'].get()
    one_time = window['-ONETIME-'].get()
    annual = window['-ANNUAL-'].get()
    notes = window['-NOTES-'].get()

    answer = sg.popup_get_text(f'Do you want to add Software Product: {software}, Y or N: ', font=('Helvetica 16'),
                               location=(1000, 90))
    answer = answer.lower()

    if answer == 'y':
        # Add (append) new software product info to DataFrame
        # df = 'software', 'where_purchased', 'vendor_name', 'date_purch', 'cost', 'free', 'one_time', 'annual', 'notes']
        df2 = {'software': software, 'where_purchased': where_purchased, 'vendor_name': vendor_name,
               'date_purch': date_purch,
               'cost': cost, 'free': free, 'one_time': one_time, 'annual': annual, 'notes': notes}
        df = df.append(df2, ignore_index=True)  # will be droped from pandas July 2022

        # save dataframe
        df.to_pickle(software_file)
        sg.popup("DataFrame was saved to disk", font=('Helvetica 16'), location=(1000, 90))
        # Clear the input fields after record added to dataframe
        clear_input_Output_fields()  # callfunction to clear fields
    else:
        sg.popup("New record was not added", font=('Helvetica 16'), location=(1000, 90))
    return


def clear_input_Output_fields():
    # keys = '-SOFTWARE NAME-‘, '-WHERE-‘, '-VENDOR-‘, '-DATE-', '-COST-‘, '-FREE-‘, '-ONETIME-‘, '-ANNUAL-‘, '-NOTES-'
    window['-SOFTWARE NAME-'].update('')
    window['-WHERE-'].update('')
    window['-VENDOR-'].update('')
    window['-DATE-'].update('')
    window['-COST-'].update('')
    window['-FREE-'].update(False)
    window['-ONETIME-'].update(False)
    window['-ANNUAL-'].update(False)
    window['-NOTES-'].update('')
    window['-LBOX1-'].update('')
    window['-LBOX2-'].update('')
    window['-lineEdit_search-'].update('')
    return


def update():
    global df
    software = window['-SOFTWARE NAME-'].get()
    where_purchased = window['-WHERE-'].get()
    vendor_name = window['-VENDOR-'].get()
    date_purch = window['-DATE-'].get()
    cost = window['-COST-'].get()
    free = window['-FREE-'].get()
    one_time = window['-ONETIME-'].get()
    annual = window['-ANNUAL-'].get()
    notes = window['-NOTES-'].get()

    answer = sg.popup_get_text(f'Do you want to update Software Product: {software}, Y or N: ', font=('Helvetica 16'),
                               location=(1000, 90))
    answer = answer.lower()

    if answer == 'y':
        # Update software product info to DataFrame
        # df = 'software', 'where_purchased', 'vendor_name', 'date_purch', 'cost', 'free', 'one_time', 'annual', 'notes']
        df.loc[item, "software"] = software
        df.loc[item, "where_purchased"] = where_purchased
        df.loc[item, "vendor_name"] = vendor_name
        df.loc[item, "date_purch"] = date_purch
        df.loc[item, "cost"] = cost
        df.loc[item, "free"] = free
        df.loc[item, "one_time"] = one_time
        df.loc[item, "annual"] = annual
        df.loc[item, "notes"] = notes
        # save dataframe
        df.to_pickle(software_file)
        sg.popup("DataFrame was saved to disk", font=('Helvetica 16'), location=(1000, 90))
        # Clear the input fields after record added to dataframe
        clear_input_Output_fields()  # callfunction to clear fields
    else:
        sg.popup("New record was not added", font=('Helvetica 16'), location=(1000, 90))
    return

def delete():
    answer= sg.popup_get_text(f'Do you really want to delete record#: {item}, Y or N: ', font=('Helvetica 16'), location=(1000,90))
    if answer == 'y':
        df.drop(item, inplace=True)  # default for row is axis=0
        # save dataframe
        df.to_pickle(software_file)
        sg.popup(f"Record# {item} was deleted and dataframe was saved to disk", font=('Helvetica 16'),  background_color= 'yellow', text_color= 'black', location=(1000,90))
        clear_input_Output_fields()
    else:
        sg.popup(f"Record# {item} was not deleted", font=('Helvetica 16'), location=(1000, 90))
    return


empty_list = []  # integrity
sg.theme('light green')

# 2 - Layout
layout = [
    [sg.Text('Enter Search Argument'), sg.Input(key='-lineEdit_search-', size=(30, 1), expand_x=True),
     sg.Button('Search', bind_return_key=True)],
    [sg.T('RECORD#', size=(10, 1)), sg.T('SOFTWARE PACKAGE NAME', size=(40, 1)), sg.T('VENDOR NAME', size=(30, 1))],
    [sg.Listbox(empty_list, size=(50, 10), select_mode=sg.LISTBOX_SELECT_MODE_EXTENDED, no_scrollbar=False,
                horizontal_scroll=False, expand_x=True, expand_y=True, enable_events=True, k='-LBOX1-'),
     sg.Listbox(empty_list, size=(25, 10), select_mode=sg.LISTBOX_SELECT_MODE_EXTENDED, no_scrollbar=False,
                horizontal_scroll=False, expand_x=True, expand_y=True, enable_events=True, k='-LBOX2-')],
    [sg.Text('Software Package', size=(14)), sg.Push(), sg.Input(key='-SOFTWARE NAME-', size=(60), expand_x=True)],
    [sg.Text('Where Purchased', size=(14)), sg.Push(), sg.Input(key='-WHERE-', size=(60), expand_x=True)],
    [sg.Text('Vendor Name', size=(14)), sg.Push(), sg.Input(key='-VENDOR-', size=(60), expand_x=True)],
    [sg.Text('Date Purchased', size=(14)), sg.Push(), sg.Input(key='-DATE-', size=(60), expand_x=True)],
    [sg.Text('Cost of Software', size=(14)), sg.Push(), sg.Input(key='-COST-', size=(60), expand_x=True)],
    # [sg.Checkbox('Free', k='-FREE-'), sg.Checkbox('One Time Purchase', k='-ONETIME-'), sg.Checkbox('Annual Charge', k='-ANNUAL-')],

    [sg.Radio('Free', 'RADIO', key='-FREE-'),
     sg.Radio('One Time Purchase', 'RADIO', key='-ONETIME-'),
     sg.Radio('Annual Charge', 'RADIO', key='-ANNUAL-')],

    [sg.Text('Notes', size=(14)), sg.Push(),
     sg.Multiline(size=(60, 3), key='-NOTES-', disabled=False, autoscroll=True, horizontal_scroll=False, expand_x=True,
                  expand_y=True)],
    [sg.Button('Add'), sg.Button('Delete'), sg.Button('Update'), sg.Button('Clear Input Fields'), sg.Button('Exit')]
]

# 3 - Window
window = sg.Window('Purchased Software', layout, font='Default 18', finalize=True, resizable=True)
# window = sg.Window('Purchased Software', layout, keep_on_top=True, font='Default 18', finalize=True, resizable=True)

while True:
    # 4 - Event loop / handling
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break

    if event == 'Search':
        search_arg = window['-lineEdit_search-'].get().lower()
        my_list = search(search_arg)  # goto search function
    try:
        if event == '-LBOX1-' or event == '-LBOX2-':
            item = window['-LBOX1-'].get()

            item = item[0]
            item = int(item.split()[0])  # get the first character in the string and convert to integer

            list_changed(item)  # call function to populate the update fields
    except Exception as e:
        sg.popup('No Record Found', any_key_closes=True, background_color='red', font=('Helvetica 16'),
                 location=(1000, 90))
    if event == 'Add':
        add_record()

    if event == 'Update':
        update()

    if event == 'Clear Input Fields':
        clear_input_Output_fields()

    if event == 'Delete':
        delete()

window.close()














