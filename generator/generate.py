import gpt_2_simple as gpt2
from generator.utils import utils

sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess)


def generate(first_person, second_person):
    first_tag = utils.tag(first_person)
    second_tag = utils.tag(second_person)

    prefix = f'''\
{first_tag}
How are you?
{first_tag}

{second_tag}
    '''

    gpt2.generate(sess, prefix=prefix, truncate=second_tag)
