import re
import unittest

import yaml
from qzonebackend.qzfeedparser import QZFeedParser as Parser


class ParserTest(unittest.TestCase):
    def testTransform(self):
        htmls = None
        with open('tmp/feeds.yaml', encoding='utf8') as f:
            feeds = yaml.load_all(f)
            htmls = [i['html'] for i in feeds if i['appid'] == '311']
        for i in htmls:
            with open('tmp/html/%d.html' % hash(i), 'w', encoding='utf8') as f:
                f.write(i)

    def testLikeData(self):
        with open('tmp/html/-217964352468340141.html') as f:
            psr = Parser(f.read())
            tp = psr.parseLikeData()
            print(tp)
            self.assertTrue(len(tp) == 5)

    def testMore(self):
        with open('tmp/html/8853557023188502000.html', encoding='utf8') as f:
            psr = Parser(f.read())
            self.assertTrue(psr.isCut())
