from pathlib import Path
import time

import soundfile as sf
from kokoro import KPipeline


CHUNKS_DIR = Path("chunks")
AUDIO_DIR = Path("audio")
VOICE = "am_adam"
LANG_CODE = "a"
SAMPLE_RATE = 24000


def main():
    AUDIO_DIR.mkdir(exist_ok=True)

    chunks = sorted(CHUNKS_DIR.glob("*.txt"))

    if not chunks:
        print("No chunks found.")
        return

    print(f"Found {len(chunks)} chunks.")
    print(f"Voice: {VOICE}")

    pipeline = KPipeline(lang_code=LANG_CODE)

    for i, chunk_path in enumerate(chunks, 1):
        audio_path = AUDIO_DIR / f"{chunk_path.stem}.wav"

        if audio_path.exists():
            print(f"[{i}/{len(chunks)}] SKIP {chunk_path.name}")
            continue

        print(f"[{i}/{len(chunks)}] Generating {chunk_path.name}...", flush=True)

        text = chunk_path.read_text(encoding="utf-8").strip()

        start = time.time()

        for _, _, audio in pipeline(text, voice=VOICE):
            sf.write(audio_path, audio, SAMPLE_RATE)
            break

        elapsed = time.time() - start

        print(
            f"    -> {audio_path.name} "
            f"({elapsed:.1f}s)",
            flush=True,
        )

    print("Done.")


if __name__ == "__main__":
    main()
