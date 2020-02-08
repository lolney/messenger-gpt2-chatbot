import generator.output_parser as output_parser
import gpt_2_simple as gpt2
import os
import textwrap
import generator.session as sess
from generator.utils.utils import tag

len_history = 1
package_directory = os.path.dirname(os.path.abspath(__file__))
checkpoint_dir = os.path.join(
    package_directory, 'checkpoint')


def perform(session, **args):
    return Generator(session, **args).generate()


class Generator:

    def __init__(self, session, first_person=None, second_person=None, truncate=False):
        self.session = sess.load()
        self.first_person = first_person
        self.second_person = second_person
        self.truncate = truncate

    def generate(self):
        prefix = self.make_prefix()
        generated_text = gpt2.generate(
            self.session, checkpoint_dir=checkpoint_dir, prefix=prefix, return_as_list=True)
        parsed_lines = output_parser.perform('\n'.join(generated_text))

        if not parsed_lines or len(parsed_lines) < len_history + 1:
            return None

        # todo: include_prefix=true, truncate="<tag>\n\n"
        if self.truncate:
            first, second = parsed_lines
            return second

        return parsed_lines[1:]

    def make_prefix(self):
        first_tag = tag(self.first_person)
        second_tag = tag(self.second_person)

        return textwrap.dedent(f'''\
            {first_tag}
            How are you?
            {first_tag}

            {second_tag}''')
