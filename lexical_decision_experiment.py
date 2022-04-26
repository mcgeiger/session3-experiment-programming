import pandas as pd
import numpy as np
from psychopy import core, visual, event, sound

participant_ID = '14' #type participant ID here. Was trying to find a way to do that in the experiment window. But didn't yet. 

output_dir = 'output/'
stimuli_df = pd.read_csv('lexical_decision_stimuli.csv')
stimuli_df["freq_category"].replace({"none": "NW"}, inplace=True)
audio_stim_list = []
results = []

# randomize stimuli
stimuli_df = stimuli_df.iloc[np.random.permutation(stimuli_df.index)].reset_index(drop=True)
for lex in stimuli_df['word']:
    target_F = stimuli_df.loc[stimuli_df['word'] == lex, 'freq_category'].iloc[0]
    audio_stim = sound.Sound(f'sounds/{target_F}/{lex}.wav')
    audio_stim_list.append(audio_stim) 
stimuli_df['audio_stim'] = audio_stim_list
    

window = visual.Window()
clock = core.Clock()
#intro screen
message = visual.TextStim(window, 'You are going to hear some words. Some words are real and some are not. If the word is real, press "z", if the word is not a real word press "m". Do this as fast as you can. When you are ready to start the experiment, press "m".') #could be made to look nicer
countdown1= visual.TextStim(window, '3')
countdown2= visual.TextStim(window, '2')
countdown3= visual.TextStim(window, '1')

message.draw()
window.flip()
ready = event.waitKeys(keyList=['m'], clearEvents=True)
if ready is not None:
    countdown1.draw()
    window.flip()
    core.wait(1)
    countdown2.draw()
    window.flip()
    core.wait(1)
    countdown3.draw()
    window.flip()
    core.wait(1)

#here the actual experiment starts
fixation = visual.TextStim(window, '+')
choice= visual.TextStim(window, '!')
for stimulus in stimuli_df['audio_stim']:
    fixation.draw()
    window.flip()
    core.wait(1)
    choice.draw()
    window.flip()
    stimulus.play()
    start_time = clock.getTime()
    keys = event.waitKeys(maxWait=5, keyList=['z', 'm'], timeStamped=clock, clearEvents=True)
    if keys is not None:
        key, end_time = keys[0]
        window.flip()
        core.wait(0.5)
    else:
        key = 'NA'
        end_time = clock.getTime()
        window.flip()
        core.wait(0.5)
    duration = stimulus.getDuration()
    results.append({
        'participant_ID': participant_ID,
        'stim_id': stimuli_df.loc[stimuli_df['audio_stim'] == stimulus, 'stim_id'].iloc[0],
        'condition': stimuli_df.loc[stimuli_df['audio_stim'] == stimulus, 'condition'].iloc[0],
        'freq_category': stimuli_df.loc[stimuli_df['audio_stim'] == stimulus, 'freq_category'].iloc[0],
        'word': stimuli_df.loc[stimuli_df['audio_stim'] == stimulus, 'word'].iloc[0],
        'subtlex_log10freq': stimuli_df.loc[stimuli_df['audio_stim'] == stimulus, 'subtlex_log10freq'].iloc[0],
        'stim_duration': duration,
        'start_time': start_time,
        'end_time': end_time,
        'key': key
    })

#thanks message
message = visual.TextStim(window, 'Thanks for participating! :)') 
message.draw()
window.flip()
core.wait(5)

results = pd.DataFrame(results)
results['reaction_time'] = results['end_time'] - results['start_time']
results.to_csv(output_dir + participant_ID + '.csv')


