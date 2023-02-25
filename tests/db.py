import unittest

from src.rss.dao import AddNewRssSub, IsTorrentAdded,ListRssSub,  MarkTorrents, NewDBManager,UpdateRssSub

dm=NewDBManager()
class TestRssSubDB(unittest.TestCase):
    def test_mark(self):
        cur =dm.NewCur()
        urlList=["http://www.baidu.com","https://www.baidu.com","https://www.google.com"]
        for url in urlList:
            self.assertEqual(IsTorrentAdded(cur=cur,url=url),False)

        MarkTorrents(cur=cur,urlList=urlList)
        for url in urlList:
            self.assertEqual(IsTorrentAdded(cur=cur,url=url),True)
    def test_add(self):
        cur=dm.NewCur()

        pre=ListRssSub(cur=cur)
        print(pre)
        AddNewRssSub(cur=cur,url="www.baidu.com",name="test",download_dir="/tmp",filters="")
        res=ListRssSub(cur=cur)
        self.assertTrue(len(pre)+1==len(res))
        print(res)

        cur.close()
    def test_update(self):
        cur=dm.NewCur()
        AddNewRssSub(cur=cur,url="www.baidu.com",name="test",download_dir="/tmp",filters="")
        pre=ListRssSub(cur=cur)
        print(pre)
        e=pre[len(pre)-1]

        UpdateRssSub(cur=cur,id=e.id,url="test_url",name="test_name",download_dir="test_dir",filters="test_filters")
        res=ListRssSub(cur=cur)

        e=res[len(res)-1]
        
        self.assertEqual(len(pre),len(res))
        self.assertEqual(e.url,"test_url")
        self.assertEqual(e.name,"test_name")
        self.assertEqual(e.download_dir,"test_dir")
        self.assertEqual(e.filters,"test_filters")
        print(res)

        cur.close()

        


if __name__ == "__mainm_":
    unittest.main()
