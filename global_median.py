import numpy as np
import csv
import gzip

# Predict via the median number of plays.
profiles_file = 'profiles.csv.gz'
artists_file = 'artists.csv.gz'
train_file = 'train.csv.gz'
test_file  = 'test.csv.gz'
soln_file  = 'solutions.csv'

# Splits data set into train_size portions, and tests on one of theose portions
# after training on the rest train_iter number of times.
def cross_vaidate(train_data, train_iter=5, train_size=10):
    keys = train_data.keys()
    size = len(keys)/train_size
    i=0
    iters = 0
    cumulative_err = 0
    while(iters<train_iter and i+size < len(keys)):
        train = keys[0:i] + keys[i+size:]
        #TODO train a model

        test = keys[i:i+size]
        err = 0
        count = 0
        for user in test:
            for artist in train_data[user].keys():
                #TODO predict using trainign data
                predict = 0
                plays = train_data[user][artist] 
                err += abs(predict-plays)
                count += 1

        cumulative_err += (err/count)
        i+=size
        iters+=1

    return (cumulative_err/iters)

user_profiles = {}
def extract_user_data():
    print "extracting user data"
    with gzip.open(profiles_file, 'r') as prof_fh:
        prof_csv = csv.reader(prof_fh, delimiter=',', quotechar='"')
        next(prof_csv, None)
        for row in prof_csv:            
            user_profiles[str(row[0])] = {
                'sex': row[1], 
                'age': row[2],
                'location': row[3]
            }

# TODO maybe feature extract on genere of music?
# artist_profiles = {}
# def extract_artist_data():
#     with gzip.open(artists_file, 'r') as art_fh:
#         art_csv = csv.reader(art_fh, delimiter=',', quotechar='"')
#         next(art_csv, None)
#         for row in art_csv:
#             artist_profiles[str(row[0])] = {'name': str(row[1])} 

# Load the training data.
train_data = {}
print "extracting training data"
with gzip.open(train_file, 'r') as train_fh:
    train_csv = csv.reader(train_fh, delimiter=',', quotechar='"')
    next(train_csv, None)
    for row in train_csv:
        user   = row[0]
        artist = row[1]
        plays  = int(row[2])
    
        if not user in train_data:
            train_data[user] = {}
        
        train_data[user][artist] = plays

# Compute the global median.
print "performing learning"
plays_array = []
for user, user_data in train_data.iteritems():
    for artist, plays in user_data.iteritems():
        plays_array.append(plays)
global_median = np.median(np.array(plays_array))
print "global median:", global_median

# Write out test solutions.
print "performing prediction"
with gzip.open(test_file, 'r') as test_fh:
    test_csv = csv.reader(test_fh, delimiter=',', quotechar='"')
    next(test_csv, None)

    print "writing out results"
    with open(soln_file, 'w') as soln_fh:
        soln_csv = csv.writer(soln_fh,
                              delimiter=',',
                              quotechar='"',
                              quoting=csv.QUOTE_MINIMAL)
        soln_csv.writerow(['Id', 'plays'])

        for row in test_csv:
            id     = row[0]
            user   = row[1]
            artist = row[2]

            soln_csv.writerow([id, global_median])