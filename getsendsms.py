from flask import Flask, request, redirect
from twilio.twiml.messaging_response import Message, MessagingResponse
import busstime 
import twilioMsgs

app = Flask(__name__)
USAGE = 'Get bus arrival estimates by texting the route number, a comma, and the stop number. \n Use the online lookup tool to look for stop numbers or to see an example: http://buss-page-deployment.s3-website-us-west-1.amazonaws.com/'
@app.route('/sms', methods=['POST'])
def sms():
    message_body = request.form['Body']
    resp = MessagingResponse()

    #The user message is expected to be two parts
    user_message = message_body.split(', ')

    route_valid = 0
    stop_valid = 0
    
    route_id = 0
    stop_id = 0 
    

    #Right now the problem is the user doens't know the route/stop id's as they are in the files
    #Parameter checking here. 
    if len(user_message) == 2:
        route_id = user_message[0]
        stop_id = user_message[1]
    else:
        resp.message(USAGE)
        return str(resp)


    #At this point, the user has entedddred the correct amount of parameters to check a bus route/stop.
    #Begin checking for existing routes 
    with open('google_transit/routes.txt') as f:
        for line in f:
            info = line.split(',')
            if info[0] == route_id:
                route_valid = 1
    
    
    with open('google_transit/stops.txt') as f:
        for line in f:
            info = line.split(',')
            if info[0] == stop_id:
                stop_valid = 1
    
    if route_valid != 1 or stop_valid != 1:
        resp.message(USAGE)
        return str(resp)

    times = busstime.get_next_arrivals(route_id, stop_id)	
    print times 
    if len(times) == 2:
        resp.message('The next two arrival times for route ' + route_id + ' at stop ' + stop_id + ' are in ' + times['first'] + ' and ' + times['second'] + ' minutes.')
    elif len(times) == 1:
        resp.message('The next arrival time for route ' +route_id + ' at stop ' + stop_id + ' is in ' + times['first'] + ' minutes. This is the last bus for today.')
    else:
        resp.message('Unfortunately there will be no arrivals at this stop in the next hour.')


    return str(resp)

def shutdown_server():
    func = request.environ.get(werkzeug.server.shutdown)
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

if __name__ == '__main__':
    app.run()
