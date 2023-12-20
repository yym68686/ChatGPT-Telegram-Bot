# # 假设你的列表如下：
# lst = [{"name": "张三", "age": 20}, {"name": "李四", "age": {"url": "wwww"}}, {"name": "王五", "age": 40}]

# # 使用列表解析和items()方法取出所有值
# values = [value for dic in lst for value in dic.values()]

# # 打印结果
# print(values)

def extract_values(obj):
    if isinstance(obj, dict):
        for value in obj.values():
            yield from extract_values(value)
    elif isinstance(obj, list):
        for item in obj:
            yield from extract_values(item)
    else:
        yield obj

lst = [{"name": "张三", "age": 20}, {"name": "李四", "age": {"url": "wwww"}}, {"name": "王五", "age": 40}]
values = list(extract_values(lst))
print(values)
