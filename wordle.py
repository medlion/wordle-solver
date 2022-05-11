number_of_letters = 5
#words = []
#tried_words = []

def filter_green(letter, position, word_list):
    for word in word_list:
        if word[position] != letter:
            word_list.remove(word)
    return word_list
            
def filter_yellow(letter, position, word_list):
    for word in word_list:
        if (word[position]) == letter:
            word_list.remove(word)
        if (letter not in word):
            word_list.remove(word)
    return word_list

def filter_black(letter, amount, word_list):
    for word in word_list:
        if word.count(letter) >= amount:
            word_list.remove(word)
    return word_list
            
def filter_words(word, pattern, word_list):
    if len(word) != 5:
        print('word more than 5 letters')
        return word_list
    if len(pattern) != 5:
        print('pattern more than 5 letters')
        return word_list
    listlen = 0
    while listlen != len(word_list): # array.remove is buggy
        listlen = len(word_list)
        for position in range(5):
            if pattern[position] == 'g':
                word_list = filter_green(word[position], position, word_list)
            elif pattern[position] == 'y':
                word_list = filter_yellow(word[position], position, word_list)
            elif pattern[position] == 'b':
                count = 1
                for pos in range(5):
                    if word[pos] == word[position] and pattern[pos] in "gy":
                        count = count + 1
                word_list = filter_black(word[position], count, word_list)
            else:
                print('pattern character not g, y or b')
                return word_list
    return word_list

def build_word_list():
    word_list = []
    file = open('wordlist', 'r')
    for line in file:
        word_list.append(line[:5])
    file.close()
    return word_list
    
def find_most_likely_word(word_list, full_word_list):
    if len(word_list) <= 2:
        return word_list[0] 
    dictionary = build_dictionary(word_list)
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
    
    word = word_list[0]
    word_score = 0
    for test_word in full_word_list:
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
    #print(word_score)
    return word
    
           
   #print (dictionary())
   #return words[0]

def build_dictionary(word_list):
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

original_words = []

def calculate_strategy_average():
    guess_count = 0
    word_count = 0
    for word in build_word_list():
        word_list = build_word_list()
        full_word_list = build_word_list()
        print("Actual Word : " + word)
        word_count = word_count + 1
        guesses = 0
        pattern = ''
        while pattern != 'ggggg':
            word_to_test = find_most_likely_word(word_list, full_word_list)
            print("Word to test : " + word_to_test)
            full_word_list.remove(word_to_test)
            guesses = guesses + 1
            pattern = get_pattern(word_to_test, word)
            word_list = filter_words(word_to_test, pattern, word_list)
            #print("Pattern : " + pattern)
        print("Guesses to get it " + str(guesses))
        guess_count = guess_count + guesses
    print("Words : " + str(word_count))
    print("Guesses : " + str(guess_count))
    print("Average guesses : " + str(guess_count/word_count))
    
def play_game():
    word_list = build_word_list()
    full_word_list = word_list.copy()
    while True:
        best_word = find_most_likely_word(word_list, full_word_list)
        print("Best word choice : " + best_word)
        word = input("Chosen Word (Blank for best choice) : ")
        if word == "exit":
            break
        elif word == "":
            word = best_word
        if (word in full_word_list):
            full_word_list.remove(word)
        else:
            print("given word not in word list")
            continue
        pattern = input("Pattern (gyb) : ")
        word_list = filter_words(word, pattern)
        
def find_first_word():
    word_list = build_word_list()
    print(find_most_likely_word(word_list, word_list))
            


calculate_strategy_average()    
#play_game()
#find_first_word()
    
#print(words)