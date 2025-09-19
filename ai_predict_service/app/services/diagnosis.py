from collections import Counter
from pathlib import Path
from typing import Dict, List

from app.api.requests.diagnosis import DiagnosisRequest
from app.predict.main_predict import _predict_one
from tempfile import TemporaryDirectory

from app.repositories.mongo import MongoRepository


class DiagnosisService:
    mongo_repository: MongoRepository = MongoRepository()

    async def get_diagnosis(
        self,
        data: DiagnosisRequest,
    ):
        predicted_result = await self.predict_all(data.mongo_ids)
        diagnosis = predicted_result["diagnosis"]
        results = predicted_result["results"]
        result_for_bot = {
            "diagnosis": diagnosis,
            "results": results,
        }
        return result_for_bot

    async def predict_all(
        self,
        mongo_ids: List[str],
    ) -> Dict[str, str]:
        """
        Принимает список путей до файлов,
        возвращает словарь:
        logs - результаты всех записей
        majority - одна конкретная болезнь, которая встречалась больше всего
        """
        if not mongo_ids:
            return {"results": {}, "diagnosis": "Нет данных"}

        with TemporaryDirectory() as tmpdir:
            paths: list[Path] = []
            for idx, oid in enumerate(mongo_ids, start=1):
                wav_bytes = await self.mongo_repository.read_wav_bytes(oid)
                p = Path(tmpdir) / f"{idx}.wav"
                p.write_bytes(wav_bytes)
                paths.append(p)

            results_dict: Dict[int, str] = {
                idx: _predict_one(p) for idx, p in enumerate(paths, start=1)
            }

        results = {str(k): v for k, v in results_dict.items()}
        diagnosis = self.majority_class(results_dict)
        return {"results": results, "diagnosis": diagnosis}

        return result

    def majority_class(
        self,
        results: Dict[int, str],
    ) -> str:
        """
        Возвращает класс, который встречается чаще других.
        """
        if not results:
            return "Нет данных"

        counts = Counter(results.values())
        most_common, freq = counts.most_common(1)[0]

        return most_common
