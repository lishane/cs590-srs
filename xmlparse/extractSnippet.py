import os

lines = []
with open('Posts.xml', mode='r', buffering=1) as f:
    with open('PostsSnippet.xml', 'w') as w:
        i = 0
        line = f.readline()
        if 'android' in line:
            lines.append(line)
            print i
            i += 1
            w.write(line)
