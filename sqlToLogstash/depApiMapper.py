def createMapping(filename):
    mapping = {}
    with open(filename, 'r') as f:
        lines = f.readlines()

    for line in lines:
        val = line.split(' => ')
        mapping[val[0]] = val[1]

    return mapping