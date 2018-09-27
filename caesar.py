alphabet = (
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w",
    "x",
    "y", "z")

k = 3


def encrypt_caesar(plaintext: str) -> str:
    ciphertext = ""

    for i in range(len(plaintext)):
        upper = False
        if plaintext[i].isupper():
            upper = True
        if plaintext[i].lower() in alphabet:
            ciphertext += setUp(alphabet[(k + alphabet.index(plaintext[i].lower())) % len(alphabet)], upper)
        else:
            ciphertext += plaintext[i]

    return ciphertext


def decrypt_caesar(ciphertext: str) -> str:
    plaintext = ""

    for i in range(len(ciphertext)):
        upper = False
        if ciphertext[i].isupper():
            upper = True
        if ciphertext[i].lower() in alphabet:
            plaintext += setUp(alphabet[(alphabet.index(ciphertext[i].lower()) - k) % len(alphabet)], upper)
        else:
            plaintext += ciphertext[i]
    return plaintext


def setUp(char: str, boolean: bool) -> str:
    if boolean:
        char = char.upper()

    return char


print(encrypt_caesar("python"))
print(decrypt_caesar("sbwkrq"))

print(encrypt_caesar("PYTHON"))
print(decrypt_caesar("SBWKRQ"))

print(encrypt_caesar("Python3.6"))
print(decrypt_caesar("Sbwkrq3.6"))
