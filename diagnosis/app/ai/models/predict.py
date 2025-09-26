import pickle
from pathlib import Path
import numpy as np
from tensorflow.keras.models import load_model
from kapre.time_frequency import STFT, Magnitude, ApplyFilterbank, MagnitudeToDecibel
from sklearn.preprocessing import LabelEncoder
from app.ai.clean import downsample_mono, envelope

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models/conv2d.h5"
LABEL_PATH = BASE_DIR / "models/label_encoder.pkl"

SAMPLE_RATE = 44_100
DT_SEC = 1.0
THRESHOLD = 400
_EPS = 1e-12

_model = load_model(
    MODEL_PATH,
    compile=False,
    custom_objects={
        "STFT": STFT,
        "Magnitude": Magnitude,
        "ApplyFilterbank": ApplyFilterbank,
        "MagnitudeToDecibel": MagnitudeToDecibel,
    },
)

with LABEL_PATH.open("rb") as f:
    _le: LabelEncoder = pickle.load(f)
_CLASSES: list[str] = list(_le.classes_)


def predict_one(wav_path: Path) -> dict:
    """
    Прогоняет один WAV-файл через модель и возвращает JSON-подобный dict:
    {
      "filename": "...",
      "predicted_index": int,
      "predicted_class": str,
      "probs": {"class_a": 0.12, "class_b": 0.34, ...},  # суммы = 1.0
    }
    """

    wav_path = Path(wav_path)
    if not wav_path.exists():
        raise FileNotFoundError(f"File not found: {wav_path}")

    rate, wav = downsample_mono(str(wav_path), SAMPLE_RATE)
    mask, _ = envelope(wav, rate, threshold=THRESHOLD)
    if not np.any(mask):
        soft_thr = max(1, THRESHOLD)
        mask, _ = envelope(wav, rate, threshold=soft_thr)

    clean = wav[mask]
    step = int(SAMPLE_RATE * DT_SEC)
    batch: list[np.ndarray] = []

    if clean.size == 0:
        batch.append(np.zeros((step, 1), np.float32))
    else:
        clean = clean.astype(np.float32) / 32768.0
        for i in range(0, clean.shape[0], step):
            chunk = clean[i : i + step]
            real_len = chunk.shape[0]

            if real_len < int(0.6 * step):
                continue

            if real_len < step:
                pad = np.zeros((step, 1), np.float32)
                pad[:real_len, 0] = chunk.reshape(-1)
                chunk = pad
            else:
                chunk = chunk.reshape(-1, 1)

            batch.append(chunk)

    if not batch:
        batch = [np.zeros((step, 1), np.float32)]

    X = np.asarray(batch, dtype=np.float32)

    y_chunks = _model.predict(X, verbose=0)
    geo = np.exp(np.log(y_chunks + _EPS).mean(axis=0))
    probs = geo / geo.sum()

    cls_idx = int(np.argmax(probs))
    cls_name = _CLASSES[cls_idx]

    return {
        "filename": wav_path.name,
        "predicted_index": cls_idx,
        "predicted_class": str(cls_name),
        "probs": {str(c): float(p) for c, p in zip(_CLASSES, probs)},
    }
