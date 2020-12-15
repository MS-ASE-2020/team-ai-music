import requests
import urllib.request
import json
import miditoolkit


def process(raw, processed):
    """
    该api仅支持单轨(旋律轨)MIDI文件输入，因此需要处理成单轨
    """
    print(f'Upload {raw}, store to {processed}')
    ip = 'http://168.61.41.164:8080'
    upload = '/api/popmag/upload_midi'
    files = {'midi': open(raw, 'rb')}
    try:
        # FIXME: Bypassing model server for now
        # raise Exception
        res = requests.post('%s%s' % (ip, upload), files=files, timeout=20)
    except Exception as e:
        print(f'Model server failed with {e}, using xuanlv instead')
        with open(processed, 'wb') as pd:
            with open(raw, 'rb') as r:
                pd.write(r.read())
    else:
        print(f'Model server success: {res.text}')
        res = json.loads(res.text)
        if res.get("file_url", None):
            urllib.request.urlretrieve('%s%s' % (ip, res["file_url"]), processed)
        else:
            raise Exception(res['errmsg'])


def select_track(filename, tracks):
    print(tracks)
    midiobj = miditoolkit.midi.parser.MidiFile(filename)    
    print(midiobj.instruments)
    midiobj.instruments = [i for i in midiobj.instruments if i.name in tracks]  
    print(midiobj.instruments)
    midiobj.dump(filename)


if __name__ == '__main__':
    # raw_midi = 'data/tmp/MainSynth.mid'
    raw_midi = './lead_tracks/6.mid'
    processed_midi = './processed.mid'
    process(raw_midi, processed_midi)
