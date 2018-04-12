from . import support
import unittest, codecs

from html5lib.inputstream import HTMLInputStream

class HTMLInputStreamShortChunk(HTMLInputStream):
    _defaultChunkSize = 2

class HTMLInputStreamTest(unittest.TestCase):

    def test_char_ascii(self):
        stream = HTMLInputStream("'", encoding='ascii')
        self.assertEqual(stream.charEncoding[0], 'ascii')
        self.assertEqual(stream.char(), "'")

    def test_char_null(self):
        stream = HTMLInputStream("\x00")
        self.assertEqual(stream.char(), '\ufffd')

    def test_char_utf8(self):
        stream = HTMLInputStream('\u2018'.encode('utf-8'), encoding='utf-8')
        self.assertEqual(stream.charEncoding[0], 'utf-8')
        self.assertEqual(stream.char(), '\u2018')

    def test_char_win1252(self):
        stream = HTMLInputStream("\xa9\xf1\u2019".encode('windows-1252'))
        self.assertEqual(stream.charEncoding[0], 'windows-1252')
        self.assertEqual(stream.char(), "\xa9")
        self.assertEqual(stream.char(), "\xf1")
        self.assertEqual(stream.char(), "\u2019")

    def test_bom(self):
        stream = HTMLInputStream(codecs.BOM_UTF8 + "'")
        self.assertEqual(stream.charEncoding[0], 'utf-8')
        self.assertEqual(stream.char(), "'")

    def test_utf_16(self):
        stream = HTMLInputStream((' '*1025).encode('utf-16'))
        self.assertTrue(stream.charEncoding[0] in ['utf-16-le', 'utf-16-be'], stream.charEncoding)
        self.assertEqual(len(stream.charsUntil(' ', True)), 1025)

    def test_newlines(self):
        stream = HTMLInputStreamShortChunk(codecs.BOM_UTF8 + "a\nbb\r\nccc\rddddxe")
        self.assertEqual(stream.position(), (1, 0))
        self.assertEqual(stream.charsUntil('c'), "a\nbb\n")
        self.assertEqual(stream.position(), (3, 0))
        self.assertEqual(stream.charsUntil('x'), "ccc\ndddd")
        self.assertEqual(stream.position(), (4, 4))
        self.assertEqual(stream.charsUntil('e'), "x")
        self.assertEqual(stream.position(), (4, 5))

    def test_newlines2(self):
        size = HTMLInputStream._defaultChunkSize
        stream = HTMLInputStream("\r" * size + "\n")
        self.assertEqual(stream.charsUntil('x'), "\n" * size)

    def test_position(self):
        stream = HTMLInputStreamShortChunk(codecs.BOM_UTF8 + "a\nbb\nccc\nddde\nf\ngh")
        self.assertEqual(stream.position(), (1, 0))
        self.assertEqual(stream.charsUntil('c'), "a\nbb\n")
        self.assertEqual(stream.position(), (3, 0))
        stream.unget("\n")
        self.assertEqual(stream.position(), (2, 2))
        self.assertEqual(stream.charsUntil('c'), "\n")
        self.assertEqual(stream.position(), (3, 0))
        stream.unget("\n")
        self.assertEqual(stream.position(), (2, 2))
        self.assertEqual(stream.char(), "\n")
        self.assertEqual(stream.position(), (3, 0))
        self.assertEqual(stream.charsUntil('e'), "ccc\nddd")
        self.assertEqual(stream.position(), (4, 3))
        self.assertEqual(stream.charsUntil('h'), "e\nf\ng")
        self.assertEqual(stream.position(), (6, 1))

    def test_position2(self):
        stream = HTMLInputStreamShortChunk("abc\nd")
        self.assertEqual(stream.position(), (1, 0))
        self.assertEqual(stream.char(), "a")
        self.assertEqual(stream.position(), (1, 1))
        self.assertEqual(stream.char(), "b")
        self.assertEqual(stream.position(), (1, 2))
        self.assertEqual(stream.char(), "c")
        self.assertEqual(stream.position(), (1, 3))
        self.assertEqual(stream.char(), "\n")
        self.assertEqual(stream.position(), (2, 0))
        self.assertEqual(stream.char(), "d")
        self.assertEqual(stream.position(), (2, 1))

def buildTestSuite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

def main():
    buildTestSuite()
    unittest.main()

if __name__ == '__main__':
    main()
