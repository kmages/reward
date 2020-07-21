import json
import math

with open('example.json', 'r') as f:
    data = json.load(f)

customers = {'reward': []}

for d in data['events']:
    if d['action'] == 'new_customer':
        customers['reward'].append({'name': d['name'], 'points': 0, 'points_per_order': 0})

    if d['action'] == 'new_order':
        time = d['timestamp'][d['timestamp'].find('T')+1:]
        starttime = time[:time.find('-')]
        starttime = starttime[0]+starttime[1]
        endtime = time[time.find('-')+1:]
        endtime = endtime[0]+endtime[1]

        points = 0
        points_per_order = 0
        if starttime >= '12' and starttime < '13':
            points = d['amount'] / 3.0
        elif (starttime >= '11' and starttime < '12') or (starttime >= '13' and starttime < '14'):
            points = d['amount'] / 2.0
        elif (starttime >= '10' and starttime < '11') or (starttime >= '14' and starttime < '15'):
            points = d['amount'] / 1.0
        else:
            points = d['amount'] / 4.0

        for c in customers['reward']:
            if c['name'] == d['customer']:
                points_per_order = points
                points_per_order = round(points_per_order, 1)
                points = math.ceil(points)
                if points >= 3 and points <= 20:
                    c['points'] += points
                    c['points_per_order'] += points_per_order

for r in customers['reward']:
    output = ''
    if r['points'] != 0:
        output = '{0}: {1} points with {2} points per order.'.format(r['name'], r['points'], r['points_per_order'])
    else:
        output = '{0}: No orders.'.format(r['name'])
    print(output)
