import random
import music21
import pandas as pd
# ignore warnings
import warnings
warnings.filterwarnings('ignore')


random.seed(1113)

# fun to fill a bar with random notes
def random_bar():
    # first = True
    first = False
    # first decide how many notes are in the bar
    # (the tempo is always 3/4)
    bar = []
    for i in range(11):
        # decide if a note is played
        if first:
            bar.append(1.0)
            first = False
        elif random.random() < 0.5:
            # if yes, decide which note
            bar.append((i/4)+1)
        # check that the bar is not empty
    if len(bar) == 0:
        bar = random_bar()
    return bar

# create a scale with all the notes from C4 to C5
sc = music21.scale.MajorScale('C4')
# get all the pitches from the scale
pitch_collection = sc.getPitches('C4', 'C5')
print(f"pitch_collection contains {len(pitch_collection)} pitches.")
print(pitch_collection)

# create list with pitches for the bar
def create_pitches(size, pitch_collection= pitch_collection):
    list_p = []
    for i in range(size):
        # append a random pitch from the scale
        list_p.append(random.choice(pitch_collection))
    return list_p

# create random song
def create_random_song():
    # make a list with 8 lists inside
    random_song = [[] for j in range(8)]
    random_pitches = [[] for j in range(8)]
    # for each list in random_song fill it with random notes
    for i in range(8):
        random_song[i] = random_bar()
        random_pitches[i] = create_pitches(len(random_song[i]))
    return random_song, random_pitches


# example
random_song, random_pitches = create_random_song()
print('random song: ')
print(random_song)
print('random pitches: ')
print(random_pitches)

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

# example
duration_list = convert_to_duration(random_song)
print('duration list: ')
print(duration_list)

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

# Function that maps the beat distribution of a bar to a series of numbers between 1 and 12 (position of each sixteenth-note in the bar)
def map_beats(notes):
    notes_mapped = []
    for bar in notes:
        bar_mapped = []
        for x in bar:
            bar_mapped.append(int(4*(x-1)+1))
        notes_mapped.append(bar_mapped)
    return notes_mapped


# example
stream = convert_to_stream(duration_list,random_pitches)
# print(type(stream))
# stream.show()

# play the stream
stream.show('midi')

# print with map_beats convertion
print('random song with map_beats: ')
print(map_beats(random_song))

# translate the music21 pitches to midi numbers
def translate_pitches(pitches):
    midi_pitches = []
    for bar in pitches:
        bar_midi = []
        for pitch in bar:
            bar_midi.append(pitch.midi)
        midi_pitches.append(bar_midi)
    return midi_pitches

# print with translate_pitches convertion
print('random song with translate_pitches: ')
print(translate_pitches(random_pitches))

# produce a dataframe size 500 samples and save it as csv
def produce_dataframe():
    df = pd.DataFrame()
    for i in range(500):
        random_song, random_pitches = create_random_song()
        # write stream to midi file
        stream = convert_to_stream(convert_to_duration(random_song),random_pitches)
        # save midi in the random_midis folder
        file_midi = f'random_midis/random_song_{i}.mid'
        stream.write('midi', file_midi)
        notes = map_beats(random_song)
        pitches = translate_pitches(random_pitches)
        tuples_note_pitch = []
        for i in range(len(notes)):
            for j in range(len(notes[i])):
                tuples_note_pitch.append((notes[i][j], pitches[i][j]))
        df = df.append({'id': i, 'notes': notes, 'pitches': pitches, 'beat_pitch': tuples_note_pitch, 'midi': file_midi}, ignore_index=True)
    df.to_csv('random_songs.csv', index=False)
    return df

# example
df = produce_dataframe()
