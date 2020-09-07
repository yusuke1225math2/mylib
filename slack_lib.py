import slackweb

channel_announce = '#003_autotwitter_announce'
channel_report = '#004_autotwitter_report'
channel_research = '#005_autotwitter_research'

def post_to_slack(message='メッセージを引数に入れてください',target_channel="#003_autotwitter_announce"):
    slack = slackweb.Slack(url="https://hooks.slack.com/services/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")
    slack.notify(text=message, channel=target_channel)

if __name__ == '__main__':
    post_to_slack()