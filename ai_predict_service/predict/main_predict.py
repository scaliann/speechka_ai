# predict.py
import pickle
from collections import Counter
from pathlib import Path
from typing import Sequence, Dict

import numpy as np
from tensorflow.keras.models import load_model
from kapre.time_frequency import STFT, Magnitude, ApplyFilterbank, MagnitudeToDecibel
from sklearn.preprocessing import LabelEncoder

from utils.clean import downsample_mono, envelope  # ваш модуль

# --- общие настройки (можно передавать параметрами) -------------------------
MODEL_PATH   = Path("./utils/models/conv2d.h5")
LABEL_PATH   = Path("./utils/logs/label_encoder.pkl")
SAMPLE_RATE  = 44_100
DT_SEC       = 1.0
THRESHOLD    = 100
# -----------------------------------------------------------------------------

# Загружаем модель один раз при импорте, чтобы не тянуть веса каждый вызов
_model = load_model(
    MODEL_PATH,
    custom_objects={
        'STFT': STFT,
        'Magnitude': Magnitude,
        'ApplyFilterbank': ApplyFilterbank,
        'MagnitudeToDecibel': MagnitudeToDecibel,
    },
)
# Загружаем label-encoder
with LABEL_PATH.open("rb") as f:
    _le: LabelEncoder = pickle.load(f)
_CLASSES = list(_le.classes_)


def _predict_one(wav_path: Path) -> str:
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


def majority_class(results: Dict[int, str]) -> str:
    """
    Возвращает класс, который встречается чаще других.
    """
    if not results:
        return "Нет данных"

    counts = Counter(results.values())          # {'burr': 12, 'healthy': 3}
    most_common, freq = counts.most_common(1)[0]

    return most_common


def predict_files(paths) -> Dict[str, str]:
    """
    Принимает список путей до файлов,
    возвращает словарь:
    logs - результаты всех записей
    majority - одна конкретная болезнь, которая встречалась больше всего
    """
    paths = [Path(p) for p in paths]
    results_dict = {idx: _predict_one(p) for idx, p in enumerate(paths, start=1)}
    diagnosis = majority_class(results_dict)
    result = {
        "logs": results_dict,
        "diagnosis": diagnosis
    }
    #print(result)
    return result






