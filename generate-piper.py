from pathlib import Path
import subprocess
import time


CHUNKS_DIR = Path("chunks")
AUDIO_DIR = Path("audio")

PIPER = "piper"
MODEL = Path("models/de_DE-karlsson-low.onnx")

SAMPLE_RATE = 22050


def main():
    AUDIO_DIR.mkdir(exist_ok=True)

    chunks = sorted(CHUNKS_DIR.glob("*.txt"))

    if not chunks:
        print("No chunks found.")
        return

    print(f"Found {len(chunks)} chunks.")
    print(f"Model: {MODEL}")

    if not MODEL.exists():
        print(f"Model not found: {MODEL}")
        return

    for i, chunk_path in enumerate(chunks, 1):
        audio_path = AUDIO_DIR / f"{chunk_path.stem}.wav"

        if audio_path.exists():
            print(f"[{i}/{len(chunks)}] SKIP {chunk_path.name}")
            continue

        print(
            f"[{i}/{len(chunks)}] Generating {chunk_path.name}...",
            flush=True,
        )

        text = chunk_path.read_text(encoding="utf-8").strip()

        if not text:
            print("    -> empty chunk, skipping")
            continue

        start = time.time()

        try:
            subprocess.run(
                [
                    PIPER,
                    "--model",
                    str(MODEL),
                    "--output_file",
                    str(audio_path),
                ],
                input=text,
                text=True,
                check=True,
            )
        except subprocess.CalledProcessError as e:
            print(f"    -> FAILED (exit code {e.returncode})")
            continue

        elapsed = time.time() - start

        print(
            f"    -> {audio_path.name} "
            f"({elapsed:.1f}s)",
            flush=True,
        )

    print("Done.")


if __name__ == "__main__":
    main()
