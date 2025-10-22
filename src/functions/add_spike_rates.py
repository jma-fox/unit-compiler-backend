import numpy as np

def add_spike_rates(data):
    task_data = data['task_data']
    event_name = data['event_name']
    unit_data = data['unit_data']
    frame_start = data['frame_start']
    frame_end = data['frame_end']

    unit = unit_data['units'].iloc[0]
    spike_times = np.array(unit_data['spike_times'])

    spike_rates = []
    for time in task_data[event_name]:
        start_time = time + frame_start
        end_time = time + frame_end
        spikes_in_window = ((spike_times >= start_time) & (spike_times <= end_time)).sum()
        window_duration = frame_end - frame_start
        spike_rate = spikes_in_window / window_duration
        spike_rates.append(spike_rate)

    task_data[f'unit_{unit}_spike_rates'] = spike_rates

    return task_data