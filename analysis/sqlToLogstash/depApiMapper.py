import json


def createMapping(filename):
    mapping = {}
    with open(filename, 'r') as f:
        lines = f.readlines()

    for line in lines:
        val = line.split(' => ')
        mapping[val[0]] = val[1]

    return mapping


def createRegexMapping(filename):
    with open(filename, 'r') as f:
        return json.load(f)


def createMetaMapping(filename):
    mapping = {}
    with open(filename, 'r') as f:
        for depMethod, meta in json.load(f).iteritems():
            if meta['isValid']:
                mapping[depMethod] = meta
    return mapping
