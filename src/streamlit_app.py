import streamlit as st

from functions.get_task_data import get_task_data
from functions.get_unit_data import get_unit_data
from functions.get_spike_rates import get_spike_rates



def streamlit_app():
    st.set_page_config(page_title="Unit Compiler")
    st.title("Unit Compiler")

    if 'task_data' not in st.session_state:
        st.session_state.task_data = None

    task_file = st.file_uploader("Upload Task File:")
    unit_files = st.file_uploader("Upload Unit File:", accept_multiple_files=True)
    
    st.subheader("Baseline Settings")
    baseline_event_name = st.text_input("Event Name:", value='rings_on_time')
    baseline_frame_start = float(st.text_input("Frame Start (s):", value='-0.2'))
    baseline_frame_end = float(st.text_input("Frame End (s):", value='0.0'))

    st.write("")
    
    st.subheader("Response Settings")
    response_event_name = st.text_input("Event Name:", value='gabors_on_time')
    response_frame_start = float(st.text_input("Frame Start (s):", value='0.0'))
    response_frame_end = float(st.text_input("Frame End (s):", value='0.2'))

    st.write("")

    if task_file and unit_files:
        st.write("")

        task_data = get_task_data(task_file)
        st.write(task_data)

        st.write("")

        if st.button("Compile Units"):
            for unit_file in unit_files:
                unit_data = get_unit_data(unit_file)

                data = {
                    'task_data': task_data,
                    'unit_data': unit_data,
                    'baseline_event_name': baseline_event_name,
                    'baseline_frame_start': baseline_frame_start,
                    'baseline_frame_end': baseline_frame_end,
                    'response_event_name': response_event_name,
                    'response_frame_start': response_frame_start,
                    'response_frame_end': response_frame_end,
                }

                task_data = get_spike_rates(data)

            st.write("")

            st.write(task_data)

            date = task_data['Date'].iloc[0]
            file_name = f'{date}_data'

            st.write("")

            st.download_button(
                label="Download Data",
                data=task_data.to_csv(index=False).encode('utf-8'),
                file_name=f'{file_name}.csv',
                mime='text/csv',
            )


if __name__ == '__main__':
    streamlit_app()
