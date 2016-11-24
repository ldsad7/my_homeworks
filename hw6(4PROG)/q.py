# Здесь я дополнительно рассматриваю такой случай, когда человек мог ввести '   asd  '(и считаю это словом 'asd') или
# 'asd   '(также считаю словом 'asd') или '  asd asd  ' и прочее
# решение задачи без использования встроенной функции strip

fl = 0
while fl != 1 :
    word = input('Please input one word:\n')
    ind = word.find(' ')
    if ind == -1 :
        fl = 1
    else :
        if ind == 0 :
            word = word[1:]
            flag = word.find(' ')
            while flag == 0 :
                word = word[1:]
                flag = word.find(' ')
            if flag > 0 :
                subword = word[flag:]
                ind = subword.find(' ')
                while ind == 0 :
                    subword = subword[1:]
                    ind = subword.find(' ')
                if subword != '' :
                    print('There is more than one word. Please try again!')
                else :
                    word = word[:flag]
                    fl = 1
            else :
                if word != '' :
                    fl = 1
                else :
                    print("You didn't type any word! Please try again!")
        else :
            subword = word[ind:]
            flag = subword.find(' ')
            while flag == 0 :
                subword = subword[1:]
                flag = subword.find(' ')
            if subword != '' :
                print('There is more than one word. Please try again!')
            else :
                word = word[:ind]
                fl = 1
for i in range(len(word)) :
    print(word[i:])
    
# решение задачи с использованием встроенной функции strip

fl = 0
while fl != 1 :
    word = input('Please input one word:\n')
    word = word.strip()
    ind = word.find(' ')
    if ind == -1 :
        if word != '' :
            fl = 1
        else :
            print("You didn't type any word! Please try again")
    else :
        print('There is more than one word. Please try again!')
for i in range(len(word)) :
    print(word[i:])
