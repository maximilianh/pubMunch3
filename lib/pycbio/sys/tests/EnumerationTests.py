# Copyright 2006-2012 Mark Diekhans
import unittest, sys, pickle
if __name__ == '__main__':
    sys.path.append("../../..")
from pycbio.sys.Enumeration import Enumeration
from pycbio.sys.TestCaseBase import TestCaseBase

class EnumerationTests(TestCaseBase):

    def __getColors(self):
	return Enumeration("Colors", ["red", "green", "blue"])

    def __checkColors(self, Colors):
        self.assertEqual(Colors.red.name, "red")
        self.assertEqual(Colors.green.name, "green")
        self.assertEqual(Colors.blue.name, "blue")
        self.assertTrue(Colors.red < Colors.blue)
        self.assertTrue(Colors.red == Colors.red)
        self.assertTrue(Colors.red != Colors.blue)
        self.assertTrue(Colors.red != None)
        self.assertTrue(None != Colors.red)

    def testBasics(self):
        Colors = self.__getColors()
        self.__checkColors(Colors)

    def testLookup(self):
        Colors = self.__getColors()
        self.assertTrue(Colors.red == Colors.lookup("red"))
        self.assertTrue(Colors.green == Colors.lookup("green"))
        self.assertTrue(Colors.green != Colors.lookup("red"))

    def testAliases(self):
        Name = Enumeration("Name", ["Fred",  ("Rick", "Richard", ("Dick", "HeyYou")), ("Bill", "Willian")])
        self.assertEqual(Name.lookup("Richard"), Name.Rick)
        self.assertTrue(Name.lookup("Richard") is Name.Rick)
        self.assertEqual(Name.lookup("Dick"), Name.Rick)
        self.assertTrue(Name.lookup("Dick") is Name.Rick)
        self.assertTrue(Name.lookup("Rick") == Name.Rick)
        self.assertTrue(Name.lookup("HeyYou") == Name.Rick)
        self.assertTrue(Name.lookup("Fred") == Name.Fred)
        self.assertTrue(Name.lookup("Fred") is Name.Fred)
        self.assertTrue(str(Name.Rick) == "Richard")

    def testAliasesBug1(self):
        "forgot comma in one-element tuple"
        try:
            Stat = Enumeration("Stat",
                               ["okay",
                                ("notConserved","notConserved", ("no_alignment")),
                                "bad_3_splice", "bad_5_splice"])
            if __debug__:
                self.fail("should have raised exception")
        except TypeError:
            pass
        
    def testBitSetValues(self):
        Stat = Enumeration("Stat",
                           ["okay",
                            ("notConserved","notConserved", ("no_alignment",)),
                            "bad_3_splice", "bad_5_splice"],
                           bitSetValues=True)
        self.assertEqual(Stat.okay, 1)
        self.assertEqual(Stat.notConserved, 2)
        self.assertEqual(Stat.bad_5_splice, 8)
        self.assertEqual(int(Stat.bad_5_splice), 8)
        self.assertEqual(Stat.maxNumValue, 8)
        vals = Stat.getValues(9)
        self.assertEqual(len(vals), 2)
        self.assertTrue(vals[0] is Stat.okay)
        self.assertTrue(vals[1] is Stat.bad_5_splice)

    def testSetOps(self):
        Colors = self.__getColors()
        colSet = set([Colors.blue, Colors.green])
        self.assertTrue(Colors.green in colSet)
        self.assertFalse(Colors.red in colSet)

    def testNumberDef(self):
        NumDef = Enumeration("NumDef",
                             (("neg", None, None, -2),
                              ("zero", None, None, 0),
                              ("pos", None, None, 2),
                              ("big", None, None, 3)))
        values = [(str(v), int(v)) for v in NumDef.values]
        self.assertEqual(values, [('neg', -2), ('zero', 0), ('pos', 2), ('big', 3)])
        self.assertEqual(NumDef.getByNumValue(2), NumDef.pos)

    def FIXME_testErrors(self):
        Colors = self.__getColors()
        # check if immutable
        try:
            Colors.red.name = "purple"
            self.fail("immutable object modified")
        except TypeError:
            pass
        try:
            Colors.red = None
            self.fail("immutable object modified")
        except TypeError:
            pass

    def __testPickleProt(self, prot):
        Colors = self.__getColors()
        stuff = {}
        stuff[Colors.red] = "red one"
        stuff[Colors.green] = "green one"
        world = pickle.dumps((Colors, stuff), prot)
        Color2, stuff2 = pickle.loads(world)

        self.assertTrue(Color2.red in stuff2)
        self.assertTrue(Color2.green in stuff2)
        self.__checkColors(Color2)

    def testPickle2(self):
        self.assertTrue(pickle.HIGHEST_PROTOCOL == 2)
        self.__testPickleProt(2)
    def testPickle1(self):
        self.__testPickleProt(1)
    def testPickle0(self):
        self.__testPickleProt(0)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(EnumerationTests))
    return suite

if __name__ == '__main__':
    unittest.main()
