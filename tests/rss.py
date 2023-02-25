import unittest

from src.rss.downloader import RssParser

testRssPath = "tests/data/rss.xml"
testRssStr = ""

with open(testRssPath) as f:
    testRssStr = f.read()
    # import json
    # data=json.dumps(entries)
    # with open("/tmp/output.json","w") as f:
    #    f.write(data)


class TestRss(unittest.TestCase):
    def test_parse(self):
        entries = RssParser.parseFeed(data=testRssStr)
        self.assertTrue(len(entries) == 24)

    def test_filter(self):
        entries = RssParser.parseFeed(data=testRssStr)
        


if __name__ == "__main__":
    unittest.main()
