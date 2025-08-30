from typing import List

from predict.main_predict import predict_files
from recommendation.recommendation_logic import return_recommendation
from fastapi import FastAPI, Body
import tempfile, shutil


# Примеры путей для тестирования (закомментированы для Docker)
# list_paths = ["/app/records/norm1.wav", "/app/records/norm2.wav", "/app/records/norm3.wav", "/app/records/burr4.wav"]
# list_paths2 = ["/app/records/693505334/24/1.wav", "/app/records/693505334/24/2.wav",
#                "/app/records/693505334/24/3.wav", "/app/records/693505334/24/4.wav"]


def diagnostic_and_return_recommendation(records_paths: list):
    print(f"AI Service received paths: {records_paths}")
    predicted_result = predict_files(records_paths)
    diagnosis = predicted_result['diagnosis']
    logs = predicted_result['logs']
    recommendation = return_recommendation(diagnosis)
    result_for_bot = {
        'diagnosis': diagnosis,
        'logs': logs,
        'recommendation': recommendation,
        'records_paths': records_paths
    }
    print(result_for_bot)
    return result_for_bot



app = FastAPI(title="AI Predict Service", description="Сервис для анализа речи")

@app.get("/")
async def root():
    return {"message": "AI Predict Service работает!", "status": "ok"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "ai_predict_service"}

@app.post("/diagnose")
async def diagnose(paths: List[str] = Body(...)):
    result = diagnostic_and_return_recommendation(paths)
    return result
