import spacy
import inflect
import argparse, csv
from  Crypto import *
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
import secrets
import base64
from pattern.en import conjugate, article
import getpass
import random
from random import shuffle
p = inflect.engine()
lengthW = 4
nseed = 31*lengthW + lengthW
secretsGenerator = secrets.SystemRandom()

#OPEN DICTIONARY
with open('dict/ADJ.csv', 'r') as f:
    reader = csv.reader(f)
    ADJ = []
    for row in reader:
        ADJ.append(row[0])
with open('dict/ADP.csv', 'r') as f:
    reader = csv.reader(f)
    ADP = []
    for row in reader:
        ADP.append(row[0])
with open('dict/ADV.csv', 'r') as f:
    reader = csv.reader(f)
    ADV = []
    for row in reader:
        ADV.append(row[0])
with open('dict/CC.csv', 'r') as f:
    reader = csv.reader(f)
    CC = []
    for row in reader:
        CC.append(row[0])
with open('dict/DET_SING.csv', 'r') as f:
    reader = csv.reader(f)
    DET_SING = []
    for row in reader:
        DET_SING.append(row[0])
with open('dict/DET_PLUR.csv', 'r') as f:
    reader = csv.reader(f)
    DET_PLUR = []
    for row in reader:
        DET_PLUR.append(row[0])
with open('dict/DET_Q.csv', 'r') as f:
    reader = csv.reader(f)
    DET_Q = []
    for row in reader:
        DET_Q.append(row[0])
with open('dict/MD.csv', 'r') as f:
    reader = csv.reader(f)
    MD = []
    for row in reader:
        MD.append(row[0])
with open('dict/NOUN.csv', 'r') as f:
    reader = csv.reader(f)
    NOUN = []
    for row in reader:
        NOUN.append(row[0])
with open('dict/NOUN_U.csv', 'r') as f:
    reader = csv.reader(f)
    NOUN_U = []
    for row in reader:
        NOUN_U.append(row[0])
with open('dict/RP.csv', 'r') as f:
    reader = csv.reader(f)
    RP = []
    for row in reader:
        RP.append(row[0])
with open('dict/PDT.csv', 'r') as f:
    reader = csv.reader(f)
    PDT = []
    for row in reader:
        PDT.append(row[0])
with open('dict/PROPN.csv', 'r') as f:
    reader = csv.reader(f)
    PROPN = []
    for row in reader:
        PROPN.append(row[0])
with open('dict/PRP_S.csv', 'r') as f:
    reader = csv.reader(f)
    PRP_S = []
    for row in reader:
        PRP_S.append(row[0])
with open('dict/PRP_O.csv', 'r') as f:
    reader = csv.reader(f)
    PRP_O = []
    for row in reader:
        PRP_O.append(row[0])
with open('dict/PRP_POSS.csv', 'r') as f:
    reader = csv.reader(f)
    PRP_POSS = []
    for row in reader:
        PRP_POSS.append(row[0])
with open('dict/VERB.csv', 'r') as f:
    reader = csv.reader(f)
    VERB = []
    for row in reader:
        VERB.append(row[0])
with open('dict/POS.csv', 'r') as f:
    reader = csv.reader(f)
    POS = []
    for row in reader:
        POS.append(row[0])
with open('dict/STR.csv') as f:
    reader = csv.reader(f)
    STR=[]
    for row in reader:
        miniSRT = []
        for col in row:
            if col != "":
                miniSRT.append(eval(col))
        STR.append(miniSRT)

#Get random numner of n string
def pattern_stopiteration_workaround():
    try:
        print(lexeme('gave'))
    except:
        pass
def NdigitRandomNumber(n):
    i = 0
    number = ''
    while i < n:
        number += str(secretsGenerator.randint(0,9))
        i = i + 1
    return number

#Get index of lemma/text in related dictionary
def getIndex(doc, i):
    type = doc[i].tag_
    dep = doc[i].dep_
    lemma = doc[i].lemma_
    text = doc[i].text

    
    if type == 'VB' or type == 'VBD' or type == 'VBG' or type == 'VBN'or type == 'VBP' or type == 'VBZ':
        if dep != "auxpass" and dep != 'aux':
            return VERB.index(lemma)
        else:
            return NdigitRandomNumber(lengthW)
    elif type == 'NNP' or type == 'NNPS':
        return PROPN.index(text)
    elif type == 'JJ':
        if lemma == 'many' or lemma == 'much':
            doc[i].dep_ = 'det'
            doc[i].tag_ = 'DT'
            doc[i].lemma_ = 'many'
            return DET_PLUR.index(lemma)
        elif lemma in DET_Q:
            doc[i].dep_ = 'det'
            doc[i].tag_ = 'DTQ'
            return DET_Q.index(lemma)
        return ADJ.index(lemma)
    elif type == 'NN' or type == 'NNS':
        if lemma in NOUN_U:
            doc[i].tag_ = 'NNU'
            return NOUN_U.index(lemma)
        return NOUN.index(lemma)
    elif type == 'MD':
        return MD.index(lemma)
    elif type == 'CC':
        return CC.index(lemma)
    elif type == 'PDT':
        return PDT.index(lemma)
    elif type == 'PRP$':
        return PRP_POSS.index(text.lower())
    elif type == 'PRP':
        if dep == 'nsubj' or dep == 'nsubjpass':
            return PRP_S.index(text.lower())
        else:
            return PRP_O.index(text.lower())
    elif type == 'RP':
        return RP.index(lemma)
    elif type == 'RB':
        print(dep)
        if dep != 'not' and dep != 'neg':
            return ADV.index(lemma)
        else:
            return NdigitRandomNumber(lengthW)
    elif type == 'IN':
        if dep == 'agent':
            return NdigitRandomNumber(lengthW)
        return ADP.index(lemma)
    elif type == 'DT':
        if lemma in DET_PLUR:
            doc[i].tag_ = 'DTP'
            return DET_PLUR.index(lemma)
        elif lemma in DET_SING:
            if lemma == 'an':
                lemma = 'a'
            doc[i].tag_ = 'DTS'
            return DET_SING.index(lemma)
        return DET.index(lemma)
    elif type == 'TO':
        return NdigitRandomNumber(lengthW)
    elif type == 'POS':
        return POS.index(lemma)
    else:
        return '0000'

def getLenDictionary(tuple):
        
    pos_tag = tuple[1]
    dep = tuple[2]

    if pos_tag == 'VB' or pos_tag == 'VBD' or pos_tag == 'VBG' or pos_tag == 'VBN'or pos_tag == 'VBP' or pos_tag == 'VBZ':
        if dep != "auxpass" and dep != 'aux':
                return len(VERB)
        else:
            return NdigitRandomNumber(2)
    elif pos_tag == 'NNP' or type == 'NNPS':
        return len(PROPN)
    elif pos_tag == 'JJ':
        return len(ADJ)
    elif pos_tag == 'NN' or pos_tag == 'NNS':
        return len(NOUN)
    elif pos_tag == 'NNU':
        return len(NOUN_U)
    elif pos_tag == 'MD':
        return len(MD)
    elif pos_tag == 'CC':
        return len(CC)
    elif pos_tag == 'PDT':
        return len(PDT)
    elif pos_tag == 'PRP$':
        return len(PRP_POSS)
    elif pos_tag == 'PRP':
        if dep == 'nsubj' or dep == 'nsubjpass':
            return len(PRP_S)
        else:
            return len(PRP_O)
    elif pos_tag == 'RP':
        return len(RP)
    elif pos_tag == 'RB':
        if dep != 'not' and dep != 'neg':
            return len(ADV)
        else:
            return NdigitRandomNumber(lengthW)
    elif pos_tag == 'IN':
        if dep == 'agent':
            return NdigitRandomNumber(lengthW)
        return len(ADP)
    elif pos_tag == 'DTS':
        return len(DET_SING)
    elif pos_tag == 'DTP':
        return len(DET_PLUR)
    elif pos_tag == 'DTQ':
        return len(DET_Q)
    elif pos_tag == 'TO':
        return NdigitRandomNumber(lengthW)
    elif pos_tag == 'POS':
        return len(POS);
    else:
        return NdigitRandomNumber(lengthW)

def getLemmaByIndex(index, list):
    print(int(index)%len(list))
    return list[int(index)%len(list)]

def getLemma(index, type, dep, parentType):
    if type == 'VB' or type == 'VBD' or type == 'VBG' or type == 'VBN'or type == 'VBP' or type == 'VBZ':
        if dep != "auxpass":
            if dep != 'aux':
                return getLemmaByIndex(index, VERB)
            elif dep == 'aux':
                if parentType == 'VBG':
                    return 'be'
                elif parentType == 'VBN':
                    return 'have'
                else:
                    return 'do'
        else:
            return "be"
    elif type == 'NNP' or type == 'NNPS':
        return getLemmaByIndex(index, PROPN)
    elif type == 'NNU':
        return getLemmaByIndex(index, NOUN_U)
    elif type == 'JJ':
        return getLemmaByIndex(index, ADJ)
    elif type == 'NN' or type == 'NNS':
        return getLemmaByIndex(index, NOUN)
    elif type == 'MD':
        return getLemmaByIndex(index, MD)
    elif type == 'CC':
        return getLemmaByIndex(index, CC)
    elif type == 'PDT':
        return getLemmaByIndex(index, PDT)
    elif type == 'PRP':
        if dep == 'nsubj' or dep == 'nsubjpass':
            return getLemmaByIndex(index, PRP_S)
        else:
            return getLemmaByIndex(index, PRP_O)
        return getLemmaByIndex(index, PRP)
    elif type == 'PRP$':
        return getLemmaByIndex(index, PRP_POSS)
    elif type == 'RP':
        return getLemmaByIndex(index, RP)
    elif type == 'RB':
        if dep != 'not' and dep != 'neg':
            return getLemmaByIndex(index, ADV)
        else:
            return 'not'
    elif type == 'IN':
        if dep == 'agent':
            return 'by'
        return getLemmaByIndex(index, ADP)
    elif type == 'DTS':
        return getLemmaByIndex(index, DET_SING)
    elif type == 'DTP':
        return getLemmaByIndex(index, DET_PLUR)
    elif type == 'DTQ':
        return getLemmaByIndex(index, DET_Q)
    elif type == 'TO':
        return "to"
    elif type == 'POS':
        return getLemmaByIndex(index, POS)
    else:
        return ''
        
def beConjPast(struct, list_lemma):
    nsubj_pos = 0
    i = 0
    for tupla in struct:
        if tupla[1] == 'nsubj' or tupla[1] == 'nsubjpass':
            nsubj_pos = i
            break
        i = i + 1
    typeSubj = struct[nsubj_pos][1]
    lemmaSubj = list_lemma[nsubj_pos]
    verb = ''
    
    if (typeSubj == 'PRP' and (lemmaSubj == 'i' or lemmaSubj == 'he' or lemmaSubj == 'it' or lemmaSubj == 'she')) or (typeSubj == 'NNP' or typeSubj == 'NN'):
        try:
            verb = en.conjugate('be', '1sgp') 
        except StopIteration:
            return
    else:
        try:
            verb = en.conjugate('be', 'p')
        except StopIteration:
            return
    return verb

def getWord(lemma, struct, pos, list_lemma):
    word = lemma
    token = struct[pos]
    index_token = struct[pos][0]
    tag_token = struct[pos][1]
    dep_token = struct[pos][2]
    index_parent_token = struct[pos][3]
    type_parent_token = struct[pos][4]
    
    if tag_token == 'NNPS' or tag_token == 'NNS':
        word = p.plural_noun(lemma)
    elif tag_token == 'JJ' and (type_parent_token == 'NNPS' or type_parent_token == 'NNS'):
        word = p.plural_adj(lemma)
    elif tag_token == 'DTS' and lemma == 'a':
        word = article(list_lemma[index_parent_token])
    elif tag_token == 'DTP' and lemma == 'many':
        if type_parent_token == 'NNU':
            word = 'much'
    elif tag_token == 'VBG':
        word = conjugate(lemma, 'part')
    elif tag_token == 'VBN':
        word = conjugate(lemma, 'ppart')
    elif tag_token == 'VB':
        word = lemma
    elif tag_token == 'VBD':
        try:
            if lemma == 'be':
                try:
                    word = beConjPast(struct, list_lemma)
                except StopIteration:
                    return
            else:
                try:
                    word = conjugate(lemma, 'p')
                except StopIteration:
                    return
        except StopIteration:
            return
    elif tag_token == 'VBP':
        try:
            word = conjugate(lemma, '1sg')
        except StopIteration:
            return
    elif tag_token == 'VBZ':
        try:
            word = conjugate(lemma, '3sg')
        except StopIteration:
            return word
    
    return word

        
def getIndexStr(list):
    if list not in STR:
        STR.append(list)
        with open("dict/STR.csv",'a', newline='') as f:
            wr = csv.writer(f)
            wr.writerow(list)
    return str(STR.index(list)).zfill(lengthW)
        
        
def divideNParts(string, n):
    rest = len(string)%n
    length_part = int(len(string)/n)
    parts = []
    
    i = 0
    j = 1
    start = 0
    stop = length_part
    
    while i < n:
        i = i + 1
        if rest <= 0:
            j = 0
        stop = stop + j
        parts.append(string[start:stop])
        start = stop
        stop += length_part
        rest =  rest - 1
    
    return parts
        

def generateSeedWords(number, idstruct, list, nelement, list_struct):
    
    numberword = number[lengthW:]
    numberstruct = number[0:lengthW]
    
    intStruct = int(idstruct)
    intRandStruct = int(numberstruct)
    structDicLen = len(STR)
    restStruct = intRandStruct%structDicLen
    if restStruct != intStruct:
            dif = intStruct - restStruct
            numberstruct = str(intRandStruct+dif)
            numberstruct = numberstruct.zfill(lengthW)
            if len(numberstruct) > lengthW:
                numberstruct = str(int(numberstruct) - structDicLen)
            numberstruct = numberstruct.zfill(lengthW)
    
    rest = len(numberword)%nelement
    length_part = int(len(numberword)/nelement)
    parts = divideNParts(numberword, nelement)
    
    i = 0
    
    for word in list:
        length_word_part = len(parts[i])
        intWord = int(word)
        intPart = int(parts[i])
        wordDicLen = int(getLenDictionary(list_struct[i]))
        restWord = intPart%wordDicLen
        if restWord != intWord:
            dif = intWord - restWord
            parts[i] = str(intPart+dif)
            parts[i] = parts[i].zfill(length_word_part)
            if len(parts[i]) > length_word_part:
                parts[i] = str(int(parts[i]) - wordDicLen)
            parts[i] = parts[i].zfill(length_word_part)
        i = i + 1
    
    numberwords = ''.join(parts)
    
    return (numberstruct + numberwords)

leet_dict = {
    'a': ['a', 'A', '@'],
    'A': ['A', 'a', '4', '^'],
    'b': ['b', 'B', '6'],
    'B': ['B', 'b', '8'],
    'c': ['c', 'C', '(', '[', '{'],
    'C': ['C', 'c', '(', '[', '{'],
    'd': ['d', 'D'],
    'D': ['D', 'd'],
    'e': ['e', 'E', '3', '€'],
    'E': ['E', 'e', '3', '€'],
    'f': ['f', 'F', 'ph'],
    'F': ['F', 'f', 'PH'],
    'g': ['g', 'G', '9'],
    'G': ['G', 'g', '6'],
    'h': ['h', 'H'],
    'H': ['H', 'h', '4'],
    'i': ['i', 'I', '!', '1', '|'],
    'I': ['I', 'i', '!', '1', '|'],
    'j': ['j', 'J'],
    'J': ['J', 'j'],
    'k': ['k', 'K'],
    'K': ['K', 'k'],
    'l': ['l', 'L', '1', '|', '!'],
    'L': ['L', 'l'],
    'm': ['m', 'M'],
    'M': ['M', 'm'],
    'n': ['n', 'N'],
    'N': ['N', 'n'],
    'o': ['o', 'O', '0'],
    'O': ['O', 'o', '0'],
    'p': ['p', 'P'],
    'P': ['P', 'p'],
    'q': ['q', 'Q'],
    'Q': ['Q', 'q'],
    'r': ['r', 'R'],
    'R': ['R', 'r'],
    's': ['s', 'S', '$', '5'],
    'S': ['S', 's', '$', '5'],
    't': ['t', 'T', '7'],
    'T': ['T', 't', '7'],
    'u': ['u', 'U'],
    'U': ['U', 'u'],
    'v': ['v', 'V'],
    'V': ['V', 'v'],
    'w': ['w', 'W', 'vv'],
    'W': ['W', 'w', 'VV'],
    'x': ['x', 'X'],
    'X': ['X', 'x'],
    'y': ['y', 'Y'],
    'Y': ['Y', 'y'],
    'z': ['z', 'Z', '2'],
    'Z': ['Z', 'z', '2']
}

#將password進行置換，產生sweetword
def permute(dict_word):
    if len(dict_word) > 0:
        current_letter = dict_word[0]
        rest_of_word = dict_word[1:]

        if current_letter in leet_dict:
            substitutions = leet_dict[current_letter] + [current_letter]
        else:
            substitutions = [current_letter]

        if len(rest_of_word) > 0:
            perms = [s + p for s in substitutions for p in permute(rest_of_word)]
        else:
            perms = substitutions
        return perms

#打亂每一個honeyword的字元順序
def shuffle_str(s):
    str_list = list(s)
    shuffle(str_list)
    return ''.join(str_list)

def encrypt(text, password):
    k = 10
    generated_sweetwords = [sweetword for sweetword in permute(password)]

    sweetwords = [{ 'Number of possible sweetwords': i + 1, 'Sweetword': sweetword} for i, sweetword in enumerate(random.sample(generated_sweetwords, k))]

    for i in range(k):
        print(sweetwords[i])
    print({'Number of possible sweetwords' : k + 1, 'Sweetword': password})
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    
    lista_struttura = []
    lista_parole = []
    number_element = 0
    i = 0
    
    randomnumber = NdigitRandomNumber(nseed)
    
    for token in doc:
        number_element = number_element + 1
        index = getIndex(doc, i)
        lista_parole.append(index)
        lista_struttura.append((token.i, token.tag_, token.dep_, token.head.i, token.head.tag_))
        i = i + 1
    
    idstruttura = getIndexStr(lista_struttura)
    randomnumber = generateSeedWords(randomnumber, idstruttura, lista_parole, number_element, lista_struttura)

    seed = randomnumber
    print("The original seed is:")
    print(seed)
    salt = secrets.token_bytes(8)
    key = PBKDF2(password, salt,32,1000)
    
    ENC=AES.new(key, AES.MODE_ECB)    
    seedAES = []
    
    for digit in seed:
        seedAES.append (int(digit))
    
    seedAES=list(map(lambda x: x+10*secrets.randbelow(24),seedAES))
        
    # print("the secret mod seed is")
    # print(seedAES);
    
    arr = bytes(seedAES)
    outText=base64.b64encode(ENC.encrypt(arr)).decode()
    print("The ciphertext is:")
    print(base64.b64encode(salt).decode() + outText)
    
    
def decrypt(publicSeed, password):
    
    salt = publicSeed[0:12]
    pseed = publicSeed[12:]
    
    salt = base64.b64decode(salt.encode())
    key = PBKDF2(password, salt,32,1000)
    
    ENC = AES.new(key, AES.MODE_ECB)
    decoded = ENC.decrypt(base64.b64decode(pseed.encode()))
    arrayseed = list(map(lambda x: x%10,decoded))
    seed = ''.join(map(str, arrayseed))
    
    print("The original seed is:")
    print(seed)
    
    idstruttura = seed[0:lengthW]
    idstruttura = str(int(idstruttura)%len(STR))
    struct = STR[int(idstruttura)]
    
    seedparole = seed[lengthW:]
    parts = divideNParts(seedparole, len(struct))
    lista_lemma = []
    lista_parole = []
    
    i = 0
    for indexword in parts:
        lemma = getLemma(indexword, struct[i][1], struct[i][2], struct[i][4])
        lista_lemma.append(lemma)
        i = i + 1
    
    i = 0
    lista_parole = lista_lemma
    for lemma in lista_lemma:
        word = getWord(lemma, struct, i, lista_lemma)
        lista_parole[i] = word
        i = i + 1
    
    frase = ' '.join(lista_parole)
    frase= frase[:1].upper() + frase[1:]
    
    print(frase)


if __name__ == '__main__':
    pattern_stopiteration_workaround()
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--encrypt", nargs=2,
                        type=str,
                        help="encrypt text")
    parser.add_argument("-d", "--decrypt",
                        nargs=2, type=str,
                        help="decrypt code")
    args = parser.parse_args()
    
    if args.encrypt:
        encrypt(args.encrypt[0], args.encrypt[1])
    elif args.decrypt:
        decrypt(args.decrypt[0], args.decrypt[1])

