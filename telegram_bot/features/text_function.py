from datetime import datetime


def make_record_text(log):
    location_text = "Reported" if log.longitude is not None else "NOT reported"
    location_text = (
        location_text if log.longitude != "Not Available" else "Not Available"
    )
    text_message = f"""
    {log.status} {"- " + log.optional_status if log.optional_status else ""}
    Log No.{log.id} : *__{log.local_date}__* *__{log.local_time}__*
    location : {location_text}
    remarks : {log.remarks if log.remarks else "-"}\n"""

    return text_message
