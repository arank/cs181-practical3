import musicbrainzngs
import csv
import gzip

artists_file = 'artists.csv.gz'

artist_profiles = {}
def extract_artist_data():
    with gzip.open(artists_file, 'r') as art_fh:
        art_csv = csv.reader(art_fh, delimiter=',', quotechar='"')
        next(art_csv, None)
        for row in art_csv:
            artist_dict = musicbrainzngs.get_artist_by_id(str(row[0]))
            print artist_dict
            artist_profiles[str(row[0])] = {'name': str(row[1])} 

extract_artist_data()
