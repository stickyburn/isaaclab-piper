#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_SOURCE="${REPO_ROOT}/piper_sim/source/piper_sim"

ASSETS_DIR="${REPO_ROOT}/assets/props"
DOWNLOADS_DIR="/tmp/piper_sim_downloads"
ASSETS_ZIP_URL="https://drive.google.com/uc?id=13GMQuDB87-cP5kB_MRCS5-M5Nnid1Tkq"
ASSETS_ZIP_NAME="piper_sim_assets.zip"

echo "Repo root: ${REPO_ROOT}"

# check IsaacLab
if ! python - <<'PY'
import importlib.util
raise SystemExit(0 if importlib.util.find_spec("isaaclab") else 1)
PY
then
  if [[ -f "/opt/isaaclab-env/bin/activate" ]]; then
    source "/opt/isaaclab-env/bin/activate"
    echo "Activated Isaac Lab venv."
  else
    echo "Isaac Lab venv not active and activation script not found." >&2
    exit 1
  fi
fi

echo "Installing piper_sim as an Isaac Lab extension (editable)."
python -m pip install -e "${REPO_ROOT}/piper_sim"

# create dirs
mkdir -p "${ASSETS_DIR}"
mkdir -p "${DOWNLOADS_DIR}"

download_and_extract() {
  local url="$1"
  local zip_path="${DOWNLOADS_DIR}/${ASSETS_ZIP_NAME}"

  echo "Downloading assets from ${url}"
  python -m gdown --fuzzy "${url}" -O "${zip_path}"

  echo "Extracting ${zip_path} -> ${ASSETS_DIR}"
  unzip -q "${zip_path}" -d "${ASSETS_DIR}"

  rm -f "${zip_path}"
}

# gdown for drive
python -m pip install gdown

download_and_extract "${ASSETS_ZIP_URL}"

rm -rf "${DOWNLOADS_DIR}" 2>/dev/null || true

echo ""
echo "✓ Setup complete!"
echo ""
echo "Assets installed to: ${ASSETS_DIR}"
echo ""
echo "You can now:"
echo "  1. Visualize the scene:   python piper_sim/scripts/visualize.py"
echo "  2. Test with random actions: python piper_sim/scripts/random_agent.py"
echo "  3. Train:                 python piper_sim/scripts/train.py"
echo ""
