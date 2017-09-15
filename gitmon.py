import git, os, re, shutil, os.path
from git import Repo
from slackclient import SlackClient
from time import localtime, strftime


def log(string):
    dt = strftime("[%d-%m-%Y %H:%M:%S] ", localtime())
    with open("gitmon.log", "a") as myfile:
        myfile.write(dt + string + "\r\n")
    pass



def send2slack(chan, msg):
	#https://api.slack.com/custom-integrations/legacy-tokens
    slack_token = "slack-token"
    #os.environ["slack-token"]
    sc = SlackClient(slack_token)
    sc.api_call(
        "chat.postMessage",
         channel=chan,
         text=msg
    )




DIR_NAME = "tmp"
REMOTE_URL = "ssh://"

if os.path.isdir(DIR_NAME):
    shutil.rmtree(DIR_NAME)

os.mkdir(DIR_NAME)

repo = git.Repo.init(DIR_NAME)
origin = repo.create_remote('origin', REMOTE_URL)
origin.fetch()
#origin.pull(origin.refs[0].remote_head)
#print(repo.heads)


repo = Repo(DIR_NAME)

call = repo.git.branch('-a')
branches = []
for x in call.splitlines():
    if x.startswith("*"):
       branches.insert(0, x[2:])
    else:
       branches.append(x[2:])

for r in branches:

    match = re.search('(branch)', r, re.IGNORECASE)
    if match and not os.path.exists('gitmon.log'):
        f = match.group(0)
        print('-' + f + '-')
        send2slack("#channel", ":mag_right: Found new branch - " + f)
        log("Found new branch - " + f)



    print(r)

#send2slack("#channel", ":ballot_box_with_check: just a check...")


#print(branches)

