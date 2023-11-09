def replace_with_asterisk(string, start=15, end=40):
    return string[:start] + '*' * (end - start) + string[end:]

original_string = "sk-zIuWeeuWY8vNCVhhHCXLroNmA6QhBxnv0ARMFcODVQwwqGRg"
result = replace_with_asterisk(original_string)
print(result)
