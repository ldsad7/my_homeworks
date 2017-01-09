import random

#выбор существительного
def noun() :
	f = open('nouns.txt', 'r', encoding = 'utf-8')
	nouns = f.read().split()
	f.close()
	return random.choice(nouns)

#выбор личного местоимения
def personal_pronoun() :
	f = open('personal_pronouns.txt', 'r', encoding = 'utf-8')
	pronouns = f.read().split()
	f.close()
	return random.choice(pronouns)

#выбор прилагательного, стоящего перед существительным
def adjective_before_noun() :
	f = open('adjectives_before_noun.txt', 'r', encoding = 'utf-8')
	adj = f.read().split()
	f.close()
	return random.choice(adj)

#выбор прилагательного, стоящего после существительного
def adjective_after_noun() :
	f = open('adjectives_after_noun.txt', 'r', encoding = 'utf-8')
	adj = f.read().split()
	f.close()
	return random.choice(adj)

#выбор наречия
def adverb() :
	f = open('adverbs.txt', 'r', encoding = 'utf-8')
	adverbs = f.read().split()
	f.close()
	return random.choice(adverbs)

#выбор усилителя наречия
def intensifier(adv):
    f = open('intensifiers.txt', 'r', encoding = 'utf-8')
    intensifiers = f.read().split()
    f.close()
    return random.choice(intensifiers) + ' ' + adv

#выбор переходного глагола
def transitive_infinitive() :
	f = open('transitive_infinitives.txt', 'r', encoding = 'utf-8')
	inf = f.read().split()
	f.close()
	return random.choice(inf)

#выбор непереходного глагола
def intransitive_infinitive() :
	f = open('intransitive_infinitives.txt', 'r', encoding = 'utf-8')
	inf = f.read().split()
	f.close()
	return random.choice(inf)	

#выбор обстоятельства времени 
def temporary_marker() :
	f = open('temporary_markers.txt', 'r', encoding = 'utf-8')
	temporary_markers = f.read().split()
	f.close()
	return random.choice(temporary_markers)

#выбор вопросительного слова из списка
def interrogative() :
	f = open('interrogatives.txt', 'r', encoding = 'utf-8')
	interrogatives = f.read().split()
	f.close()
	return random.choice(interrogatives)

#выбор числа из списка	
def number() :
	f = open('numbers.txt', 'r', encoding = 'utf-8')
	numbers = f.read().split()
	f.close()
	return random.choice(numbers)

#по роду существительного и предложенному пользователем числу
#прилагательное, существительное и артикль ставятся в нужную форму
def declension(noun, adjective, number) :
    f = open('declension_of_nouns.txt', 'r', encoding = 'utf-8')
    g = open('declension_of_adjectives.txt', 'r', encoding = 'utf-8')
    nouns = dict()
    adjectives = dict()
    for line in f.readlines() :
        s = line.split(' ', maxsplit = 1)		
        nouns[s[0]] = s[1].split()
    for line in g.readlines() :
        s = line.split(' ', maxsplit = 1)
        adjectives[s[0]] = s[1].split()
    f.close()
    g.close()
    if nouns[noun][0] == 'm' and number == 'sg' :
        return noun, adjective, random.choice(['le', 'un'])
    elif nouns[noun][0] == 'm' and number == 'pl' :
        return nouns[noun][1], adjectives[adjective][1], random.choice(['les', 'des'])
    elif nouns[noun][0] == 'f' and number == 'sg' :
        return noun, adjectives[adjective][0], random.choice(['la', 'une'])
    elif nouns[noun][0] == 'f' and number == 'pl' :
        return nouns[noun][1], adjectives[adjective][2], random.choice(['les', 'des'])

#сборка словосочетания
def collocation_bef(noun, adj_before_noun, article)	:
		return article + ' ' + adj_before_noun + ' ' + noun

#сборка словосочетания
def collocation_aft(noun, adj_after_noun, article)	:
		return article + ' ' + noun + ' ' + adj_after_noun

#определение по местоимению нужной формы глагола
def conjugation(pronoun, infinitive) :
	f = open('conjugations.txt', 'r', encoding = 'utf-8')
	verbs = dict()
	for line in f.readlines() :
		s = line.split(' ', maxsplit = 1)	
		verbs[s[0]] = s[1].split()
	f.close()
	if pronoun == 'je' :
		return verbs[infinitive][0]
	elif pronoun == 'tu' :
		return verbs[infinitive][1]
	elif pronoun == 'il' or pronoun == 'elle' :
		return verbs[infinitive][2]
	elif pronoun == 'nous' :
		return verbs[infinitive][3]
	elif pronoun == 'vous' :
		return verbs[infinitive][4]
	else :
		return verbs[infinitive][5]

#прямой порядок слов (SV) в утвердительном предложении
def affirmative_sequence(pronoun, verb) :
	if verb[0] in 'aàâeéèêiîoôuùûy' and pronoun == 'je' :
		return "j'" + verb
	else :
		return pronoun + ' ' + verb

#инверсия (VS) в вопросительном предложении
def interrogative_sequence(pronoun, verb) :
	if verb[len(verb) - 1] in 'aàâeéèêiîoôuùûy' and pronoun[0] in 'aàâeéèêiîoôuùûy' :
		return verb + '-t-' + pronoun
	else :
		return verb + '-' + pronoun

#сборка утвердительного предложения
def affirmative_sentence() :
    pron = personal_pronoun()
    noun1, adj1, art1 = declension(noun(), adjective_before_noun(), 'sg')
    noun2, adj2, art2 = declension(noun(), adjective_before_noun(), 'pl')
    return affirmative_sequence(pron, conjugation(pron, transitive_infinitive())) + ' ' + collocation_bef(noun1, adj1, art1) + ' et ' + number() + ' ' + adj2 + ' ' + noun2 + '.'

#сборка вопросительного предложения
def interrogative_sentence() :
    pron = personal_pronoun()
    return interrogative() + ' ' + interrogative_sequence(pron, conjugation(pron, intransitive_infinitive())) + ' ' + temporary_marker() + '?'

#сборка отрицательного предложения
def negative_sentence() :
    noun1, adj1, art1 = declension(noun(), adjective_before_noun(), 'pl')
    noun2, adj2, art2 = declension(noun(), adjective_before_noun(), 'sg')
    return collocation_aft(noun1, adj1, art1) + ' ne ' + conjugation('elle', transitive_infinitive()) + ' pas ' + collocation_bef(noun2, adj2, art2) + ' ' + temporary_marker() + ' ' + intensifier(adverb()) + '.'

#сборка условного предложения не удалась :(
def conditional_sentence() :
	return '[Здесь должно быть условное предложение, но я пока не представляю, как оно устроено во французском :( ].'

#сборка предложения повелительного наклонения
def imperative_sentence() :
	return 'ne ' + conjugation('vous', intransitive_infinitive()) + ' pas' +'!'
	
#вызов функции, формирующей предложение
def random_sentence(n) :
    if n == 1 :
        return affirmative_sentence()
    elif n == 2 :
        return interrogative_sentence()
    elif n == 3 :
        return negative_sentence()
    elif n == 4 :
        return conditional_sentence()
    else :
        return imperative_sentence()

		
#печать		
def text_print() :
    a = set('12345')
    for n in a :
        print(random_sentence(int(n)).capitalize(), end = ' ')


#основная программа			
text_print()
