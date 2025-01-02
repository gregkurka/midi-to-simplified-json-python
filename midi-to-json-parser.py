import mido
from mido import MidiFile

global BPM

def ticks_to_musical_duration(ticks, ticks_per_beat):
    quarter_note_duration = ticks_per_beat
    duration_ratio = ticks / quarter_note_duration
    return f"{duration_ratio:.3f}"

# Function to convert MIDI note number to note name
def midi_note_to_name(note):
    notes = ['c', '#c', 'd', '#d', 'e', 'f', '#f', 'g', '#g', 'a', '#a', 'b']
    octave = note // 12 - 4
    if octave < 1:
        if octave == 0:
            octave = ''
        elif octave == -1:
            notes = ['C', '#C', 'D', '#D', 'E', 'F', '#F', 'G', '#G', 'A', '#A', 'B']
            octave = '-1'
        elif octave == -2:
            notes = ['C', '#C', 'D', '#D', 'E', 'F', '#F', 'G', '#G', 'A', '#A', 'B']
            octave = '-2'
    return notes[note % 12] + str(octave)

def noteDurationJSON(duration, is_rest):
    string = 'isTuplet'
    duration = float(duration)

    if is_rest:
        possibleDurations = {
          'R,R,R,R,R,R,R,R,R,R,R,R,R,R,T,V': 57.25,
          'R,R,R,R,R,R,R,R,R,R,ST,U': 43.5,'R,R,R,R,R,R,R,R,R,R': 40,
          'R,R,R,R,R,R,R,R': 32, 'R,R,R,R,R,R,R,T,UV':29.75,'R,R,R,R,R,R,R': 28,
          'R,R,R,R,R,R': 24, 'R,R,R,R,R,T': 21, 'R,R,R,R,R': 20,'R,R,R,R,ST,U': 19.5, 'R,R,R,R,ST,V': 19.25,
          'R,R,R,R,T': 17, 'R,R,R,R': 16, 'R,R,R': 12, 'R,R,T,V': 9.25, 'R,R,T': 9,
          'R,R': 8,'R,R,R,R,U': 16.5, 'R,R,R,R,V': 16.25, 'R,R,R,ST':15, 'R,R,R,T,U': 13.5, 'R,R,R,T': 13,
          'R,R,R,U': 12.5, 'R,R,R': 12, 'R,R,S,T,V': 11.25,'R,R,ST': 11, 'R,R,T,T': 10, 
          'R,R,U,W': 8.875, 'R,R,U': 8.5,
          'R,ST,U': 7.5, 'R,S,UV': 6.75, 'R,S,V': 6.25, 'R,S,U': 6.5, 'R,S': 6, 'R,T,UV': 5.75,
          'R,T,U,W': 5.625, 'R,T,U': 5.5, 'R,T': 5,
          'R,UV': 4.75, 'R,U': 4.5, 'R': 4, 'ST,UV': 3.75, 'ST,U,W': 3.625,'ST,U':3.5,
          'ST, V': 3.25, 'ST': 3, 'S, UV': 2.75, 'S,U': 2.5, 'S,V': 2.25, 'S': 2,
          'TU': 1.5, 'T,UV': 1.75, 'T,W,W,W': 1.375, 'T,W': 1.125, 'T,V': 1.25,
          'T': 1, 'UVW': .875, 'UV': .75, 'U,W': .625, 'U': .5, 'W,W,W': .375, 'V': 0.25, 'W': 0.125
        }
        for key, value in possibleDurations.items():
            if value == duration:
                string = key
                break
    else:
        possibleDurations = {
            'HHJ': 18, 'HH': 16,
            'HI': 12, 'HJK': 11, 'HJ': 10, 'HKL': 9.5, 'HK': 9, 
            'HLN': 8.625, 'HL': 8.5, 'H': 8, 
            'IJKLMN': 7.875, 'IJKLM': 7.75, 'IJKL': 7.5, 'IJKN': 7.125, 'IJK':7,
            'IJLM': 6.75, 'IJL': 6.5, 'IJMN': 6.375,'IJM': 6.25,
            'IJ':6,'IKLM': 5.75, 'IKLN': 5.625,
            'IKL': 5.5, 'IKMN': 5.375, 'IKM': 5.25, 'IKN': 5.125, 'IK': 5, 
            'ILMN': 4.875, 'ILM': 4.75, 'IL': 4.5, 'IMN': 4.375, 'IM': 4.25, 'I': 4.00,
            'JKLMN': 3.875, 'JKLM': 3.75, 'JKL': 3.5,  'JKM': 3.25, 'JKN': 3.125, 'JK': 3,
            'JLMN': 2.875, 'JLM': 2.75, 'JLN': 2.625, 'JL':2.5,
            'JMN': 2.375, 'JM': 2.25, 'JN': 2.125,'J': 2, 
            'KLMN':1.875,'KLM': 1.75, 'KLN': 1.625,'KL': 1.5,
            'KMN': 1.375, 'KM': 1.25, 'KN': 1.125,
            'K': 1, 'LMN': 0.875, 'LM': .75, 'LN': .625, 'L': .5,
            'MN': 0.375, 'M': 0.25, 'N': 0.125
        }
        for key, value in possibleDurations.items():
            if value == duration:
                string = key
                break
    
    return string

def songCreator(midi_path):
    mid = MidiFile(midi_path)
    ticks_per_beat = mid.ticks_per_beat
    song = []

    for i, track in enumerate(mid.tracks):
        song.append({"Track": track.name})
        note_start_times = {}
        last_note_off_time = 0
        last_activity_time = 0  # Tracks the last time of any musical activity
        cumulative_time = 0
        first_event = True  # Flag to check for the first event

        for msg in track:
            if not msg.is_meta:
                cumulative_time += msg.time

                # Check for an initial rest
                if first_event and cumulative_time > 0:
                    rest_duration = ticks_to_musical_duration(cumulative_time, ticks_per_beat)
                    song.append({'Rest': True, 'Duration': rest_duration})
                    first_event = False
                    last_activity_time = cumulative_time
                
                if msg.type == 'note_on' and msg.velocity > 0:
                    note_start_times[msg.note] = cumulative_time
                    if cumulative_time - last_activity_time > 0 and last_note_off_time != 0:
                        rest_duration_ticks = cumulative_time - last_activity_time
                        rest_duration = ticks_to_musical_duration(rest_duration_ticks, ticks_per_beat)
                        song.append({'Rest': True, 'Duration': rest_duration})
                        last_activity_time = cumulative_time
                    first_event = False
                elif (msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0)) and msg.note in note_start_times:
                    start_time = note_start_times.pop(msg.note)
                    duration_ticks = cumulative_time - start_time
                    duration = ticks_to_musical_duration(duration_ticks, ticks_per_beat)
                    song.append({'Note': midi_note_to_name(msg.note), 'Duration': duration, 'Time': cumulative_time})
                    last_note_off_time = cumulative_time
                    last_activity_time = cumulative_time  # Update last activity time here as well
  

    return song

def ticks_to_timestamp(event):
    """
    Convert MIDI ticks to a real-time timestamp.

    :param event: A dictionary containing the 'Time' key with cumulative ticks.
    :param ticks_per_beat: The number of ticks per beat (PPQ) in the MIDI file.
    :param tempo: The tempo in microseconds per quarter note.
    :return: A string with the timestamp in minutes and seconds format.
    """
    global BPM
    tempo = int(60_000_000 / int(BPM))
    ticks_per_beat = 120
    # Extract the cumulative time in ticks from the event
    ticks = 0
    if 'Time' in event:
        ticks = int(event['Time'])

    # Calculate the time in seconds
    # tempo is in microseconds per quarter note, so we convert it to seconds per quarter note
    # then multiply by the number of beats (ticks / ticks_per_beat)
    seconds = (ticks / ticks_per_beat) * (tempo / 1_000_000)

    # Convert seconds to minutes and seconds
    minutes = int(seconds // 60)
    seconds = seconds % 60

    # Format the timestamp as MM:SS
    timestamp = f"{minutes}:{seconds:02.0f}"

    return timestamp

def print_next_items(start_index, song, max_lookahead=20):
    # Calculate the maximum number of items to print, based on song length
    max_index = min(len(song), start_index + max_lookahead)
    # Iterate through the next items up to the max index
    iterateVar = 1
    for index in range(start_index, max_index):
        item = song[index]
        # Print 'Duration' and 'Time' if present, else print the whole item
        print(iterateVar, end = ": ")
        iterateVar += 1
        print(item.get('Duration', item), end = " , ")
        print(item.get('Time', ''), end = " , ")
        print(ticks_to_timestamp(item))


def calculate_unique_total_duration(list_of_dicts):
    encountered_times = set()  # Set to keep track of encountered 'Time' values
    total_duration = 0  # Variable to hold the total duration

    for dct in list_of_dicts:
        time = dct.get('Time')
        # Check if this 'Time' has not been encountered and 'Duration' is a valid key
        if time not in encountered_times and 'Duration' in dct:
            total_duration += float(dct['Duration'])
            encountered_times.add(time)  # Mark this 'Time' as encountered

    return round(total_duration, 2)


def convertTrackJson(song):
    #for item in song:
        #print(item)
    jsonString = ''
    trackIndex = 0
    index = 0

    while index < len(song):
        ### Main Loop ###
            #deal with tracks
            #check for tuplets
            #check for polyphony in tuplets
            #check for polyphony in general
            #add regular notes
            #################

            #Deal with Tracks
        if 'Track' in song[index]:
                if trackIndex == 0:
                    trackIndex += 1
                elif trackIndex == 1:
                    trackIndex += 1
                elif trackIndex > 1:
                    jsonString += '","'
                    trackIndex += 1
                index += 1
                continue

            #All logic for track notes
        elif 'Rest' in song[index] or 'Note' in song[index]:
                #Check for tuplets
                if noteDurationJSON(song[index]['Duration'], False) == 'isTuplet' and noteDurationJSON(song[index]['Duration'], True) == 'isTuplet':
                    print_next_items(index, song)
                    try:
                        tupletGroupSize = int(input("Enter the number of notes in the tuplet group: "))
                    except ValueError:
                        print("Invalid input, using default group size of 3")
                        tupletGroupSize = 3

                    tupletList = []
                    totalDuration = 0.000
                    index2 = 0
                    while index2 < tupletGroupSize:
                        tupletList.append(song[index + index2])
                        index2 += 1
                    totalDuration = calculate_unique_total_duration(tupletList)
                    print("The total duration is ", end = ": ")
                    print(totalDuration)

                    tupletString = '('
                    for i, item in enumerate(tupletList):
                        print(item, end=" *** \n")
                        
                        # Add the current item's 'Note' to the string
                        tupletString += item['Note']
                        
                        # Check if we are not at the last item and compare the current and next item's 'Time'
                        if i < len(tupletList) - 1 and item['Time'] == tupletList[i + 1]['Time']:
                            separator = '.'  # Use a period if the next item has the same 'Time'
                        else:
                            separator = '~'  # Use a tilde otherwise
                        
                        # Add the separator, except for the last item
                        if i < len(tupletList) - 1:
                            tupletString += separator

                    tupletString = tupletString.rstrip('~.')  # Remove the last tilde or period if any
                    tupletString += ')[' + noteDurationJSON(totalDuration, False) + '],'
                    print(tupletString)
                    jsonString += tupletString
                    index += tupletGroupSize
                    continue
                
                #Deal with anything that are not tracks and tuplets
                else:
                    #Rests
                    if 'Rest' in song[index]:
                        jsonString += noteDurationJSON(song[index]['Duration'], True) + ','
                        index += 1
                        continue

                    #All notes that are not tuplets
                    else:
                        multiNote = [song[index]]
                        indexX = 1
                        while (indexX + index) < len(song):
                            if 'Track' in song[indexX+index]:
                                break
                            elif 'Rest' in song[indexX+index]:
                                break
                            elif song[index]['Time'] == song[indexX+index]['Time']:
                                multiNote.append(song[indexX+index])
                                indexX += 1
                            else:
                                break
                        if len(multiNote) > 1:
                            polyphonicString = "("
                            for item in multiNote:
                                polyphonicString += item['Note'] + "."
                            polyphonicString = polyphonicString.rstrip('.')
                            polyphonicString += ")[" + noteDurationJSON(song[index]['Duration'], False) + "],"
                            jsonString += polyphonicString

                        else:
                            jsonString += song[index]['Note'] + "[" + noteDurationJSON(song[index]['Duration'], False) + "],"
                        
                        index += len(multiNote)
                        continue
    jsonString += '"],"instruments":['
    for x in range(trackIndex-1):
        jsonString += '"piano",'
    jsonString = jsonString.rstrip(',')

    jsonString += '],"alternatives":['
    for y in range(trackIndex-1):
        jsonString+='"",'
    jsonString = jsonString.rstrip(',')

    
    return jsonString

#main
BPM = input("enter BPM: ")
baseBeats = input("enter Base Beats: ")
totalJsonString = '{"baseBpm":' + BPM + ',"demo":null,"audition":null,"musics":['
totalJsonString += '{"baseBeats":' + baseBeats + ',"measureBeats":4,"scores":["'
totalJsonString += convertTrackJson(songCreator('1.mid'))
print("***END OF TRACK 1!!!!!****")
totalJsonString += '],"id":1,"bpm":' + BPM + '},{"baseBeats":' + baseBeats + ',"measureBeats":4,"scores":["'
totalJsonString += convertTrackJson(songCreator('2.mid'))
print("***END OF TRACK 2!!!!!****")
totalJsonString += '],"id":2,"bpm":' + BPM + '},{"baseBeats":' + baseBeats + ',"measureBeats":4,"scores":["'
totalJsonString += convertTrackJson(songCreator('3.mid'))
print("***END OF TRACK 3!!!!!****")
totalJsonString += '],"id":3,"bpm":' + BPM + '}]}'
print(totalJsonString)

with open('load.json','w') as file:
    file.write(totalJsonString)
