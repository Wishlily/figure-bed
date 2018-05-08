import flickrapi
import webbrowser
import os
import json

def parse(filename):
    configfile = open(filename)
    jsonconfig = json.load(configfile)
    configfile.close()
    return jsonconfig

def key(cf):
    key = cf['key']
    return key['api_key'], key['api_secret']

if __name__ == '__main__':
    config = parse("flickr.conf")
    api_key,api_secret  = key(config)

    flickr = flickrapi.FlickrAPI(api_key, api_secret)
    flickr.authenticate_via_browser(perms='write')

    count = 0
    path = 'flickr'
    images = {}
    for parent, dirnames, filenames in os.walk(path):
        count += len(filenames)
        for filename in filenames:
            filepath = os.path.join(parent,filename)
            print("uploading: " + filepath)
            rsp = flickr.upload(filename=filepath)
            if rsp.attrib['stat'] != 'ok':
                print("uploading: failed")
                continue
            os.remove(filepath)

            photo_id = rsp.find('photoid').text
            rsp = flickr.photos_getSizes(photo_id=photo_id)
            sizes = rsp.find('sizes')
            urls = {}
            for size in sizes:
                info = size.attrib
                urls[info['label']] = info['source']

            if 'Medium 800' in urls:
                url = urls['Medium 800']
            elif 'Medium 640' in urls:
                url = urls['Medium 640']
            elif 'Medium' in urls:
                url = urls['Medium']
            elif 'Small 320' in urls:
                url = urls['Small 320']
            elif 'Small' in urls:
                url = urls['Small']
            else:
                url = ''
            images[filename] = url
            print(filename, url)
    print("up: ",count)

    with open('flickr.json', 'w') as f:
        json.dump(images,f)