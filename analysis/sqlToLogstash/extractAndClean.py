import MySQLdb
import depApiChecker
import depInfo
import depApiMapper


# Id, PostTypeId, CreationDate, Score, ViewCount, Body, OwnerUserId, LastEditorUserId, LastEditDate, LastActivityDate, Title, AnswerCount, CommentCount

def connectDb():
    depInfo.db = MySQLdb.connect(
        host='127.0.0.1',
        user="root",
        passwd="  ",
        db="stackoverflow"
    )
    depInfo.c = depInfo.db.cursor()


def postMeta():
    depInfo.depMetaMapping = depApiMapper.createMetaMapping('../mapping/cleanedOutput.txt')
    depInfo.depMapping = depApiMapper.createMapping('../mapping/cleanedMapping.txt')
    depInfo.depRegexMapping = depApiMapper.createRegexMapping('../mapping/regexMapping.txt')

    depInfo.c.execute("SELECT * FROM posts WHERE tags LIKE '%android%'")
    i = 0
    for row in depInfo.c:
        # Rows from SQL
        id = row[0]
        postTypeId = row[1]
        parentId = row[2]
        acceptedAnswerId = row[3]
        creationDate = row[4]
        score = row[5]
        viewCount = row[6]
        body = row[7]
        ownerUserId = row[8]
        lastEditorUserId = row[9]
        lastEditDate = row[10]
        lastActivityDate = row[11]
        title = row[12]
        answerCount = row[13]
        commentCount = row[14]

        meta = {}

        foundReplacement = False
        replacementMethod = None

        # Check if deprecated API found, if so, check if replacement was found
        foundDeprecated, deprecatedMethod = depApiChecker.checkBodyForDepApi(body)
        if foundDeprecated:
            foundReplacement, replacementMethod = depApiChecker.checkBodyForRepApi(body, deprecatedMethod)

        meta['foundDep'] = foundDeprecated
        meta['depMethod'] = deprecatedMethod
        meta['foundRep'] = foundReplacement
        meta['repMethod'] = replacementMethod

        depInfo.postMeta[id] = meta

        if postTypeId == 1:
            if id not in depInfo.parentPostMeta:
                depInfo.parentPostMeta[id] = {'foundDep': False, 'foundRep': False}
            if foundDeprecated:
                depInfo.parentPostMeta[id]['foundDep'] = True
            if foundReplacement:
                depInfo.parentPostMeta[id]['foundRep'] = True
            if acceptedAnswerId is not None:
                depInfo.acceptedPostMeta[id] = acceptedAnswerId

        # If its a answer, we need to take care of parent meta
        if postTypeId == 2:
            if parentId not in depInfo.parentPostMeta:
                depInfo.parentPostMeta[parentId] = {'foundDep': False, 'foundRep': False}
            if foundDeprecated:
                depInfo.parentPostMeta[parentId]['foundDep'] = True
            if foundReplacement:
                depInfo.parentPostMeta[parentId]['foundRep'] = True

        # Logging
        if i % 1000 == 0:
            print "Processed " + str(i)
        i += 1


def outputJson():
    numFoundDep = 0
    numFoundRep = 0
    numScanned = 0

    with open('result.csv', 'w') as f:
        # depInfo.c.execute("SELECT * FROM posts WHERE tags LIKE '%android%'")
        depInfo.c.execute("SELECT * FROM posts")
        i = 0
        for row in depInfo.c:
            # Rows from SQL
            id = row[0]
            postTypeId = row[1]
            parentId = row[2]
            acceptedAnswerId = row[3]
            creationDate = row[4]
            score = row[5]
            viewCount = row[6]
            body = row[7]
            ownerUserId = row[8]
            lastEditorUserId = row[9]
            lastEditDate = row[10]
            lastActivityDate = row[11]
            title = row[12]
            tags = row[13]
            answerCount = row[14]
            commentCount = row[15]

            # Set whether or not found
            foundDep = depInfo.postMeta[id]['foundDep']
            foundRep = depInfo.postMeta[id]['foundRep']

            # Set parent, since for elastic, we have a column where relevant posts to that question will be true
            if postTypeId == 1:
                postFoundDep = depInfo.parentPostMeta[id]['foundDep']
                postFoundRep = depInfo.parentPostMeta[id]['foundRep']
                parentId = id
            else:
                postFoundDep = depInfo.parentPostMeta[parentId]['foundDep']
                postFoundRep = depInfo.parentPostMeta[parentId]['foundRep']

            # Set methods that were found
            depMethod = depInfo.postMeta[id]['depMethod']
            repMethod = depInfo.postMeta[id]['repMethod']

            # Get whether or not is accepted answer
            acceptedAnswer = False
            if postTypeId == 2:
                if parentId in depInfo.acceptedPostMeta:
                    if depInfo.acceptedPostMeta[parentId] == id:
                        acceptedAnswer = True

            # Format body/title
            body = body.replace('"', '\'')
            if title is not None:
                title = title.replace('"', '\'')

            # Handle Questions
            csv = '"{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}"\n'.format(
                id,
                postTypeId,
                parentId,
                acceptedAnswerId,
                creationDate,
                foundDep,
                foundRep,
                postFoundDep,
                postFoundRep,
                depMethod,
                repMethod,
                acceptedAnswer,
                score,
                viewCount,
                body,
                lastEditDate,
                lastActivityDate,
                title,
                tags,
                answerCount)

            numScanned += 1
            if foundDep:
                numFoundDep += 1
            if foundRep:
                numFoundRep += 1

            f.write(csv)
            # Logging
            if i % 1000 == 0:
                print "Processed " + str(i)
            i += 1

    print numFoundDep, numFoundRep, numScanned


def main():
    connectDb()
    postMeta()
    outputJson()


main()
