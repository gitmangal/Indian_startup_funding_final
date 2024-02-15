import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title='StartUp Analysis')

df = pd.read_csv('startup_cleaned.csv')
df['date'] = pd.to_datetime(df['date'],errors='coerce')
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

def load_overall_analysis():
    st.title('Overall Analysis')

    # total invested amount
    total = round(df['amount'].sum())
    # max amount infused in a startup
    max_funding = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
    # avg ticket size
    avg_funding = df.groupby('startup')['amount'].sum().mean()
    # total funded startups
    num_startups = df['startup'].nunique()

    col1,col2,col3,col4 = st.columns(4)

    with col1:
        st.metric('Total',str(total) + ' Cr')
    with col2:
        st.metric('Max', str(max_funding) + ' Cr')

    with col3:
        st.metric('Avg',str(round(avg_funding)) + ' Cr')

    with col4:
        st.metric('Funded Startups',num_startups)

    st.header('Month by month graph')
    selected_option = st.selectbox('Select Type',['Total investment in every months','Count of investment in every months'])
    if selected_option == 'Total investment in every months':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()
        
    temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')
    fig3, ax3 = plt.subplots()
    ax3.plot(temp_df['x_axis'], temp_df['amount'])
    
    # Specify the nth value you want to show
    nth_value = 5
    
    # Set tick positions and labels
    x_values = temp_df['x_axis'][::nth_value]
    x_labels = temp_df['x_axis'].iloc[::nth_value]
    ax3.set_xticks(x_values)
    ax3.set_xticklabels(x_labels, rotation=45)  # Rotate x-axis labels for better readability
    # Show plot inStreamlit
    st.pyplot(fig3)

    col5,col6 = st.columns(2)
    with col5:
        st.header('Top 10 Sectors')
        df['vertical']=df['vertical'].str.replace('eCommerce','E-commerce')
        df['vertical']=df['vertical'].str.replace('ECommerce','E-commerce')
        df['vertical']=df['vertical'].str.replace('E-Commerce & M-Commerce platform','E-commerce')
        df['vertical']=df['vertical'].str.replace('E-Commerce','E-commerce')
        sanalysis = df.groupby('vertical')['amount'].sum().sort_values(ascending=False).head(10)
        # Create column chart
        fig4, ax4 = plt.subplots()
        ax4.bar(sanalysis.index, sanalysis.values)
        
        # Customize plot
        plt.xticks(rotation=45, ha='right')
        plt.xlabel('Sectors')
        plt.ylabel('Values (in millions)')
        
        # Display chart in Streamlit
        st.pyplot(fig4)
        
    with col6:
       newdic = {}
       for i, row in df.iterrows():
            investors = row['investors'].split(',')
            amount = row['amount']
            for investor in investors:
                investor = investor.strip()
                if investor in newdic:
                    newdic[investor] += amount / len(investors)
                else:
                    newdic[investor] = amount / len(investors)
        #created a new dataframe for investers            
        tempdf = pd.DataFrame(list(newdic.values()),index=list(newdic.keys()))
        fig5, ax5 = plt.subplots()
        ax5.bar(tempdf.index, tempdf.values)
        plt.xticks(rotation=45, ha='right')
        plt.xlabel('Investors')
        plt.ylabel('Values (in millions)')
        
        # Display chart in Streamlit
        st.pyplot(fig5)

df3 = pd.DataFrame(list(newdic.values()),index=list(newdic.keys()))
print(df3)
print(df2)
def load_investor_details(investor):
    st.title(investor)
    # load the recent 5 investments of the investor
    last5_df = df[df['investors'].str.contains(investor)].head()[['date', 'startup', 'vertical', 'city', 'round', 'amount']]
    st.subheader('Most Recent Investments')
    st.dataframe(last5_df)

    col1, col2 = st.columns(2)
    with col1:
        # biggest investments
        big_series = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        st.subheader('Biggest Investments')
        fig, ax = plt.subplots()
        ax.bar(big_series.index,big_series.values)

        st.pyplot(fig)

    with col2:
        verical_series = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()

        st.subheader('Sectors invested in')
        fig1, ax1 = plt.subplots()
        ax1.pie(verical_series,labels=verical_series.index,autopct="%0.01f%%")

        st.pyplot(fig1)
        
    df['year'] = df['date'].dt.year
    year_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()

    st.subheader('YoY Investment')
    fig2, ax2 = plt.subplots()
    ax2.plot(year_series.index,year_series.values)

    st.pyplot(fig2)

st.sidebar.title('Startup Funding Analysis')

option = st.sidebar.selectbox('Select One',['Overall Analysis','StartUp','Investor'])

if option == 'Overall Analysis':
    load_overall_analysis()

elif option == 'StartUp':
    st.sidebar.selectbox('Select StartUp',sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find StartUp Details')
    st.title('StartUp Analysis')
else:
    selected_investor = st.sidebar.selectbox('Select StartUp',sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2:
        load_investor_details(selected_investor)
