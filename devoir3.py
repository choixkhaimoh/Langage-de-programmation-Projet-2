import re
from collections import Counter     # une classe qui implémente un tableau associatif (map) avec des méthodes supplémentaires pour compter des choses (cés = objets à compter, valeurs = compte)

def words(text): return re.findall(r'\w+', text.lower())    # fonction qui identifie tous les mots en utilisant une expression régulière: l'expression régulière est '\w+' et identifie toutes les séquences d'au moins une lettre minuscule
                                                            # text.lower() met tout le texte en minuscules

WORDS = Counter(words(open('big.txt').read())) #compteur créé à partir des mots (fonction ci-dessus) lust dans le fichier 'big.txt'. Le tableau associatif WORDS contient environ 30K mots de vocabulaire (clés du tableau associatif) et y associe le compte de chaque mot dans le fichier big.txt (valeurs).

def P(word, N=sum(WORDS.values())): # N=valeur signifie que le deuxième paramètre est optionnel et la valeur sum(WORDS.values()) est la valeur par défaut
    "Probability of `word`."
    return WORDS[word] / N          # probabilité du mot approximée par sa fréquence dans le fichier big.txt (voir ci-dessus)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)   # + = concaténation de listes, set() élimine les doublons

def edits2(word):
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1)) # compréhension de liste entre parenthèses: générateur (voir ci-dessus)
                                                            # ici deux compréhensions imbriquées (équivalent à deux for imbriqués)
# la fonction correction récursive sans utiliser max, en utilisant un fonction d'aide avec accumulateurs (correction_helper)
def correction(word):
    return correction_helper(candidates(word), word, 0)

#fonction d'aide à la fonction récursive correction
def correction_helper(c, r, max):
    if len(c) == 0:
        return r
    else:
        word = c.pop()
        p = P(word)
        if p > max:
            max = p
            r = word
        return correction_helper(c, r, max)

# - focntion candidates avec des expressions conditionnelles de la forme "a if b else c". qui retourne des mots avec des erreurs potientelles
def candidates(word):
    return known([word]) if known([word]) else known(edits1(word)) if known(edits1(word)) else known(edits2(word)) if known(edits2(word)) else [word]

# - fonction known: en remplacant la compréhension de liste par une fonction qui utilise map et filter. nous avons remaqué que seulement filter était nécessaire
def known(words):
    return set(filter(lambda s: s in WORDS, words))
    #return set(map(lambda w: w, filter(lambda s: s in WORDS, words)))

# ne pas exécuter si appelé d'un autre programme
if __name__ == "__main__":
    word = 'devoir'

    print(candidates(word))
    print(correction(word))

