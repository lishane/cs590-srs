import re
import json


def getArgumentString(method):
    if method.endswith(')'):
        search = re.search('\((.*)\)', method)
        return search.group(1)
    else:
        return method


def getMethodRegex(method, methodArgs):
    if len(methodArgs) == 0 or (len(methodArgs) == 1 and methodArgs[0] == ''):
        return method

    methodRegex = method.split('(')[0] + '\('
    for arg in methodArgs:
        methodRegex += '([^,]*),'
    methodRegex = methodRegex[:-1]
    methodRegex += '\)'
    return methodRegex


def getArguments(argString):
    if argString == '':
        return []
    elif ',' not in argString:
        return [argString]
    else:
        return argString.split(',')


def main():
    regexMappings = {}
    with open('cleanedMapping.txt') as f:
        lines = [x.strip() for x in f.readlines()]

        for line in lines:
            methods = line.split(' => ')
            depMethod = methods[0]
            repMethod = methods[1]

            # Get Argument String
            depArgString = getArgumentString(depMethod)
            repArgString = getArgumentString(repMethod)

            # Get list of arguments
            depArgs = getArguments(depArgString)
            repArgs = getArguments(repArgString)

            # Get regex for method
            depRegex = getMethodRegex(depMethod, depArgs)
            repRegex = getMethodRegex(repMethod, repArgs)

            # Get method name only no arguments
            depName = depMethod.split('(')[0]
            repName = repMethod.split('(')[0]

            # Get search queries
            depSearch = depName + '('
            repSearch = repName + '('

            # Get number of arguments
            numDepArgs = len(depArgs)
            numRepArgs = len(repArgs)

            mapping = {'depRegex': depRegex, 'repMethod': repMethod, 'repRegex': repRegex, 'depName': depName,
                       'repName': repName, 'depSearch': depSearch, 'repSearch': repSearch, 'numDepArgs': numDepArgs,
                       'numRepArgs': numRepArgs}
            regexMappings[depMethod] = mapping

    with open('regexMapping.txt', 'w') as f:
        json.dump(regexMappings, f)


main()
