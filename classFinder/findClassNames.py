import re

with open('classIndex.txt') as f:
    classIndex = f.read()

pattern = re.compile(r'<a(.*)">(.*)<\/a><\/td>')

classes = []
for (_, className) in re.findall(pattern, classIndex):
    classes.append(className + '\n')

with open('classes.txt', 'w') as f:
    f.writelines(classes)
