# Tehya Yi 11/29/2022
import config
import pymongo
import datetime
import sched
import time
import socket

client = pymongo.MongoClient(f"mongodb+srv://raspi:{config.password}"
                             f"@cluster0.tev7xup.mongodb.net/?retryWrites=true&w=majority",
                             server_api=pymongo.server_api.ServerApi('1'))
db = client.test
SCHEDULER = sched.scheduler(time.time, time.sleep)
PI_NAME = socket.gethostname()


def update_database(sc):
    """Send some sensor data to a mongo db."""
    print("doing something")
    print(db.list_collection_names())
    # TODO: make new collection if collection for curr not made
    collection = db[f"{PI_NAME}"]

    machine = {
        "id": str(PI_NAME),
        "date": str(datetime.datetime.utcnow()),
        "data1": "test 1",
        "data2": "test 2",
        "data3": "test 3",
    }

    result = collection.insert_one(machine)
    sc.enter(5, 1, update_database, (sc,))


def main():
    """Send data every 5 minutes."""
    SCHEDULER.enter(5, 1, update_database, (SCHEDULER,))
    SCHEDULER.run()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
