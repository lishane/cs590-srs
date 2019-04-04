import re
import depInfo


def checkBodyForDepApi(body):
    # Check every deprecated API
    found = False
    foundDep = None

    # Check Regex First
    for dep, meta in depInfo.depRegexMapping.iteritems():
        if str(meta['depName']) in body:
            search = re.search(meta['depRegex'], body)
            if search is not None:
                found = True
                foundDep = dep
                break

    if not found:
        return False, None

    # Check for context
    meta = depInfo.depRegexMapping[foundDep]
    if meta['numDepArgs'] == 0:
        return False, None

    # Passed all checks, return True and depMethod
    return True, foundDep


def checkBodyForRepApi(body, depMethod):
    for dep, new in depInfo.depMapping.iteritems():
        if new in body:
            return True, dep
    return False, None
