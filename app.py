from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
from interpark_ticket_finder import evolved_interpark_ticket_finder
from melon_ticket_finder import evolved_melon_ticket_finder

def google_calendar_writer(string):
    ticket_data_interpark_list = evolved_interpark_ticket_finder(string)
    ticket_data_melon_list = evolved_melon_ticket_finder(string)
    ticket_data_list = ticket_data_interpark_list + ticket_data_melon_list
    print("this is combined " + str(ticket_data_list))

    SCOPES = 'https://www.googleapis.com/auth/calendar'
    store = file.Storage('storage.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    GCAL = discovery.build('calendar', 'v3', http=creds.authorize(Http()))

    notification_list =[]
    for n in range(len(ticket_data_list)):
        #creating event based on dictionary format
        GMT_OFF = '+09:00'      # PDT/MST/GMT+9
        EVENT = {
            'summary': string + ": " + ticket_data_list[n]['title'],
            'start':  {'date': ticket_data_list[n]['start_date'], "timeZone": GMT_OFF},
            'end':    {'date': ticket_data_list[n]['end_date'], "timeZone": GMT_OFF},
            'description': "예매 링크: "+ ticket_data_list[n]['url'],
            'attendees': [
                {'email': 'friend1@example.com'},
                {'email': 'friend2@example.com'},
            ],
        }

        e = GCAL.events().insert(calendarId='primary',
                sendNotifications=True, body=EVENT).execute()

        print('''*** %r event added:
            Start: %s
            End:   %s''' % (e['summary'].encode('utf-8'),
                e['start']['date'], e['end']['date']))

