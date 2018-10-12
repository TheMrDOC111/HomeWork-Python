def encrypt_caesar(plaintext: str) -> str:
    """
       >>> encrypt_caesar("PYTHON")
       'SBWKRQ'
       >>> encrypt_caesar("python")
       'sbwkrq'
       >>> encrypt_caesar("Python3.6")
       'Sbwkrq3.6'
       >>> encrypt_caesar("")
       ''
       """

    ciphertext = ""

    alphabet = (
        "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v",
        "w",
        "x",
        "y", "z")

    for i in range(len(plaintext)):
        upper = False
        if plaintext[i].isupper():
            upper = True
        if plaintext[i].lower() in alphabet:
            if upper:
                ciphertext += str(alphabet[(3 + alphabet.index(plaintext[i].lower())) % len(alphabet)]).upper()
            else:
                ciphertext += alphabet[(3 + alphabet.index(plaintext[i].lower())) % len(alphabet)]
        else:
            ciphertext += plaintext[i]

    return ciphertext


def decrypt_caesar(ciphertext: str) -> str:
    """
       >>> decrypt_caesar("SBWKRQ")
       'PYTHON'
       >>> decrypt_caesar("sbwkrq")
       'python'
       >>> decrypt_caesar("Sbwkrq3.6")
       'Python3.6'
       >>> decrypt_caesar("")
       ''
       """
    plaintext = ""

    alphabet = (
        "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v",
        "w",
        "x",
        "y", "z")

    for i in range(len(ciphertext)):
        upper = False
        if ciphertext[i].isupper():
            upper = True
        if ciphertext[i].lower() in alphabet:
            if upper:
                plaintext += str(alphabet[(alphabet.index(ciphertext[i].lower()) - 3) % len(alphabet)]).upper()
            else:
                plaintext += alphabet[(alphabet.index(ciphertext[i].lower()) - 3) % len(alphabet)]
        else:
            plaintext += ciphertext[i]
    return plaintext
