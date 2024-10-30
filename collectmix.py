import os
import random
import tkinter as tk
from tkinter import filedialog

def collect_blocks(directory):
    blocks = []
    for filename in os.listdir(directory):
        if filename.endswith('.ngc'):
            with open(os.path.join(directory, filename), 'r') as file:
                block = file.readlines()
                blocks.append(block)
    return blocks

def shuffle_and_save_blocks(blocks, output_file):
    random.shuffle(blocks)
    with open(output_file, 'w') as out_file:
        for block in blocks:
            out_file.writelines(block)
            out_file.write('\n\n')  # Добавляем две новые строки между блоками для явного разделения
    print(f'Блоки сохранены в случайном порядке в файл {output_file}.')

def remove_empty_lines(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    with open(file_path, 'w') as file:
        for line in lines:
            if line.strip():  # Удаляем пустые строки
                file.write(line)

def select_directory():
    directory = filedialog.askdirectory(title="Select Directory")
    directory_entry.delete(0, tk.END)
    directory_entry.insert(0, directory)

def select_output_file():
    output_file = filedialog.asksaveasfilename(title="Select Output File")
    output_entry.delete(0, tk.END)
    output_entry.insert(0, output_file)

def process_files():
    directory = directory_entry.get()
    output_file = output_entry.get()
    if directory and output_file:
        blocks = collect_blocks(directory)
        shuffle_and_save_blocks(blocks, output_file)
        remove_empty_lines(output_file)
        result_label.config(text="Processing completed successfully!")
    else:
        result_label.config(text="Please select both directory and output file.")

# Создание основного окна
root = tk.Tk()
root.title("Block Shuffler")

# Поле для ввода директории
tk.Label(root, text="Directory:").grid(row=0, column=0, padx=10, pady=10)
directory_entry = tk.Entry(root, width=50)
directory_entry.grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=select_directory).grid(row=0, column=2, padx=10, pady=10)

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
