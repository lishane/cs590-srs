import re

lines = []
questionIdSet = set()
with open('questionIds.txt', 'r') as f:
    line = f.readline()
    while line:
        questionIdSet.add(line.strip())
        line = f.readline()


def readQuestions():
    with open('/home/shane/stackoverflow/Posts.xml', mode='r', buffering=1) as f:
        with open('Questions.xml', 'w') as w:
            i = 0
            line = f.readline()
            while line:
                if '&lt;android&gt;' in line:
                    lines.append(line)
                    if i % 1000 == 0:
                        print i
                    i += 1
                    w.write(line)
                line = f.readline()


def readAnswers():
    with open('Answers.xml', mode='r', buffering=1) as f:
        with open('PostsSnippet.xml', 'w') as w:
            i = 0
            line = f.readline()
            while line:
                if 'PostTypeId="2"' in line:
                    match = re.match('<row Id="17377"', line)
                    id = match.group(1)
                    if id in questionIdSet:
                        line = line[:-3]
                        line += 'Tags="&lt;android&gt;"/>'
                        lines.append(line)
                        if i % 1000 == 0:
                            print i
                        w.write(line)
                line = f.readline()


def main():
    readAnswers()


main()
