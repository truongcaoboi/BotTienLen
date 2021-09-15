import numpy as np
import os
class Util:

    def __init__(self):
        pass

    def convert_array_toString(self,array):
        strArr = ""
        array = np.array(array, np.int_)
        for num in array:
            strArr += str(num)
        return strArr

    def generateArrayBinary(self,lenBin):
        arrays = []
        arrayBin = np.zeros((lenBin))
        arrays.append(arrayBin.copy())
        flag = False
        while not flag:
            for i in range(lenBin):
                if(arrayBin[lenBin - i - 1]) == 0:
                    arrayBin[lenBin - i - 1] = 1
                    break
                else:
                    arrayBin[lenBin - i - 1] = 0
            # if(self.checkOptimizeActionSpace(arrayBin)):
            arrays.append(arrayBin.copy())
            count = 0
            for num in arrayBin:
                if(num == 1):
                    count += 1
            if(count == lenBin):
                flag = True
        # file = open("Dump/arrayBinary.txt", "w", encoding="utf-8")
        # arrays = np.array(arrays, dtype=np.int_)
        # for arr in arrays:
        #     strWrite = "["
        #     for num in arr:
        #         strWrite += "{},".format(num)
        #     strWrite = strWrite[:len(strWrite) - 1] + "]\n"
        #     file.write(strWrite)
        # file.flush()
        # file.close()
        # np.savez("arrayBinary13.npz", data = arrays)
        # return arrays
        return np.array(arrays, dtype=np.int_)

    def checkOptimizeActionSpace(self, arrBin):
        countActive = 0
        for bin in arrBin:
            if(bin == 1):
                countActive += 1
        if(countActive == 2):
            return self.checkOptimizeActionHaveTwoActive(arrBin)
        elif countActive == 3:
            return self.checkOptimizeActionHaveThreeActive(arrBin)
        elif countActive > 3 and countActive < 7:
            return self.checkOptimizeActionHave456Active(arrBin)
        elif countActive <= 11:
            return True
        return False
        
    def checkOptimizeActionHaveTwoActive(self,arrBin): 
        maxEmpty, totalEmpty = self.maxAndTotalSizeEmpty(arrBin)
        if(maxEmpty > 2):
            return False
        return True

    def checkOptimizeActionHaveThreeActive(self,arrBin):
        maxEmpty,totalEmpty = self.maxAndTotalSizeEmpty(arrBin)
        if(maxEmpty > 6 or totalEmpty > 9):
            return False
        return True

    def checkOptimizeActionHave456Active(self, arrBin):
        maxEmpty, totalEmpty = self.maxAndTotalSizeEmpty(arrBin)
        if(maxEmpty > 6):
            return False
        return True

    def maxAndTotalSizeEmpty(self, arr):
        countMax = -1
        totalEmpty = 0
        countTemp = 0
        totalTemp = 0
        start = False
        for bin in arr:
            if not start:
                if bin == 1:
                    start = True
            else:
                if(bin == 0):
                    countTemp += 1
                    totalTemp += 1
                else:
                    if(countTemp > countMax):
                        countMax = countTemp
                        countTemp = 0
                    totalEmpty += totalTemp
                    totalTemp = 0
        return (countMax, totalEmpty)

    def printStrIntoFile(self, strContent, fileName):
        dir = "Dump"
        fileName = os.path.join(dir, fileName)
        file = open(fileName, "a+")
        file.write(strContent)
        file.write("\n")
        file.flush()
        file.close()