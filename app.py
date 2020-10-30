import requests
import json
# from dotenv import load_dotenv
import os 
import helpers

# load_dotenv()
insta_api = helpers.get_instagram_api()
api_key = os.getenv('YT_DATA_API_KEY')
channel_id = os.getenv('CHANNEL_ID')
insta_user_id = os.getenv('INSTAUSERID')
insta_email = os.getenv('INSTAEMAIL')


def getSubscriberCount():
    url = f'https://youtube.googleapis.com/youtube/v3/channels?part=snippet%2CcontentDetails%2Cstatistics&id={channel_id}&key={api_key}'
    json_url = requests.get(url)
    data = json.loads(json_url.text)
    items = data.get('items', {})
    return items[0].get('statistics', {}).get('subscriberCount')

def updateDescription():
    current_sub_count = getSubscriberCount()
    SUB_COUNT_IDENTIFIER = 'Current YT Sub Count: '
    user_info = insta_api.user_info(insta_user_id)
    user = user_info.get('user', {})
    
    bio = user.get('biography').strip()
    name = user.get('full_name')
    url = user.get('external_url')
    gender = 1
    email = insta_email
    new_bio = ''
    has_changed = False
    for line in bio.split('\n'):
        if SUB_COUNT_IDENTIFIER in line:
            count = line.split(SUB_COUNT_IDENTIFIER)[1]
            if count != current_sub_count:
                line = SUB_COUNT_IDENTIFIER + current_sub_count
                has_changed = True
        new_bio += line + '\n'
    
    if has_changed:
        insta_api.edit_profile(biography=new_bio, first_name=name, external_url=url, gender=gender, phone_number=None, email=email)    
    else:
        print('no change!')

updateDescription()
# if __name__ == '__main__':
#     updateDescription()
