import re

def escapeshape(text):
    poslist = [0]
    strlist = []
    originstr = []
    regex = r"(#+\s.+?$)|```[\D\d\s]+?```"
    matches = re.finditer(regex, text, re.MULTILINE)
    for match in matches:
        start = match.start(1)
        end = match.end(1)
        if match.group(1) != None:
            poslist += [start, end]
            strlist.append('▎*' + text[start:end].split()[1] + '*')
    poslist.append(len(text))
    for i in range(0, len(poslist), 2):
        j, k = poslist[i:i+2]
        originstr.append(text[j:k])
    if len(strlist) < len(originstr):
        strlist.append('')
    else:
        originstr.append('')
    new_list = [item for pair in zip(originstr, strlist) for item in pair]
    return ''.join(new_list)

def escape(text):
    # In all other places characters
    # _ * [ ] ( ) ~ ` > # + - = | { } . !
    # must be escaped with the preceding character '\'.
    text = re.sub(r"_", '\_', text)
    text = re.sub(r"\*{2}(.*?)\*{2}", '@@@\\1@@@', text)
    text = re.sub(r"\n\*\s", '\n\n• ', text)
    text = re.sub(r"\*", '\*', text)
    text = re.sub(r"\@{3}(.*?)\@{3}", '*\\1*', text)
    text = re.sub(r"\!?\[(.*?)\]\((.*?)\)", '@@@\\1@@@^^^\\2^^^', text)
    text = re.sub(r"\[", '\[', text)
    text = re.sub(r"\]", '\]', text)
    text = re.sub(r"\(", '\(', text)
    text = re.sub(r"\)", '\)', text)
    text = re.sub(r"\@{3}(.*?)\@{3}\^{3}(.*?)\^{3}", '[\\1](\\2)', text)
    text = re.sub(r"~", '\~', text)
    text = re.sub(r">", '\>', text)
    text = escapeshape(text)
    text = re.sub(r"#", '\#', text)
    text = re.sub(r"\+", '\+', text)
    text = re.sub(r"\n-\s", '\n\n• ', text)
    text = re.sub(r"\-", '\-', text)
    text = re.sub(r"=", '\=', text)
    text = re.sub(r"\|", '\|', text)
    text = re.sub(r"{", '\{', text)
    text = re.sub(r"}", '\}', text)
    text = re.sub(r"\.", '\.', text)
    text = re.sub(r"!", '\!', text)
    return text

text = '''
# title

**bold**
```
# comment
print(qwer) # ferfe
ni1
```
# bn

# b

# Header
## Subheader

[1.0.0](http://version.com)
![1.0.0](http://version.com)

- item 1 -
* item 2
* item 3 ~

```python
print("1.1")_
```

And simple text with + some - **symbols**.


```
print("Hello, World!")
```

Cxy = abs (Pxy)**2/ (Pxx*Pyy)
'''

if __name__ == '__main__':
    text = escape(text)
    print(text)