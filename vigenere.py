def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """

    alphabet = (
        "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l",
        "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x",
        "y", "z")

    ciphertext = ""

    for i in range(len(plaintext)):
        upper = False
        if plaintext[i].isupper():
            upper = True
        if plaintext[i].lower() in alphabet:
            k = (alphabet.index(plaintext[i].lower()) + alphabet.index(
                keyword[i % len(keyword)].lower()))
            if upper:
                ciphertext += str(
                    alphabet[k % len(alphabet)]).upper()
            else:
                ciphertext += str(alphabet[k % len(alphabet)])
        else:
            ciphertext += plaintext[i]

    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """

    alphabet = (
        "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l",
        "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x",
        "y", "z")

    plaintext = ""

    for i in range(len(ciphertext)):
        upper = False
        if ciphertext[i].isupper():
            upper = True
        if ciphertext[i].lower() in alphabet:
            k = (alphabet.index(ciphertext[i].lower()) - alphabet.index(
                keyword[i % len(keyword)].lower()))
            if upper:
                plaintext += str(
                    alphabet[k % len(alphabet)]).upper()
            else:
                plaintext += str(
                    alphabet[k % len(alphabet)])
        else:
            plaintext += ciphertext[i]

    return plaintext
