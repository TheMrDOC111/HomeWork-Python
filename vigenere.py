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
            k = (string.ascii_lowercase.index(plaintext[i].lower()) + string.ascii_lowercase.index(
                keyword[i % len(keyword)].lower()))
            if upper:
                ciphertext += (
                    string.ascii_lowercase[
                        k % len(string.ascii_lowercase)]).upper()
            else:
                ciphertext += string.ascii_lowercase[
                    k % len(string.ascii_lowercase)]
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
            k = (string.ascii_lowercase.index(ciphertext[i].lower()) - string.ascii_lowercase.index(
                keyword[i % len(keyword)].lower()))
            if upper:
                plaintext += (
                    string.ascii_lowercase[
                        k % len(string.ascii_lowercase)]).upper()
            else:
                plaintext += (
                    string.ascii_lowercase[
                        k % len(string.ascii_lowercase)])
        else:
            plaintext += ciphertext[i]
    return plaintext
