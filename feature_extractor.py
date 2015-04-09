import musicbrainzngs
import csv
import gzip
import operator

artists_file = 'artists.csv.gz'
extractd_artist_file = 'extracted_artists.csv'

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


def genere_histogram():
    hist = {}
    with open(extractd_artist_file, 'r') as art_fh:
        art_csv = csv.reader(art_fh, delimiter=',', quotechar='"')
        next(art_csv, None)
        for row in art_csv:
            if str(row[4]) != "":
                for word in str(row[4]).split():
                    if word in hist.keys():
                        hist[word] += 1
                    else:
                        hist[word] = 1

        print hist




musicbrainzngs.set_useragent("app", "version")
# extract_artist_data()
genere_histogram()
