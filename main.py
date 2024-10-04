import pandas as pd
import numpy as np
import streamlit as st
# import matplotlib.pyplot as plt
# import seaborn as sns
import plotly.express as px
import plotly.graph_objs as go


# Page configuration
st.set_page_config(
    page_title="AI Visionaries",
    page_icon="🍁",
    layout="wide",
    initial_sidebar_state="expanded")

##Setting Title
st.markdown(
    """
    <h1 style='text-align: center; color: skyblue;'>🍁: State/UT wise Sexual Assault Data Analysis (India)</h1>
    """, 
    unsafe_allow_html=True
)
st.markdown('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)

## add our logo 
st.sidebar.image("Ai_vis_01.jpg")
## create finters
st.sidebar.header("Applu filters: ")
## read the data 
## lode the crime against woman 2001 - 2014 data
df_state_UT= pd.read_csv('crimes_against_women_2001-2014.csv')

# # rename some columns
df_state_UT.rename(columns={
 'Assault on women with intent to outrage her modesty':'Outraging_Modesty',
 'Insult to modesty of Women':'Insult_modesty',
 'Cruelty by Husband or his Relatives':'Husband_relatives',
},inplace=True)
# ## convert all state name to lower case
df_state_UT['STATE/UT'] = df_state_UT['STATE/UT'].str.title()

## put all Union Teritory into UT
df_state_UT['STATE/UT'] = df_state_UT['STATE/UT'].replace({
    'A & N Islands': 'UT',
    'Puducherry': 'UT',
    'Chandigarh': 'UT',
    'A&N Islands': 'UT',
    'Delhi Ut': 'UT',
    'Lakshadweep': 'UT',
    'Daman & Diu': 'UT',
    'D & N Haveli': 'UT',
    'D&N Haveli': 'UT',
    'Delhi':'UT'
})

## Streamlit portion and Plotting 

# put the side bar filter 
state_filter = st.sidebar.multiselect("Chose State or select all ", df_state_UT["STATE/UT"].unique())
year_filter = st.sidebar.multiselect("Chose Year or select all ", df_state_UT["Year"].unique())

#create a check box
val_checkbox = st.checkbox("Select all",value= True)



# plot the total rape cases data using line plot
rape=df_state_UT.groupby('Year')['Rape'].count().reset_index()

def plot_rapes(rape):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=rape['Year'],
        y=rape['Rape'],
        mode='markers+lines',
        marker=dict(symbol='x', color='red', size=6),
        line=dict(width=2),
        name='Total rapes'
    ))

    fig.update_layout(
        title="TotalRape cases in India by states",
        title_font=dict(size=20, color='navy', family='Arial', weight='bold'),
        xaxis_title='Year',
        xaxis_title_font=dict(size=15),
        yaxis_title='Total cases',
        yaxis_title_font=dict(size=15),
        template='plotly_white'  
    )

    fig.update_layout(showlegend=True)

    return fig

st.plotly_chart(plot_rapes(rape))

## Total Cases of Kidnapping and Insult Modesty (2001 - 2014)
kidnap=df_state_UT.groupby('Year')['Kidnapping and Abduction'].mean().reset_index()
insult=df_state_UT.groupby('Year')['Insult_modesty'].mean().reset_index()
outraging=df_state_UT.groupby('Year')['Outraging_Modesty'].mean().reset_index()
husband=df_state_UT.groupby('Year')['Husband_relatives'].mean().reset_index()

##plot the data from other categories
def plot_o_h_k_i(outraging, husband, kidnap,insult):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=outraging['Year'],
        y=outraging['Outraging_Modesty'],
        mode='markers+lines',
        marker=dict(symbol='star', color='orange', size=6),
        line=dict(width=1),
        name='Outraging Modesty'
    ))

    fig.add_trace(go.Scatter(
        x=husband['Year'],
        y=husband['Husband_relatives'],
        mode='markers+lines',
        marker=dict(symbol='star', color='purple', size=6),
        line=dict(width=1),
        name='Husband & relatives'
    ))

    fig.add_trace(go.Scatter(
        x=kidnap['Year'],
        y=kidnap['Kidnapping and Abduction'],
        mode='markers+lines',
        marker=dict(symbol='star', color='blue', size=6),
        line=dict(width=1),
        name='Kidnap & Abduction'
    ))

    fig.add_trace(go.Scatter(
        x=insult['Year'],
        y=insult['Insult_modesty'],
        mode='markers+lines',
        marker=dict(symbol='star', color='green', size=6),
        line=dict(width=1),
        name='Insult modesty'
    ))
    
    fig.update_layout(
        title="Total Cases of Husband_relatives Cases VS Outraging_Modesty Cases",
        title_font=dict(size=20, color='navy', family='Arial', weight='bold'),
        xaxis_title='Year',
        xaxis_title_font=dict(size=15),
        yaxis_title='Total cases',
        yaxis_title_font=dict(size=15),
        template='plotly_white'  
    )

    fig.update_layout(showlegend=True)

    return fig

st.plotly_chart(plot_o_h_k_i(outraging, husband, kidnap,insult))

# Calculate the top 7 states with the most rape cases
def get_top_states_by_rape(df):
    top_states = df.groupby('STATE/UT')['Rape'].sum().reset_index()
    return top_states

top_states = get_top_states_by_rape(df_state_UT)

#  plot top 7 states by rape cases
def plot_top_states_by_rape(top_states):
    fig = px.bar(
        top_states,
        x='STATE/UT',
        y='Rape',
        title='Top 7 States by Total Rape Cases (2001 - 2014)',
        labels={'STATE/UT': 'State Names', 'Rape': 'Total Rape Cases'},
        color='Rape',
        color_continuous_scale=px.colors.sequential.Viridis
    )
    fig.update_layout(
        title_font=dict(size=20, color='navy', family='Arial'),
        xaxis_title_font_size=15,
        yaxis_title_font_size=15,
        xaxis_tickangle=-45,
        xaxis_tickfont=dict(size=9, family='bold'),
        yaxis_tickfont=dict(size=9, family='bold'),
        showlegend=False,
        font_color='white'
    )
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    return fig

st.plotly_chart(plot_top_states_by_rape(top_states))

#States Having the Maximum Dowry Deaths
dowry_grouped=df_state_UT.groupby('STATE/UT')['Dowry Deaths'].sum().reset_index()
Dowry_states = dowry_grouped.sort_values(by='Dowry Deaths',ascending=False)

### pie plot 
def plot_dowry_deaths_pie(Dowry_states):
    fig = px.pie(
        Dowry_states,
        names='STATE/UT',
        values='Dowry Deaths',       
        title='States with their Dowry Deaths',
        color='Dowry Deaths',
        color_discrete_sequence=px.colors.qualitative.Set1
    )

    fig.update_layout(
        title_font=dict(size=20, color='navy', family='Arial'),
        showlegend=True
    )
    return fig

st.plotly_chart(plot_dowry_deaths_pie(Dowry_states))

#### # Top 10 States Having Importation of Girls
girl_import = df_state_UT.groupby('STATE/UT')['Importation of Girls'].sum().reset_index()
GI_states = girl_import.sort_values(by='Importation of Girls',ascending=False).head(20)

#plot

def plot_importation_of_girls_bar(GI_states):
 
    fig = px.bar(
        GI_states,
        x='STATE/UT',
        y='Importation of Girls',
        title='States by Importation of Girls',
        labels={'STATE/UT': 'State/UT', 'Importation of Girls': 'Number of Girls Imported'},
        color='Importation of Girls', 
        color_continuous_scale=px.colors.qualitative.Bold
    )

    fig.update_layout(
        title_font=dict(size=20, color='navy', family='Arial'),
        xaxis_title_font_size=15,
        yaxis_title_font_size=15,
        xaxis_tickangle=-45,
        xaxis_tickfont=dict(size=10, family='bold'),
        yaxis_tickfont=dict(size=10, family='bold'),
    )

    return fig

st.plotly_chart(plot_importation_of_girls_bar(GI_states))

df = pd.read_csv('State wise Sexual Assault (Detailed) 1999 - 2013.csv')