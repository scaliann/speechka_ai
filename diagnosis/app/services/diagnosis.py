from collections import Counter
from pathlib import Path
from typing import Dict, List, Any
from aiogram import Bot

from app.ai.models.predict import predict_one
from app.common.report_path import get_report_path
from app.config import settings
from app.kafka.schemas.diagnosis import DiagnosisSchema
from tempfile import TemporaryDirectory
from app.repositories.mongo import MongoRepository
from app.services.send_report import send_pdf_report


class DiagnosisService:
    """
    Сервис инкапсулирует бизнес-логику работы с диагнозами.
    """

    mongo_repository: MongoRepository = MongoRepository()

    async def get_and_send_diagnosis(
        self,
        data: DiagnosisSchema,
    ) -> Dict[str, Any]:
        """
        Принимает список mongo_id и chat_id.
        Содержит в себе основную логику диагностики и отправки.
        """

        predicted_result = await self.predict_all(data.mongo_object_ids)

        report_path = get_report_path(diagnosis="healthy")
        await send_pdf_report(
            chat_id=data.chat_id,
            report_path=report_path,
        )

    async def predict_all(
        self,
        mongo_ids: List[str],
    ) -> Dict[int, dict] | dict:
        """
        Принимает список mongo_id,
        возвращает словарь с подробными результатами
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
            results_dict: Dict[int, dict] = {
                idx: predict_one(p) for idx, p in enumerate(paths, start=1)
            }

        return results_dict

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
