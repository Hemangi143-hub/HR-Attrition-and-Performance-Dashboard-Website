import io
import pandas as pd
import streamlit as st

def space(num_lines=1):
    for _ in range(num_lines):
        st.write("")

def sidebar_space(num_lines=1):
    for _ in range(num_lines):
        st.sidebar.write("")


def sidebar_multiselect_container(massage, arr, key):
    container = st.sidebar.container()
    select_all_button = st.sidebar.checkbox("Select all for " + key + " plots")
    if select_all_button:
        selected_num_cols = container.multiselect(massage, arr, default = list(arr))
    else:
        selected_num_cols = container.multiselect(massage, arr, default = arr[0])
        
    return selected_num_cols