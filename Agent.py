from datetime import datetime
import json

def lambda_handler(event, context):
    print(event)
    agent = event['agent']
    actionGroup = event['actionGroup']
    function = event['function']
    parameters = event.get('parameters', [])

    try:
        parameters = parameters[0].get('value')
        input_date = datetime.strptime(parameters, "%d/%m/%Y").date()
        today = datetime.now().date()
        days_difference = (today - input_date).days
        output = f"The number of days between customer's last payment date{input_date} and {today} is {days_difference} days."
    except Exception as e:
        output = 'unalbe to find the customer last payment date, please ask customer to provide other information such as phone/mobile number'
        print(output)

    responseBody =  {
        "TEXT": {
            "body": output
        }
    }

    action_response = {
        'actionGroup': actionGroup,
        'function': function,
        'functionResponse': {
            'responseBody': responseBody
        }

    }

    dummy_function_response = {'response': action_response, 'messageVersion': event['messageVersion']}
    print("Response: {}".format(dummy_function_response))

    return dummy_function_response
