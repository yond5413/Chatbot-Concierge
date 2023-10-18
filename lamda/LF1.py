import json
from datetime import datetime
def lambda_handler(event, context):
    intent_name = event['sessionState']['intent']['name']
    if intent_name == "GreetingIntent":
        response = greetingIntent(event)
    elif intent_name == "ThankYouintent":
        response = thankYouIntent(event)
    elif intent_name == "DiningSuggestionsIntent":
        #response = diningIntent(event)
        #session_attributes = event.get('sessionAttributes', {})
        '''print(event)
        # Get the slot to elicit from the current intent
        slot_to_elicit = event['sessionState']['dialogAction']['slotToElicit']
        if slot_to_elicit:
            # A slot is being elicited; validate and store the response
            validation_result = validate_slot(intent_request, slot_to_elicit,event)
            if validation_result['isValid']:
                # Slot is valid; find the next slot to elicit
                next_slot = find_next_slot(intent_request, slot_order, slot_to_elicit)
                if next_slot:
                    # Elicit the next slot
                    return elicit_slot_response(intent_request, next_slot)
                else:
                    # All required slots are filled; fulfill the intent
                    return fulfill_reservation(intent_request)
            else:
                # Slot is not valid; elicit the same slot again
                return elicit_slot_response(event,intent_request, slot_to_elicit, validation_result['message'])
        else:
            return elicit_slot_response(event,intent_request, 'Cuisine')'''
        intent_request = intent_name
        print(f'event: {event}')
        print(f'event keys: {list(event.keys())}')
        print(f"next: {event['proposedNextState']['dialogAction']['slotToElicit']}")
        print(f"one-back: {event['proposedNextState']['dialogAction']}")
        if 'dialogAction' in event.get('sessionState', {}):
            # A slot is being elicited; validate the user's response and decide the next step
            slot_to_elicit = event['sessionState']['dialogAction']['slotToElicit']
            validation_result = validate_slot(intent_request, slot_to_elicit, event)
            if validation_result['isValid']:
                # Slot is valid; find the next slot to elicit
                next_slot = event['proposedNextState'].get('slotToElicit')
        
                if next_slot:
                    # Elicit the next slot
                    print('next')
                    return elicit_slot_response(intent_request, next_slot)
                else:
                    # All required slots are filled; fulfill the intent
                    return fulfill_reservation(intent_request)
            else:
                # Slot is not valid; elicit the same slot again
                print('not valid')
                return elicit_slot_response(event, intent_request, slot_to_elicit, validation_result['message'])
        else:
            # Check if 'proposedNextState' is present in the event
            if 'proposedNextState' in event:
                next_slot = event['proposedNextState']['dialogAction']['slotToElicit']
                if next_slot:
                # Elicit the slot specified in 'proposedNextState'
                    print('nextslot else')
                    return elicit_slot_response(event, intent_request, next_slot)
            # If 'proposedNextState' is not present or doesn't specify a slot, elicit the 'Cuisine' slot by default (or the initial slot)
            return elicit_slot_response(event, intent_request, 'Cuisine')
       

def validate_slot(intent_request, slot_name,event):
    #if 'slots' in intent_request and slot_name in intent_request['slots']:
        #print(f"in validate_slot {intent_request}, \n{slot_name}")
        slot_value = event['sessionState']['intent']['slots']['Cuisine']
        #print(slot_value)
        if slot_name == 'email':
            if validate_email(slot_name):
                return {'isValid': True}
            else:
                return {'isValid': False, 'message': 'Invalid email format. Please provide a valid email address.'}
        ### add similar thing for each 
        elif slot_name == "Cuisine":
            if validate_cusine(slot_value):
                return {'isValid': True}
            else:
                return {'isValid': False, 'message': 'Do not think we offer that type of cusine. Anything else?'}
        elif slot_name == "Dining_Time":
            if validate_time(slot_value):
                return {'isValid': True}
            else:
                return {'isValid': False, 'message': 'Please pick a reasonable time in the future.'}
        elif slot_name == "Location":
            if validate_location(slot_value):
                return {'isValid': True}
            else:
                return {'isValid': False, 'message': 'Our only options are in Manhattan, NY aplogoizes for any inconviences'}
        elif slot_name == "Number_of_people":
            if validate_number_of_people(slot_value):
                return {'isValid': True}
            else:
                return {'isValid': False, 'message': 'Obviously need to bring at least one person.'}
        else:
            # Handle cases where the slot doesn't exist or 'slots' is not in 'intent_request'
            return {'isValid': False, 'message': 'Slot not found or empty.'}
def greetingIntent(event):
    response_message = "How are you doing today? Is there anything I can do to help today?"

    ret = {
            "sessionAttributes": event["sessionState"]["sessionAttributes"],
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Fulfilled",
                "message": {
                    "contentType": "PlainText",
                    "content": response_message
                },
            },
        }
    return ret
def thankYouIntent(event):
    pass
def validate_email(email):
    # just checking for an @ tbh
    if email != None:
        return '@' in email
    else:
        return False
def validate_cusine(cusine):
   #is it an option from the slot type value
    categories = '''
    Italian,
    Mexican,
    Chinese,
    Japanese,
    Indian,
    French,
    Mediterranean,
    Thai,
    Vietnamese,
    Korean,
    Spanish,
    Greek,
    Ethiopian,
    Peruvian,
    Cajun/Creole,
    Brazilian,
    African,
    Caribbean,
    Nepali/Tibetan,
    Irish,
    Turkish,
    Russian,
    Other
    '''
    if cusine !=None:
        return cusine in categories
    else:
        return False
def validate_time(time):
    # Is it in the future
    input_time = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S")
    current_time = datetime.now()
    if input_time > current_time:
            return True  # The input time is in the future
    else:
            return False  # The input time is in the past
def validate_location(location):
    # is it in Manhattan NY
    if location !=None:
        location_str = location_str.lower()
        # Check if the location contains "manhattan, ny"
        return "manhattan, ny" in location_str
    else:
        return False
    
def validate_number_of_people(number):
    ### is it greater than 0?
    if number != None:
        return number >0
    else:
        return False

def elicit_slot_response(event,intent_request, slot_to_elicit, message=None):
    print("in elicit_slot_response")
    print(f"intent_request: {intent_request}, slot: {slot_to_elicit}")
    print(f"sessionState: {event['sessionState']}")#['sessionAttributes']}")
    response = {
        'sessionAttributes': event['sessionState']['sessionAttributes'],
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': event['sessionState']['intent']['name'],
            'slotToElicit': slot_to_elicit,  # Use intent_request as the slot to elicit
        }
    }

    if message:
        response['dialogAction']['message'] = {
            'contentType': 'PlainText',
            'content': message
        }
    else:
        response['dialogAction']['message'] = {
            'contentType': 'PlainText',
            'content': "How about for "+slot_to_elicit
        }

    return response

def fulfill_reservation(intent_request):
    # Add fulfillment logic here
    # In this example, we're just confirming the reservation
    confirmation_message = "Thank you! Your reservation is confirmed."

    response = {
        'sessionAttributes': intent_request['sessionAttributes'],
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': 'Fulfilled',
            'message': {
                'contentType': 'PlainText',
                'content': confirmation_message
            },
        }
    }

    return response
