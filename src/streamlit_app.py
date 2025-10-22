import streamlit as st

from functions.get_task_data import get_task_data
from functions.get_unit_data import get_unit_data
from functions.add_spike_rates import add_spike_rates


def streamlit_app():
    st.set_page_config(page_title="Unit Compiler")
    st.title("Unit Compiler")

    if 'task_data' not in st.session_state:
        st.session_state.task_data = None

    task_file = st.file_uploader("Upload Task File:")
    unit_files = st.file_uploader("Upload Unit File:", accept_multiple_files=True)

    st.write("")

    event_name = st.text_input("Event Name:", value='gabors_on_time')
    frame_start = float(st.text_input("Frame Start (s):", value='0.0'))
    frame_end = float(st.text_input("Frame End (s):", value='0.2'))

    st.write("")

    if st.button("Compile Units"):
        if st.session_state.task_data is None:
            task_data = get_task_data(task_file)
            st.session_state.task_data = task_data
        task_data = st.session_state.task_data

        for unit_file in unit_files:
            unit_data = get_unit_data(unit_file)

            data = {
                'task_data': task_data,
                'event_name': event_name,
                'unit_data': unit_data,
                'frame_start': frame_start,
                'frame_end': frame_end
            }

            task_data = add_spike_rates(data)
            st.session_state.task_data = task_data

    task_data = st.session_state.task_data

    if task_data is not None:
        st.write(task_data)

        date = task_data['Date'].iloc[0]
        experiment = task_data['Experiment'].iloc[0]
        file_name = f'{date}_{experiment}_full'

        st.download_button(
            label="Download Data",
            data=task_data.to_csv(index=False).encode('utf-8'),
            file_name=f'{file_name}.csv',
            mime='text/csv',
        )


if __name__ == '__main__':
    streamlit_app()
