import praw

app_ua = '/u/Superf1cial, Telegram + Redditbot'
app_id = 'lYBgeaVpswXoYg'
app_secret = 'Z9e-FdRnJzSjRknsJ7xKMQZG-b4'
app_uri = 'https://127.0.0.1:65010/authorize_callback'
app_scopes = 'account creddits edit flair history identity livemanage modconfig modcontributors modflair modlog modothers modposts modself modwiki mysubreddits privatemessages read report save submit subscribe vote wikiedit wikiread'
app_account_code='KQCqBY3Rnl4KfneXUFy7JExZTfo'
app_refresh= '35935394-yGTJflSmQp9x_w87gq-n-dkVVl0'

def login():
    r = praw.Reddit(app_ua)
    r.set_oauth_app_info(app_id, app_secret, app_uri)
    r.refresh_access_information(app_refresh)
    return r

