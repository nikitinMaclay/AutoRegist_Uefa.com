import random


def password_generator() -> str:
    valid_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!$%()=?+#-.:~*@[]_'
    text_len = 16
    text = ''
    for i in range(text_len):
        pos = random.randint(0, len(valid_chars) - 1)
        text = text + valid_chars[pos]
    return text + "A!4b"
