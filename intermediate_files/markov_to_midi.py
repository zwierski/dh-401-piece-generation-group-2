import pandas as pd
import music21

# open the csv file
df = pd.read_csv('intermediate_files\markov_songs_with_pitch.csv')

# convert into duration
def convert_to_duration(random_song_list):
    last = 3.0
    # read the list backwards
    random_song_list.reverse()
    # create a list with the duration of each note
    duration_list = []
    for bar in random_song_list:
        # reverse the inner list
        bar.reverse()
        for note in bar:
            duration_list.append(last - note)
            last = note
        last += 3.0
    # reverse the list again
    duration_list.reverse()
    # return original order to original song aswell
    random_song_list.reverse()
    for bar in random_song_list:
        bar.reverse()
    return duration_list

def elongate_pitch_list(pitch_list):
    new_list = []
    for bar in pitch_list:
        for note in bar:
            new_list.append(note)
    return new_list

# convert duration list into music21 stream
def convert_to_stream(duration_list, pitch_list):
    pitch_list = elongate_pitch_list(pitch_list)
    # create an empty stream
    stream = music21.stream.Stream()
    # define the tempo as 3/4
    stream.append(music21.meter.TimeSignature('3/4'))
    # create note
    # assign the pitch of the random_pitches list
    # assign duration (quarter)
    # append the note into empty stream
    count = 0
    for duration in duration_list:
        note = music21.note.Note(pitch=pitch_list[count], quarterLength=duration)
        stream.append(note)
        count += 1
    return stream

def transform_beat_list(beat_list):
    new_list = []
    beat_list = beat_list.split('], [')
    for bar in beat_list:
        bar = bar.replace('[', '')
        bar = bar.replace(']', '')
        bar = bar.split(', ')
        bar = [float(x) for x in bar]
        new_list.append(bar)
    return new_list

# example for row 0
# beat_list = df.iloc[0]['beat']
# pitch_list = df.iloc[0]['pitch']
# beat_list = transform_beat_list(beat_list)
# pitch_list = transform_beat_list(pitch_list)
# print(beat_list)
# duration_list = convert_to_duration(beat_list)
# stream = convert_to_stream(duration_list, pitch_list)
# stream.show('midi')

# create a new column in the dataframe
df['midi'] = None

# iterate over the dataframe
for index, row in df.iterrows():
    beat_list = row['beat']
    pitch_list = row['pitch']
    beat_list = transform_beat_list(beat_list)
    pitch_list = transform_beat_list(pitch_list)
    duration_list = convert_to_duration(beat_list)
    stream = convert_to_stream(duration_list, pitch_list)
    # save the stream as midi file in the markov_midis folder
    address = 'markov_midis\markov_song_' + str(index) + '.mid'
    stream.write('midi', fp=address)
    df.at[index, 'midi'] = address

# save the dataframe as csv
df.to_csv('intermediate_files\markov_songs_with_midi.csv', index=False)