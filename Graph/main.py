import matplotlib.pyplot as plt
import numpy as np
import db
import logging
import datetime

def get_speed():
    service = db.Api()
    speed = service.get_speed()
    x = []
    y = []
    try:
        logging.info(speed)
        records = speed['Records']
        for record in records:
            y.append(record['Download'])
            date = datetime.datetime.strptime(record['TimeOfTest'], "%a, %d %b %Y %H:%M:%S %Z")
            x.append(date.strftime("%H:%M"))
            # average.append(average_value)
    except KeyError as error:
        logging.error('Records do not look correct: {}'.format(error))
    return x, y

x, y = get_speed()
ypoints = np.array(y)
xpoints = np.array(x)

plt.plot(xpoints, ypoints)
plt.show()