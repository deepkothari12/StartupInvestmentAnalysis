import  streamlit as st
import pandas as pd 
import matplotlib.pyplot as plt

st.set_page_config(layout='wide' , page_title='StartupAnalysis')

df = pd.read_csv('clean_startup.csv')

st.sidebar.title("Startup Funding")
# st.sidebar.subheader("logX")
option = st.sidebar.selectbox("Select One" , ['OverAll' , "Startupss" , "Invester"])


def load_investor(investor):
    st.title(investor)
    #Personal Investment
    st.subheader("Personal Investment")
    st.dataframe(df[df['Investors Name'] == investor][['Date' ,'Startup','Industry Vertical', 'City','InvestmentnType','CR']])

    col0 , col00 = st.columns(2)
    with col0 :
        #group Investment
        st.subheader("Group Investment")
        st.dataframe(df[df['Investors Name'].str.contains(investor)][['Date' ,'Startup','Industry Vertical', 'City','InvestmentnType','CR']])
  
    with col00:
        st.subheader("Investment Type")
        stages = df[df['Investors Name'].str.contains(investor)].groupby(df['InvestmentnType'])['CR'].sum().sort_values(ascending=False)
        fig , ax = plt.subplots()
        ax.pie(stages, autopct='%1.2f%%' , labels=stages.index)
        st.pyplot(fig)

    col1 , col2 = st.columns(2)
    with col1:
        #Big Investment graph
        st.subheader("Big Investment")
        big_series = df[df['Investors Name'].str.contains(investor)].groupby(['Startup'])['CR'].max().sort_values(ascending=False).head(5)
        
        fig , ax = plt.subplots()
        ax.bar(big_series.index , big_series.values )

        st.pyplot(fig)

    with col2:
        #different secotr incestment 
        st.subheader("Top 5 Sectorss of Investment")
        sector = df[df['Investors Name'].str.contains(investor)].groupby(df['Industry Vertical'])['CR'].sum().sort_values(ascending=False).head(5)

        fig , ax = plt.subplots()
        ax.pie(sector, autopct='%1.2f%%' , labels=sector.index)

        st.pyplot(fig)
    col3 , col4 = st.columns(2)
    with col3:
        st.subheader("Year By Year Investment")
        yey = df[df['Investors Name'].str.contains(investor)].groupby(['Year'])['CR'].sum()

        fig , ax = plt.subplots()
        ax.plot(yey , marker = "*")
        st.pyplot(fig)

def overallAna():
    st.title("OverAll Analysis")
    tottal = round(df['CR'].sum())
    col1 , col2, col3 , col4 = st.columns(4)
    with col1:
        st.metric("Total Investment In Indian Startup" , str(tottal) + " CR")
    with col2:
        max_ = df.groupby(['Startup'])['CR'].max().sort_values(ascending=False).values[0]
        st.metric("Max amount In Indian Starup is" , max_)
    with col3:
        st.metric("Higest Funded Comapy is" , str(df.groupby(['Startup'])['CR'].max().sort_values(ascending=False).index[0]))
    with col4:
        st.metric("Avg Funcding In Indian Startup" , str(round(df.groupby(['Startup'])['CR'].sum().mean())) + "CR")

    col5 , col6 = st.columns(2)
    with col5:
        st.subheader("Month By Month Startup")
        select_type = st.selectbox("select type" , ['Total' , 'Count'])
        #clik = st.button("clik")
        if select_type == "Total":
            temp_df = df.groupby(['Year' , 'Month'])['CR'].sum().reset_index()
            temp_df['x-axis'] = temp_df['Month'].astype('str') + '-' + temp_df['Year'].astype('str')

            fig , ax = plt.subplots()
            ax.plot(temp_df['x-axis'] , temp_df['CR'])
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)
        else:
            temp_df = df.groupby(['Year' , 'Month'])['CR'].count().reset_index()
            temp_df['x-axis'] = temp_df['Month'].astype('str') + '-' + temp_df['Year'].astype('str')

            fig , ax = plt.subplots()
            ax.plot(temp_df['x-axis'] , temp_df['CR'])
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)

    with col6:
        st.subheader("Top Sectors")
        select_type_pie = st.selectbox("select type" , ['Top-5' , 'Top-8' , "Top-10"])
        if select_type_pie == "Top-5":
            top_5 = round(df.groupby(df['Industry Vertical'])['CR'].sum().sort_values(ascending=False).head(5))
            fig , ax = plt.subplots()
            ax.pie(top_5 , labels = top_5.index , autopct='%1.2f%%')
            st.pyplot(fig)
        elif select_type_pie == "Top-8":
            top_8 = round(df.groupby(df['Industry Vertical'])['CR'].sum().sort_values(ascending=False).head(8))
            fig , ax = plt.subplots()
            ax.pie(top_8 , labels = top_8.index , autopct='%1.2f%%')
            st.pyplot(fig)
        else :
            top_10 = round(df.groupby(df['Industry Vertical'])['CR'].sum().sort_values(ascending=False).head(10))
            fig , ax = plt.subplots()
            ax.pie(top_10 , labels = top_10.index , autopct='%1.2f%%')
            st.pyplot(fig)
    col7 , col8 = st.columns(2)
    with col7:
        st.subheader("Top Investor")
        top_investor = df.groupby(df['Investors Name'])['CR'].sum().sort_values(ascending=False).head(5)
        fig , ax = plt.subplots()
        ax.bar(top_investor.index , top_investor.values)
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)
    with col8:
        st.subheader("top 5 City With Big Investment")
        h = round(df.groupby(df['City'])['CR'].sum().sort_values(ascending=False).head(5))
        fig , ax = plt.subplots()
        ax.bar(h.index , h.values)
        st.pyplot(fig)


def startup(s_name):
    st.title("Startupss Analysis")
    st.subheader(s_name)
    col1 , col2 , col3 , col4= st.columns(4)
    with col1:
        s_city = str(df[df['Startup'] == s_name]["City"].values[0])
        st.metric('City' , s_city)
    with col2:
        s_year = str(df[df['Startup'] == s_name]["Year"].values[0])
        st.metric("Year" , s_year)
    with col3:
        s_month = str(df[df['Startup'] == s_name]["Month"].values[0])
        st.metric("Month" , s_month)
    with col4:
        s_verti = str(df[df['Startup'] == s_name]["SubVertical"].values[0])
        st.metric("Vertical" , s_verti)

    col5 , col6 = st.columns(2)
    with col5:
        s_investor = str(df[df['Startup'] == s_name]["InvestmentnType"].values[0])
        st.metric("InvestmentnType" , s_investor)
    with col6:
        ver = str(df[df['Startup'] == s_name]['SubVertical'].values[0])
        si_name1 = str(df[df['SubVertical'].isin([ver])]['Startup'].values[0])
        si_name2 = str(df[df['SubVertical'].isin([ver])]['Startup'].values[1])
        si_name3 = str(df[df['SubVertical'].isin([ver])]['Startup'].values[2])
        st.metric("Similar Comapny" , si_name1 + ","+ " "+ si_name2 +","+ " " + si_name3 )
    
        

if option == 'OverAll':
        overallAna()
    
elif option == "Startupss":
    
    s_name = st.sidebar.selectbox("Select One", sorted(df['Startup'].unique().tolist()))
    btn1 = st.sidebar.button("Find Startup details")
    if btn1:
        startup(s_name)

else:
    #st.title("Invester Analysis")
    selectd_ivestor =  st.sidebar.selectbox("Select One ", sorted(set(df['Investors Name'].str.split(",").sum())))
    btn2 = st.sidebar.button("Invester details")
    if btn2:
        load_investor(selectd_ivestor)
    

