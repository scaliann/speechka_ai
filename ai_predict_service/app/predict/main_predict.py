import pickle
from pathlib import Path

import numpy as np
from tensorflow.keras.models import load_model
from kapre.time_frequency import STFT, Magnitude, ApplyFilterbank, MagnitudeToDecibel
from sklearn.preprocessing import LabelEncoder

from app.utils.clean import downsample_mono, envelope

MODEL_PATH = Path("./app/utils/models/conv2d.h5")
LABEL_PATH = Path("./app//utils/logs/label_encoder.pkl")
SAMPLE_RATE = 44_100
DT_SEC = 1.0
THRESHOLD = 100

_model = load_model(
    MODEL_PATH,
    custom_objects={
        "STFT": STFT,
        "Magnitude": Magnitude,
        "ApplyFilterbank": ApplyFilterbank,
        "MagnitudeToDecibel": MagnitudeToDecibel,
    },
)
# Загружаем label-encoder
with LABEL_PATH.open("rb") as f:
    _le: LabelEncoder = pickle.load(f)
_CLASSES = list(_le.classes_)


def _predict_one(
    wav_path: Path,
) -> str:
    """Возвращает метку для одного WAV-файла."""
    rate, wav = downsample_mono(str(wav_path), SAMPLE_RATE)
    mask, _ = envelope(wav, rate, threshold=THRESHOLD)
    clean_wav = wav[mask]

    step = int(SAMPLE_RATE * DT_SEC)
    batch = []
    for i in range(0, clean_wav.shape[0], step):
        sample = clean_wav[i : i + step].reshape(-1, 1)
        if sample.shape[0] < step:  # дополняем нулями
            padded = np.zeros((step, 1), np.float32)
            padded[: sample.shape[0], 0] = sample[:, 0]
            sample = padded
        batch.append(sample)

    X = np.asarray(batch, dtype=np.float32)
    y_pred = _model.predict(X, verbose=0)
    y_mean = y_pred.mean(axis=0)
    return _CLASSES[int(np.argmax(y_mean))]
