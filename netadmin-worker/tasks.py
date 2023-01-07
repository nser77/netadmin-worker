import csv
from celery import shared_task
from maxmind import MaxMind

@shared_task(name="worker.tasks.broad_message")
def broad_message(message, *args, **kwargs):
    mm=MaxMind()
    mm.download_key="000000"
    if mm.getCsvDB():
        with mm.gl2_country_blocks_ipv4_db.open() as f:
            index_db=csv.reader(f)
            for al in message["address_list"]:
                for r in index_db:
                    print(r)
        f.close()

    return True
