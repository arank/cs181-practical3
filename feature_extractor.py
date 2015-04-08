import musicbrainzngs
import csv
import gzip

artists_file = 'artists.csv.gz'

artist_profiles = {}
def extract_artist_data():
    print "artist,name,country,gender,genere,year"
    with gzip.open(artists_file, 'r') as art_fh:
        art_csv = csv.reader(art_fh, delimiter=',', quotechar='"')
        next(art_csv, None)
        for row in art_csv:
            cunt = ""
            gender = ""
            genere = ""
            year = ""
            try:
                artist_dict = musicbrainzngs.get_artist_by_id(str(row[0]))
                artist_info = artist_dict['artist']
                
                if artist_info.get('country') is not None:
                    cunt = artist_info['country']

                if artist_info.get('gender') is not None:
                    gender = artist_info['gender']

                if artist_info.get('disambiguation') is not None:
                    genere = artist_info['disambiguation']

                if artist_info.get('life-span') is not None:
                    if artist_info['life-span'].get('begin') is not None:
                        year = artist_info['life-span']['begin'][:4]

                print str(row[0])+","+str(row[1])+","+str(cunt)+","+str(gender)+","+str(genere)+","+str(year)

            except:
                print str(row[0])+","+str(row[1])+",,,,"



musicbrainzngs.set_useragent("app", "version")
extract_artist_data()
