# Copyright 2006-2012 Mark Diekhans
import unittest, sys
if __name__ == '__main__':
    sys.path.append("../../..")
from pycbio.sys.TestCaseBase import TestCaseBase
from pycbio.hgdata.ClusterGenes import ClusterGenes

class ReadTests(TestCaseBase):
    def testLoad(self):
        clusters = ClusterGenes(self.getInputFile("models.loci"))

        clCnt = 0
        geneCnt = 0
        for cl in clusters:
            clCnt += 1
            for g in cl:
                geneCnt += 1
        self.assertEqual(clCnt, 169)
        self.assertEqual(geneCnt, 192)

        # try getting gene, and go back to it's cluster
        self.assertEqual(len(clusters.genes["NM_022114.2"]), 1)
        g = clusters.genes["NM_022114.2"][0]
        cl = g.clusterObj
        self.assertEqual(len(cl), 2)
        self.assertTrue((cl[0].gene == "NM_199454.1") or (cl[1].gene == "NM_199454.1"))
        

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ReadTests))
    return suite

if __name__ == '__main__':
    unittest.main()
