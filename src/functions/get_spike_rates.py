import numpy as np

def get_spike_rates(data):
    task_data = data['task_data']
    unit_data = data['unit_data']

    baseline_event_name = data['baseline_event_name']
    baseline_frame_start = data['baseline_frame_start']
    baseline_frame_end = data['baseline_frame_end']

    response_event_name = data['response_event_name']
    response_frame_start = data['response_frame_start']
    response_frame_end = data['response_frame_end']

    unit = unit_data['units'].iloc[0]
    spike_times = np.array(unit_data['spike_times'])

    baseline_rates = []
    for time in task_data[baseline_event_name]:
        start_time = time + baseline_frame_start
        end_time = time + baseline_frame_end
        spikes_in_window = ((spike_times >= start_time) & (spike_times <= end_time)).sum()
        window_duration = baseline_frame_end - baseline_frame_start
        spike_rate = spikes_in_window / window_duration
        baseline_rates.append(spike_rate)

    response_rates = []
    for time in task_data[response_event_name]:
        start_time = time + response_frame_start
        end_time = time + response_frame_end
        spikes_in_window = ((spike_times >= start_time) & (spike_times <= end_time)).sum()
        window_duration = response_frame_end - response_frame_start
        spike_rate = spikes_in_window / window_duration
        response_rates.append(spike_rate)

    spike_rates = np.array(response_rates) - np.array(baseline_rates)

    mu = float(np.mean(spike_rates))
    sigma = float(np.std(spike_rates, ddof=1))
    eps = 1e-12
    if not np.isfinite(sigma) or sigma < eps:
        sigma = eps
    z_scores = (spike_rates - mu) / sigma

    task_data[f'unit_{unit}_z_scores'] = z_scores.tolist()

    return task_data