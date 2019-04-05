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
    with open('/home/shane/stackoverflow/Posts.xml', mode='r', buffering=1) as f:
        with open('Answers.xml', 'w') as w:
            i = 0
            line = f.readline()
            while line:
                if 'PostTypeId="2"' in line:
                    match = re.search('ParentId=\"(\d*)\"', line)
                    id = match.group(1)
                    if id in questionIdSet:
                        line = line[:-3]
                        line += 'Tags="&lt;android&gt;"/>\n'
                        lines.append(line)
                        if i % 1000 == 0:
                            print i
                        i += 1
                        w.write(line)
                line = f.readline()


def main():
    readAnswers()


main()
