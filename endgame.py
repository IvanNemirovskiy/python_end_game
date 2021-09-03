import argparse, sys
import sqlite3
import time
import re

import requests
import logging
import uuid
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import *
import yaml
import json
from requests.auth import HTTPBasicAuth
import tkmacosx

from history import add_history, history, show_index_from_history, clear_history

#logger = logging.getLogger("ENDGAME")

# def log_endgame(message, level = logging.INFO):
#     log_level = logging.DEBUG
#     if args.log:
#         if args.log == "info":
#             log_level = logging.INFO
#         elif args.log == "warning":
#             log_level = logging.WARNING
#         elif args.log == "debug":
#             log_level = logging.DEBUG
#
#
#     logger = logging.getLogger("ENDGAME")
#     logger.setLevel(log_level)
#     logFormatter = logging.Formatter("CLI %(levelname)s - %(asctime)s : %(message)s")
#
#     fileHandler = logging.FileHandler("end-game.log")
#     fileHandler.setFormatter(logFormatter)
#     fileHandler.setLevel(log_level)
#     logger.addHandler(fileHandler)
#
#     consoleHandler = logging.StreamHandler()
#     consoleHandler.setFormatter(logFormatter)
#     consoleHandler.setLevel(log_level)
#     logger.addHandler(consoleHandler)
#
#     if level is logging.DEBUG:
#         logger.debug(message)
#     elif level is logging.INFO:
#         logger.info(message)
#     elif level is logging.WARNING:
#         logger.warning(message)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--method', choices=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'], help='Set request method')
    parser.add_argument('--history', choices=['show', 'clear'], help='Show or delete history')
    parser.add_argument('--endpoint', type=str, help='Set endpoint URL')
    parser.add_argument('--auth', metavar=('username', 'password'), nargs='*', help='Set AUTH')
    parser.add_argument('--params', type=str, nargs='+', help='Set request parameters')
    parser.add_argument('--body', type=str, help='Set request body')
    parser.add_argument('--headers', type=str, nargs='+', help='Set request headers')
    parser.add_argument('--yaml', action='store_true', help='Set YAML output view')
    parser.add_argument('--json', action='store_true', help='Set JSON output view')
    parser.add_argument('--gui', action='store_true',help='Set GUI mode')
    parser.add_argument('--log', choices=['debug', 'info', 'warning'], help='Set logging level')

    if len(sys.argv) == 1:
        parser.print_usage()
        exit()

    args, unknown = parser.parse_known_args()
    return args


def get_params():
    if args.params:
        PARAMS = dict()
        for param in args.params:
            PARAMS.update({param.split('=')[0]: param.split('=')[1]})
        return PARAMS
    else:
        return None


def get_headers():
    if args.headers:
        HEADERS = dict()
        for header in args.headers:
            HEADERS.update({header.split('=')[0]: header.split('=')[1]})
        return HEADERS
    else:
        return None


def get_auth():
    if args.auth:
        return HTTPBasicAuth(args.auth[0], args.auth[1])
    else:
        return None


def perform_request():  # Decide what request to do and make it

    # GET method
    if args.method == 'GET':
        logging.info(f"Perform request")
        logging.debug(f"Request params [{args.method}]")
        request = requests.get(args.endpoint, params=get_params(), auth=get_auth())
        logging.info(f"Got response {request.status_code} {ok if request.ok is True else request.status_code} in {str(round(request.elapsed.total_seconds(), 2))} seconds")


    # POST method
    if args.method == 'POST':
        logging.info(f"Perform request")
        logging.debug(f"Request params [{args.method}]")
        request = requests.post(args.endpoint, params=get_params(), auth=get_auth(), data=args.body, headers=get_headers())
        logging.info(f"Got response {request.status_code} {ok if request.ok is True else request.status_code} in {str(round(request.elapsed.total_seconds(), 2))} seconds")


    # PUT method
    if args.method == 'PUT':
        logging.info(f"Perform request")
        logging.debug(f"Request params [{args.method}]")
        request = requests.put(args.endpoint, params=get_params(), auth=get_auth(), data=args.body, headers=get_headers())
        logging.info(f"Got response {request.status_code} {ok if request.ok is True else request.status_code} in {str(round(request.elapsed.total_seconds(), 2))} seconds")


    # PATCH method
    if args.method == 'PATCH':
        logging.info(f"Perform request")
        logging.debug(f"Request params [{args.method}]")
        request = requests.patch(args.endpoint, params=get_params(), auth=get_auth(), data=args.body, headers=get_headers())
        logging.info(f"Got response {request.status_code} {ok if request.ok is True else request.status_code} in {str(round(request.elapsed.total_seconds(), 2))} seconds")


    # DELETE method
    if args.method == 'DELETE':
        logging.info(f"Perform request")
        logging.debug(f"Request params [{args.method}]")
        logging.info(f"Got response {request.status_code} {ok if request.ok is True else request.status_code} in {str(round(request.elapsed.total_seconds(), 2))} seconds")

    logging.debug(f"Method {args.method} got response {request.status_code} {ok if request.ok is True else 'Not Found'} in {round(request.elapsed.total_seconds(), 2)} seconds from {args.endpoint}")
    print_result(request)


def print_result(request):  # print results to JSON,YAML or text
    request_result = {}

    request_result['Params'] = get_params()
    request_result['Method'] = args.method
    request_result['URL'] = args.endpoint
    request_result['Auth'] = args.auth
    request_result['Status'] = request.status_code
    try:
        request_result['Response'] = request.json()
    except:
        request_result['Response'] = "Can not parse response"
    request_result['Body'] = args.body
    request_result['Headers'] = get_headers()

    logging.debug("Adding record to the history")
    auth = str(request_result['Auth'])
    request_result['Auth'] = auth
    add_history(request_result)
    logging.debug("Printing results")

    try:
        print("---Got response " + str(request.status_code) + " " + f"{ok if request.ok is True else request.status_code}" + " " + f"{str(round(request.elapsed.total_seconds(), 2))}" + " seconds---")
        print('---Response body---')
        if args.json:
            print(json.dumps(request.json(), indent=2))
        elif args.yaml:
            yaml_response = yaml.safe_dump(request.json())
            print(yaml_response)
        else:
            json_data = json.dumps(request.json())
            dic_data = json.loads(json_data)
            print(dic_data)
    except:
        print("Can not parse request results")


def focus_out_entry_box(widget, widget_text):
    if widget['fg'] == 'Black' and len(widget.get()) == 0:
        widget.delete(0, END)
        widget['fg'] = 'Grey'
        widget.insert(0, widget_text)
    if widget['fg'] == 'aquamarine' and len(widget.get()) == 0:
        widget.delete(0, END)
        widget['fg'] = 'grey'
        widget.insert(0, widget_text)


def focus_in_entry_box(widget):
    if widget['fg'] == 'Grey':
        widget['fg'] = 'Black'
        widget.delete(0, END)
    if widget['fg'] == 'grey':
        widget['fg'] = 'aquamarine'
        widget.delete(0, END)


def main_gui():
    options_requests = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    pattern = r"^^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$"
    root = Tk()
    root.title("PATCHMAN")
    root.geometry("915x530")
    root.config()
    intro_label = Label(root, text='API client program')
    intro_label.pack(side=TOP, anchor=NW)

    # frame for buttons
    global_frame = Frame(root)
    global_frame.place(x=0, y=55)

    # Create two frames in the window
    main_frame_request = LabelFrame(global_frame, text='')
    main_frame_request.pack()
    main_frame_history = Frame(global_frame)

    # Define functions for switching the frames
    def change_to_request():
        root.geometry("915x530")
        main_frame_request.pack(fill='both', expand=1)
        main_frame_history.pack_forget()

    def change_to_history():
        root.geometry("605x310")
        main_frame_history.pack(fill='both', expand=1)
        main_frame_request.pack_forget()

    # Add a button to switch between two frames
    switch_to_request_menu = Button(root, text="Send Request", command=change_to_request)
    switch_to_request_menu.pack(side=LEFT, anchor="nw")

    switch_to_history_menu = Button(root, text="Request History", command=change_to_history)
    switch_to_history_menu.pack(side=LEFT, anchor="nw")

    # request frame
    request_frame = LabelFrame(main_frame_request, text='Shape your request', labelanchor='n')
    request_frame.pack(expand='yes', fill='both', side='left')

    choose_method = StringVar()
    choose_method.set(options_requests[0])
    drop_methods = OptionMenu(request_frame, choose_method, *options_requests)
    drop_methods.grid(row=0, column=0)

    url_entry = tk.Entry(request_frame, width=30, fg='grey', bg='black')
    url_entry.insert(0, 'URL')
    url_entry.grid(row=0, column=1)
    url_entry.bind("<FocusIn>", lambda args: focus_in_entry_box(url_entry))
    url_entry.bind("<FocusOut>", lambda args: focus_out_entry_box(url_entry, 'URL'))

    # Basic Authentication Frame
    auth_frame = LabelFrame(request_frame, text="Basic Authentication", labelanchor='n')
    auth_frame.grid(row=1, column=0, sticky="nsew", columnspan=2)

    # username placeholder entry
    username_entry = Entry(auth_frame, fg='Grey')
    username_entry.insert(0, 'username')
    username_entry.grid(row=2, column=0)
    username_entry.bind("<FocusIn>", lambda args: focus_in_entry_box(username_entry))
    username_entry.bind("<FocusOut>", lambda args: focus_out_entry_box(username_entry, 'username'))

    # user password placeholder entry
    password_entry = Entry(auth_frame, fg='Grey')
    password_entry.insert(0, 'password')
    password_entry.grid(row=2, column=1)
    password_entry.bind("<FocusIn>", lambda args: focus_in_entry_box(password_entry))
    password_entry.bind("<FocusOut>", lambda args: focus_out_entry_box(password_entry, 'password'))

    # Label and Frame for output
    output_frame = LabelFrame(main_frame_request, text='')
    output_frame.pack(side=TOP)
    titleframe = Frame(output_frame)
    titleframe.pack(side=TOP)
    output_label = Label(output_frame, text='')
    # output_label.pack()

    def remove_text():
        if response_view.get() == 'text' or response_view.get() =='yaml' or response_view.get() =='json':
            output_label.configure(text='')

    # Frame, Entries and Button for Params
    # Frame
    params_frame = LabelFrame(request_frame, text='+ params', labelanchor='n')
    params_frame.grid(row=2, column=0, columnspan=3)

    # Entries
    keyword_entry1 = Entry(params_frame)
    keyword_entry1.grid(row=0, column=0)

    value_entry1 = Entry(params_frame)

    value_entry1.grid(row=0, column=1)

    keyword_entry2 = Entry(params_frame)
    keyword_entry2.grid(row=1, column=0)

    value_entry2 = Entry(params_frame)
    value_entry2.grid(row=1, column=1)

    keyword_entry3 = Entry(params_frame)
    keyword_entry3.grid(row=2, column=0)

    value_entry3 = Entry(params_frame)
    value_entry3.grid(row=2, column=1)

    keyword_entry4 = Entry(params_frame)
    keyword_entry4.grid(row=3, column=0)

    value_entry4 = Entry(params_frame)
    value_entry4.grid(row=3, column=1)

    keyword_entry5 = Entry(params_frame)
    keyword_entry5.grid(row=4, column=0)

    value_entry5 = Entry(params_frame)
    value_entry5.grid(row=4, column=1)

    def take_params():
        PARAMS = {keyword_entry1.get(): value_entry1.get(), keyword_entry2.get(): value_entry2.get(),
                  keyword_entry3.get(): value_entry3.get(),
                  keyword_entry4.get(): value_entry4.get(), keyword_entry5.get(): keyword_entry5.get()}
        return PARAMS

    def take_headers():
        HEADERS = {keyheader_entry.get(): valueheader_entry.get()}
        return HEADERS

    def take_body():
        BODY = {keybody_entry.get(): valuebody_entry.get()}
        return BODY

    # Set params Button
    set_params_button = tkmacosx.Button(params_frame, text='+', fg="aquamarine", background='black', command=take_params)
    set_params_button.grid(row=4, column=2)

    # Body frame, entries and button
    # Body param Frame
    body_request_frame = LabelFrame(request_frame, text='+ body', labelanchor='n')
    body_request_frame.grid(row=3, column=0, columnspan=3)

    # Entries for body param
    keybody_entry = Entry(body_request_frame, fg='Grey')
    keybody_entry.insert(0, 'key')
    keybody_entry.grid(row=0, column=0)
    keybody_entry.bind("<FocusIn>", lambda args: focus_in_entry_box(keybody_entry))
    keybody_entry.bind("<FocusOut>", lambda args: focus_out_entry_box(keybody_entry, 'key'))

    valuebody_entry = Entry(body_request_frame, fg='Grey')
    valuebody_entry.insert(0, 'value')
    valuebody_entry.grid(row=0, column=1)
    valuebody_entry.bind("<FocusIn>", lambda args: focus_in_entry_box(valuebody_entry))
    valuebody_entry.bind("<FocusOut>", lambda args: focus_out_entry_box(valuebody_entry, 'value'))

    # Button set body param
    set_body_button = tkmacosx.Button(body_request_frame, text="+", fg='aquamarine', bg='black', command=take_body)
    set_body_button.grid(row=0, column=2)

    # Headers frame, entries and button
    # Frame for headers
    headers_frame = LabelFrame(request_frame, text='+ headers', labelanchor='n')
    headers_frame.grid(row=4, column=0, columnspan=3)

    # Entries for headers
    keyheader_entry = Entry(headers_frame, fg='Grey')
    keyheader_entry.insert(0, 'key')
    keyheader_entry.grid(row=0, column=0)
    keyheader_entry.bind("<FocusIn>", lambda args: focus_in_entry_box(keyheader_entry))
    keyheader_entry.bind("<FocusOut>", lambda args: focus_out_entry_box(keyheader_entry, 'key'))

    valueheader_entry = Entry(headers_frame, fg='Grey')
    valueheader_entry.insert(0, 'value')
    valueheader_entry.grid(row=0, column=1)
    valueheader_entry.bind("<FocusIn>", lambda args: focus_in_entry_box(valueheader_entry))
    valueheader_entry.bind("<FocusOut>", lambda args: focus_out_entry_box(valueheader_entry, 'value'))

    # Button set headers
    set_header_button = tkmacosx.Button(headers_frame, text="+", fg='aquamarine', bg='black', command=take_headers)
    set_header_button.grid(row=0, column=2)

    # log level frame, label and radiobutton
    # log level frame
    log_level_frame = Frame(request_frame)
    log_level_frame.grid(row=5, column=0, columnspan=2)

    # log level label
    log_level_label = Label(log_level_frame, text='Log Level')
    log_level_label.grid(row=0, column=0)

    # variable to get radiobutton value
    log_level = StringVar()



    # log level radiobutton
    level_debug_radiobutton = tkmacosx.Radiobutton(log_level_frame, text='DEBUG', variable=log_level, value='DEBUG',
                                                   background='black', selectcolor='dark green',
                                                   foreground='aquamarine', indicatoron=0, padx=15)
    level_debug_radiobutton.grid(row=0, column=1)

    level_info_radiobutton = tkmacosx.Radiobutton(log_level_frame, text='INFO', variable=log_level, value='INFO',
                                                  background='black', selectcolor='dark green', foreground='aquamarine', indicatoron=0, padx=15)
    level_info_radiobutton.select()
    level_info_radiobutton.grid(row=0, column=2)

    level_warning_radiobutton = tkmacosx.Radiobutton(log_level_frame, text='WARNING', variable=log_level,
                                                     value='WARNING', background='black', selectcolor='dark green',
                                                     foreground='aquamarine', indicatoron=0, padx=15)
    level_warning_radiobutton.grid(row=0, column=3)

    # Response view
    response_view = StringVar(root, 'treeview')
    response_type_frame = Frame(request_frame)
    response_type_frame.grid(row=6, column=0, columnspan=10, pady=8)

    response_label = Label(response_type_frame, text='Response view')
    response_label.grid(row=0, column=0)

    response_treeview_radiobutton = tkmacosx.Radiobutton(response_type_frame, text='Treeview', variable=response_view,
                                                     value='treeview',background='black', selectcolor='dark green',
                                                     foreground='aquamarine', indicatoron=0)
    response_treeview_radiobutton.grid(row=0, column=1)

    response_json_radiobutton = tkmacosx.Radiobutton(response_type_frame, text='Pretty JSON', variable=response_view,
                                                         value='json', background='black', selectcolor='dark green',
                                                         foreground='aquamarine', indicatoron=0)
    response_json_radiobutton.grid(row=0, column=2)

    response_yaml_radiobutton = tkmacosx.Radiobutton(response_type_frame, text='YAML', variable=response_view,
                                                         value='yaml', background='black', selectcolor='dark green',
                                                         foreground='aquamarine', indicatoron=0)
    response_yaml_radiobutton.grid(row=0, column=3)

    response_table_radiobutton = tkmacosx.Radiobutton(response_type_frame, text='Table', variable=response_view,
                                                     value='table', background='black', selectcolor='dark green',
                                                     foreground='aquamarine', indicatoron=0)
    response_table_radiobutton.grid(row=0, column=4)

    response_raw_radiobutton = tkmacosx.Radiobutton(response_type_frame, text='Raw', variable=response_view,
                                                      value='text', background='black', selectcolor='dark green',
                                                      foreground='aquamarine', indicatoron=0)
    response_raw_radiobutton.grid(row=0, column=5)



    # Bottom response
    bottom_output = Label(request_frame, text="RESPONSE DATA", bg='black', fg='aquamarine')
    bottom_output.place(x=175, y=430)

    def show_tree(tree, bId, dictionary, type):
        tree["column"] = ()
        i = 0
        for data in dictionary:
            key = dictionary[data]
            if isinstance(key, list):
                string = f'{data}' + ": [" + f'{len(key)}' + "]"
                newId = tree.insert(bId, i, text=string)
                show_tree(tree, newId, key, 1)
            elif isinstance(key, dict):
                if type == 1:
                    string = f'{i}' + ": {" + f'{len(key)}' + "}"
                elif type == 2:
                    string = f'{data}' + ": {" + f'{len(key)}' + "}"
                newId = tree.insert(bId, i, text=string)
                show_tree(tree, newId, key, 2)
            else:
                if type == 1:
                    if isinstance(key, str):
                        string = f'{i}: "{key}"'
                    else:
                        string = f'{i}: {key}'
                elif type == 2:
                    if isinstance(key, str):
                        string = f'{data}: "{key}"'
                    else:
                        string = f'{data}: {key}'
                tree.insert(bId, i, text=string)
            i = i + 1


    s = ttk.Style()
    s.theme_use('clam')
    s.configure('Treeview.Heading', background="Black", foreground='aquamarine')
    tree = ttk.Treeview(output_frame, height=22)
    tree.column('#0', width=400)
    tree.pack(fill=BOTH, expand=True)

    # clear_output_btn = tkmacosx.Button(output_frame, text='Clear', command=remove_text, bg='aquamarine', width=50)
    # clear_output_btn.place(x=353, y=3)

    def make_tree(data):
        tree.delete(*tree.get_children())
        tree.column('#0', width=400)
        tree.heading("#0", text="")
        string = "{" + f'{len(data)}' + "}"
        bId = tree.insert('', 0, text=string)
        show_tree(tree, bId, data, 2)

    def show_table(table, dictionary: dict):
        tree.delete(*tree.get_children())
        table.column('#0', width=0, stretch=NO)
        table['columns'] = ("id", "value")
        table.column('id', width=200, stretch=YES)
        table.column("value", width=200, stretch=YES)
        table.heading("value", text="value", anchor=CENTER)
        table.heading("id", text="", anchor=CENTER)
        i = 0
        for data in dictionary:
            table.insert(parent='', index=i, iid=i, text='', values=(data, dictionary.get(data)))
            i = i + 1

    def show_json(tree, data):
        tree.delete(*tree.get_children())
        tree['columns'] = ()
        tree.column("#0", width=400, stretch=YES)

        i =0
        for p_data in data:
            string = p_data
            string += " : "
            if isinstance(data[p_data], dict):
                string += "{}"
            elif isinstance(data[p_data], list):
                string += "[]"
            else:
                string += str(data[p_data])
            tree.insert('', i, text=string)
            i = i + 1

    def show_yaml(tree, data):
        tree.delete(*tree.get_children())
        tree['columns'] = ()
        tree.column('#0', width=400, stretch=YES)
        yaml_res = yaml.safe_dump(data)
        tree.insert('', 0, text=str(yaml_res))

    def show_raw(tree, data):
        tree.delete(*tree.get_children())
        tree['columns'] = ()
        tree.column("#0", width=400, stretch=YES)
        l_data = json.loads(data)
        tree.insert('', 0, text=l_data)

    conn = sqlite3.connect('history.sqlite')
    cursor = conn.cursor()

    def url_request():

        cursor.execute(f'''
                        CREATE TABLE IF NOT EXISTS history(
                            requests TEXT NOT NULL,
                            methods TEXT NOT NULL 
                        )
                    ''')


        # GET — getting data from API
        # POST — method is used when you want to send some data to the server
        # PUT — method is used to send data to the API to update or create a resource
        # PATCH - method is used to partially send data to the API to update or create a resource
        # DELETE — method is used to delete data from API

        logging_format = 'GUI %(levelname)s : %(asctime)s - %(message)s'
        if log_level.get() == 'INFO':
            logging.basicConfig(filename='end-game.log', level=logging.INFO, format=logging_format)
        if log_level.get() == 'DEBUG':
            logging.basicConfig(filename='end-game.log', level=logging.DEBUG, format=logging_format)
        else:
            logging.basicConfig(filename='end-game.log', level=logging.WARNING, format=logging_format)

        username = username_entry.get()
        password = password_entry.get()
        current_method = choose_method.get()
        url_response = url_entry.get()
        ok = 'OK'
        if not re.match(pattern, url_response):
            messagebox.showerror('Invalid url', message="Please enter valid url \n for example: \n http://httpbin.org/get")

        if str(current_method) == "GET":
            if username == 'username' and password == 'password':

                messagebox.showwarning(title='Error', message='enter your username and password')
                logging.error('not authorized user')
            elif response_view.get() == 'text':
                request_data = requests.get(url_response, auth=HTTPBasicAuth(username, password))
                output_label.configure(text=show_raw(tree, request_data.text))
                bottom_output.config(text="Got response " + str(
                    request_data.status_code) + " " + f"{ok if request_data.ok is True else 'Not found'} " + f"{str(round(request_data.elapsed.total_seconds(), 2))}" + " seconds")
                logging.info('get method called (raw response)')
                cursor.execute(f'''INSERT INTO history (requests, methods) VALUES(?,?)''',
                               (url_response, current_method))
            elif response_view.get() == 'json':
                request_data = requests.get(url_response, auth=HTTPBasicAuth(username, password))
                output_label.configure(text=show_json(tree, request_data.json()))
                logging.info('get method called (json response)')
                cursor.execute(f'''INSERT INTO history (requests, methods) VALUES(?,?)''',
                               (url_response, current_method))
            elif response_view.get() == 'table':
                request_data = requests.get(url_response, auth=HTTPBasicAuth(username, password))
                output_label.configure(text=show_table(tree, request_data.json()))
                bottom_output.config(text="Got response " + str(
                    request_data.status_code) + " " + f"{ok if request_data.ok is True else 'Not found'} " + f"{str(round(request_data.elapsed.total_seconds(), 2))}" + " seconds")
                logging.info('get method called (table response)')
                cursor.execute(f'''INSERT INTO history (requests, methods) VALUES(?,?)''',
                               (url_response, current_method))
            elif response_view.get() == 'yaml':
                request_data_yaml = requests.get(url_response, auth=HTTPBasicAuth(username, password))
                output_label.configure(text=show_yaml(tree, request_data_yaml.json()))
                bottom_output.config(text="Got response " + str(
                    request_data_yaml.status_code) + " " + f"{ok if request_data_yaml.ok is True else 'Not found'} "+ f"{str(round(request_data_yaml.elapsed.total_seconds(), 2))}" + " seconds")
                logging.info('get method called (yaml response)')
                cursor.execute(f'''INSERT INTO history (requests, methods) VALUES(?,?)''',
                               (url_response, current_method))
            elif response_view.get() == 'treeview':
                request_data = requests.get(url_response, auth=HTTPBasicAuth(username, password))
                output_label.configure(text=make_tree(request_data.json()))
                bottom_output.config(text="Got response " + str(
                    request_data.status_code) + " " + f"{ok if request_data.ok is True else 'Not found'} "+ f"{str(round(request_data.elapsed.total_seconds(), 2))}" + " seconds")
                logging.info('get method called (treeview response)')
                cursor.execute(f'''INSERT INTO history (requests, methods) VALUES(?,?)''',
                               (url_response, current_method))

        if str(current_method) == "POST":
            PARAMS = take_params()
            HEADERS = take_headers()
            BODY_params = take_body()
            if username == 'username' and password == 'password':
                messagebox.showwarning(title='Error', message='enter your username and password')
                logging.error('not authorized user')
            if response_view.get() == 'text':
                text_response = requests.post(url_response, params=PARAMS, headers=HEADERS, data=BODY_params, auth=HTTPBasicAuth(username, password))
                output_label.configure(text=show_raw(tree, text_response.json()))
                bottom_output.config(text="Got response " + str(
                    text_response.status_code) + " " + f"{ok if text_response.ok is True else 'Not found'} " + f"{str(round(text_response.elapsed.total_seconds(), 2))}" + " seconds")
            elif response_view.get() == 'json':
                post_response = requests.post(url_response, params=PARAMS, headers=HEADERS, data=BODY_params , auth=HTTPBasicAuth(username, password))
                output_label.configure(text=show_json(tree, post_response.json()))
                bottom_output.config(text="Got response " + str(
                    post_response.status_code) + " " + f"{ok if post_response.ok is True else 'Not found'} " + f"{str(round(post_response.elapsed.total_seconds(), 2))}" + " seconds")
                logging.info('get method called (json response)')
            elif response_view.get() == 'yaml':
                yaml_response = requests.post(url_response, params=PARAMS, headers=HEADERS, data=BODY_params, auth=HTTPBasicAuth(username, password))
                output_label.configure(text=show_yaml(tree, yaml_response.json()))
                bottom_output.config(text="Got response " + str(
                    yaml_response.status_code) + " " + f"{ok if yaml_response.ok is True else 'Not found'} " + f"{str(round(yaml_response.elapsed.total_seconds(), 2))}" + " seconds")
            elif response_view.get() == 'table':
                table_response = requests.post(url_response, params=PARAMS, headers=HEADERS, data=BODY_params, auth=HTTPBasicAuth(username, password))
                output_label.configure(text=show_table(tree, table_response.json()))
                bottom_output.config(text="Got response " + str(
                    table_response.status_code) + " " + f"{ok if table_response.ok is True else 'Not found'} "+ f"{str(round(table_response.elapsed.total_seconds(), 2))}" + " seconds")
            elif response_view.get() == 'treeview':
                treeview_response = requests.post(url_response, params=PARAMS, headers=HEADERS, data=BODY_params, auth=HTTPBasicAuth(username, password))
                output_label.configure(text=make_tree(treeview_response.json()))
                bottom_output.config(text="Got response " + str(
                    treeview_response.status_code) + " " + f"{ok if treeview_response.ok is True else 'Not found'} " + f"{str(round(treeview_response.elapsed.total_seconds(), 2))}" + " seconds")

        if str(current_method) == 'PUT':
            PARAMS = take_params()
            HEADERS = take_headers()
            BODY_params = take_body()
            if username == 'username' and password == 'password':
                messagebox.showwarning(title='Error', message='enter your username and password')
                logging.error('not authorized user')
            if response_view.get() == 'text':
                text_response = requests.put(url_response, params=PARAMS, headers=HEADERS, data=BODY_params, auth=HTTPBasicAuth(username, password))
                output_label.configure(text=show_raw(tree, text_response.json()))
                bottom_output.config(text="Got response " + str(
                    text_response.status_code) + " " + f"{ok if text_response.ok is True else 'Not found'} " + f"{str(round(text_response.elapsed.total_seconds(), 2))}" + " seconds")
            elif response_view.get() == 'json':
                post_response = requests.put(url_response, params=PARAMS, headers=HEADERS, data=BODY_params, auth=HTTPBasicAuth(username, password))
                output_label.configure(text=show_json(tree, post_response.json()))
                bottom_output.config(text="Got response " + str(
                    post_response.status_code) + " " + f"{ok if post_response.ok is True else 'Not found'} " + f"{str(round(post_response.elapsed.total_seconds(), 2))}" + " seconds")
                logging.info('get method called (json response)')
            elif response_view.get() == 'yaml':
                yaml_response = requests.put(url_response, params=PARAMS, headers=HEADERS, data=BODY_params, auth=HTTPBasicAuth(username, password))
                output_label.configure(text=show_yaml(tree, yaml_response.json()))
                bottom_output.config(text="Got response " + str(
                    yaml_response.status_code) + " " + f"{ok if yaml_response.ok is True else 'Not found'} " + f"{str(round(yaml_response.elapsed.total_seconds(), 2))}" + " seconds")
            elif response_view.get() == 'table':
                table_response = requests.put(url_response, params=PARAMS, headers=HEADERS, data=BODY_params, auth=HTTPBasicAuth(username, password))
                output_label.configure(text=show_table(tree, table_response.json()))
                bottom_output.config(text="Got response " + str(
                    table_response.status_code) + " " + f"{ok if table_response.ok is True else 'Not found'} " + f"{str(round(table_response.elapsed.total_seconds(), 2))}" + " seconds")
            elif response_view.get() == 'treeview':
                treeview_response = requests.put(url_response, params=PARAMS, headers=HEADERS, data=BODY_params, auth=HTTPBasicAuth(username, password))
                output_label.configure(text=make_tree(treeview_response.json()))
                bottom_output.config(text="Got response " + str(
                    treeview_response.status_code) + " " + f"{ok if treeview_response.ok is True else 'Not found'} " + f"{str(round(treeview_response.elapsed.total_seconds(), 2))}" + " seconds")

        if str(current_method) == 'PATCH':
            PARAMS = take_params()
            HEADERS = take_headers()
            BODY_params = take_body()
            if username == 'username' and password == 'password':
                messagebox.showwarning(title='Error', message='enter your username and password')
                logging.error('not authorized user')
            if response_view.get() == 'text':
                text_response = requests.patch(url_response, params=PARAMS, headers=HEADERS, data=BODY_params, auth=HTTPBasicAuth(username, password))
                output_label.configure(text=show_raw(tree, text_response.json()))
                bottom_output.config(text="Got response " + str(
                    text_response.status_code) + " " + f"{ok if text_response.ok is True else 'Not found'} " + f"{str(round(text_response.elapsed.total_seconds(), 2))}" + " seconds")
            elif response_view.get() == 'json':
                post_response = requests.patch(url_response, params=PARAMS, headers=HEADERS, data=BODY_params, auth=HTTPBasicAuth(username, password))
                output_label.configure(text=show_json(tree, post_response.json()))
                bottom_output.config(text="Got response " + str(
                    post_response.status_code) + " " + f"{ok if post_response.ok is True else 'Not found'} " + f"{str(round(post_response.elapsed.total_seconds(), 2))}" + " seconds")
                logging.info('get method called (json response)')
            elif response_view.get() == 'yaml':
                yaml_response = requests.patch(url_response, params=PARAMS, headers=HEADERS, data=BODY_params, auth=HTTPBasicAuth(username, password))
                output_label.configure(text=show_yaml(tree, yaml_response.json()))
                bottom_output.config(text="Got response " + str(
                    yaml_response.status_code) + " " + f"{ok if yaml_response.ok is True else 'Not found'} " + f"{str(round(yaml_response.elapsed.total_seconds(), 2))}" + " seconds")
            elif response_view.get() == 'table':
                table_response = requests.patch(url_response, params=PARAMS, headers=HEADERS, data=BODY_params, auth=HTTPBasicAuth(username, password))
                output_label.configure(text=show_table(tree, table_response.json()))
                bottom_output.config(text="Got response " + str(
                    table_response.status_code) + " " + f"{ok if table_response.ok is True else 'Not found'} " + f"{str(round(table_response.elapsed.total_seconds(), 2))}" + " seconds")
            elif response_view.get() == 'treeview':
                treeview_response = requests.patch(url_response, params=PARAMS, headers=HEADERS, data=BODY_params, auth=HTTPBasicAuth(username, password))
                output_label.configure(text=make_tree(treeview_response.json()))
                bottom_output.config(text="Got response " + str(
                    treeview_response.status_code) + " " + f"{ok if treeview_response.ok is True else 'Not found'} " + f"{str(round(treeview_response.elapsed.total_seconds(), 2))}" + " seconds")
        if str(current_method) == 'DELETE':
            PARAMS = take_params()
            HEADERS = take_headers()
            BODY_params = take_body()
            if username == 'username' and password == 'password':
                delete_request = requests.delete(url_response, params=PARAMS, headers=HEADERS, data=BODY_params)
                output_label.configure(text=show_raw(tree, delete_request.json()))
                bottom_output.config(text="Got response " + str(
                    delete_request.status_code) + " " + f"{ok if delete_request.ok is True else 'Not found'} " + f"{str(round(delete_request.elapsed.total_seconds(), 2))}" + " seconds")
            else:
                delete_request = requests.delete(url_response, params=PARAMS, headers=HEADERS, data=BODY_params, auth=HTTPBasicAuth(username, password))
                output_label.configure(text=show_raw(tree, delete_request.json()))
                bottom_output.config(text="Got response " + str(
                    delete_request.status_code) + " " + f"{ok if delete_request.ok is True else 'Not found'} " + f"{str(round(delete_request.elapsed.total_seconds(), 2))}" + " seconds")
        conn.commit()
    send_button = tkmacosx.Button(request_frame, fg='aquamarine', text='Send', bg='black', command=url_request)
    send_button.grid(row=0, column=2)

    # request history frame

    def show_history():
        data = cursor.execute("""SELECT * FROM history LIMIT 10""")
        i=0
        for url, method in data:
            history_table.insert(parent='', index=i, iid=i, text='', values=(url, method))
            i = i + 1
        history_table.pack(expand=True, fill=BOTH)
        conn.commit()
    show_btn = Button(main_frame_history, text='show history', command=show_history)
    show_btn.grid(row=0, column=0,columnspan=1, sticky=NW)

    def clear_history():
        cursor.execute("""DELETE FROM history""")
        for row in history_table.get_children():
            history_table.delete(row)
        conn.commit()
    delete_btn = Button(main_frame_history, text='clear history', command=clear_history)
    delete_btn.grid(row=0, column=1, columnspan=1, sticky=NW)
    history_frame = Frame(main_frame_history)
    history_frame.grid(row=1, column=0, columnspan=250)
    history_table = ttk.Treeview(history_frame, column=("URL", "method"), show='headings')
    history_table.column("#1", stretch=YES, width=300)
    history_table.heading("#1", text='URL')
    history_table.column("#2", stretch=YES, width=300)
    history_table.heading("#2", text='method')
    history_table.pack(expand=True, fill=BOTH)

    root.mainloop()


    conn.close()

def main_cli():
    if args.history:
        if args.history == "show":
            logging.debug("Command to show History entered")

            indexes = history()
            index = input(f'Enter request index to view full info, or "q" to quit: ')
            if index == "q":
                logging.debug(f"Command to quit from History entered")
                sys.exit()
            elif int(index) in tuple(indexes):
                logging.debug(f"Command to show History item #[{index}] entered")
                show_index_from_history(index)
                logging.debug(f"History for item #[{index}] is displayed")

                sys.exit()
            else:
                print('Wrong Input. We will quit now')
                logging.debug("Wrong input on item select in history")
                sys.exit()

        elif args.history == "clear":
            logging.debug("Command to clear History entered")
            clear_history()
            logging.debug("History Cleared")
    else:
        logging.debug("Ready to perform request")
        perform_request()

if __name__ == "__main__":
    args = parse_args()
    if args.log:
        if args.log == "info":
            log_level = logging.INFO
        elif args.log == "debug":
            log_level = logging.DEBUG
        else:
            log_level = logging.WARNING
    else:
        log_level = logging.WARNING

    logging.basicConfig(filename="end-game.log",
                        filemode="a",
                        format=f"%(levelname)s - "
                               + f"%(asctime)s "
                               + f": %(message)s",
                        datefmt='%H:%M:%S',
                        level=log_level)

    ok = 'OK'
    pattern = r"^^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$"

    if args.endpoint and not re.match(pattern, args.endpoint):
        print("You have entered an invalid URL")
        logging.error("You have entered an invalid URL")
        sys.exit()

    if args.gui:
        logging.warning(f"GUI is running with logging level [{args.log}]")
        main_gui()
    else:
        logging.warning(f"CLI is running with logging level [{args.log}]")
        main_cli()

