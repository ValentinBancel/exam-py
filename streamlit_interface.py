import pandas as pd
import time
import streamlit as st
import requests
import random

def get_data():
    df = pd.DataFrame(requests.get('https://jsonplaceholder.typicode.com/users').json())
    user1 = create_user()
    user2 = create_user()
    user3 = {
        'id': 44,
        'name': 'valentin bancel',
        'username': 'skyangel1804',
        'email':'valentin.bancel@ynov.com',
        'address': {
            'street': '1 rue de la paix',
            'suite': 'appartement 1',
            'city': 'Paris',
            'zipcode': '75000',
            'geo': {
                'lat': '48.8575' ,
                'lng': '2.3514'
            }
        },
        'phone': '0123456789',
        'website': 'https://www.valentin-bancel.tech',
        'company': {
            'name': 'Isi-Dsi',
            'catchPhrase': 'Innovate the future',
            'bs': 'Innovation' 
        }
    }
    df = pd.concat([df, pd.DataFrame([user3])], ignore_index=True)
    df = pd.concat([df, pd.DataFrame([user1]), pd.DataFrame([user2])], ignore_index=True)
    clean_address(df)
    df.rename(columns={'lng': 'lon'}, inplace=True)
    df['lat'] = df['lat'].astype(float)
    df['lon'] = df['lon'].astype(float)
    return df

def filter_data(df, filters):
    for filter, value in filters.items():
        if value:
            df = df[df[filter].str.contains(value, case=False, na=False)]
    return df

def clean_data():
    st.empty()


def clean_address(df: pd.DataFrame):
    df['city'] = df['address'].apply(lambda x: x['city'])
    df['lat'] = df['address'].apply(lambda x: x['geo']['lat'])
    df['lng'] = df['address'].apply(lambda x: x['geo']['lng'])
    df['street'] = df['address'].apply(lambda x: x['street'])
    df['suite'] = df['address'].apply(lambda x: x['suite'])
    df['zipcode'] = df['address'].apply(lambda x: x['zipcode'])
    df['company_name'] = df['company'].apply(lambda x: x['name'])
    df['company_catchPhrase'] = df['company'].apply(lambda x: x['catchPhrase'])
    df['company_bs'] = df['company'].apply(lambda x: x['bs'])
    df.drop('address', axis=1, inplace=True)
    df.drop('company', axis=1, inplace=True)
    return df

def create_user():
    user = {
        'id': random.randint(1, 1000),
        'name': f'User{random.randint(1, 1000)}',
        'username': f'username{random.randint(1, 1000)}',
        'email': f'user{random.randint(1, 1000)}@example.com',
        'address': {
            'street': f'{random.randint(1, 100)} Main St',
            'suite': f'Apt {random.randint(1, 100)}',
            'city': f'City{random.randint(1, 100)}',
            'zipcode': f'{random.randint(10000, 99999)}',
            'geo': {
                'lat': f'{random.uniform(-90, 90):.4f}',
                'lng': f'{random.uniform(-180, 180):.4f}'
            }
        },
        'phone': f'{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}',
        'website': f'www.user{random.randint(1, 1000)}.com',
        'company': {
            'name': f'Company{random.randint(1, 1000)}',
            'catchPhrase': f'CatchPhrase{random.randint(1, 1000)}',
            'bs': f'BS{random.randint(1, 1000)}'
        }
    }
    return user

def display_progess_bar():
    progress_text = "Operation in progress. Please wait."
    my_bar = st.progress(0, text=progress_text)
    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text=progress_text)
    time.sleep(1)
    my_bar.empty()

def display_map(df):
    if not df.empty:
        st.map(df[['lat', 'lon']])

st.set_page_config(layout="wide")

st.title('Data views List')

df = get_data()
filters = st.columns(3)
filters = {
    'name': filters[0].text_input('Name'),
    'username': filters[1].text_input('Username'),
    'email': filters[2].text_input('Email'),
    'city': filters[0].text_input('City'),
    'zipcode': filters[1].text_input('Zipcode'),
    'company_name': filters[2].text_input('Company name'),
}

if 'search_results' not in st.session_state:
    st.session_state.search_results = df

if st.button('Search'):
    display_progess_bar()
    st.session_state.search_results = filter_data(df, filters)
    # st.snow()
    if st.session_state.search_results.empty:
        st.write("No results found.")
    else:
        col1, col2 = st.columns([3, 2])
        with col1:
            st.write(st.session_state.search_results)
        with col2:
            display_map(st.session_state.search_results)
else:
    if st.session_state.search_results.empty:
        st.write("No results found.")
    else:
        col1, col2 = st.columns([3, 2])
        with col1:
            st.write(st.session_state.search_results)
        with col2:
            display_map(st.session_state.search_results)
