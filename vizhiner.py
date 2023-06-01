def decrypt(text, key):
    de_message = ''
    chars = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я', '_', 'z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f', 'e', 'd', 'c', 'b', 'a', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '/', '.', ',', ' ']
    text = text.lower()
    key = key.lower()
    slavewar = dict()

    for index_symbol in range(0, len(chars)):
        slavewar[chars[index_symbol]] = chars[index_symbol:len(chars)] + chars[0:index_symbol]
    index_key = 0
    for symbol in text:
        try:
            de_message += chars[slavewar[key[index_key]].index(symbol)]
            index_key = 0 if index_key == len(key) - 1 else index_key + 1
        except ValueError:
            de_message += symbol
            index_key = 0 if index_key == len(key) - 1 else index_key + 1
    return de_message


def encrypt(text, key):
    en_crypt = ''
    chars = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я', '_', 'z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f', 'e', 'd', 'c', 'b', 'a', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '/', '.', ',', ' ']
    text = text.lower()
    key = key.lower()
    slavewar = dict()
    for index_symbol in range(0, len(chars)):
        slavewar[chars[index_symbol]] = chars[index_symbol:len(chars)] + chars[0:index_symbol]
    index_key = 0

    for symbol in text:
        try:
            en_crypt += slavewar[key[index_key]][chars.index(symbol)]
            index_key = 0 if index_key == len(key) - 1 else index_key + 1
        except ValueError:
            en_crypt += symbol
            index_key = 0 if index_key == len(key) - 1 else index_key + 1
    return en_crypt
