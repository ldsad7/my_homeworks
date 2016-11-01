a = input('Введите слово первого склонения\n')
while a != '' :
    if a[-1] == 'а' or a[-1] == 'я' :
        print('NOM, sg')
    elif a[-1] == 'и' and a[-2] == 'м':
        print('INS, pl')
    elif a[-1] == 'и' or a[-1] == 'ы' :
        print('GEN, sg or NOM, pl or ACC, pl')
    elif a[-1] == 'е' :
        print('DAT, sg or LOC, sg')
    elif a[-1] == 'й' and a[-2] == 'ё' or a[-1] == 'й' and a[-2] == 'е' or a[-1] == 'й' and a[-2] == 'о' :
        print('INS, sg')
    elif a[-1] == 'ю' or a[-1] == 'у' :
        print('ACC, sg')
    elif a[-1] == 'м' and a[-2] == 'я' or a[-1] == 'м' and a[-2] == 'а' :
        print('DAT, pl')
    elif a[-1] == 'и' and a[-2] == 'м':
        print('INS, pl')
    elif a[-1] == 'х' and a[-2] == 'я' or a[-1] == 'х' and a[-2] == 'а' :
        print('LOC, pl')
    else :
        print('GEN, pl')
    a = input('Введите новое слово первого склонения\n')
