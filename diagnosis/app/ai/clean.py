import numpy as np
import pandas as pd
import librosa
import wavio


def envelope(y, rate, threshold):
    mask = []
    y = pd.Series(y).apply(np.abs)
    y_mean = y.rolling(window=int(rate / 20), min_periods=1, center=True).max()
    for mean in y_mean:
        if mean > threshold:
            mask.append(True)
        else:
            mask.append(False)
    return mask, y_mean


def downsample_mono(path, sr):
    obj = wavio.read(path)
    wav = obj.data.astype(np.float32, order="F")
    rate = obj.rate
    try:
        channel = wav.shape[1]
        if channel == 2:
            wav = librosa.to_mono(wav.T)
        elif channel == 1:
            wav = librosa.to_mono(wav.reshape(-1))
    except IndexError:
        wav = librosa.to_mono(wav.reshape(-1))
        pass
    except Exception as exc:
        raise exc
    wav = librosa.resample(wav, orig_sr=rate, target_sr=sr)
    wav = wav.astype(np.int16)
    return sr, wav
