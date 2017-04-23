# Вариант №6

import os

def walking():
    num = 0
    
    for root, dirs, files in os.walk('.'):
        d_files = {}
        flag = False
        
        for file in files:
            file_name, file_ext = os.path.splitext(file)
            if file_ext not in d_files:
                d_files[file_ext] = 1
            else:
                flag = True
                print(file)
                break
        
        if not flag:
            num += 1
        
    return num

def main():
    num = walking()
    print('Количество папок, в которых встречаются несколько файлов с одним\
и тем же расширением = {}.'.format(num))

if __name__ == '__main__':
    main()
