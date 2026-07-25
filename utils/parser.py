def parse_sections(text):

    sections = {}

    current = None

    for line in text.splitlines():

        if line.startswith("##"):

            current = line.replace("##", "").strip()

            sections[current] = ""

        elif current:

            sections[current] += line + "\n"

    return sections