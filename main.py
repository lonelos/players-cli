#!/usr/bin/python3

import json
import os.path
import argparse
import requests
import datetime
import dateutil.parser

BASE_URL = 'http://localhost:5000'
RESOURCE_URL = '/player/'
RESOURCES_URL = '/players'
ALL_FILE = 'players_all.json'
INDIVIDUAL_FILE = 'players_individial.json'


def resource_url(id):
    return BASE_URL + RESOURCE_URL + str(id)


def resources_url():
    return BASE_URL + RESOURCES_URL


def update_resource(dict, resource):
    if dict['last_fetched'] != '':
        last_fetched = dateutil.parser.isoparse(dict['last_fetched'])
    else:
        last_fetched = datetime.datetime.now()

    for i, record in enumerate(dict['current']):
        if record['id'] == resource['id']:
            last_modified = dateutil.parser.isoparse(resource['last_modified'])
            if (last_modified > last_fetched):
                old_resource = dict['current'].pop(i)
                dict['current'].append(resource)
                dict['history'].append(old_resource)
            break
    else:
        dict['current'].append(resource)


def create_dict():
    return {
        'last_fetched': '',
        'current': [],
        'history': [],
    }


def get_dict(filename):
    if os.path.exists(filename):
        with open(filename) as json_file:
            return json.load(json_file)
    else:
        return create_dict()


def get_resource(id):
    dict = get_dict(INDIVIDUAL_FILE)
    resp = requests.get(resource_url(id))
    update_resource(dict, resp.json())
    dict['last_fetched'] = str(datetime.datetime.utcnow())
    with open(INDIVIDUAL_FILE, 'w') as outfile:
        json.dump(dict, outfile)


def get_all_resources():
    dict = get_dict(ALL_FILE)
    resp = requests.get(resources_url())
    for resource in resp.json():
        update_resource(dict, resource)
    dict['last_fetched'] = str(datetime.datetime.utcnow())
    with open(ALL_FILE, 'w') as outfile:
        json.dump(dict, outfile)


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-a', '--all', action='store_true', help='Fetches all players from the API')
    group.add_argument('-p', '--player', metavar='id', type=int, help='get player by id')
    args = parser.parse_args()

    if (args.all):
        get_all_resources()
    elif (args.player):
        get_resource(args.player)


if __name__ == '__main__':
    main()
