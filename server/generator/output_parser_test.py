import generator.output_parser as output_parser
import textwrap
import unittest

text1 = textwrap.dedent('''
<|Second M Person|>
Test
<|Second M Person|>

<|First Person|>
Test
Test2
<|First Person|>

<|Second M Person|>
Test3
<|Second M Person|>

<|Second M Person|>
Test4
<|Second M Person|>
''')

results1 = [
    {
        "person": "Second M Person",
        "text": "Test"
    },
    {
        "person": "First Person",
        "text": "Test\nTest2"
    },
    {
        "person": "Second M Person",
        "text": "Test3"
    },
    {
        "person": "Second M Person",
        "text": "Test4"
    }
]

text2 = textwrap.dedent('''
ope.com/2017/03/28/california-shines-light-on-local-activities-over-san-francisco-13-years-ago/

http://www.sfmazbay.com/sf/sfgate/2017/05/the-friefures-in-california/142712793.php
<|First Person|>

<|Third Person|>
http://kc.sfm.edu/newsroom/index.cfm?id=sfnewsroom
<|Third Person|>

<|First Person|>
Do birds in the sky actually have the same brightness as our own sun?
<|First Person|>
''')

results2 = [
    {
        "person": "Third Person",
        "text": "http://kc.sfm.edu/newsroom/index.cfm?id=sfnewsroom"
    },
    {
        "person": "First Person",
        "text": "Do birds in the sky actually have the same brightness as our own sun?"
    }
]

text3 = '''
<|First Person|>

<|Third Person|>
http://kc.sfm.edu/newsroom/index.cfm?id=sfnewsroom
<|Third Person|>

<|First Person|>
'''

results3 = [
    {
        "person": "Third Person",
        "text": "http://kc.sfm.edu/newsroom/index.cfm?id=sfnewsroom"
    }
]


class TestOutputParser(unittest.TestCase):

    def test_parser(self):
        for msg, expected in zip(
                [text1, text2, text3], [results1, results2, results3]
        ):
            with self.subTest(msg[:10]):
                result = output_parser.perform(msg)
                self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
