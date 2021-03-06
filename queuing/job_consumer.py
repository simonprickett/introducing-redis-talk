import json
import random
import redis
import time

LIST_KEY = "jobs"

r = redis.Redis(decode_responses = True)

while True:
    print("Checking for jobs...")

    pipeline = r.pipeline()
    pipeline.brpop(LIST_KEY, timeout = 5)
    pipeline.llen(LIST_KEY)
    results = pipeline.execute()
    
    next_job = results[0]
    backlog = results[1]

    if next_job is None:
        print("Nothing to do right now.")
        time.sleep(5)
    else:
        # next_job is a Tuple, that looks like this:
        # ('jobs', '{"room": 343, "job": "Room Service"}')
        job = json.loads(next_job[1])
        print(f"Performing job {job['job']} for room {str(job['room'])}. Backlog {backlog} jobs.")
        time.sleep(random.randint(2, 6))