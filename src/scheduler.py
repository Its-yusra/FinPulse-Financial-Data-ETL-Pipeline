
import subprocess
import sys
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
PYTHON = sys.executable
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "scheduler.log"


def run_pipeline():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(f"\n\n[{timestamp}] Pipeline started\n")

        result = subprocess.run(
            [PYTHON, str(BASE_DIR / "src" / "main.py")],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
        )

        log.write(result.stdout or "")
        if result.stderr:
            log.write("\nERRORS / WARNINGS:\n")
            log.write(result.stderr)

        status = "SUCCESS" if result.returncode == 0 else "FAILED"
        log.write(f"\n[{timestamp}] Status: {status}\n")

        print(f"Pipeline status: {status}")
        print(f"Log saved to: {LOG_FILE}")

        if result.returncode != 0:
            print(result.stderr)


if __name__ == "__main__":
    run_pipeline()
