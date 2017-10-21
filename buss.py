import datetime
import json

def get_trips(route_id):
	# dictionary with trip_ids as key and service_ids as values
	# service_ids indicate days of the week the bus operates
	trip_info = {}
	with open('google_transit/trips.txt') as f:
		for line in f:
			if line[:3] == route_id:
				parts = line.split(',')
				trip_info[parts[2]] = parts[1]
	return trip_info

def get_schedule(trip_info, stop_id):
	arrival_times = []

	# stop_times.txt has trip_id, arrival_time, departure_time(not used), stop_id, ...
	with open('google_transit/stop_times.txt') as f:
		for line in f:
			parts = line.split(',')
			if (parts[0] in trip_info) and (parts[3] == stop_id):
				# service_parts[1] has format 0000000 with 0 indicating not operating and 1 otherwise
				service_parts = trip_info[parts[0]].split('-')
				running_days = service_parts[1]
				if running_days[datetime.datetime.today().weekday()] == '1':
					arrival_times.append(parts[1])
	return sorted(arrival_times)

def get_next_arrivals(route_id, stop_id):
	arrival_times = get_schedule(get_trips(route_id), stop_id)
	ret_times = {}
	
	# time format '00:00:00'
	for time in arrival_times:
		arrival = datetime.datetime.time(datetime.datetime.strptime(time, "%H:%M:%S"))
		current = datetime.datetime.time(datetime.datetime.today())
		if arrival > current and len(ret_times) == 0:
			ret_times['first'] = arrival.strftime("%H:%M:%S")
		elif arrival > current and len(ret_times) == 1:
			ret_times['second'] = arrival.strftime("%H:%M:%S")
	ret_times = json.dumps(ret_times)
	return json.loads(ret_times)
