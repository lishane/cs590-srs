import os

lines = []
with open('Posts.xml', mode='r', buffering=1) as f:
    with open('PostsSnippet.xml', 'w') as w:
        i = 0
        line = f.readline()
        while line:
            if '&lt;android&gt;' in line:
                lines.append(line)
                print i
                i += 1
                w.write(line)
            line = f.readline()
