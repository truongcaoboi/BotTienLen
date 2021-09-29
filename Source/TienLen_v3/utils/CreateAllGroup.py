import numpy as np


"numCard: 3,4,5,6,7,8,9,10,J,Q,K,A,2"
"suitCard: 4 - Heart, 3 - Diamond, 2 - Club, 1 - Spider"
def createAllGroup():

    def getNumTu(cardId):
        num = (cardId - 1) % 13 + 2
        return num


    def convert_id_card_to_string(iCard):
        numCard = getNumTu(iCard)
        if numCard == 11:
            numCard = "J"
        elif numCard == 12:
            numCard = "Q"
        elif numCard == 13:
            numCard = "K"
        elif numCard == 14:
            numCard = "A"
        suitCard = (iCard - 1) // 13 + 1
        if(suitCard == 1):
            suitCard = "♠"
        elif suitCard == 2:
            suitCard = "♣"
        elif suitCard == 3:
            suitCard = "♦"
        elif suitCard == 4:
            suitCard = "♥"
        # print("{} {} {}".format(iCard,numCard,suitCard))
        return "{} {}".format(numCard, suitCard)


    def printFile(fname, mode, arrs = None, arr= None):
        file = open("Dump/"+fname, mode, encoding="utf-8")
        if(arrs is not None):
            for ar in arrs:
                strCards = ""
                for idCard in ar:
                    # strCards += convert_id_card_to_string(idCard)+", "
                    strCards += "{},".format(idCard)
                strCards = strCards[:len(strCards) - 1]
                file.write(strCards+"\n")
        if(arr is not None):
            strCards = ""
            for idCard in arr:
                # strCards += convert_id_card_to_string(idCard)+", "
                strCards += "{},".format(idCard)
            strCards = strCards[:len(strCards) - 1]
            file.write(strCards+"\n")
        file.flush()
        file.close()

    cards = np.arange(52) + 1
    all = []
    count = 0
    #ones
    print("Creating group one card ...")
    ones = np.arange(52) + 1
    ones.shape = (52,1)
    printFile(fname="ones.txt", mode="w",arrs=ones)
    # input()
    #twos
    print("Creating group two card same number ...")
    # doi 3
    doi3 = []
    for i in range(3):
        cardId = i * 13 + 2
        for j in range(3):
            add = (j + 1) * 13
            if(cardId + add <= 52):
                doi3.append([cardId,cardId + add])
            else:
                break
    printFile(fname="dois.txt", mode="a",arrs=doi3)
    # doi 4
    doi4 = []
    for i in range(3):
        cardId = i * 13 + 3
        for j in range(3):
            add = (j + 1) * 13
            if(cardId + add <= 52):
                doi4.append([cardId,cardId + add])
            else:
                break
    printFile(fname="dois.txt", mode="a",arrs=doi4)
    # doi 5
    doi5 = []
    for i in range(3):
        cardId = i * 13 + 4
        for j in range(3):
            add = (j + 1) * 13
            if(cardId + add <= 52):
                doi5.append([cardId,cardId + add])
            else:
                break
    printFile(fname="dois.txt", mode="a",arrs=doi5)
    # doi 6
    doi6 = []
    for i in range(3):
        cardId = i * 13 + 5
        for j in range(3):
            add = (j + 1) * 13
            if(cardId + add <= 52):
                doi6.append([cardId,cardId + add])
            else:
                break
    printFile(fname="dois.txt", mode="a",arrs=doi6)
    # doi 7
    doi7 = []
    for i in range(3):
        cardId = i * 13 + 6
        for j in range(3):
            add = (j + 1) * 13
            if(cardId + add <= 52):
                doi7.append([cardId,cardId + add])
            else:
                break
    printFile(fname="dois.txt", mode="a",arrs=doi7)
    # doi 8
    doi8 = []
    for i in range(3):
        cardId = i * 13 + 7
        for j in range(3):
            add = (j + 1) * 13
            if(cardId + add <= 52):
                doi8.append([cardId,cardId + add])
            else:
                break
    printFile(fname="dois.txt", mode="a",arrs=doi8)
    # doi 9
    doi9 = []
    for i in range(3):
        cardId = i * 13 + 8
        for j in range(3):
            add = (j + 1) * 13
            if(cardId + add <= 52):
                doi9.append([cardId,cardId + add])
            else:
                break
    printFile(fname="dois.txt", mode="a",arrs=doi9)
    # doi 10
    doi10 = []
    for i in range(3):
        cardId = i * 13 + 9
        for j in range(3):
            add = (j + 1) * 13
            if(cardId + add <= 52):
                doi10.append([cardId,cardId + add])
            else:
                break
    printFile(fname="dois.txt", mode="a",arrs=doi10)
    # doi J
    doiJ = []
    for i in range(3):
        cardId = i * 13 + 10
        for j in range(3):
            add = (j + 1) * 13
            if(cardId + add <= 52):
                doiJ.append([cardId,cardId + add])
            else:
                break
    printFile(fname="dois.txt", mode="a",arrs=doiJ)
    # doi Q
    doiQ = []
    for i in range(3):
        cardId = i * 13 + 11
        for j in range(3):
            add = (j + 1) * 13
            if(cardId + add <= 52):
                doiQ.append([cardId,cardId + add])
            else:
                break
    printFile(fname="dois.txt", mode="a",arrs=doiQ)
    # doi K
    doiK = []
    for i in range(3):
        cardId = i * 13 + 12
        for j in range(3):
            add = (j + 1) * 13
            if(cardId + add <= 52):
                doiK.append([cardId,cardId + add])
            else:
                break
    printFile(fname="dois.txt", mode="a",arrs=doiK)
    # doi A
    doiA = []
    for i in range(3):
        cardId = i * 13 + 13
        for j in range(3):
            add = (j + 1) * 13
            if(cardId + add <= 52):
                doiA.append([cardId,cardId + add])
            else:
                break
    printFile(fname="dois.txt", mode="a",arrs=doiA)
    # doi 2
    doi2 = []
    for i in range(3):
        cardId = i * 13 + 1
        for j in range(3):
            add = (j + 1) * 13
            if(cardId + add <= 52):
                doi2.append([cardId,cardId + add])
            else:
                break
    printFile(fname="dois.txt", mode="a",arrs=doi2)
    print("Creating group four card same number ...")
    #tu3
    tu3 = []
    for i in range(4):
        tu3.append(i*13 + 2)
    printFile(fname="tus.txt", mode="a",arr=tu3)
    #tu4
    tu4 = []
    for i in range(4):
        tu4.append(i*13 + 3)
    printFile(fname="tus.txt", mode="a",arr=tu4)
    #tu5
    tu5 = []
    for i in range(4):
        tu5.append(i*13 + 4)
    printFile(fname="tus.txt", mode="a",arr=tu5)
    #tu6
    tu6 = []
    for i in range(4):
        tu6.append(i*13 + 5)
    printFile(fname="tus.txt", mode="a",arr=tu6)
    #tu7
    tu7 = []
    for i in range(4):
        tu7.append(i*13 + 6)
    printFile(fname="tus.txt", mode="a",arr=tu7)
    #tu8
    tu8 = []
    for i in range(4):
        tu8.append(i*13 + 7)
    printFile(fname="tus.txt", mode="a",arr=tu8)
    #tu9
    tu9 = []
    for i in range(4):
        tu9.append(i*13 + 8)
    printFile(fname="tus.txt", mode="a",arr=tu9)
    #tu10
    tu10 = []
    for i in range(4):
        tu10.append(i*13 + 9)
    printFile(fname="tus.txt", mode="a",arr=tu10)
    #tuJ
    tuJ = []
    for i in range(4):
        tuJ.append(i*13 + 10)
    printFile(fname="tus.txt", mode="a",arr=tuJ)
    #tuQ
    tuQ = []
    for i in range(4):
        tuQ.append(i*13 + 11)
    printFile(fname="tus.txt", mode="a",arr=tuQ)
    #tuK
    tuK = []
    for i in range(4):
        tuK.append(i*13 + 12)
    printFile(fname="tus.txt", mode="a",arr=tuK)
    #tuA
    tuA = []
    for i in range(4):
        tuA.append(i*13 + 13)
    printFile(fname="tus.txt", mode="a",arr=tuA)
    #tu2
    tu2 = []
    for i in range(4):
        tu2.append(i*13 + 1)
    printFile(fname="tus.txt", mode="a",arr=tu2)

    print("Creating group three card same number ...")
    #xam3
    xam3 = []
    for i in range(4):
        tu = tu3.copy()
        tu.remove(i*13 + 2)
        xam3.append(tu)
    printFile(fname="xams.txt", mode="a",arrs=xam3)
    #xam4
    xam4 = []
    for i in range(4):
        tu = tu4.copy()
        tu.remove(i*13 + 3)
        xam4.append(tu)
    printFile(fname="xams.txt", mode="a",arrs=xam4)
    #xam5
    xam5 = []
    for i in range(4):
        tu = tu5.copy()
        tu.remove(i*13 + 4)
        xam5.append(tu)
    printFile(fname="xams.txt", mode="a",arrs=xam5)
    #xam6
    xam6 = []
    for i in range(4):
        tu = tu6.copy()
        tu.remove(i*13 + 5)
        xam6.append(tu)
    printFile(fname="xams.txt", mode="a",arrs=xam6)
    #xam7
    xam7 = []
    for i in range(4):
        tu = tu7.copy()
        tu.remove(i*13 + 6)
        xam7.append(tu)
    printFile(fname="xams.txt", mode="a",arrs=xam7)
    #xam8
    xam8 = []
    for i in range(4):
        tu = tu8.copy()
        tu.remove(i*13 + 7)
        xam8.append(tu)
    printFile(fname="xams.txt", mode="a",arrs=xam8)
    #xam9
    xam9 = []
    for i in range(4):
        tu = tu9.copy()
        tu.remove(i*13 + 8)
        xam9.append(tu)
    printFile(fname="xams.txt", mode="a",arrs=xam9)
    #xam10
    xam10 = []
    for i in range(4):
        tu = tu10.copy()
        tu.remove(i*13 + 9)
        xam10.append(tu)
    printFile(fname="xams.txt", mode="a",arrs=xam10)
    #xamJ
    xamJ = []
    for i in range(4):
        tu = tuJ.copy()
        tu.remove(i*13 + 10)
        xamJ.append(tu)
    printFile(fname="xams.txt", mode="a",arrs=xamJ)
    #xamQ
    xamQ = []
    for i in range(4):
        tu = tuQ.copy()
        tu.remove(i*13 + 11)
        xamQ.append(tu)
    printFile(fname="xams.txt", mode="a",arrs=xamQ)
    #xamK
    xamK = []
    for i in range(4):
        tu = tuK.copy()
        tu.remove(i*13 + 12)
        xamK.append(tu)
    printFile(fname="xams.txt", mode="a",arrs=xamK)
    #xamA
    xamA = []
    for i in range(4):
        tu = tuA.copy()
        tu.remove(i*13 + 13)
        xamA.append(tu)
    printFile(fname="xams.txt", mode="a",arrs=xamA)
    #xam2
    xam2 = []
    for i in range(4):
        tu = tu2.copy()
        tu.remove(i*13 + 1)
        xam2.append(tu)
    printFile(fname="xams.txt", mode="a",arrs=xam2)


    def getDoi(numDoi):
        if(numDoi == 3):
            return doi3
        if(numDoi == 4):
            return doi4
        if(numDoi == 5):
            return doi5
        if(numDoi == 6):
            return doi6
        if(numDoi == 7):
            return doi7
        if(numDoi == 8):
            return doi8
        if(numDoi == 9):
            return doi9
        if(numDoi == 10):
            return doi10
        if(numDoi == 11):
            return doiJ
        if(numDoi == 12):
            return doiQ
        if(numDoi == 13):
            return doiK
        if(numDoi == 14):
            return doiA
        if(numDoi == 2):
            return doi2

    #2 doi thong
    print("Creating group two pair straight ...")
    doithong2 = []
    for i in range(11):
        dois = getDoi(i+3)
        for doi in dois:
            numDoi = getNumTu(doi[len(doi) - 1]) + 1
            if(numDoi <= 14):
                ds = getDoi(numDoi)
                for d in ds:
                    dt = doi.copy()
                    for item in d:
                        dt.append(item)
                    doithong2.append(dt)
            else:
                break
    printFile(fname="doithongs.txt", mode="a",arrs=doithong2)
    #3 doi thong
    print("Creating group three pair straight ...")
    doithong3 = []
    for doi in doithong2:
        numDoi = getNumTu(doi[len(doi) - 1]) + 1
        if(numDoi <= 14):
            ds = getDoi(numDoi)
            for d in ds:
                dt = doi.copy()
                for item in d:
                    dt.append(item)
                doithong3.append(dt)
        else:
            break
    printFile(fname="doithongs.txt", mode="a",arrs=doithong3)

    #4 doi thong
    print("Creating group four pair straight ...")
    doithong4 = []
    for doi in doithong3:
        numDoi = getNumTu(doi[len(doi) - 1]) + 1
        if(numDoi <= 14):
            ds = getDoi(numDoi)
            for d in ds:
                dt = doi.copy()
                for item in d:
                    dt.append(item)
                doithong4.append(dt)
        else:
            break
    printFile(fname="doithongs.txt", mode="a",arrs=doithong4)


    print("Creating group straight three card ...")
    #roc3
    roc3 = []
    for i in range(10):
        for j in range(4):
            cardFirst = j * 13 + i + 2
            for k in range(4):
                cardSecond = k * 13 + i + 3
                for n in range(4):
                    cardThird = n * 13 + i + 4
                    roc3.append([cardFirst,cardSecond,cardThird])
    printFile(fname="rongroc3s.txt", mode="a",arrs=roc3)
    def getTu(numTu):
        if(numTu == 3):
            return tu3
        if(numTu == 4):
            return tu4
        if(numTu == 5):
            return tu5
        if(numTu == 6):
            return tu6
        if(numTu == 7):
            return tu7
        if(numTu == 8):
            return tu8
        if(numTu == 9):
            return tu9
        if(numTu == 10):
            return tu10
        if(numTu == 11):
            return tuJ
        if(numTu == 12):
            return tuQ
        if(numTu == 13):
            return tuK
        if(numTu == 14):
            return tuA
        if(numTu == 1):
            return tu2
    #roc4
    print("Creating group straight four card ...")
    roc4 = []
    for roc in roc3:
        numTu = getNumTu(roc[len(roc) - 1]) + 1
        if(numTu <= 14):
            tu = getTu(numTu)
            for cardi in tu:
                r = roc.copy()
                r.append(cardi)
                roc4.append(r)
        else:
            break
    printFile(fname="rongroc4s.txt", mode="a",arrs=roc4)
    #roc5
    print("Creating group straight five card ...")
    roc5 = []
    for roc in roc4:
        numTu = getNumTu(roc[len(roc) - 1]) + 1
        if(numTu <= 14):
            tu = getTu(numTu)
            for cardi in tu:
                r = roc.copy()
                r.append(cardi)
                roc5.append(r)
        else:
            break
    printFile(fname="rongroc5s.txt", mode="a",arrs=roc5)
    #roc6
    print("Creating group straight six card ...")
    roc6 = []
    for roc in roc5:
        numTu = getNumTu(roc[len(roc) - 1]) + 1
        if(numTu <= 14):
            tu = getTu(numTu)
            for cardi in tu:
                r = roc.copy()
                r.append(cardi)
                roc6.append(r)
        else:
            break
    printFile(fname="rongroc6s.txt", mode="a",arrs=roc6)
    #roc7
    print("Creating group straight seven card ...")
    roc7 = []
    for roc in roc6:
        numTu = getNumTu(roc[len(roc) - 1]) + 1
        if(numTu <= 14):
            tu = getTu(numTu)
            for cardi in tu:
                r = roc.copy()
                r.append(cardi)
                roc7.append(r)
        else:
            break
    printFile(fname="rongroc7s.txt", mode="a",arrs=roc7)
    #roc8
    print("Creating group straight eight card ...")
    roc8 = []
    for roc in roc7:
        numTu = getNumTu(roc[len(roc) - 1]) + 1
        if(numTu <= 14):
            tu = getTu(numTu)
            for cardi in tu:
                r = roc.copy()
                r.append(cardi)
                roc8.append(r)
        else:
            break
    printFile(fname="rongroc8s.txt", mode="a",arrs=roc8)
    #roc9
    print("Creating group straight nine card ...")
    roc9 = []
    for roc in roc8:
        numTu = getNumTu(roc[len(roc) - 1]) + 1
        if(numTu <= 14):
            tu = getTu(numTu)
            for cardi in tu:
                r = roc.copy()
                r.append(cardi)
                roc9.append(r)
        else:
            break
    printFile(fname="rongroc9s.txt", mode="a",arrs=roc9)
    #roc10
    print("Creating group straight ten card ...")
    roc10 = []
    for roc in roc9:
        numTu = getNumTu(roc[len(roc) - 1]) + 1
        if(numTu <= 14):
            tu = getTu(numTu)
            for cardi in tu:
                r = roc.copy()
                r.append(cardi)
                roc10.append(r)
        else:
            break
    printFile(fname="rongroc10s.txt", mode="a",arrs=roc10)
    #roc11
    print("Creating group straight elevent card ...")
    roc11 = []
    for roc in roc10:
        numTu = getNumTu(roc[len(roc) - 1]) + 1
        if(numTu <= 14):
            tu = getTu(numTu)
            for cardi in tu:
                r = roc.copy()
                r.append(cardi)
                roc11.append(r)
        else:
            break
    printFile(fname="rongroc11s.txt", mode="a",arrs=roc11)


    for arr in ones:
        all.append(arr)

    for arr in doi3:
        all.append(arr)
    for arr in doi4:
        all.append(arr)
    for arr in doi5:
        all.append(arr)
    for arr in doi6:
        all.append(arr)
    for arr in doi7:
        all.append(arr)
    for arr in doi8:
        all.append(arr)
    for arr in doi9:
        all.append(arr)
    for arr in doi10:
        all.append(arr)
    for arr in doiJ:
        all.append(arr)
    for arr in doiQ:
        all.append(arr)
    for arr in doiK:
        all.append(arr)
    for arr in doiA:
        all.append(arr)
    for arr in doi2:
        all.append(arr)

    for arr in xam3:
        all.append(arr)
    for arr in xam4:
        all.append(arr)
    for arr in xam5:
        all.append(arr)
    for arr in xam6:
        all.append(arr)
    for arr in xam7:
        all.append(arr)
    for arr in xam8:
        all.append(arr)
    for arr in xam9:
        all.append(arr)
    for arr in xam10:
        all.append(arr)
    for arr in xamJ:
        all.append(arr)
    for arr in xamQ:
        all.append(arr)
    for arr in xamK:
        all.append(arr)
    for arr in xamA:
        all.append(arr)
    for arr in xam2:
        all.append(arr)

    all.append(tu3)
    all.append(tu4)
    all.append(tu5)
    all.append(tu6)
    all.append(tu7)
    all.append(tu8)
    all.append(tu9)
    all.append(tu10)
    all.append(tuJ)
    all.append(tuQ)
    all.append(tuK)
    all.append(tuA)
    all.append(tu2)

    for arr in doithong2:
        all.append(arr)
    for arr in doithong3:
        all.append(arr)
    for arr in doithong4:
        all.append(arr)

    for arr in roc3:
        all.append(arr)
    for arr in roc4:
        all.append(arr)
    for arr in roc5:
        all.append(arr)
    for arr in roc6:
        all.append(arr)
    for arr in roc7:
        all.append(arr)
    for arr in roc8:
        all.append(arr)
    for arr in roc9:
        all.append(arr)
    for arr in roc10:
        all.append(arr)
    for arr in roc11:
        all.append(arr)

    all = np.array(all)
    count = len(all)
    print("count {}".format(count))
    np.savez("Dump/allGroup.npz", data = all)
    print("Finish!")


# createAllGroup()