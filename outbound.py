import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image

st.set_page_config(page_title='CUSTOMER SERVICE DEPARTMENT')
st.header('DINAMIC STATISTICS - CUSTOMER SERVICE DEPARTMENT')
st.subheader('Pick on the different categories to filter the information')

### --- LOAD DATAFRAME
excel_file = 'outbound_week_49.xlsx'
sheet_name = 'DATA'

df = pd.read_excel(excel_file,
                   sheet_name = sheet_name,
                   header = 0,
                   usecols='B:E')

df_nacionality = pd.read_excel(excel_file,
                                sheet_name= sheet_name,
                                usecols='G:H',
                                header=4)
df_nacionality.dropna(inplace=True)

df_week_day = pd.read_excel(excel_file,
                                sheet_name= sheet_name,
                                usecols='G:H',
                                header=11)
df_week_day.dropna(inplace=True)

df_hour_call = pd.read_excel(excel_file,
                                sheet_name= sheet_name,
                                usecols='G:H',
                                header=19)
df_hour_call.dropna(inplace=True)


# --- STREAMLIT SELECTION
nacionality = df['nacionality'].unique().tolist()
week_day = df['week day'].unique().tolist()
hour_call = df['hour call'].unique().tolist()

nacionality_selection = st.multiselect('Nacionality:',
                                    nacionality,
                                    default=nacionality)

week_day_selection = st.multiselect('Week day:',
                                    week_day,
                                    default=week_day)

hour_call_selection = st.multiselect('Hour call:',
                                    hour_call,
                                    default=hour_call)

# --- FILTER DATAFRAME BASED ON SELECTION
mask = (df['nacionality'].isin(nacionality_selection)) & (df['week day'].isin(week_day_selection)) & (df['hour call'].isin(hour_call_selection))
number_of_result = df[mask].shape[0]
st.markdown(f'*Available Results: {number_of_result}*')

# --- GROUP DATAFRAME AFTER SELECTION
df_grouped = df[mask].groupby(by=['disposition']).count()[['nacionality']]
df_grouped = df_grouped.rename(columns={'nacionality': 'Nº Customers'})
df_grouped = df_grouped.reset_index()

# --- PLOT BAR CHART
bar_chart = px.bar(df_grouped,
             x='disposition',
             y='Nº Customers',
             text='Nº Customers',
             color_discrete_sequence =['#F63366']*len(df_grouped),
             template= 'plotly_white')
st.plotly_chart(bar_chart)

# --- PLOT PIE CHART 1
pie_chart = px.pie(df_nacionality,
                title='PIE chart distributed by Nationality',
                values='Total',
                names='nacionality')

st.plotly_chart(pie_chart)

# --- DISPLAY IMAGE & DATAFRAME
col1, col2 = st.beta_columns(2)
image = Image.open('images/cs.jpg')
print(image)
col1.image(image,
        caption='Designed by slidesgo / Freepik',
        use_column_width=True)
col2.dataframe(df[mask])