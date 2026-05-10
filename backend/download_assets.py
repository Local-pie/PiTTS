import os
import urllib.request
import tarfile

MODELS_DIR = "models"
os.makedirs(MODELS_DIR, exist_ok=True)

# 1. Download Piper Linux binary
# Using the stable 2023.11.14-2 release for linux aarch64 (Raspberry Pi)
piper_url = "https://github.com/rhasspy/piper/releases/download/2023.11.14-2/piper_linux_aarch64.tar.gz"
piper_tar = os.path.join(MODELS_DIR, "piper.tar.gz")

print("Downloading Piper Linux binary...")
urllib.request.urlretrieve(piper_url, piper_tar)

print("Extracting Piper...")
with tarfile.open(piper_tar, "r:gz") as tar:
    tar.extractall(path=MODELS_DIR)

# Cleanup the tar file
os.remove(piper_tar)

# 2. Download Voices
# Format: { "voice_name": "base_huggingface_url" }
voices = {
    "en_US-lessac-medium": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/medium/en_US-lessac-medium",
    "en_US-amy-medium": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/amy/medium/en_US-amy-medium",
    "fr_FR-siwis-medium": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/fr/fr_FR/siwis/medium/fr_FR-siwis-medium"
}

for voice, base_url in voices.items():
    print(f"Downloading voice: {voice}...")
    onnx_file = os.path.join(MODELS_DIR, f"{voice}.onnx")
    json_file = os.path.join(MODELS_DIR, f"{voice}.onnx.json")
    
    if not os.path.exists(onnx_file):
        urllib.request.urlretrieve(f"{base_url}.onnx", onnx_file)
    if not os.path.exists(json_file):
        urllib.request.urlretrieve(f"{base_url}.onnx.json", json_file)

print("All assets downloaded successfully into /models directory!")
