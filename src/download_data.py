"""Download TRACE and MALT datasets from Hugging Face and save locally."""

import os
import dotenv
from pathlib import Path

from datasets import load_dataset
from huggingface_hub import login

dortenv.load_dotenv()  # Load .env if it exists, to get HF token from environment variables

ROOT = Path(__file__).resolve().parent.parent
TRACE_DIR = ROOT / "data" / "trace"
MALT_DIR = ROOT / "data" / "malt"


def get_token():
    token = os.environ.get("HF_TOKEN") or os.environ.get("hugging_face_token")
    if not token:
        env_path = ROOT / ".env"
        if env_path.exists():
            for line in env_path.read_text().splitlines():
                if line.startswith("hugging_face_token="):
                    token = line.split("=", 1)[1].strip()
    if not token:
        raise RuntimeError("No HF token found. Set HF_TOKEN or add to .env")
    return token


def download_trace():
    print("Downloading TRACE dataset...")
    ds = load_dataset("PatronusAI/trace-dataset")
    TRACE_DIR.mkdir(parents=True, exist_ok=True)
    ds["train"].save_to_disk(str(TRACE_DIR))
    print(f"Saved {ds['train'].num_rows} TRACE trajectories to {TRACE_DIR}")


def download_malt():
    print("Downloading MALT dataset...")
    ds = load_dataset("metr-evals/malt-public")
    MALT_DIR.mkdir(parents=True, exist_ok=True)
    for split in ds:
        out = MALT_DIR / split
        ds[split].save_to_disk(str(out))
        print(f"Saved {ds[split].num_rows} MALT rows ({split}) to {out}")


def main():
    login(token=get_token())
    download_trace()
    download_malt()
    print("\nDone. All datasets saved to data/")


if __name__ == "__main__":
    main()
