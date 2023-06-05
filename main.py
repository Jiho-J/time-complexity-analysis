import random
import tkinter as tk
from tkinter import ttk

import numpy as np
import sys

import detect
import funcs

sys.setrecursionlimit(10 ** 7)
operate_count = 0


def analysis_code():
    global operate_count
    modified_code = funcs.modify_code(code_text.get("1.0", tk.END))

    print(modified_code)

    try:
        exec(modified_code, globals())

        selected_type = argument_type.get()

        x = []
        y = []

        if selected_type == "숫자":
            max_value = int(value_max_entry.get())
            min_value = int(value_min_entry.get())
            step = int(value_step_entry.get())

            for i in range(min_value, max_value + 1, step):
                operate_count = 0
                result = exec('func(i)')
                x.append(i)
                y.append(operate_count)

        elif selected_type == "배열":
            max_size = int(size_max_entry.get())
            min_size = int(size_min_entry.get())
            step_size = int(size_step_entry.get())
            test_count = int(test_count_entry.get())

            for i in range(min_size, max_size, step_size):
                operate_count = 0
                for n in range(test_count):
                    ran_list = [random.random() * 1000 for _ in range(i)]
                    exec("func(ran_list)")
                x.append(i)
                y.append(operate_count / test_count)

        detect.detect_trend(np.array(x), np.array(y))
        display_error_message(False, "")
    except Exception as ex:
        display_error_message(True, str(ex))


window = tk.Tk()
window.title("시간 복잡도 분석")

# Code Input Frame
code_frame = ttk.Frame(window)
code_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

code_label = ttk.Label(code_frame, text="코드 입력:")
code_label.pack(anchor=tk.W)

code_text = tk.Text(code_frame, height=30)
code_text.pack(fill=tk.BOTH, expand=True)

# Arguments Frame
arguments_frame = ttk.Frame(window)
arguments_frame.pack(padx=20, pady=10)

argument_type = tk.StringVar()
argument_type.set("숫자")


def switch_arguments():
    selected_type = argument_type.get()

    if selected_type == "숫자":
        value_label.grid()
        value_max_label.grid()
        value_max_entry.grid()
        value_min_label.grid()
        value_min_entry.grid()
        value_step_label.grid()
        value_step_entry.grid()
        size_label.grid_remove()
        size_max_label.grid_remove()
        size_max_entry.grid_remove()
        size_min_label.grid_remove()
        size_min_entry.grid_remove()
        size_step_label.grid_remove()
        size_step_entry.grid_remove()
        test_count_label.grid_remove()
        test_count_entry.grid_remove()
    elif selected_type == "배열":
        value_label.grid_remove()
        value_max_label.grid_remove()
        value_max_entry.grid_remove()
        value_min_label.grid_remove()
        value_min_entry.grid_remove()
        value_step_label.grid_remove()
        value_step_entry.grid_remove()
        size_label.grid()
        size_max_label.grid()
        size_max_entry.grid()
        size_min_label.grid()
        size_min_entry.grid()
        size_step_label.grid()
        size_step_entry.grid()
        test_count_label.grid()
        test_count_entry.grid()


# Switch Label
switch_label = ttk.Label(arguments_frame, text="인수 유형:")
switch_label.grid(row=0, column=0, sticky=tk.W)

number_button = ttk.Radiobutton(arguments_frame, text="숫자", variable=argument_type, value="숫자",
                                command=switch_arguments)
number_button.grid(row=0, column=1, sticky=tk.W)

array_button = ttk.Radiobutton(arguments_frame, text="배열", variable=argument_type, value="배열", command=switch_arguments)
array_button.grid(row=0, column=2, sticky=tk.W)

# Number Arguments Settings
value_label = ttk.Label(arguments_frame, text="숫자 인수 설정:")
value_label.grid(row=1, column=0, sticky=tk.W)

value_max_label = ttk.Label(arguments_frame, text="최대 값:")
value_max_label.grid(row=2, column=0, sticky=tk.W)

value_max_entry = ttk.Entry(arguments_frame, validate="key",
                            validatecommand=(window.register(funcs.validate_number), '%P'))
value_max_entry.grid(row=2, column=1, sticky=tk.W)
value_max_entry.insert(0, "100")

value_min_label = ttk.Label(arguments_frame, text="최소 값:")
value_min_label.grid(row=3, column=0, sticky=tk.W)

value_min_entry = ttk.Entry(arguments_frame, validate="key",
                            validatecommand=(window.register(funcs.validate_number), '%P'))
value_min_entry.grid(row=3, column=1, sticky=tk.W)
value_min_entry.insert(0, "1")

value_step_label = ttk.Label(arguments_frame, text="간격:")
value_step_label.grid(row=4, column=0, sticky=tk.W)

value_step_entry = ttk.Entry(arguments_frame, validate="key",
                             validatecommand=(window.register(funcs.validate_number), '%P'))
value_step_entry.grid(row=4, column=1, sticky=tk.W)
value_step_entry.insert(0, "1")

# Array Arguments Settings
size_label = ttk.Label(arguments_frame, text="배열 크기 설정:")
size_label.grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
size_label.grid_remove()

size_max_label = ttk.Label(arguments_frame, text="최대 크기:")
size_max_label.grid(row=2, column=0, sticky=tk.W)
size_max_label.grid_remove()

size_max_entry = ttk.Entry(arguments_frame, validate="key",
                           validatecommand=(window.register(funcs.validate_number), '%P'))
size_max_entry.grid(row=2, column=1, sticky=tk.W)
size_max_entry.insert(0, "1000")
size_max_entry.grid_remove()

size_min_label = ttk.Label(arguments_frame, text="최소 크기:")
size_min_label.grid(row=3, column=0, sticky=tk.W)
size_min_label.grid_remove()

size_min_entry = ttk.Entry(arguments_frame, validate="key",
                           validatecommand=(window.register(funcs.validate_number), '%P'))
size_min_entry.grid(row=3, column=1, sticky=tk.W)
size_min_entry.insert(0, "10")
size_min_entry.grid_remove()

size_step_label = ttk.Label(arguments_frame, text="크기 간격:")
size_step_label.grid(row=4, column=0, sticky=tk.W)
size_step_label.grid_remove()

size_step_entry = ttk.Entry(arguments_frame, validate="key",
                            validatecommand=(window.register(funcs.validate_number), '%P'))
size_step_entry.grid(row=4, column=1, sticky=tk.W)
size_step_entry.insert(0, "10")
size_step_entry.grid_remove()

test_count_label = ttk.Label(arguments_frame, text="테스트 횟수:")
test_count_label.grid(row=8, column=0, sticky=tk.W)
test_count_label.grid_remove()

test_count_entry = ttk.Entry(arguments_frame, validate="key",
                             validatecommand=(window.register(funcs.validate_number), '%P'))
test_count_entry.grid(row=8, column=1, sticky=tk.W)
test_count_entry.insert(0, "10")
test_count_entry.grid_remove()

# Execute Button
execute_button = ttk.Button(window, text="실행", command=analysis_code)
execute_button.pack(pady=10)

# Error Message
error_message = tk.StringVar()
error_label = ttk.Label(window, textvariable=error_message, foreground="red")
error_label.pack()


def display_error_message(isShow, message):
    if isShow:
        error_message.set("오류: " + message)
    else:
        error_message.set("")


window.mainloop()
