import tkinter as tk
from tkinter import ttk, messagebox

import yaml

import pandas as pd


# 创建主窗口
root = tk.Tk()
root.geometry("800x700")
root.title("状态编辑器")

root.grid_rowconfigure((0,1,2,3,5,6,7,8,9,10,11,12,13,14,15), weight=1)
root.grid_columnconfigure((0,1), weight=1)

# 创建状态名称标签和输入框
tk.Label(root, text="状态名称").grid(row=0, column=0, padx=2, pady=1, sticky="ew")
stateNameText = tk.Text(root, width=60, height=1)
stateNameText.grid(row=0, column=1, padx=5, pady=2)

# 创建状态描述信息标签和输入框
tk.Label(root, text="状态描述").grid(row=1, column=0, padx=2, pady=1, sticky="ew")
stateDescriptionText = tk.Text(root, width=60, height=1)
stateDescriptionText.grid(row=1, column=1, padx=5, pady=2)

# 创建状态类型标签
tk.Label(root, text="状态类型").grid(row=2, column=0, padx=2, pady=1, sticky="ew")

# 创建状态类型组合框
state_type_var = tk.StringVar()
state_type_combo = ttk.Combobox(root, textvariable=state_type_var, width=57)

# 设置组合框的选项
state_type_combo['values'] = ("Composite", "Normal", "Pseudo")

# 将组合框放置在网格中
state_type_combo.grid(row=2, column=1, padx=2, pady=2)

tk.Label(root, text="所属父状态").grid(row=3, column=0, padx=2, pady=1, sticky="ew")
fatherStateText = tk.Text(root, width=60, height=1)
fatherStateText.grid(row=3, column=1, padx=5, pady=2)

# # 创建时间锁标签和输入框
# tk.Label(root, text="时间锁").grid(row=4, column=0, padx=2, pady=1, sticky="ew")
# timeLockText = tk.Text(root, width=60, height=1)
# timeLockText.grid(row=4, column=1, padx=5, pady=2)
# 创建时间锁标签

# 创建最小停留时间标签和输入框
tk.Label(root, text="最小停留时间").grid(row=4, column=0, padx=2, pady=1, sticky="ew")
minTimeLockText = tk.Text(root, width=60, height=1)
minTimeLockText.grid(row=4, column=1, padx=5, pady=2)

# 创建最大停留时间标签和输入框
tk.Label(root, text="最大停留时间").grid(row=5, column=0, padx=2, pady=1, sticky="ew")
maxTimeLockText = tk.Text(root, width=60, height=1)
maxTimeLockText.grid(row=5, column=1, padx=5, pady=2)

# 创建Entry标签和输入框
tk.Label(root, text="Entry").grid(row=6, column=0, padx=2, pady=1, sticky="ew")
entryText = tk.Text(root, width=60, height=1)
entryText.grid(row=6, column=1, padx=5, pady=2)

# 创建During标签和输入框
tk.Label(root, text="During").grid(row=7, column=0, padx=2, pady=1, sticky="ew")
duringText = tk.Text(root, width=60, height=1)
duringText.grid(row=7, column=1, padx=5, pady=2)

# 创建Exit标签和输入框
tk.Label(root, text="Exit").grid(row=8, column=0, padx=2, pady=1, sticky="ew")
exitText = tk.Text(root, width=60, height=1)
exitText.grid(row=8, column=1, padx=5, pady=2)

events_data = {}   # 创建一个空字典来保存事件的详细信息
transitions_data = {}   # 创建一个空字典来保存迁移的详细信息

# 插入分隔线
ttk.Separator(root, orient="horizontal").grid(row=9, column=0, columnspan=2, sticky="ew")

tk.Label(root, text="产生事件").grid(row=10, column=0, padx=10, pady=5, columnspan=2)

# 定义表格列名
columns = ("事件名称", "事件产生条件")

# 创建表格
events_table = ttk.Treeview(root, height=8, show="headings", columns=columns)
events_table.grid(row=11, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

# 创建滚动条
scrollBar = ttk.Scrollbar(root, orient="vertical", command=events_table.yview)
events_table.configure(yscrollcommand=scrollBar.set)
scrollBar.grid(row=11, column=2, sticky='ns')

# 定义列
for col in columns:
    events_table.column(col, width=100, anchor='center')
    events_table.heading(col, text=col)

# 定义右键菜单
def show_popup_menu(event, table, add_func, edit_func):
    item = table.identify_row(event.y)
    if not item:
        return
    menu = tk.Menu(root, tearoff=0)
    menu.add_command(label="编辑", command=lambda: edit_func(True, item))
    menu.add_command(label="删除", command=lambda: delete_item(table, item))
    menu.post(event.x_root, event.y_root)


def delete_item(table, item_id):
    item_values = table.item(item_id)['values']
    if table == events_table:
        del events_data[item_values[0]]
    elif table == transitions_table:
        del transitions_data[item_values[0]]
    table.delete(item_id)

def add_event(edit=False, row_id=''):
    global new_window
    new_window = tk.Toplevel(root)
    new_window.grab_set()

    # 更新窗口，以确保可以获得准确的窗口大小
    root.update()
    new_window.update()

    # 获得主窗口和新窗口的位置和大小
    root_x, root_y, root_width, root_height = root.winfo_x(), root.winfo_y(), root.winfo_width(), root.winfo_height()
    new_width, new_height = new_window.winfo_reqwidth(), new_window.winfo_reqheight()

    # 计算新窗口出现在主窗口中心时的位置
    x = root_x + (root_width // 2) - (new_width // 2)
    y = root_y + (root_height // 2) - (new_height // 2)

    # 设置新窗口的位置
    new_window.geometry(f"+{x}+{y}")

    new_window.title("编辑事件" if edit else "添加事件")

    # 创建输入框和标签
    global data_entries
    data_entries = []

    data_row = ()
    if edit:
        data_row = events_table.item(row_id)['values']

    for i in range(len(columns)):
        tk.Label(new_window, text=columns[i]).grid(row=i, column=0)
        entry = tk.Entry(new_window)
        entry.insert(0, data_row[i] if edit and len(data_row) > i else "")
        entry.grid(row=i, column=1)
        data_entries.append(entry)

    # 绑定右键菜单到事件表格
    events_table.bind("<Button-3>", lambda e: show_popup_menu(e, events_table, add_event, add_event))

    # 创建按钮
    tk.Button(new_window, text="保存", command=lambda: save_event(edit, row_id)).grid(row=len(columns), column=0,
                                                                                     columnspan=2)

    new_window.mainloop()


# 保存事件到表格
def save_event(edit=False, row_id=''):
    data = []
    for entry in data_entries:
        data.append(entry.get())

    event_name = data[0]
    condition = data[1]
    if edit:
        events_table.item(row_id, values=tuple(data))
        # 更新事件数据字典
        events_data[event_name] = {'name': event_name, 'guard': condition}
    else:
        events_table.insert('', 'end', values=tuple(data))
        # 添加新的事件数据到字典
        events_data[event_name] = {'name': event_name, 'guard': condition}
    new_window.destroy()  # close new_window after adding data

# 创建添加事件按钮
btn_add = tk.Button(root, text="添加事件", command=add_event, width=20, height=1, foreground='black', background='white')
btn_add.grid(row=10, column=0, columnspan=2, padx=10, pady=5, sticky="e")

# 插入分隔线
ttk.Separator(root, orient="horizontal").grid(row=12, column=0, columnspan=2, sticky="ew")

tk.Label(root, text="迁移").grid(row=13, column=0, padx=10, pady=5, columnspan=2)

# 定义迁移表格列名
transitions_columns = ("激励事件", "迁移目标")

# 创建迁移表格
transitions_table = ttk.Treeview(root, height=8, show="headings", columns=transitions_columns)
transitions_table.grid(row=14, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

# 创建滚动条
scrollBar_event = ttk.Scrollbar(root, orient="vertical", command=events_table.yview)
transitions_table.configure(yscrollcommand=scrollBar_event.set)
scrollBar_event.grid(row=14, column=2, sticky='ns')

# 定义列
for col in transitions_columns:
    transitions_table.column(col, width=100, anchor='center')
    transitions_table.heading(col, text=col)

# 创建一个函数来添加外部事件
def add_transition(edit=False, row_id=''):
    global new_window
    new_window = tk.Toplevel(root)
    new_window.grab_set()

    # 更新窗口，以确保可以获取准确的窗口大小
    root.update()
    new_window.update()

    # 获取主窗口和新窗口的位置和大小
    root_x, root_y, root_width, root_height = root.winfo_x(), root.winfo_y(), root.winfo_width(), root.winfo_height()
    new_width, new_height = new_window.winfo_reqwidth(), new_window.winfo_reqheight()

    # 计算新窗口出现在主窗口中心时的位置
    x = root_x + (root_width // 2) - (new_width // 2)
    y = root_y + (root_height // 2) - (new_height // 2)

    # 设置新窗口的位置
    new_window.geometry(f"+{x}+{y}")

    new_window.title("编辑迁移" if edit else "添加迁移")

    # 创建输入框和标签
    global transition_entries
    transition_entries = []

    transition_row = ()
    if edit:
        transition_row = transitions_table.item(row_id)['values']

    for i in range(len(transitions_columns)):
        tk.Label(new_window, text=transitions_columns[i]).grid(row=i, column=0)
        entry = tk.Entry(new_window)
        entry.insert(0, transition_row[i] if edit and len(transition_row) > i else "")
        entry.grid(row=i, column=1)
        transition_entries.append(entry)

    # 绑定右键菜单到迁移表格
    transitions_table.bind("<Button-3>",
                           lambda e: show_popup_menu(e, transitions_table, add_transition, add_transition))

    # 创建按钮
    tk.Button(new_window, text="保存", command=lambda: save_transition(edit, row_id)).grid(row=len(transitions_columns), column=0,
                                                                                     columnspan=2)

    new_window.mainloop()

# 保存事件数据到表格
def save_transition(edit=False, row_id=''):
    data = []
    for entry in transition_entries:
        data.append(entry.get())

    trigger_event = data[0]
    transition_target = data[1]
    if edit:
        transitions_table.item(row_id, values=tuple(data))
        # 更新迁移数据字典
        transitions_data[trigger_event] = {'event': trigger_event, 'target': transition_target}
    else:
        transitions_table.insert('', 'end', values=tuple(data))
        # 添加新的迁移数据到字典
        transitions_data[trigger_event] = {'event': trigger_event, 'target': transition_target}
    new_window.destroy()  # close new_window after adding data

# 创建添加状态按钮
btn_add_transition = tk.Button(root, text="添加迁移", command=add_transition, width=20, height=1, foreground='black', background='white')
btn_add_transition.grid(row=13, column=0, columnspan=2, padx=10, pady=5, sticky="e")



# 新建 Frame，将它放在 GUI 的第 2 列
state_list_frame = tk.Frame(root)
state_list_frame.grid(row=0, column=2, sticky="ns", rowspan=15)

# 在这个新的 Frame 内创建标签和列表框
tk.Label(state_list_frame, text="所有状态").grid(row=0, column=0, padx=2, pady=2, sticky="ew")
all_states_listbox = tk.Listbox(state_list_frame, width=20)
all_states_listbox.grid(row=1, column=0, padx=5, pady=2, sticky="ew")


# 创建滚动条
state_list_scrollbar = tk.Scrollbar(state_list_frame, orient="vertical", command=all_states_listbox.yview)
all_states_listbox.configure(yscrollcommand=state_list_scrollbar.set)
state_list_scrollbar.grid(row=1, column=1, sticky='ns')

# 定义删除当前状态的函数
def delete_current_state():
    selected_index = all_states_listbox.curselection()
    if selected_index:
        all_states_listbox.delete(selected_index)

# 创建右键菜单
context_menu = tk.Menu(all_states_listbox, tearoff=0)
context_menu.add_command(label="删除当前状态", command=delete_current_state)

# 绑定右键点击事件
def show_context_menu(event):
    # 获取当前选中的项
    selected_index = all_states_listbox.nearest(event.y)
    if selected_index is not None:
        all_states_listbox.selection_set(selected_index)
        context_menu.post(event.x_root, event.y_root)

all_states_listbox.bind("<Button-3>", show_context_menu)  # 右键点击事件


# 修改第 0 列和第 1 列的宽度，以适应新的布局
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=2)
root.grid_columnconfigure(2, weight=1)

states_data = {}

def save_state():
    # 同样地，把所有需要保存的信息保存到一个字典
    state_data = {
        'name': stateNameText.get("1.0", 'end-1c'),
        'description': stateDescriptionText.get("1.0", 'end-1c'),
        'type': state_type_var.get(),
        'father': fatherStateText.get("1.0", 'end-1c'),
        'minTimeLock': minTimeLockText.get("1.0", 'end-1c'),
        'maxTimeLock': maxTimeLockText.get("1.0", 'end-1c'),
        'entry': entryText.get("1.0", 'end-1c'),
        'during': duringText.get("1.0", 'end-1c'),
        'exit': exitText.get("1.0", 'end-1c'),
        'events': list(events_data.values()),
        'transitions': list(transitions_data.values()),
    }

    state_name = state_data['name']



    # 获取最小停留时间
    min_time_lock = state_data['minTimeLock']

    # 检查最大停留时间是否有内容
    if state_data['maxTimeLock']:
        # 生成新的事件
        new_event = {
            'name': 'max_time',
            'guard': state_name + '_count' + ' > ' +state_data['maxTimeLock']
        }

        # 将新事件添加到 events 列表
        state_data['events'].append(new_event)
        # 生成新的迁移
        state_data['transitions'].append({'event': 'max_time', 'target': 'time_out'})

    # 检查状态是否已经存在
    if state_name in states_data:
        # 更新已存在状态的信息
        states_data[state_name] = state_data
    else:
        # 向 states_data 添加新的状态信息
        states_data[state_name] = state_data
        # 在列表框中添加新的状态名
        all_states_listbox.insert('end', state_name)



# 清空处理函数
def clear_all():
    # 清空状态名称输入框
    stateNameText.delete(1.0, 'end')
    # 清空状态描述输入框
    stateDescriptionText.delete(1.0, 'end')
    # 清空状态类型组合框
    state_type_var.set("")
    # 清空父状态输入框
    fatherStateText.delete(1.0, 'end')
    # 清空时间锁输入框
    minTimeLockText.delete(1.0, 'end')
    maxTimeLockText.delete(1.0, 'end')
    # 清空Entry输入框
    entryText.delete(1.0, 'end')
    # 清空During输入框
    duringText.delete(1.0, 'end')
    # 清空Exit输入框
    exitText.delete(1.0, 'end')

    # 清空事件表格
    events_table.delete(*events_table.get_children())
    events_data.clear()

    # 清空迁移表格
    transitions_table.delete(*transitions_table.get_children())
    transitions_data.clear()


def load_state(event):
    # 获取选中的状态名
    state_name = all_states_listbox.get(all_states_listbox.curselection())
    # 根据状态名从字典中获取状态信息
    state_data = states_data.get(state_name)
    if state_data is None:
        print(f"No data found for state {state_name}")
        return
    # 将状态信息显示在对应的输入框里
    stateNameText.delete(1.0, 'end')
    stateNameText.insert(1.0, state_data['name'])
    stateDescriptionText.delete(1.0, 'end')
    stateDescriptionText.insert(1.0, state_data.get('description', ''))
    state_type_var.set(state_data.get('type', 'Normal'))
    fatherStateText.delete(1.0, 'end')
    fatherStateText.insert(1.0, state_data.get('father', ''))
    minTimeLockText.delete(1.0, 'end')
    minTimeLockText.insert(1.0, state_data.get('minTimeLock', ''))
    maxTimeLockText.delete(1.0, 'end')
    maxTimeLockText.insert(1.0, state_data.get('maxTimeLock', ''))
    entryText.delete(1.0, 'end')
    entryText.insert(1.0, state_data.get('entry', ''))
    duringText.delete(1.0, 'end')
    duringText.insert(1.0, state_data.get('during', ''))
    exitText.delete(1.0, 'end')
    exitText.insert(1.0, state_data.get('exit', ''))
    # 清空事件和迁移表格，并添加新的信息
    events_data.clear()
    events_table.delete(*events_table.get_children())
    for event in state_data.get('events', []):
        events_data[event['name']] = event
        events_table.insert('', 'end', values=(event['name'], event['guard']))
    transitions_data.clear()
    transitions_table.delete(*transitions_table.get_children())
    for transition in state_data.get('transitions', []):
        transitions_data[transition['event']] = transition
        transitions_table.insert('', 'end', values=(transition['event'], transition['target']))

# 在列表框上设置<<ListboxSelect>>绑定，当选择一个状态时调用 load_state 函数
all_states_listbox.bind('<<ListboxSelect>>', load_state)


def export_all_states():

    try:
        all_states_excel = []
        all_states_yaml = []

        for state_name, state_info in states_data.items():  # 遍历所有的状态
            #
            data_excel = {
                '状态名称': state_info['name'],  # 从字典中获取信息
                '状态描述': state_info['description'],
                '状态类型': state_info['type'],
                '父状态': state_info['father'],
                '最小停留时间': state_info['minTimeLock'],
                '最大停留时间': state_info['maxTimeLock'],
                '产生事件': list(state_info['events'].values()) if isinstance(state_info['events'], dict) else state_info['events'],
                '迁移': list(state_info['transitions'].values()) if isinstance(state_info['transitions'], dict) else state_info['transitions'],
            }

            data_yaml = {
                'name': state_info['name'],
                'type': state_info['type'],
                'minTimeLock': state_info['minTimeLock'],
                'maxTimeLock': state_info['maxTimeLock'],
                'on entry': state_info['entry'],
                'on during': state_info['during'],
                'on exit': state_info['exit'],
                'events': list(state_info['events'].values()) if isinstance(state_info['events'], dict) else state_info['events'],
                'transitions': list(state_info['transitions'].values()) if isinstance(state_info['transitions'], dict) else state_info['transitions'],
            }

            all_states_excel.append(data_excel)
            all_states_yaml.append(data_yaml)

        # 获得父状态名称
        father_name = fatherStateText.get(1.0, 'end').strip()
        # 写入到文件中
        with open(f'export_data/{father_name}_states.yaml', 'w') as f:
            yaml.safe_dump({"states": all_states_yaml}, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

        excel_filename = f'export_data/{father_name}_states.xlsx'
        df = pd.DataFrame(all_states_excel)
        df.to_excel(excel_filename, index=False)

        messagebox.showinfo('信息', '导出所有状态成功')
    except Exception as e:
        messagebox.showerror('错误', f'导出失败，出现错误: {str(e)}')

def clear_states():
    # 清空状态列表
    all_states_listbox.delete(0, 'end')
    states_data.clear()


clear_states_button = tk.Button(state_list_frame, text="清空状态", command=clear_states)
clear_states_button.grid(row=2, column=0, columnspan=2, pady=(5, 10), sticky="ew")


# 创建新的Frame，并将它加入到grid布局中
frame_buttons = tk.Frame(root)
frame_buttons.grid(row=15, column=1, sticky='se')

save_button = tk.Button(frame_buttons, text="保存", command=save_state)
save_button.pack(side='left', padx=10, pady=5)

export_button = tk.Button(frame_buttons, text="导出", command=export_all_states)
export_button.pack(side='right', padx=10, pady=5)

clear_button = tk.Button(frame_buttons, text="清空", command=clear_all)
clear_button.pack(side='right', padx=10, pady=5)

root.mainloop()