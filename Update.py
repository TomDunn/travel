import pickle
import urlparse
import datetime
import time
import simplejson

from Insta import api, DuplicateMediumError, InstaPhotos

pickle_file = "insta_photos.pecl"
insta_photos = None
tag_name = 'tdxcpicalbum'
count = 5

try:
    insta_photos = pickle.load(open(pickle_file))
except IOError:
    print "doesnt exist, instantiating"
    insta_photos = InstaPhotos()

done = False
max_tag_id = None
while not done:
    print "getting..."
    media = api.tag_recent_media(count=count, tag_name=tag_name, max_tag_id=max_tag_id)

    for medium in media[0]:
        try:
            insta_photos.add(medium)
            print "added %s" % medium.id
        except DuplicateMediumError:
            done = True

    if media[1] == None:
        done = True
    else:
        max_tag_id = urlparse.parse_qs(urlparse.urlparse(media[1]).query)['max_tag_id'][0]

"""
    Pickling can be bad mmkay...
"""
pickle.dump(insta_photos, open(pickle_file, 'w'))

photos_by_day = {}
for m in insta_photos.media:

    # convert instagram time to localtime of laptop - E,C,M,P
    epoch = datetime.datetime(1970,1,1)
    delta = (m.created_time - epoch).total_seconds()
    lctime= time.localtime(delta)
    time_str = "%d-%d-%d" % (lctime.tm_year, lctime.tm_mon, lctime.tm_mday)

    if time_str not in photos_by_day:
        photos_by_day[time_str] = []

    photos_by_day[time_str].append({
        'username':       m.user.username,
        'created_time':   delta,
        'images':         {'thumbnail':m.images['thumbnail'].url, 'standard_resolution':m.images['standard_resolution'].url},
        'caption':        m.caption.text,
        'filter':         m.filter
    })

outfile_dir = '_assets/js/data'
for key in photos_by_day.keys():
    photos_by_day[key] = sorted(photos_by_day[key], key=lambda m: m['created_time'])
    f = open('%s/%s.json' % (outfile_dir, key), 'w')
    f.write(simplejson.dumps({key: photos_by_day[key]}))
    f.close()

f = open('%s/all.json' % outfile_dir, 'w')
f.write(simplejson.dumps(photos_by_day))
f.close()
