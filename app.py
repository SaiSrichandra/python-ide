#!/usr/bin/python
import PySimpleGUI as sg
import re
import sys
import os
import threading


def clear():
    window['-TEXT-'].update("")

if not os.path.exists("dataset"): os.mkdir("dataset")
roll_no = ""
counter = 0
prog = 1
    
var = sys.stdout
w_wid = 50
w_hei = 50

f_run = "Run .. (F5)"
f_prog = "New Program ... (F9)"
menu_layout = [['Run', [f_run]],['New', [f_prog]]]


layout = [[sg.Menu(menu_layout)],[sg.Text(size=(24,3), key='-TEXT-')],[sg.Text(size=(24,10), key='-TEXT-')], [sg.Multiline(font=('Arial',15), size=(w_wid,w_hei), key='_BODY_')]]

layout_inp = [
    [sg.Text('Please enter your Roll No')],
    [sg.Text('Roll Number', size =(15, 1)), sg.InputText()],
    [sg.Submit(bind_return_key = False,)]
]

window = sg.Window('PY IDE', layout=layout, margins=(0, 0), resizable=True, return_keyboard_events=True)#,web_port=2222)


window_inp = sg.Window('PY INP', layout = layout_inp, resizable=True, return_keyboard_events=True).Finalize()
window_inp['Submit'].update(disabled=True)

while(True):
    event,values = window_inp.read()
    if values[0] != '' and re.match('[0-9]{12}$', values[0]):
        window_inp['Submit'].update(disabled=False)
    else:
        window_inp['Submit'].update(disabled=True)
    
    if(event in (None,'Exit')):
        exit(0)
    if event == 'Submit':
        roll_no = values[0]
        window_inp.close()
        break


window.Finalize()
window.Maximize()
w_win,h_win = window.size
_,h_body = window['_BODY_'].Size
layout = [[sg.Menu(menu_layout)],[sg.Text(size=(24,10), key='-TEXT-')], [sg.Multiline(font=('Arial',15), size=(w_win,h_body), key='_BODY_')]]
window.close()
window = sg.Window('PY IDE', layout=layout, margins=(0, 0), resizable=True, return_keyboard_events=True).Finalize()
window.Maximize()

while(True):
    event, values = window.read()
    # print(event, values)
    if(event in None or event == 'F12:96' ):
        break
    if(event == f_run or event == 'F5:71'):
        try :
            with open("out.txt", "w+") as sys.stdout:
                exec(values['_BODY_'])
            with open("out.txt", "r") as sys.stdout:
                window['-TEXT-'].update(str(sys.stdout.read()))
            
            path = "dataset"
            filename = roll_no+"-"+str(counter)+"-"+str(prog)+".txt"
            file_path = os.path.join(path, filename)

            with open(file_path, "w+") as fp:
                fp.write(values['_BODY_'])
            counter+=1

        except Exception as e:
            with open("err.txt", "w+") as sys.stdout:
                print(e)
            window['-TEXT-'].update("ERROR : " + str(e))

        sys.stdout = var
        timer = threading.Timer(10.0, clear)
        timer.start()
    
    if(event == '\r'):
        try:
            exec(values['_BODY_'])
            path = "dataset"
            filename = roll_no+"-"+str(counter)+"-"+str(prog)+".txt"
            file_path = os.path.join(path, filename)

            with open(file_path, "w+") as fp:
                fp.write(values['_BODY_'])
            counter+=1
        except Exception as e:
            with open("err_int.txt", "w+") as sys.stdout:
                print(e)
            sys.stdout = var

    if(event == f_prog or event == 'F9:75'):
        prog+=1
        window['-TEXT-'].update("")
        window['_BODY_'].update("")

    
