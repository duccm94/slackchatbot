import os
import time
import re
from slackclient import SlackClient

# instantiate Slack client
slack_client = SlackClient("xoxb-370457668161-466471908902-VW63PzBtxeY4FCensfeKTPLQ")
chatbot_id = None

# constants
RTM_READ_DELAY = 1
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

def parse_bot_commands(slack_events):
  for event in slack_events:
    if event["type"] == "message" and not "subtype" in event:
      print(event)
      mention_id, message = parse_direct_mention(event["text"])
      if mention_id == chatbot_id:
        return message, event["user"], event["channel"]
  return None, None, None

def parse_direct_mention(message_text):
  matches = re.search(MENTION_REGEX, message_text)
  return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def handle_command(command, userID, channel):
  response = f"<@{userID}> hihi"

  slack_client.api_call(
    "chat.postMessage",
    channel=channel,
    text=response
  )

if __name__ == "__main__":
  if slack_client.rtm_connect(with_team_state=False):
    print("Bot connected and running!")
    chatbot_id = slack_client.api_call("auth.test")["user_id"]
    while True:
      command, userID, channel = parse_bot_commands(slack_client.rtm_read())
      if command:
        handle_command(command, userID, channel)
      time.sleep(RTM_READ_DELAY)
  else:
    print("Connection failed. Exception traceback printed above.")