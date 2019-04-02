import re
import json

with open('cda-output-android-9.0.0_r9:28.txt') as f:
    content = f.readlines()
content = [x.strip() for x in content]

results = {}
i = 0
while i < len(content):
    line = content[i]
    if line.startswith('<') and line.endswith('>'):
        data = {}

        # Try to get comments
        replacementComments = ""
        i += 1
        line = content[i]
        if '/**' in line:
            while '*/' not in line:
                replacementComments += line + '\n'
                i += 1
                line = content[i]
            replacementComments += line + '\n'
            i += 1
            line = content[i]

        # Get method stuff
        if 'PUBLIC' in line and not line.endswith('---->'):
            fullMethod = re.search(': (.*)>    -', line).group(1)
            methodName = re.search(': (.*) (.*)\((.*)>', line).group(2)
            methodClass = re.search('<(.*):', line).group(1)
            dirtyReplacement = re.search('-->    (.*)', line).group(1)
            if dirtyReplacement.startswith('#'):
                dirtyReplacement = dirtyReplacement[1:]
            splitMethod = fullMethod.split(' ')
            data['methodReturn'] = splitMethod[0]
            data['method'] = splitMethod[1]
            data['fullMethod'] = fullMethod
            data['methodName'] = methodName
            data['methodClass'] = methodClass
            data['dirtyReplacement'] = dirtyReplacement
            data['replacementComments'] = replacementComments
            results[methodName] = data
    i += 1

with open('dirtyOutput.json', 'w') as f:
    json.dump(results, f)
