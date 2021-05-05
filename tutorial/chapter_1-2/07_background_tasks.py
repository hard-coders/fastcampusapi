"""
source from: https://fastapi.tiangolo.com/tutorial/background-tasks
위 소스 코드에서 time 만 추가했습니다.
"""
import time

from typing import Optional
from fastapi import BackgroundTasks, Depends, FastAPI, status

app = FastAPI()


def write_log(message: str):
    time.sleep(2.0)

    with open("log.txt", mode="a") as log:
        log.write(message)


def get_query(background_tasks: BackgroundTasks, q: Optional[str] = None):
    if q:
        message = f"found query: {q}\n"
        background_tasks.add_task(write_log, message)
    return q


@app.post("/send-notification/{email}", status_code=status.HTTP_202_ACCEPTED)
async def send_notification(
    email: str, background_tasks: BackgroundTasks, q: str = Depends(get_query)
):
    message = f"message to {email}\n"
    background_tasks.add_task(write_log, message)

    return {"message": "Message sent"}
