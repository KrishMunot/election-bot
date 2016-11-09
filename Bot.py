from slackclient import SlackClient
import requests
import time
import json

slack_token = "xoxp-xxxx"

sc = SlackClient(slack_token)

clinton = 0
trump = 0
cached_states = {}
nop = 0

while True:
    r = requests.get("https://intf.nyt.com/newsgraphics/2016/11-08-election-forecast/president.json")

    electorate = r.json()["president"]["current"]["electoral_votes_counted"]
    share = r.json()["president"]["current"]["vote_share_counted"]

    states = r.json()["president"]["races"]

    if clinton != electorate["clintonh"] or trump != electorate["trumpd"]:
        trump = electorate["trumpd"]
        clinton = electorate["clintonh"]

        johnvar = (share["clintonh"] + share["johnsong"]) - share["trumpd"]
        print johnvar

        sc.api_call(
          "chat.postMessage",
          channel="#random",
          text="Hillary now has " + str(clinton) + " (" + str(share["clintonh"] * 100) + "%) electoral votes, and Trump has " + str(trump) + " (" + str(share["trumpd"] * 100) + "%) electoral votes. Johnson is at " + str(share["johnsong"] * 100) + "%."
        )

        sc.api_call(
          "chat.postMessage",
          channel="#random",
          text="Hillary would be " + str(johnvar) + "% (pop. vote) over Trump if Johnson voters voted for her instead."
        )

        for state in states:
            try:
                stype = state["type"]
                winner = state["current"]["winner"]
                statev = state["state"]
            except KeyError:
                print json.dumps(state)
                continue

            if stype != "president" or not winner:
                continue

            if statev in cached_states:
                continue

            cached_states[statev] = 1

            print statev

            if nop == 0:
                continue

            sc.api_call(
                  "chat.postMessage",
                  channel="#random",
                  text=state["current"]["winner"]["candidate_key"] + " probably won " + state["state"] + "."
            )
    nop = 1
    time.sleep(5)
