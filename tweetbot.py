#twitter display dimensions: 435 x 375
#http://freshtakeoncontent.com/twitter-image-sizes-dimensions/

import tweepy, time, sys, PIL, yaml
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import glob, os, __keys
from random import randint

auth = tweepy.OAuthHandler(__keys.CONSUMER_KEY, __keys.CONSUMER_SECRET)
auth.set_access_token(__keys.ACCESS_TOKEN, __keys.ACCESS_TOKEN_SECRET)
auth.set_access_token(__keys.ACCESS_TOKEN, __keys.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)
sn = '_s_z_o_'

def get_last_tweet(self):
    tweet = self.user_timeline(sn, count = 1)[0]
    return tweet

def find_new_caption(self,since_id):
    mentions_since = api.mentions_timeline(since_id)
    last_tweet = get_last_tweet(self)
    for i in mentions_since:
	try:
	    self.create_favorite(i.id)
	except Exception:
	    ""
    return mentions_since[randint(0,len(mentions_since)-1)]

def rebuild_caption(split_cap,maxchar):
    caption = ""
    line = ""
    r = range(len(split_cap))
    for word in split_cap:
        if len(line + word) >= maxchar:
            line += word + "\n"
            caption += line
	    line = ""
        else:
            line += word + " " 
    caption += line
    return caption 

def format_caption(caption, maxchar):
    if len(caption) < maxchar:
        return caption
    else:
        split_cap = caption.split(" ")   
        return rebuild_caption(split_cap, maxchar)        

def position_sn(caption_sn, caption_text, maxchar):
    l = len(caption_text)/maxchar + 1
    x = 435.0 - (len(caption_sn) * 14) 
    y = 2 * 349.0 / 3 + (l * 25)
    if y > 349:
      y = 349
    return (x,y)

def position_caption(caption, maxchar):
    x = 20
    y = 2 * 349.0 / 3 
    return (x, y)

def get_dm_pics():
    media_files = set()
    msgs = api.direct_messages()
    for m in msgs:
	media = m.entities.get('media',[])
	if(len(media) > 0):
	    media_files.add(media[0]['media_url'])
    return media_files	

def run_bot():
    while True:
	np = open('nextpost.yml', "r")
	dataMap = yaml.safe_load(np)
	np.close()
	count = dataMap['c']
	image_num = dataMap['n']
	im = Image.open('./images/{}.png'.format(image_num))
	w = im.width + 0.0
	h = im.height + 0.0
	num_posts = 11
	loop_thru = range(num_posts+1) 
	loop_thru.remove(0)
	p = (375+ 0.0)/435 
    	box = (w/2 - (count*w/(num_posts*2)), h/2 - (count*w*p/(num_posts*2)), w/2 + (count*w/(num_posts*2)), h/2 + (count*w*p/(num_posts*2)))
    	im_to_post = im.crop(box)
    	im_to_post = im_to_post.resize((435,375))
    	draw = ImageDraw.Draw(im_to_post)
    	font = ImageFont.truetype("./fonts/zillah_modern_thin.ttf",31)
    	last_tweet = get_last_tweet(api)
	maxchar = 30 
    	mentions_since = api.mentions_timeline(last_tweet.id)
    	if len(mentions_since) == 0: 
    	    caption_text = r'"_____!"'
    	    caption_sn = ''
    	else:
    	    caption = find_new_caption(api, last_tweet.id)
    	    caption_text = r'"' + caption.text.replace("@" + sn, "") + r'"'
    	    caption_sn = " ~" + caption.user.screen_name
    	#caption_text = "@ my bot tush sometime why don't you you fucking weirdo?"
    	#caption_sn = "~@youdontreallylovemedou"
    	draw.text(position_caption(caption_text, maxchar),format_caption(caption_text, maxchar),(255,250,0),font=font)
    	draw.text(position_sn(caption_sn, caption_text, maxchar),format_caption(caption_sn, maxchar),(250,250,0),font=font)
    	im_to_post.save('./images/a.png')
	if count >= num_posts - 1:
	    dataMap['n'] += 1
	    dataMap['c'] = 1
	elif count >= num_posts/2:
	    dataMap['c'] += 2
	else:
	    dataMap['c'] += 1
	np = open('nextpost.yml', "w")
	yaml.dump(dataMap, np)
	np.close()
    	api.update_with_media('./images/a.png',status="")
    	os.remove('./images/a.png')
	#for follower in tweepy.Cursor(api.followers).items():
	#    follower.follow()
	#    print follower.screen_name
	time.sleep(25626)

run_bot()
    
def save_image():
    count = 0
    msgs = api.direct_messages()
    for m in msgs:
	media = m.entities.get('media',[])
	if(len(media) > 0) and media['type'] == 'photo':
	    count += 1
	    media_files.add(media[0]['media_url'] + ':large')
	    image_uri = media[0]['media_url'] + ':large'		
	    print image_uri
	    filename = './a' + str(count) + '.png'
	    urllib.urlretrieve(image_uri, filename)
            # identify mime type and attach extension
		
