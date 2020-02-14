import gpt_2_simple as gpt2
import os
import logging
log = logging.getLogger('app.create_app')

package_directory = os.path.dirname(os.path.abspath(__file__))
checkpoint_dir = os.path.join(
    package_directory, 'checkpoint')


def load():
    sess = gpt2.start_tf_sess(threads=1)
    gpt2.load_gpt2(sess, checkpoint_dir=checkpoint_dir)
    log.info('Finished loading model')
    return sess
