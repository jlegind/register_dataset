''' Insertion module that uses the GBIF API to add entities such as "comments"
or "installations".
'''
import requests
import json


credentials = ('user', 'pw')


def add_entity(header, category, uuid, payload, type=None, api_url='http://api.gbif.org/v1'):
    '''
    :param header: Content type submitted (JSON)
    :param category: Which kind of entity is being added (for instance 'dataset')
    :param uuid: The key to the entity
    :param type: Select 'comment' or 'contact' or 'tag'. If None, a straight post for that category is made
    :param api_url: GBIF API URL
    :param payload: JSON string
    :return: HTTP status code
    '''
    if type:
        post_url = '{}/{}/{}/{}'.format(api_url, category, uuid, type)
    else:
        post_url = '{}/{}/{}'.format(api_url, category, uuid)
    print(post_url)
    r = requests.post(post_url, auth=credentials, headers=header, data=json.dumps(payload))
    return r