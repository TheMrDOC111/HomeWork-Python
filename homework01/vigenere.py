import string


def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    for i in range(len(plaintext)):
        upper = False
        if plaintext[i].isupper():
            upper = True
        if plaintext[i].lower() in string.ascii_lowercase:
            k = string.ascii_lowercase.index(plaintext[i].lower())
            id = keyword[i % len(keyword)].lower()
            k += string.ascii_lowercase.index(id)
            k %= len(string.ascii_lowercase)
            if upper:
                ciphertext += (string.ascii_lowercase[k]).upper()
            else:
                ciphertext += string.ascii_lowercase[k]
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
    plaintext = ""
    for i in range(len(ciphertext)):
        upper = False
        if ciphertext[i].isupper():
            upper = True
        if ciphertext[i].lower() in string.ascii_lowercase:
            k = string.ascii_lowercase.index(ciphertext[i].lower())
            id = keyword[i % len(keyword)]
            k -= string.ascii_lowercase.index(id.lower())
            k %= len(string.ascii_lowercase)
            if upper:
                plaintext += (string.ascii_lowercase[k]).upper()
            else:
                plaintext += (string.ascii_lowercase[k])
        else:
            plaintext += ciphertext[i]
    return plaintext
