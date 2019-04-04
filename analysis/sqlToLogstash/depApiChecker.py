import depInfo


def checkBodyForDepApi(body):
    for dep, new in depInfo.depMapping.iteritems():
        if dep in body:
            return True, dep
    return False, None


def checkBodyForRepApi(body):
    for dep, new in depInfo.depMapping.iteritems():
        if new in body:
            return True, dep
    return False, None
