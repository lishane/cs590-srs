import json

with open('dirtyOutput.json') as f:
    dirtyOutput = json.load(f)

with open('../classFinder/classes.txt') as f:
    dirtyClasses = f.readlines()

classes = [x.strip() for x in dirtyClasses]

# Get rid of methods with incorrect dirtyReplacements
incorrect = {}
for methodName, data in dirtyOutput.iteritems():
    dirtyReplacement = data['dirtyReplacement']
    if dirtyReplacement.endswith('}') or '@' in dirtyReplacement:
        incorrect[methodName] = data

for methodName in incorrect:
    dirtyOutput.pop(methodName, None)

# Find methods whose classes are completely deprecated
for methodName, data in dirtyOutput.iteritems():
    data['isClassDeprecated'] = False
    dirtyReplacement = data['dirtyReplacement']
    names = dirtyReplacement.split('.')
    if len(names) <= 1 or '#' in dirtyReplacement or dirtyReplacement.endswith(')'): continue
    firstCapital = 0
    newClassName = ""

    while firstCapital < len(names):
        if len(names[firstCapital]) == 0: break
        if names[firstCapital][0].isupper():
            break
        firstCapital += 1

    while firstCapital < len(names):
        newClassName += names[firstCapital] + '.'
        firstCapital += 1
    newClassName = newClassName[:len(newClassName) - 1]
    if newClassName in classes:
        data['isClassDeprecated'] = True

# Produce clean replacements
for methodName, data in dirtyOutput.iteritems():
    data['isValid'] = False
    dirtyReplacement = data['dirtyReplacement']

    # Take care of duplicate replacement
    if len(dirtyReplacement.split('() ')) > 1:
        dirtyReplacement = dirtyReplacement.split('() ')[1]

    # If class deprecated, we can skip since it is already cleaned
    if data['isClassDeprecated']:
        data['cleanReplacement'] = dirtyReplacement
        data['isValid'] = True
        continue

    # Handle a normal case where the ending methods are not the same
    if dirtyReplacement.endswith(')'):
        if '#' in dirtyReplacement:
            dirtyReplacement = dirtyReplacement.split('#')[1]
        if not dirtyReplacement == data['method']:
            data['isValid'] = True
            data['cleanReplacement'] = dirtyReplacement
            continue

    # Handle a normal case where the methods are the same, in this case, we add classes
    if dirtyReplacement.endswith(')'):
        if '#' in dirtyReplacement:
            dirtyReplacement = dirtyReplacement.split('#')[1]
        if dirtyReplacement == data['method']:
            dirtyReplacement = data['dirtyReplacement']
            data['isValid'] = True
            data['cleanReplacement'] = dirtyReplacement
        continue

    # Handle where replacement is not empty, but malformed
    if len(dirtyReplacement.strip()) > 0:
        data['cleanReplacement'] = 'Malformed Replacement'

    # Handle where replacement is empty
    if len(dirtyReplacement.strip()) == 0:
        data['cleanReplacement'] = 'Empty Replacement'

with open('cleanedOutput.txt', 'w') as f:
    json.dump(dirtyOutput, f)

with open('cleanedMapping.txt', 'w') as f:
    for (methodName, data) in dirtyOutput.iteritems():
        if data['isValid']:
            f.write(data['method'] + ' => ' + data['cleanReplacement'] + '\n')
