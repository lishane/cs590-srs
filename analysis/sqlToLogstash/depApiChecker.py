import re
import depInfo


# Checking String only 862/5974
# Checking Regex only 745/5974
# Checking Class only 110/5974
# Checking class uppercase split

def checkBodyForDepApi(body):
    # Check every deprecated API
    found = False
    foundDep = None

    # Check Regex First
    for dep, meta in depInfo.depRegexMapping.iteritems():
        if str(meta['depSearch']) in body:
            search = re.search(meta['depRegex'], body)
            if search is not None:
                found = True
                foundDep = dep
                break

    if not found:
        return False, None

    # Check for context
    regexMeta = depInfo.depRegexMapping[foundDep]
    depMeta = depInfo.depMetaMapping[regexMeta['depName']]
    classSplit = depMeta['methodClass'].split('.')
    classOnly = ""
    for split in classSplit:
        if split[0].isupper():
            classOnly += split + "."
    classOnly = classOnly[:-1]
    
    if str(classOnly) not in body:
        return False, None

    # Passed all checks, return True and depMethod
    return True, foundDep


def checkBodyForRepApi(body, depMethod):
    # Check every deprecated API
    found = False
    foundRep = None

    # Check Regex First
    meta = depInfo.depRegexMapping[depMethod]
    if str(meta['repSearch']) in body:
        search = re.search(meta['repRegex'], body)
        if search is not None:
            found = True
            foundRep = meta['repMethod']

    if not found:
        return False, None

    # Check for context
    regexMeta = depInfo.depRegexMapping[depMethod]
    depMeta = depInfo.depMetaMapping[regexMeta['depName']]
    # TODO how to check context for Rep???

    # Passed all checks, return True and depMethod
    return True, foundRep
