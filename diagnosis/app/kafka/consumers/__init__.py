from app.kafka.consumers.diagnosis import send_diagnosis_report
from app.utils.consumer import RoutingData


send_diagnosis = RoutingData(
    topic="diagnosis_topic",
    group_id="pdf_sender",
    handler=send_diagnosis_report,
)

routes = [routing for routing in locals().values() if isinstance(routing, RoutingData)]
