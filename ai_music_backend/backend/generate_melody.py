from miditoolkit.midi import parser as mid_parser  
from miditoolkit.midi import containers as ct
import io
# import miditoolkit
import random
import os
import shutil


SEP = '[sep]'
ALIGN = '[align]'
bpm = 240
prec = 1000000
mspb = 60 * 1000 / bpm
REST_NOTE = 128


Duration_vocab = dict([(129+i, str(x/100))
                       for i, x in enumerate(list(range(25, 3325, 25)))])


def get_pitch_duration_structure(note_seq):
    seq = []

    # 遍历寻找pitch-duration的结构
    # 当有不合法情况出现时，找最后一个pitch和第一个duration，保证其相邻
    # p1 d1 p2 p3 d2 p4 d3-> p1 d1 p3 d1 p4 d3
    # p1 d1 p2 d2 d3 p3 d4-> p1 d1 p2 d2 p3 d4
    # p1 d1 p2 p3 d2 d3 p4 d4 -> p1 d1 p3 d2 p4 d4

    i = 0
    while (i < len(note_seq)):
        if note_seq[i] > 128:
            # Duration
            i += 1
            continue
        else:
            # Pitch
            if i+1 >= len(note_seq):
                # No Duration Followed
                break
            if note_seq[i+1] <= 128:
                # Followed by a pitch
                i += 1
                continue

            # Here trans back to str for bleu calculate
            pitch = str(note_seq[i])
            duration = str(note_seq[i+1])

            seq.append(pitch)
            seq.append(duration)
            i += 2
    return seq


def ms_to_time(input):
    ms = input % 1000 // 10
    input //= 1000
    s = input % 60
    minute = s // 60
    return f'[{minute:02d}:{s:02d}.{ms:02d}]'

def lyric_align(inputs):
    lst = inputs.split()
    sep_positions = [i for i, x in enumerate(lst) if x == SEP]
    sep_positions.insert(0, -1)

    cur_time = 0
    ret = []
    for i in range(len(sep_positions)-1):
        # SZH: not include sep token
        sent = lst[sep_positions[i]+1:sep_positions[i+1]]
        sent = list(map(int, sent))
        duration = 0
        for x in sent:
            if x > 128:
                duration += float(Duration_vocab[x])

        ret.append(ms_to_time(int(cur_time)))
        cur_time += duration * mspb

    return ret


def separate_sentences(x, convert_int=False, find_structure=False):
    lst = x.copy()
    sep_positions = [i for i, x in enumerate(lst) if x == SEP]
    sep_positions.insert(0, -1)

    ret = []
    for i in range(len(sep_positions)-1):
        # SZH: not include sep token
        sent = lst[sep_positions[i]+1:sep_positions[i+1]]
        if convert_int:
            sent = list(map(int, sent))
        if find_structure:
            sent = list(map(int, sent))
            sent = get_pitch_duration_structure(sent)
        ret.append(sent)

    return ret


def gen_midi(note_seq, out_file):
    #Check Seq
    seq = []
    current_is_pitch = 'PITCH'

    #遍历寻找pitch-duration的结构
    #当有不合法情况出现时，找最后一个pitch和第一个duration，保证其相邻
    #p1 d1 p2 p3 d2 p4 d3-> p1 d1 p3 d1 p4 d3
    #p1 d1 p2 d2 d3 p3 d4-> p1 d1 p2 d2 p3 d4
    #p1 d1 p2 p3 d2 d3 p4 d4 -> p1 d1 p3 d2 p4 d4

    i = 0
    while (i < len(note_seq)):
        if note_seq[i] > 128:
            #Duration
            i += 1
            continue
        else:
            #Pitch
            if i+1 >= len(note_seq):
                #No Duration Followed
                break
            if note_seq[i+1] <= 128:
                #Followed by a pitch
                i += 1
                continue

            #Followed by a duration
            pitch = note_seq[i]
            duration = float(Duration_vocab[note_seq[i+1]])
            seq.append((pitch, duration))
            i += 2

    # pattern = midi.Pattern()
    # track = midi.Track()
    # pattern.append(track)

    # create an empty file
    mido_obj = mid_parser.MidiFile()
    beat_resol = mido_obj.ticks_per_beat

    # create an  instrument
    track = ct.Instrument(program=0, is_drum=False, name='Lead')
    mido_obj.instruments = [track]

    prev_end = 0
    # rest_time = 0

    for note in seq:
        print(note)
        duration = round(note[1] * beat_resol)
        if note[0] < 128:  # Pitch
            start = prev_end
            end = prev_end + duration
            print(f"{note[0]} from {start} to {end}")
            nt = ct.Note(start=start, end=end, pitch=note[0], velocity=100)
            mido_obj.instruments[0].notes.append(nt)
            prev_end += duration

            # Instantiate a MIDI note on event, append it to the track
            # tick:according to last?
            # on = midi.NoteOnEvent(tick=rest_time, velocity=100, pitch=note[0])
            # track.append(on)

            # # Instantiate a MIDI note off event, append it to the track
            # off = midi.NoteOffEvent(tick=round(note[1]*mspb), pitch=note[0])
            # track.append(off)

            # rest_time = 0
        else:  # Rest
            assert note[0] == REST_NOTE
            prev_end += duration
            # rest_time += round(note[1]*mspb)

    # create makers
    marker_hi = ct.Marker(time=0, text='HI')
    mido_obj.markers.append(marker_hi)

    mido_obj.tempo_changes.append(ct.TempoChange(240, 0))

    mido_obj.dump(out_file)
    # Add the end of track event, append it to the track
    # eot = midi.EndOfTrackEvent(tick=1)
    # track.append(eot)

    # pattern.append(track)
    # return pattern


def to_midi(inputs, path):
    notes = inputs.split()
    print(notes)
    sents = separate_sentences(notes, True, True)
    # print(sents)
    note_seq = []
    for s in sents:
        note_seq.extend(s)
    note_seq = list(map(int, note_seq))
    print(note_seq)
    gen_midi(note_seq, path)
    # midi.write_midifile(path, pattern)
