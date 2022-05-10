def filter_green(letter, position):
    for word in words:
        if word[position] != letter:
            words.remove(word)
            
def filter_yellow(letter, position):
    for word in words:
        if (word[position]) == letter:
            words.remove(word)
        if (letter not in word):
            words.remove(word)

def filter_black(letter, amount = 1):
    for word in words:
        if word.count(letter) >= amount:
            words.remove(word)
            
def filter_words(word, pattern):
    if len(word) != 5:
        print('word more than 5 letters')
        return
    if len(pattern) != 5:
        print('pattern more than 5 letters')
        return
    listlen = 0
    while listlen != len(words): # array.remove is buggy
        listlen = len(words)
        for position in range(5):
            if pattern[position] == 'g':
                filter_green(word[position], position)
            elif pattern[position] == 'y':
                filter_yellow(word[position], position)
            elif pattern[position] == 'b':
                count = 1
                for pos in range(5):
                    if word[pos] == word[position] and pattern[pos] in "gy":
                        count = count + 1
                filter_black(word[position], count)
            else:
                print('pattern character not g, y or b')
                return

def build_word_list():
    file = open('wordlist', 'r')
    for line in file:
        words.append(line[:5])
    file.close()
    
def find_most_likely_word():
    if len(words) <= 2:
        return words[0] 
    dictionary = build_dictionary()
    empties = []
    biggest = -1
    biggest_num = 0
    for pos in range(number_of_letters):
        letters = dictionary[pos]
        if len(letters) == 1:
            empties.append(pos)
            dictionary[pos] = {}
        if len(letters) > biggest_num:
            biggest = pos
            biggest_num = len(letters)
    for empty in empties:
        dictionary[empty] = dictionary[biggest]
    
    word = words[0]
    word_score = 0
    test_words = original_words.copy()
    while len(test_words) > 0:
        test_word = test_words[0]
        if test_word in tried_words:
            test_words.remove(test_word)
            continue
        score = 0
        for pos in range(number_of_letters):
            if test_word[pos] in dictionary[pos]:
                divi = 1
                for posi in range(pos):
                    if test_word[posi] == test_word[pos]:
                        divi = divi + 1
                score = score + dictionary[pos][test_word[pos]]/divi
        if score > word_score:
            word = test_word
            word_score = score
        test_words.remove(test_word)
    return word
    
           
   #print (dictionary())
   #return words[0]

def build_dictionary():
    word_list = words.copy()
    dictionary = []
    for pos in range(number_of_letters):
        dictionary.append({})
    #print(dictionary)
    for word in word_list:
        #print(word)
        for pos in range(number_of_letters):
            if word[pos] in dictionary[pos]:
                dictionary[pos][word[pos]] = dictionary[pos][word[pos]] + 1
            else:
                dictionary[pos][word[pos]] = 1  
    #print(dictionary)
    return dictionary

def get_pattern(test_word, actual_word):
    pattern = []
    for num  in range(number_of_letters):
        pattern.append('b')
    exclusion_list = []
    for pos in range(number_of_letters): #reen
        if test_word[pos] == actual_word[pos]:
            pattern[pos] = 'g'
            exclusion_list.append(pos)
        else:
            for posi in range(number_of_letters):
                if pattern[pos] not in "gy" and posi not in exclusion_list and test_word[pos] == actual_word[posi] and test_word[posi] != actual_word[posi]:
                        pattern[pos] = 'y'
                        exclusion_list.append(posi)
    return ''.join(pattern)

def calculate_strategy_average():
    guess_count = 0
    word_count = 0
    for word in original_words:
    #for word in ["studs"]:
        tried_words = []
        print("Actual Word : " + word)
        word_count = word_count + 1
        guesses = 0
        build_word_list()
        pattern = ''
        while pattern != 'ggggg':
            word_to_test = find_most_likely_word()
            tried_words.append(word_to_test)
            print("Word to test : " + word_to_test)
            guesses = guesses + 1
            pattern = get_pattern(word_to_test, word)
            filter_words(word_to_test, pattern)
            print("Pattern : " + pattern)
        print("Guesses to get it " + str(guesses))
        guess_count = guess_count + guesses
    print("Words : " + str(word_count))
    print("Guesses : " + str(guess_count))
    print("Average guesses : " + str(guess_count/word_count))
            
number_of_letters = 5
words = []
build_word_list()
original_words = words.copy()
tried_words = []

calculate_strategy_average()    

while True:
    break
    print("Best word choice : " + find_most_likely_word())
    word = input("Chosen Word : ")
    if word == "exit":
        break
    tried_words.append(word)
    pattern = input("Pattern (gyb) : ")
    filter_words(word, pattern)
    
#print(words)