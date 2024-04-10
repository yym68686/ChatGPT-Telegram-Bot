def delete_model_digit_tail(lst):
    for i in range(len(lst) - 1, -1, -1):
        if not lst[i].isdigit():
            if i == len(lst) - 1:
                return "-".join(lst)
            else:
                return "-".join(lst[:i + 1])


# 示例
lst = ["hello", "123", "world", "456"]
index = find_last_string_index(lst)
print("Index of the last numeric string:", index)