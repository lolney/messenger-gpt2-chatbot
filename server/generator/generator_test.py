import gpt_2_simple
import generator.generator as generator


class MockSession:

    def close(self):
        pass


text1 = '''
<|Ted Olney-Bell|>
Nina Pat?
<|Ted Olney-Bell|>

<|Peter Olney|>
YES
<|Peter Olney|>

<|Luke Olney|>
Peter missed your call.
<|Luke Olney|>

<|Luke Olney|>
You called Ted.
<|Luke Olney|>

<|Luke Olney|>
Ted missed your video chat.
<|Luke Olney|>

<|Luke Olney|>
Ted missed your video chat.
<|Luke Olney|>

<|Peter Olney|>
Luke missed your video chat.
<|Peter Olney|>

<|Luke Olney|>
Ted missed your video chat.
<|Luke Olney|
'''

params1 = {
    'session': MockSession(),
    'first_person': 'Ted Olney-Bell',
    'second_person': 'Peter Olney',
    'truncate': True
}

lines1 = [
    {'person': 'Peter Olney', 'text': "YES"},
    {'person': 'Peter Olney', 'text': "Luke missed your video chat."},
]


def create_mock_generate(text):
    def mock_generate(session, **args):
        return text
    return mock_generate


cases = [
    {"params": params1, "lines": lines1, "text": text1},
]


class TestGenerator(object):
    def test_generate(self, monkeypatch):
        for case in cases:
            text = [case['text']]
            params = case['params']
            lines = case['lines']
            monkeypatch.setattr(gpt_2_simple, "generate",
                                create_mock_generate(text))
            result = generator.perform(**params)

            assert result == lines
