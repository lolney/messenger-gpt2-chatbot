import re


def perform(*args):
    return OutputParser(*args).parse()


class OutputParser:

    def __init__(self, output):
        self.remaining_lines = iter(output.split('\n'))

    def parse(self):
        lines = []

        while True:
            person = self.next_person()
            if not person:
                break
            lines.append(person)

        return lines

    def next_person(self):
        person = None
        lines = []

        for line in self.remaining_lines:
            next_person = self.match_person(line)
            if person and not next_person:
                lines.append(line)
            elif person and next_person:
                if next_person == person:
                    return {"person": person, "text": "\n".join(lines)}
                else:
                    person = next_person
                    lines = []
            elif not person and next_person:
                person = next_person

        return None

    def match_person(self, line):
        m = re.match(r"<\|(.*)\|>", line)
        if m:
            try:
                return m.group(1)
            except IndexError:
                return None
