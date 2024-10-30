import os
import math
import tkinter as tk
from tkinter import filedialog

def parse_coordinates(line):
    parts = line.split()
    if len(parts) < 3:
        return None
    try:
        x = float(parts[1][1:])
        y = float(parts[2][1:])
        return x, y
    except ValueError:
        return None

def calculate_distance(coord1, coord2):
    return math.sqrt((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2)

def collect_blocks_from_file(input_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    blocks = []
    block = []
    start_coord = None
    end_coord = None
    inside_block = False

    for i, line in enumerate(lines):
        if 'G1 Z1' in line and not inside_block:
            start_coord = parse_coordinates(lines[i - 1])
            block.append(lines[i - 1])
            block.append(line)
            inside_block = True
        elif 'G1 Z30' in line and inside_block:
            end_coord = parse_coordinates(lines[i - 1])
            block.append(lines[i - 1])
            block.append(line)
            blocks.append((block, start_coord, end_coord))
            block = []
            inside_block = False
        elif inside_block:
            block.append(line)

    print(f"Собрано {len(blocks)} блоков")
    return blocks

def arrange_blocks(blocks):
    arranged_blocks = []
    if not blocks:
        return arranged_blocks

    current_block = blocks.pop(0)
    arranged_blocks.append(current_block)
    
    while blocks:
        last_end_coord = current_block[2]
        next_block = min(blocks, key=lambda b: calculate_distance(last_end_coord, b[1]))
        blocks.remove(next_block)
        arranged_blocks.append(next_block)
        current_block = next_block

    print(f"Упорядочено {len(arranged_blocks)} блоков")
    return arranged_blocks

def save_blocks(blocks, output_file):
    with open(output_file, 'w') as out_file:
        for block in blocks:
            for line in block[0]:
                out_file.write(line)
            out_file.write('\n\n')
    print(f'Блоки сохранены в оптимальном порядке в файл {output_file}.')

def remove_consecutive_duplicates_and_empty_lines(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    unique_lines = []
    previous_line = None
    for line in lines:
        if line.strip() and line != previous_line:
            unique_lines.append(line)
        previous_line = line

    with open(file_path, 'w') as file:
        file.writelines(unique_lines)

def select_input_file():
    input_file = filedialog.askopenfilename(title="Select Input File")
    input_entry.delete(0, tk.END)
    input_entry.insert(0, input_file)

def select_output_file():
    output_file = filedialog.asksaveasfilename(title="Select Output File")
    output_entry.delete(0, tk.END)
    output_entry.insert(0, output_file)

def process_files():
    input_file = input_entry.get()
    output_file = output_entry.get()
    if input_file and output_file:
        blocks = collect_blocks_from_file(input_file)
        arranged_blocks = arrange_blocks(blocks)
        save_blocks(arranged_blocks, output_file)
        remove_consecutive_duplicates_and_empty_lines(output_file)
        result_label.config(text="Processing completed successfully!")
    else:
        result_label.config(text="Please select both input and output files.")

# Создание основного окна
root = tk.Tk()
root.title("Block Arranger")

# Поле для ввода имени входного файла
tk.Label(root, text="Input File:").grid(row=0, column=0, padx=10, pady=10)
input_entry = tk.Entry(root, width=50)
input_entry.grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=select_input_file).grid(row=0, column=2, padx=10, pady=10)

# Поле для ввода имени выходного файла
tk.Label(root, text="Output File:").grid(row=1, column=0, padx=10, pady=10)
output_entry = tk.Entry(root, width=50)
output_entry.grid(row=1, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=select_output_file).grid(row=1, column=2, padx=10, pady=10)

# Кнопка для запуска обработки файлов
tk.Button(root, text="Process", command=process_files).grid(row=2, column=1, padx=10, pady=10)

# Метка для отображения результата
result_label = tk.Label(root, text="")
result_label.grid(row=3, column=1, padx=10, pady=10)

# Запуск основного цикла обработки событий
root.mainloop()
