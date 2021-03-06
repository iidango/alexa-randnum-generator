# -*- coding: utf-8 -*-
"""
generate random number
"""

from __future__ import print_function
import random


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session, card_content=None):
    card_content = output if card_content is None else card_content
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            # 'title': "SessionSpeechlet - " + title,
            # 'content': "SessionSpeechlet - " + output
            'title': title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "乱数のある生活ヘルプ"
    speech_output = "あなたのほしい乱数を生成します。" \
                    "3つから一つ選んで、や、サイコロを3回振ってなどと言ってみてください"

    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    # reprompt_text = speech_output
    reprompt_text = ""

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_help_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "乱数のある生活"
    speech_output = "あなたのほしい乱数を生成します。" \
                    "3つの選択肢から1つを選んでほしい時は，「3つのうちから一つ選んで」と話しかけてみてください。" \
                    "サイコロやルーレットを振りたい時は，「サイコロを1回振って」などと話しかけてみてください。" \
                    "「もう一度」と話しかけると一つ前と同じ条件で新しい乱数を生成します。" \

    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    # reprompt_text = speech_output
    reprompt_text = ""

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    # card_title = "Session Ended"
    card_title = "セッション終了"

    speech_output = "乱数のある生活を終了します。さようなら。 "

    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def handle_error_status():
    # card_title = "Session Ended"
    card_title = "エラー"

    speech_output = "すいません。よくわかりませんでした。"

    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def generate_random_num(intent, session, num1=1, num2=6, count=1):
    """ Create random number
    """
    try:
        if 'slots' in intent:
            num1 = int(intent['slots'].get('firstNum', {}).get('value', num1))
            num2 = int(intent['slots'].get('secondNum', {}).get('value', num2))
            count = int(intent['slots'].get('count', {}).get('value', count))
    except ValueError:
        return handle_error_status()

    if count > 100:
        session_attributes = {}
        session_attributes.update({'num1': num1, 'num2': num2, 'count': count})
        should_end_session = True

        # card_title = intent['name']
        card_title = "{}から{}の乱数を{}個".format(num1, num2, count)
        print("create {} random number from {} to {}".format(count, num1, num2))

        speech_output = "すいません。同時に振れる回数は100回までです。さようなら。"
        reprompt_text = ""
        return build_response(session_attributes, build_speechlet_response(
            card_title, speech_output, reprompt_text, should_end_session))
    
    session_attributes = {}
    session_attributes.update({'num1': num1, 'num2': num2, 'count': count})
    should_end_session = False

    # card_title = intent['name']
    card_title = "{}から{}の乱数を{}個".format(num1, num2, count)
    print("create {} random number from {} to {}".format(count, num1, num2))

    speech_output = ""
    card_content = ""
    for i in range(count):
        num = random.randint(num1, num2)
        speech_output += str(num) + "、"
        card_content += str(num) + "、"
    speech_output += "です。別の値が欲しい場合はさらに話しかけてください。終了する場合は「さようなら」と話しかけてください。"
    card_content += "です。"

    # reprompt_text = speech_output
    reprompt_text = ""
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session, card_content))


# --------------- Events ------------------


def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "RandNumIntent":
        return generate_random_num(intent, session)
    elif intent_name == "RangeRandNumIntent":
        return generate_random_num(intent, session)
    elif intent_name == "DiceIntent":
        return generate_random_num(intent, session, num1=1, num2=6)
    elif intent_name == "HundredDiceIntent":
        return generate_random_num(intent, session, num1=1, num2=100)
    elif intent_name == "RouletteIntent":
        return generate_random_num(intent, session, num1=1, num2=10)
    elif intent_name == "SelectIntent":
        return generate_random_num(intent, session, num1=1)
    elif intent_name == "RepeatIntent":
        if 'attributes' not in session:
            return handle_error_status()
        else:
            attributes = session.get('attributes')
            return generate_random_num(intent, session, **attributes)
    elif intent_name == "AMAZON.HelpIntent":
        return get_help_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------


def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
