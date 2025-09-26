from pathlib import Path
from collections import Counter

from app.ai.models.predict import predict_one

records_dir = Path(r"C:\speechka_data\for_training\norm2")

counts = Counter()
wav_paths = sorted(records_dir.glob("*.wav"), key=lambda p: p.name.lower())

if not wav_paths:
    print("В папке нет .wav файлов")
else:
    for p in wav_paths:
        pred = predict_one(p)
        counts[pred] += 1
        print(f"{p.name} -> {pred}")

    total = sum(counts.values())
    print("\n— Итоговая статистика —")
    for cls in ["healthy", "burr", "lisp", "lisp_burr"]:
        n = counts.get(cls, 0)
        pct = (n / total * 100) if total else 0
        print(f"{cls:9s}: {n:5d}  ({pct:6.2f}%)")
    print(f"Всего файлов: {total}")
