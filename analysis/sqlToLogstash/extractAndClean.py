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
    depInfo.depMapping = depApiMapper.createMapping('../mapping/cleanedMapping.txt')

    depInfo.c.execute("SELECT * FROM posts WHERE tags LIKE '%android%'")
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
        lastEditeDate = row[10]
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
            print id, deprecatedMethod, body
            foundReplacement, replacementMethod = depApiChecker.checkBodyForRepApi(body)
            if foundReplacement:
                print foundReplacement, replacementMethod

        meta['foundDep'] = foundDeprecated
        meta['depMethod'] = deprecatedMethod
        meta['foundRep'] = foundReplacement
        meta['repMethod'] = replacementMethod

        depInfo.postMeta[id] = meta

        # If its a answer, we need to take care of parent meta
        if postTypeId == 2:
            if parentId not in depInfo.parentPostMeta:
                depInfo.parentPostMeta[parentId] = {'foundDep': False, 'foundRep': False}
            if foundDeprecated:
                depInfo.parentPostMeta[parentId]['foundDep'] = True
            if foundReplacement:
                depInfo.parentPostMeta[parentId]['foundRep'] = True


def outputJson():
    depInfo.c.execute("SELECT * FROM posts WHERE tags LIKE '%android%'")
    for row in depInfo.c:
        # Rows from SQL
        id = row[0]
        postTypeId = row[1]
        creationDate = row[2]
        score = row[3]
        viewCount = row[4]
        body = row[5]
        ownerUserId = row[6]
        lastEditorUserId = row[7]
        lastEditeDate = row[8]
        lastActivityDate = row[9]
        title = row[10]
        answerCount = row[11]
        commentCount = row[12]

        # Handle Questions
        # if postTypeId == 1:


def main():
    connectDb()
    postMeta()


main()
