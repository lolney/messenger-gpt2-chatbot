from . import output_parser as output_parser
import gpt_2_simple as gpt2
import os
import gc
import textwrap
import tensorflow
from . import session as sess
from .utils.utils import tag
from .utils.log_process_stats import log_process_stats
import logging
log = logging.getLogger('app.create_app')

len_history = 1
package_directory = os.path.dirname(os.path.abspath(__file__))
checkpoint_dir = os.path.join(
    package_directory, 'checkpoint')


def perform(**args):
    return Generator(**args).generate()


class Generator:

    def __init__(
        self,
        session=None,
        first_person=None,
        second_person=None,
        truncate=False,
        text="How are you?",
        **rest
    ):
        self.session = session if session is not None else sess.load()
        self.first_person = first_person
        self.second_person = second_person
        self.truncate = truncate
        self.text = text
        self.other_args = rest

    def generate(self):
        prefix = self.make_prefix()
        log_process_stats()
        generated_text = gpt2.generate(
            self.session,
            checkpoint_dir=checkpoint_dir,
            prefix=prefix,
            return_as_list=True,
            **self.other_args
        )
        self.cleanup()
        log_process_stats()
        log.info(f"generated text: {generated_text}")
        parsed_lines = output_parser.perform('\n'.join(generated_text))
        log.info(f"parsed lines: {parsed_lines}")

        if not parsed_lines or len(parsed_lines) < len_history + 1:
            return None

        if self.truncate:
            return self.truncate_output(
                parsed_lines[len_history:]
            )

        return parsed_lines[1:]

    def truncate_output(self, parsed_lines):
        if not parsed_lines or len(parsed_lines) == 0:
            return None

        return list(filter(
            lambda line: line["person"] == self.second_person,
            parsed_lines
        ))

    def make_prefix(self):
        first_tag = tag(self.first_person)
        second_tag = tag(self.second_person)

        return textwrap.dedent(f'''\
            {first_tag}
            {self.text}
            {first_tag}

            {second_tag}''')

    def cleanup(self):
        tensorflow.reset_default_graph()
        self.session.close()
        gc.collect()
