#Вариант №6
#Я считаю два раза файлы с одинковым названием, но разными расширениями, поскольку в задании не сказано посчитать "файлы с уникальными названиями".
import os

def files_and_folders():
    lst = os.listdir('.')

    files = []
    folders = []
    for f in lst:
        if os.path.isfile(f):
            files.append(f)
        else:
            folders.append(f)
            
    d_files = {}

    for f in files:
        f_name, f_ext = os.path.splitext(f)
        if f_name not in d_files:
            d_files[f_name] = 1
        else:
            d_files[f_name] += 1
    #В случае с папками ясно, что они не могут повторяться два раза с одним и тем же именем.

    return d_files, folders

def counting(d_files):
    num = 0
    punct_marks = '.!?:;,-()"\'<>' #Возможно, что я не учёл какого-то знака препинания. Я не включал знак '_', хотя, возможно, нужно было.
    # Также в Windows имя файла не может содержать некоторых символов, так что можно было бы их исключить, но я не стал этого делать.
    for key in d_files:
        fl = 0
        i = 0
        while fl != 1 and i < len(punct_marks): 
            if punct_marks[i] in key:
                fl = 1
            i += 1
        if fl == 1:
            num += d_files[key]
    return num

def output(num, d_files, d_folders):
    #Я так понял, что нужно вывести уникальные название файлов и папок, рассматриваемых совместно.
    print('Количество файлов, название которых содержит знаки препинания = ', num)
    print('Названия файлов и папок в данной папке следующие:') #сначала идут названия, являющиеся именами файлов (возможно, что в т.ч. и папок), а затем названия, являющиеся именами только папок .
    i = 1
    for key in d_files:
        print('%s) %s' % (str(i), str(key)))
        i += 1
    for key in d_folders:
        if key not in d_files: 
            print( '{}) {}'.format(str(i), str(key)))
        i += 1
    
def main():
    d_files, folders = files_and_folders()
    num = counting(d_files)
    output(num, d_files, folders)

if __name__ == '__main__':
    main()
