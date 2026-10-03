import re
import sys
from pathlib import Path

import spacy


TARGET_WORDS = 100
MAX_WORDS = 140


def split_into_chunks(text):
    nlp = spacy.blank("en")
    nlp.add_pipe("sentencizer")

    paragraphs = re.split(r"\n\s*\n", text.strip())
    chunks = []

    for paragraph in paragraphs:
        doc = nlp(paragraph)

        current = []
        current_words = 0

        for sentence in doc.sents:
            sentence = sentence.text.strip()
            words = len(sentence.split())

            if current and current_words + words > MAX_WORDS:
                chunks.append(" ".join(current))
                current = []
                current_words = 0

            current.append(sentence)
            current_words += words

            if current_words >= TARGET_WORDS:
                chunks.append(" ".join(current))
                current = []
                current_words = 0

        if current:
            chunks.append(" ".join(current))

    return chunks


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} INPUT.txt OUTPUT_DIR")
        sys.exit(1)

    source = Path(sys.argv[1])
    output = Path(sys.argv[2])
    output.mkdir(parents=True, exist_ok=True)

    text = source.read_text(encoding="utf-8")
    chunks = split_into_chunks(text)

    for number, chunk in enumerate(chunks, 1):
        path = output / f"{number:04d}.txt"
        path.write_text(chunk + "\n", encoding="utf-8")

    print(f"Created {len(chunks)} chunks.")


if __name__ == "__main__":
    main()
