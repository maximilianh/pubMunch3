# Copyright 2006-2012 Mark Diekhans
import unittest, sys, string
if __name__ == '__main__':
    sys.path.append("../../..")
from pycbio.tsv import TSVTable
from pycbio.tsv import TSVError
from pycbio.tsv import TSVReader
from pycbio.sys.TestCaseBase import TestCaseBase
from pycbio.sys import procOps
from pycbio.hgdata.AutoSql import intArrayType

class ReadTests(TestCaseBase):
    def testLoad(self):
        tsv = TSVTable(self.getInputFile("mrna1.tsv"))
        self.assertEqual(len(tsv), 10)
        for r in tsv:
            self.assertEqual(len(r), 22)
        r = tsv[0]
        self.assertEqual(r["qName"], "BC032353")
        self.assertEqual(r[10],"BC032353")
        self.assertEqual(r.qName, "BC032353")

    def testMultiIdx(self):
        tsv = TSVTable(self.getInputFile("mrna1.tsv"), multiKeyCols=("tName", "tStart"))
        rows = tsv.idx.tName["chr1"]
        self.assertEqual(len(rows), 10)
        self.assertEqual(rows[1].qName, "AK095183")

        rows = tsv.idx.tStart["4268"]
        self.assertEqual(len(rows), 5)
        self.assertEqual(rows[0].qName, "BC015400")

    @staticmethod
    def onOffParse(str):
        if str == "on":
            return True
        elif str == "off":
            return False
        else:
            raise ValueError("invalid onOff value: " + str)

    @staticmethod
    def onOffFmt(val):
        if type(val) != bool:
            raise TypeError("onOff value not a bool: " + str(type(val)))
        if val:
            return "on"
        else:
            return "off"

    def doTestColType(self, inFile):
        typeMap = {"intCol": int, "floatCol": float, "onOffCol": (self.onOffParse, self.onOffFmt)}

        tsv = TSVTable(self.getInputFile(inFile), typeMap=typeMap)

        r = tsv[0]
        self.assertEqual(r.strCol, "name1")
        self.assertEqual(r.intCol, 10)
        self.assertEqual(r.floatCol, 10.01)
        self.assertEqual(str(r), "name1\t10\t10.01\ton")

        r = tsv[2]
        self.assertEqual(r.strCol, "name3")
        self.assertEqual(r.intCol, 30)
        self.assertEqual(r.floatCol, 30.555)
        self.assertEqual(str(r), "name3\t30\t30.555\toff")

    def testColType(self):
        self.doTestColType("types.tsv")

    def testColCommentType(self):
        self.doTestColType("typesComment.tsv")

    def testColTypeDefault(self):
        # default to int type
        typeMap = {"strand": str, "qName": str, "tName": str,
                   "blockSizes": intArrayType,
                   "qStarts": intArrayType, "tStarts": intArrayType}
        
        tsv = TSVTable(self.getInputFile("mrna1.tsv"), uniqKeyCols="qName",
                  typeMap=typeMap, defaultColType=int)
        r = tsv.idx.qName["AK095183"]
        self.assertEqual(r.tStart, 4222)
        self.assertEqual(r.tEnd, 19206)
        self.assertEqual(r.tName, "chr1")
        self.assertEqual(r.tStart, 4222)

        tStarts = (4222,4832,5658,5766,6469,6719,7095,7355,7777,8130,14600,19183)
        self.assertEqual(len(r.tStarts), len(tStarts))
        for i in range(len(tStarts)):
            self.assertEqual(r.tStarts[i], tStarts[i])

    def testMissingIdxCol(self):
        err = None
        try:
            tsv = TSVTable(self.getInputFile("mrna1.tsv"), multiKeyCols=("noCol",))
        except TSVError as e:
            err = e
        self.assertNotEqual(err, None)
        # should have chained exception
        self.assertNotEqual(err.cause, None)
        self.assertEqual(err.cause.message, "key column \"noCol\" is not defined")

    def testColNameMap(self):
        typeMap = {"int_col": int, "float_col": float, "onOff_col": (self.onOffParse, self.onOffFmt)}

        tsv = TSVTable(self.getInputFile('typesColNameMap.tsv'), typeMap=typeMap, columnNameMapper=lambda s: s.replace(' ', '_'))

        r = tsv[0]
        self.assertEqual(r.str_col, "name1")
        self.assertEqual(r.int_col, 10)
        self.assertEqual(r.float_col, 10.01)
        self.assertEqual(str(r), "name1\t10\t10.01\ton")

        r = tsv[2]
        self.assertEqual(r.str_col, "name3")
        self.assertEqual(r.int_col, 30)
        self.assertEqual(r.float_col, 30.555)
        self.assertEqual(str(r), "name3\t30\t30.555\toff")

    def testWrite(self):
        tsv = TSVTable(self.getInputFile("mrna1.tsv"), uniqKeyCols="qName")
        fh = open(self.getOutputFile(".tsv"), "w")
        tsv.write(fh)
        fh.close()
        self.diffExpected(".tsv")

    def testAddColumn(self):
        tsv = TSVTable(self.getInputFile("mrna1.tsv"), uniqKeyCols="qName")
        tsv.addColumn("joke")
        i = 0
        for row in tsv:
            row.joke = i
            i += 1
        fh = open(self.getOutputFile(".tsv"), "w")
        tsv.write(fh)
        fh.close()
        self.diffExpected(".tsv")

    def readMRna1(self, inFile):
        "routine to verify TSVReader on a mrna1.tsv derived file"
        rowCnt = 0
        for row in TSVReader(inFile):
            self.assertEqual(len(row), 22)
            rowCnt += 1
        self.assertEqual(rowCnt, 10)

    def testReader(self):
        self.readMRna1(self.getInputFile("mrna1.tsv"))

    def testReadGzip(self):
        tsvGz = self.getOutputFile("tsv.gz")
        procOps.runProc(["gzip", "-c", self.getInputFile("mrna1.tsv")], stdout=tsvGz)
        self.readMRna1(tsvGz)

    def testReadBzip2(self):
        tsvBz = self.getOutputFile("tsv.bz2")
        procOps.runProc(["bzip2", "-c", self.getInputFile("mrna1.tsv")], stdout=tsvBz)
        self.readMRna1(tsvBz)

    def testDupColumn(self):
        err = None
        try:
            tsv = TSVTable(self.getInputFile("dupCol.tsv"))
        except TSVError as e:
            err = e
        self.assertNotEqual(err, None)
        self.assertEqual(str(err), "Duplicate column name: col1")

    def testAllowEmptyReader(self):
        cnt = 0
        for row in TSVReader("/dev/null", allowEmpty=True):
            cnt += 1
        self.assertEqual(cnt, 0)

    def testAllowEmptyTbl(self):
        tbl = TSVTable("/dev/null", allowEmpty=True)
        self.assertEqual(len(tbl), 0)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ReadTests))
    return suite

if __name__ == '__main__':
    unittest.main()
