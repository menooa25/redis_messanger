import tkinter as tk
from multiprocessing import Process
from threading import Thread

from redis_message import Server

server = Server()
last_processor = None
window = tk.Tk()
window.title('Redis messanger')
window.columnconfigure([0, 1, 2, 3], weight=1, minsize=1)
window.rowconfigure([0, 1, 2, 3], weight=1, minsize=1)

frm_connection = tk.Frame()
lbl_ip_and_port = tk.Label(frm_connection, text="Redis ip with port: ")
lbl_ip_and_port.pack(side=tk.LEFT)
ent_ip_and_port = tk.Entry(frm_connection)
ent_ip_and_port.insert(0, 'localhost:6379')
ent_ip_and_port.pack(side=tk.LEFT)
lbl_channel = tk.Label(frm_connection, text='Channel: ')
lbl_channel.pack(side=tk.LEFT)
ent_channel = tk.Entry(frm_connection)
ent_channel.pack(side=tk.LEFT)
frm_connection.grid(column=0, row=0, columnspan=2)


def on_connect():
    try:
        host_port = ent_ip_and_port.get().split(':')
        host = host_port[0]
        port = host_port[1]
        status = server.connect(host=host, port=port)
        if status:
            lbl_status['text'] = 'Connected'
            lbl_status['fg'] = 'green'
        else:
            lbl_status['text'] = 'Connection refused'
            lbl_status['fg'] = 'red'
    except:
        lbl_status['text'] = 'Error'
        lbl_status['fg'] = 'red'


def on_send_msg():
    msg = ent_message.get()
    channel = ent_channel.get()
    server.send_message(channel=channel, msg=msg)


def on_receive_message(msg):
    if txt_message.is_first:
        txt_message.insert(tk.END, f'{msg}')
        txt_message.is_first = False
    else:
        txt_message.insert(tk.END, f'\n{msg}')


def on_start_receive_msgs():
    channel = ent_channel.get()
    th = Thread(target=server.receive_messages, kwargs={'channel': channel, 'set_message': on_receive_message})
    th.start()


is_server = tk.IntVar(value=1)
frm_usage = tk.Frame()
frm_usage.grid(column=1, row=0)
btn_connect = tk.Button(text='Connect', command=on_connect)
btn_connect.grid(column=0, row=1, sticky='wns')
lbl_status = tk.Label(text='Disconnected', fg='red')
lbl_status.grid(column=1, row=1, sticky='w')
frm_message = tk.Frame()
frm_message.grid(row=2, column=0, columnspan=2)
btn_start_receive_msgs = tk.Button(frm_message, text='Receive messages', command=on_start_receive_msgs)
btn_start_receive_msgs.pack(side=tk.LEFT)
lbl_message = tk.Label(frm_message, text='Message: ')
lbl_message.pack(side=tk.LEFT)
ent_message = tk.Entry(frm_message)
ent_message.pack(side=tk.LEFT)
btn_send_msg = tk.Button(frm_message, text='Send', command=on_send_msg)
btn_send_msg.pack(side=tk.LEFT)
txt_message = tk.Text()
txt_message.is_first = True
txt_message.grid(column=0, row=3, columnspan=2)

if __name__ == '__main__':
    window.mainloop()
