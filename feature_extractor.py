import musicbrainzngs
import csv
import gzip

artists_file = 'artists.csv.gz'

artist_profiles = {}
def extract_artist_data():
    with gzip.open(artists_file, 'r') as art_fh:
        art_csv = csv.reader(art_fh, delimiter=',', quotechar='"')
        next(art_csv, None)
        count = 0
        country = 0
        gender = 0
        genere = 0
        date = 0
        mismatch = 0
        err = 0
        for row in art_csv:
            count += 1
            try:
                artist_dict = musicbrainzngs.get_artist_by_id(str(row[0]))
                artist_info = artist_dict['artist']
                
                a = None
                b = None

                if artist_info.get('area') is not None:
                    if artist_info['area'].get('iso-3166-1-code-list') is not None:
                        a = artist_info['area']['iso-3166-1-code-list'][0] 

                if artist_info.get('country') is not None:
                    b = artist_info['country']

                if a is not None and b is not None:
                    country += 1
                    if a != b:
                        mismatch += 1

                if artist_info.get('gender') is not None:
                    gender += 1
                    # print artist_info['gender']

                if artist_info.get('disambiguation') is not None:
                    genere += 1
                    # print artist_info['disambiguation']

                if artist_info.get('life-span') is not None:
                    if artist_info['life-span'].get('begin') is not None:
                        date += 1
                        # print artist_info['life-span']['begin'][:4]

            except:
                err += 1
                print "there was an error"
            
            artist_profiles[str(row[0])] = {'name': str(row[1])} 

        print "total:" + str(count) + ", 404:"+ str(err)+", mismatch:"+str(mismatch)+", country:"+str(country)+", gender:"+str(gender)+", date:"+str(date)+", genere:"+str(genere)


musicbrainzngs.set_useragent("app", "version")
extract_artist_data()
