from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

import redis
import time
import signal

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
QUEUE_NAME = os.getenv("QUEUE_NAME", "jobs")

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

running = True

def shutdown_handler(signum, frame):
    global running
    running = False

signal.signal(signal.SIGTERM, shutdown_handler)
signal.signal(signal.SIGINT, shutdown_handler)


def process_job(job_id):
    print(f"Processing job {job_id}")
    time.sleep(2)
    r.hset(f"job:{job_id}", "status", "completed")
    print(f"Done: {job_id}")


while running:
    try:
        job = r.brpop(QUEUE_NAME, timeout=5)
    except redis.RedisError:
        print("Redis error, retrying...")
        time.sleep(2)
        continue

    if job:
        _, job_id = job
        job_id = job_id.decode() if isinstance(job_id, bytes) else job_id
        process_job(job_id)