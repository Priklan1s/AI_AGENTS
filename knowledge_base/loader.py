import os


def load_knowledge(path):

    texts = []

    for file in os.listdir(path):

        if file.endswith(".txt"):

            with open(
                os.path.join(path, file),
                encoding="utf-8"
            ) as f:

                texts.append(f.read())

    return texts