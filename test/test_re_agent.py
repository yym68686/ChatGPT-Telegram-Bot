import re
matches = re.finditer(r"answer: (.*)", test_str, re.MULTILINE)
result = []
for matchNum, match in enumerate(matches, start=1):
    for groupNum in range(0, len(match.groups())):
        groupNum = groupNum + 1
        result.append(match.group(groupNum))

print("\n\n".join(result))
