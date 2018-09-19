alphabet = (
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w",
    "x",
    "y", "z")


def encrypt_vigenere(plaintext, keyword):
    ciphertext = ""

    for i in range(len(plaintext)):
        upper = False
        if plaintext[i].isupper():
            upper = True
        if plaintext[i].lower() in alphabet:

            ciphertext += setUp(alphabet[(alphabet.index(plaintext[i].lower()) + alphabet.index(
                keyword[i % len(keyword)].lower())) % len(alphabet)], upper)
        else:
            ciphertext += plaintext[i]

    return ciphertext


def decrypt_vigenere(ciphertext, keyword):
    plaintext = ""

    for i in range(len(ciphertext)):
        upper = False
        if ciphertext[i].isupper():
            upper = True
        if ciphertext[i].lower() in alphabet:

            plaintext += setUp(alphabet[(alphabet.index(ciphertext[i].lower()) - alphabet.index(
                keyword[i % len(keyword)].lower())) % len(alphabet)], upper)
        else:
            plaintext += ciphertext[i]

    return plaintext


def setUp(char, boolean):
    if boolean:
        char = char.upper()

    return char


print(encrypt_vigenere("PYTHON", "A"))
print(encrypt_vigenere("python", "a"))
print(encrypt_vigenere("ATTACKATDAWN", "LEMON"))

print(decrypt_vigenere("PYTHON", "A"))
print(decrypt_vigenere("python", "a"))
print(decrypt_vigenere("LXFOPVEFRNHR", "LEMON"))