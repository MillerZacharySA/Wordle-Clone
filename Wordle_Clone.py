from sty import fg, bg, rs
#from english_words import english_words_lower_alpha_set
from random import choice

#Get only five letter words
def load_words_hard():
    with open('words_alpha.txt') as word_file:
        valid_words = set(word_file.read().split())
        valid_words = [i for i in valid_words if len(i) == 5]
    
    return valid_words

def load_words_easy():
    with open('wordle-answers-alphabetical.txt') as word_file:
        valid_words = set(word_file.read().split())
        valid_words = [i for i in valid_words if len(i) == 5]
    
    return valid_words

all_words = load_words_hard()
difficulty = input("Press n for normal difficulty and h for hard difficulty!\n").strip().lower()
if difficulty == "n":
    fiveLetterWords = load_words_easy()
elif difficulty == "h":
    fiveLetterWords = all_words
else:
    print("You really wanna play but can't even press one letter properly?")
    print("Here's a letter for you\nL")
    exit()

word = choice(fiveLetterWords)
if word == "queue" or word == "alloo":
    word = choice(fiveLetterWords)

guesses = 0

wrong_letters = set({})

while guesses < 6:
    guess = input("Guess: ").strip().lower()
    if guess == "quit":
        exit()
    elif guess not in all_words:
        print(fg.red + "Word not found in word list, try again" + fg.rs)
        continue
   
    word_letters = {}
    isMultiLetter = False
    for letter in guess:
        if letter in word_letters.keys():
            word_letters[letter] += 1
            isMultiLetter = letter
        else:
            word_letters[letter] = 1 

    pos = {}

    for i in range(5):
        if isMultiLetter == False or isMultiLetter not in word or word.count(isMultiLetter) >= word_letters[isMultiLetter]:
            if guess[i] == word[i]:
                pos[i] = 2
            elif guess[i] in word:
                pos[i] = 1
            else:
                pos[i] = 0
                wrong_letters.add(guess[i])
        else:
            indices = []

            for j,letter in enumerate(guess):
                if letter == isMultiLetter:
                    indices.append(j)
                    
            correctPosThere = False
            for j in indices:
                if isMultiLetter == word[j]:
                    pos[j] = 2
                    correctPosThere = True
            else:
                if not correctPosThere:
                    pos[indices[0]] = 1
            
            for j in range(5):
                if j not in indices:
                    if guess[j] == word[j]:
                        pos[j] = 2
                    elif guess[j] in word:
                        pos[j] = 1
                    else:
                        pos[j] = 0
                        wrong_letters.add(guess[j])
            
    for i in range(5):
        if i not in pos.keys():
            pos[i] = 0
            wrong_letters.add(guess[i])
    
    colored_letters = []      
    for i in range(5):
        if pos[i] == 0:
            colored_letters.append(fg.black + bg.grey + guess[i] + bg.rs)
        elif pos[i] == 1:
            colored_letters.append(fg.black + bg.yellow + guess[i] + bg.rs)
        else:
            colored_letters.append(fg.black + bg.green + guess[i] + bg.rs)
    colored_letters.append(bg.black + fg.white +  bg.rs)
    

    print(''.join(colored_letters))

    print("\nNOT IN THE WORD")
    print("-"*((len(wrong_letters)*2)+1))
    print("|"+" ".join(sorted(list(wrong_letters)))+"|")
    print("-"*((len(wrong_letters)*2)+1))

    guesses += 1

    if guess == word:
        break

print(f"The word was {word}.")
