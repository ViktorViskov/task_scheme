# function for delete all not allowed characters
def sql_inj_clean(word: str):
    not_allowed_chars = ['\'','"'," ","`",";",":"]
    for some_char in not_allowed_chars:
        word = word.replace(some_char,"")
    return word