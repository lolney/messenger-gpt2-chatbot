import json
import os

dirname = os.path.dirname(__file__)
data_file = os.path.join(
    dirname, "../Chatistics/exports/chatistics_export_2020-02-02_15-11-38.json")
training_file = os.path.join(dirname, 'data/training.txt')


def create_metadata_tag(name):
    return f"<|{name}|>"


with open(data_file) as json_fp:
    data = json.load(json_fp)
    with open(training_file, 'w') as txt_fp:
        for datum in data[::-1]:
            sender_name = datum['senderName']
            lines = [
                create_metadata_tag(sender_name),
                datum['text'],
                create_metadata_tag(sender_name),
                '\n',
            ]
            txt_fp.write('\n'.join(lines))
