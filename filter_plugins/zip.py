def zip_encrypt(value, key):
    encrypt_str = ''
    for i, j in zip(str(value), key):
        temp = str(ord(i) + ord(j)) + '_'
        encrypt_str = encrypt_str + temp
    return 'cip@' + encrypt_str


def zip_decrypt(value, key):
    try:
        decrypt_str = ''
        if value.startswith("cip@") and value.__contains__("_"):
            value = value[4:]
        for i, j in zip(value.split("_")[:-1], key):
            temp = chr(int(i) - ord(j))
            decrypt_str = decrypt_str + temp
        return decrypt_str
    except Exception as e:
        return value


class FilterModule(object):

    def filters(self):
        return {
            'zip_encrypt': zip_encrypt,
            'zip_decrypt': zip_decrypt
        }
