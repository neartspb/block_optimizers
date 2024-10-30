import tkinter as tk
from tkinter import filedialog, messagebox
import os
import random

def split_ngc_file(input_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()
    block = []
    blocks = []
    block_number = 1
    for line in lines:
        block.append(line)
        if 'G1 Z30' in line:
            blocks.append(block)
            block = []
            block_number += 1
    print(f'Разделение завершено. Создано {block_number - 1} блоков.')
    return blocks

def shuffle_and_save_blocks(blocks, output_file):
    random.shuffle(blocks)
    with open(output_file, 'w') as out_file:
        for block in blocks:
            out_file.writelines(block)
            out_file.write('\n')  # Добавляем перенос строки после каждого блока
    print(f'Блоки сохранены в случайном порядке в файл {output_file}.')

def process_file(input_file, output_file):
    blocks = split_ngc_file(input_file)
    shuffle_and_save_blocks(blocks, output_file)
    messagebox.showinfo("Успех", "Обработка файла завершена.")

def choose_files():
    input_file = filedialog.askopenfilename(title="Выберите входящий файл", filetypes=[("NGC files", "*.ngc")])
    if input_file:
        output_file = filedialog.asksaveasfilename(title="Выберите файл для сохранения", defaultextension=".ngc", filetypes=[("NGC files", "*.ngc")])
        if output_file:
            process_file(input_file, output_file)

# Создание графического интерфейса
root = tk.Tk()
root.title("NGC File Processor")
frame = tk.Frame(root, padx=10, pady=10)
frame.pack(padx=10, pady=10)
button = tk.Button(frame, text="Выбрать файлы и обработать", command=choose_files)
button.pack()
root.mainloop()
