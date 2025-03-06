import tkinter as tk
from tkinter import ttk, messagebox

import yaml


# 创建主窗口
root = tk.Tk()
root.geometry("600x800")
root.title("状态机编辑器")

root.grid_rowconfigure((0,1,2,3,5,6,7,8,9,10,11), weight=1)
root.grid_columnconfigure((0,1), weight=1)

# 创建状态机名称标签和输入框
tk.Label(root, text="状态机名称").grid(row=0, column=0, padx=2, sticky="ew")
machineNameText = tk.Text(root, width=60, height=1)
machineNameText.grid(row=0, column=1, padx=5, pady=5)
# machineNameEntry = tk.Entry(root, width=30)
# machineNameEntry.grid(row=0, column=1, padx=2, pady=5, sticky="ew")

# 创建初始化信息标签和输入框
tk.Label(root, text="状态机描述").grid(row=1, column=0, padx=2, sticky="ew")
stateDescriptionText = tk.Text(root, width=60, height=1)
stateDescriptionText.grid(row=1, column=1, padx=5, pady=5)
# initInfoEntry = tk.Entry(root, width=30)
# initInfoEntry.grid(row=1, column=1, padx=2, pady=5, sticky="ew")

states_data = {}   # 创建一个空字典来保存状态的详细信息
transitions_data = {}
events_data = {}   # 创建一个空字典来保存外部事件的详细信息

# 插入分隔线
ttk.Separator(root, orient="horizontal").grid(row=2, column=0, columnspan=2, sticky="ew")

tk.Label(root, text="包含状态").grid(row=3, column=0, padx=10, pady=5, columnspan=2)

# 定义表格列名
columns = ( "状态名称", "状态类型")

# 创建表格
states_table = ttk.Treeview(root, height=8, show="headings", columns=columns)
states_table.grid(row=4, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

# 创建滚动条
scrollBar = ttk.Scrollbar(root, orient="vertical", command=states_table.yview)
states_table.configure(yscrollcommand=scrollBar.set)
scrollBar.grid(row=4, column=3, sticky='ns')

# 定义列
for col in columns:
    states_table.column(col, width=100, anchor='center')
    states_table.heading(col, text=col)

def add_data(edit=False, row_id=''):
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

    new_window.title("编辑状态" if edit else "添加状态")

    # 创建输入框和标签
    global data_entries
    data_entries = []

    data_row = ()
    if edit:
        data_row = states_table.item(row_id)['values']

    for i in range(len(columns)):
        tk.Label(new_window, text=columns[i]).grid(row=i, column=0)

        # 如果当前创建的是"状态类型"字段，我们使用下拉菜单替换手动输入
        if columns[i] == '状态类型':
            state_type = tk.StringVar()
            combobox = ttk.Combobox(new_window, textvariable=state_type, width=15)
            combobox['values'] = ('Composite', 'Normal', 'Pseudo')  # 这是下拉菜单的可选项
            combobox.grid(row=i, column=1)
            data_entries.append(combobox)
        else:
            entry = tk.Entry(new_window, width=17)
            entry.insert(0, data_row[i] if edit and len(data_row) > i else "")
            entry.grid(row=i, column=1)
            data_entries.append(entry)

    # 创建保存按钮
    tk.Button(new_window, text="保存", command=lambda: save_data(edit, row_id)).grid(row=len(columns), column=2,
                                                                                     sticky="W")
    new_window.lift()

    # new_window.mainloop()
# 保存数据到表格
# 保存数据到表格
def save_data(edit=False, row_id=''):
    data = []
    for entry in data_entries:
        data.append(entry.get())

    status_name = data[0]
    status_type = data[1]

    if edit:
        states_table.item(row_id, values=(status_name, status_type))
        states_data[status_name] = {'name': status_name, 'type': status_type}
    else:
        states_table.insert('', 'end', text=status_name, values=(status_name, status_type))
        states_data[status_name] = {'name': status_name, 'type': status_type}

    new_window.destroy()

# 创建添加状态按钮
btn_add = tk.Button(root, text="添加状态", command=add_data, width=20, height=1, foreground='black', background='white')
btn_add.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="e")

# 插入分隔线
ttk.Separator(root, orient="horizontal").grid(row=5, column=0, columnspan=2, sticky="ew")

# 创建 "包含迁移" 标签 和 表格
tk.Label(root, text="包含迁移").grid(row=6, column=0, padx=10, pady=5, columnspan=2)

# 定义迁移表格列名
transition_columns = ("起始状态", "目标状态", "激励事件")

# 创建迁移表格
transitions_table = ttk.Treeview(root, height=8, show="headings", columns=transition_columns)
transitions_table.grid(row=7, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

# 创建滚动条
scrollBar_transition = ttk.Scrollbar(root, orient="vertical", command=transitions_table.yview)
transitions_table.configure(yscrollcommand=scrollBar_transition.set)
scrollBar_transition.grid(row=7, column=3, sticky='ns')

# 定义列
for col in transition_columns:
    transitions_table.column(col, width=100, anchor='center')
    transitions_table.heading(col, text=col)


# 创建添加迁移的函数
def add_transition(edit=False, row_id=''):
    global new_window
    new_window = tk.Toplevel(root)
    new_window.grab_set()

    # 更新窗口，以确保可以获得准确的窗口大小
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

    for i in range(len(transition_columns)):
        tk.Label(new_window, text=transition_columns[i]).grid(row=i, column=0)
        entry = tk.Entry(new_window)
        entry.insert(0, transition_row[i] if edit and len(transition_row) > i else "")
        entry.grid(row=i, column=1)
        transition_entries.append(entry)

    # 创建按钮
    tk.Button(new_window, text="保存", command=lambda: save_transition(edit, row_id)).grid(row=len(transition_columns),
                                                                                           column=0,
                                                                                           columnspan=2)

    new_window.mainloop()


# 保存迁移数据到表格
def save_transition(edit=False, row_id=''):
    data = []
    for entry in transition_entries:
        data.append(entry.get())

    start_status = data[0]
    target_status = data[1]
    event = data[2]

    # 如果状态字典已有该开始状态，则获取它的迁移数组，否则使其迁移数组为空
    if start_status in states_data:
        transitions = states_data[start_status].get('transitions', [])
    else:
        transitions = []

    # 将新的迁移添加到迁移数组
    transitions.append({'target': target_status, 'event': event})

    # 保存开始状态，状态类型，和迁移数组到状态字典
    states_data[start_status] = {'name': start_status, 'type': states_data[start_status]['type'],
                                 'transitions': transitions}

    if edit:
        transitions_table.item(row_id, values=tuple(data))

    else:
        transitions_table.insert('', 'end', values=tuple(data))

    new_window.destroy()  # close new_window after adding data


# 创建添加状态按钮
btn_add_transition = tk.Button(root, text="添加迁移", command=add_transition, width=20, height=1, foreground='black',
                               background='white')
btn_add_transition.grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky="e")

# 插入分隔线
ttk.Separator(root, orient="horizontal").grid(row=8, column=0, columnspan=2, sticky="ew")

tk.Label(root, text="外部事件").grid(row=9, column=0, padx=10, pady=5, columnspan=2)

# 定义外部事件表格列名
event_columns = ("事件名称", "描述")

# 创建外部事件表格
events_table = ttk.Treeview(root, height=4, show="headings", columns=event_columns)
events_table.grid(row=10, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

# 创建滚动条
scrollBar_event = ttk.Scrollbar(root, orient="vertical", command=events_table.yview)
events_table.configure(yscrollcommand=scrollBar_event.set)
scrollBar_event.grid(row=10, column=3, sticky='ns')

# 定义列
for col in event_columns:
    events_table.column(col, width=100, anchor='center')
    events_table.heading(col, text=col)

# 创建一个函数来添加外部事件
def add_event(edit=False, row_id=''):
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

    new_window.title("编辑事件" if edit else "添加事件")

    # 创建输入框和标签
    global event_entries
    event_entries = []

    event_row = ()
    if edit:
        event_row = events_table.item(row_id)['values']

    for i in range(len(event_columns)):
        tk.Label(new_window, text=event_columns[i]).grid(row=i, column=0)
        entry = tk.Entry(new_window)
        entry.insert(0, event_row[i] if edit and len(event_row) > i else "")
        entry.grid(row=i, column=1)
        event_entries.append(entry)

    # 创建按钮
    tk.Button(new_window, text="保存", command=lambda: save_event(edit, row_id)).grid(row=len(event_columns), column=0,
                                                                                     columnspan=2)

    new_window.mainloop()

# 保存事件数据到表格
def save_event(edit=False, row_id=''):
    data = []
    for entry in event_entries:
        data.append(entry.get())

    event_name = data[0]
    event_description = data[1]
    if edit:
        events_table.item(row_id, values=tuple(data))
        # 更新事件数据字典
        events_data[event_name] = {'事件名称': event_name, '描述': event_description}
    else:
        events_table.insert('', 'end', values=tuple(data))
        # 添加新的事件数据到字典
        events_data[event_name] = {'事件名称': event_name, '描述': event_description}
    new_window.destroy()  # close new_window after adding data

# 创建添加状态按钮
btn_add_event = tk.Button(root, text="添加外部事件", command=add_event, width=20, height=1, foreground='black', background='white')
btn_add_event.grid(row=9, column=0, columnspan=2, padx=10, pady=5, sticky="e")

# 在状态表格中右键时，展示"编辑"和"删除"选项
def popup_states(event):
    # 未选中事件则直接返回
    if not states_table.selection():
        return
    menu_states.post(event.x_root, event.y_root)

def delete_selection():
    selected = states_table.selection()
    # If there is no selection, return without doing anything
    if not selected:
        return
    selected_item = states_table.item(selected)['values'][0]
    states_table.delete(selected)
    states_data.pop(selected_item)

menu_states = tk.Menu(root, tearoff=0)
menu_states.add_command(label="编辑", command=lambda: add_data(True, states_table.selection()))
menu_states.add_command(label="删除", command=delete_selection)
states_table.bind('<Button-3>', popup_states)

# 在迁移表格中右键时，展示"编辑"和"删除"选项
def popup_transitions(event):
    # 未选中事件则直接返回
    if not transitions_table.selection():
        return
    menu_transitions.post(event.x_root, event.y_root)

def delete_transition():
    selected = transitions_table.selection()
    if not selected:
        return
    selected_item = transitions_table.item(selected)['values'][0]
    transitions_table.delete(selected)
    transitions_data.pop(selected_item)

menu_transitions = tk.Menu(root, tearoff=0)
menu_transitions.add_command(label="编辑", command=lambda: add_transition(True, transitions_table.selection()))
menu_transitions.add_command(label="删除", command=delete_transition)
transitions_table.bind('<Button-3>', popup_transitions)

# 在外部事件表格中右键时，展示"编辑"和"删除"选项
def popup_external_events(event):
    # 未选中事件则直接返回
    if not events_table.selection():
        return
    menu_external_events.post(event.x_root, event.y_root)

def delete_event():
    selected = events_table.selection()
    if not selected:
        return
    selected_item = events_table.item(selected)['values'][0]
    events_table.delete(selected)
    events_data.pop(selected_item)

menu_external_events = tk.Menu(root, tearoff=0)
menu_external_events.add_command(label="编辑", command=lambda: add_event(True, events_table.selection()))
menu_external_events.add_command(label="删除", command=delete_event)
events_table.bind('<Button-3>', popup_external_events)

def export_to_yaml():

    external_events = [events_data[labels]['描述'] for labels in events_data.keys()]
    # 这是需要保存的数据字典
    data_excel = {
        '状态机名称': machineNameText.get("1.0", 'end-1c'),
        '状态机描述': stateDescriptionText.get("1.0", 'end-1c'),
        # 转化类型为list
        '状态': list(states_data.values()),

        '外部事件': list(events_data.values()),
    }
    # #列表换行化处理
    preamble_list = [events_data[labels]['描述'] for labels in events_data.keys()]
    #
    with open('preamble.py', 'w') as f:
        for line in preamble_list:
            f.write(line + '\n')  # 添加换行符，确保每行代码单独一行

    with open('preamble.py', 'r') as preamble_file:
        preamble_content = preamble_file.read()

    data_yaml = {
        'name': machineNameText.get("1.0", 'end-1c'),
        'initial': next(iter(states_data.values()))['name'],
        # 转化类型为list
        'states': list(states_data.values()),
    }

    sm_name = machineNameText.get("1.0", 'end-1c')
    # 保存为 YAML 文件
    with open(f'export_data/{sm_name}_statemachine.yaml', 'w') as f:
        yaml.dump({
            "statechart":
                {'name': machineNameText.get("1.0", 'end-1c'),
                 'preamble': preamble_content,
                 'root state': data_yaml}}, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    # 在成功导出后显示弹窗信息
    messagebox.showinfo('成功', '文件已成功导出')

# 在界面上添加"导出为YAML"的按钮
tk.Button(root, text="导出", command=export_to_yaml).grid(row=11, column=0, padx=10, pady=5)

root.mainloop()