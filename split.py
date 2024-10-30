import os

def split_ngc_file(input_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    block = []
    block_number = 1

    for line in lines:
        block.append(line)
        if 'G1 Z30' in line:
            output_file = f'block_{block_number}.ngc'
            with open(output_file, 'w') as out_file:
                out_file.writelines(block)
            block = []
            block_number += 1

    print(f'Разделение завершено. Создано {block_number - 1} блоков.')

# Укажите имя файла .ngc, который находится в той же директории, что и скрипт
input_file = 'gcode_newuzhas3_inv_pen0_100.ngc'
split_ngc_file(input_file)
