import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
import os

cwd = os.getcwd()

sns.set(style='dark')

def RentTrend_2011_df(df):
    pivot_RentperMonth_2011 = df[df['year']==2011].groupby(by=['year', 'month']).agg(
        {
            'rented': 'mean',
            
        }
    ).reset_index()
    #print(pivot_RentperMonth_2011)
    return pivot_RentperMonth_2011

def RentTrend_2012_df(df):
    pivot_RentperMonth_2012 = df[df['year']==2012].groupby(by=['year', 'month']).agg(
        {
            'rented': 'mean'
            
        }
    ).reset_index()
    #print(pivot_RentperMonth_2012)
    return pivot_RentperMonth_2012

def PivotCasualRegistered(df):
    pivot_CasualRegistered = df.groupby(by=['year','month']).agg(
        {
            'casual' : 'sum',
            'registered': 'sum',
            'rented': 'sum'
        }
    ).reset_index()
    pivot_CasualRegistered['amount registered'] = pivot_CasualRegistered['registered']*100/pivot_CasualRegistered['rented']
    #print(pivot_CasualRegistered)
    return pivot_CasualRegistered

def PivotRent_perHour(df):
    pivot_RentperHour = df.groupby(by='hour').agg(
        {
            'rented': 'mean'
        }
    ).reset_index()
    pivot_RentperHour['percentage'] = pivot_RentperHour['rented']*100/pivot_RentperHour['rented'].sum()
    #print(pivot_RentperHour)
    return pivot_RentperHour

rev_day_dir = os.path.join(os.getcwd(), 'dashboard/rev_day.csv')
rev_hour_dir = os.path.join(os.getcwd(), 'dashboard/rev_hour.csv')

day_df = pd.read_csv(rev_day_dir)
hour_df = pd.read_csv(rev_hour_dir)

day_df.sort_values(by="date", inplace=True)
day_df.reset_index(inplace=True)
day_df['date'] = pd.to_datetime(day_df['date'])


RentTrend_2011 = RentTrend_2011_df(day_df)
RentTrend_2012 = RentTrend_2012_df(day_df)
Customers_type = PivotCasualRegistered(day_df)
RentTrend_perHour = PivotRent_perHour(hour_df)

def mainView(previewMode):

    ############################
    #THIS PART FOR 1st Question#
    ############################

    st.subheader('Rent per month trends')
    col1, col2, col3 = st.columns(3)

    with col1:
        total_rent_2011 = day_df[day_df['year']==2011].rented.sum()
        st.metric("Total Rent 2011", value=total_rent_2011)

    with col2:
        total_rent_2012 =  day_df[day_df['year']==2012].rented.sum()
        st.metric("Total Rent 2012", value=total_rent_2012)

    with col3:
        total_rent = total_rent_2011 + total_rent_2012
        st.metric("Total Rent ", value=total_rent)

    fig, ax = plt.subplots(figsize = (16,8))
    ax.plot(
        RentTrend_2011['month'],
        RentTrend_2011['rented'],
        marker='o',
        linewidth=2,
        color="#90CAF9",
        label = "Rent Trend in 2011"
    )
    ax.plot(
        RentTrend_2011['month'],
        RentTrend_2012['rented'],
        marker= 'o',
        linewidth=2,
        color="orange",
        label = "Rent Trend in 2012"
    )

    ax.set_title('Average Monthly Rent in 2011 and 2012', fontsize=28, fontweight='bold')
    
    ax.set_xlabel('Month',fontsize=16)
    ax.set_ylabel('Rented',fontsize=16)
   
    month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    ax.set_xticks(RentTrend_2011['month'])
    ax.set_xticklabels(month_names, rotation=45)  # Rotate labels by 45 degrees

    ax.legend()
    ax.grid()

    ax.set_facecolor('lightgray')
    
    st.pyplot(fig)

    if previewMode == 'See Insight':
        with st.expander("More Explanation"):
            st.write(
                """Insight:
                \n- Tren penyewaan sepeda meningkat dari tahun 2011 ke 2012 pada setiap bulannya. 
                \n- Range dari bulan 6 sampai bulan 10 merupakan puncak tertinggi dalam setahun dengan lonjakan terbesar terjadi pada bulan september 2012 dibanding september 2011. 
                \n- Kenaikan paling drastis terjadi antara bulan 3 sampai bulan 5.
                \n- Puncak rental adalah pada September 2012
                """
            )

    ############################
    #THIS PART FOR 2nd Question#
    ############################

    st.subheader('Rent per month trends')
    with st.container():
        col1, col2,  = st.columns(2)
        with col1:
            total_RentCasual_2011 = day_df[day_df['year']==2011].casual.sum()
            st.metric("Total Rental Casual 2011: ", total_RentCasual_2011)
        
        with col2:
            total_RentCasual_2012 = day_df[day_df['year']==2012].casual.sum()
            st.metric("Total Rental Casual 2012: ", total_RentCasual_2012)
        
        col3, col4,  = st.columns(2)
        with col1:
            total_RentRegistered_2011 = day_df[day_df['year']==2011].registered.sum()
            st.metric("Total Rental Registered 2011", total_RentRegistered_2011)
           
        with col2:
            total_RentRegistered_2012 = day_df[day_df['year']==2012].registered.sum()
            st.metric("Total Rental Registered 2012: ", total_RentRegistered_2012)
    CasualRegistered_melted = Customers_type.melt(id_vars='year', value_vars=['casual', 'registered'],
                    var_name='customers_type', value_name='Rented')
    #print(CasualRegistered_melted)
    CasualRegistered_melted=CasualRegistered_melted.groupby(by=['year','customers_type']).agg(
            {
            'Rented' : 'sum'
        }
    ).reset_index()
    
    #print(CasualRegistered_melted)
    
    fig, ax = plt.subplots(figsize=(16,8))
    sns.barplot(data=CasualRegistered_melted,x = 'year', y='Rented', hue='customers_type')
    ax.set_title("Grafic of Casual vs Rented Customers", fontsize=28, fontweight='bold')
    st.pyplot(fig)

    if previewMode == 'See Insight':
        with st.expander("More Explanation"):
            st.write(
                """Insight:
                \n- Orang dengan status registered lebih cenderung untuk menyewa sepeda dibandingkan 'casual' renters.
                \n- Dengan range 77 sampai 91 persen dari rata-rata pengguna yang menyewa adalah registered
                \n- Registered memiliki pengaruh cukup besar terhadap kemungkinan orang untuk menyewa
                """
            )


    ############################
    #THIS PART FOR 3rd Question#
    ############################ 

    #print(RentTrend_perHour)


    st.subheader('Average Hourly Rent trends')
    
    fig, ax = plt.subplots(figsize=(16,8))
    colors = ['#D3D3D3' if value != RentTrend_perHour['rented'].max() else '#72BCD4' for value in RentTrend_perHour['rented']]
    sns.barplot(data=RentTrend_perHour, x='hour', hue = 'hour', y='rented', palette=colors, legend=False)
    
    ax.set_title("Bike Rent per Hour", fontsize=28, fontweight='bold')

    #ax.set_xticks(RentTrend_perHour['hour'])

    st.pyplot(fig)

    if previewMode == 'See Insight':
        with st.expander("See Explanation"):
            st.write(
                """Insight:
                \n- Penyewaan sepeda paling banyak terjadi pada jam 17 dan hampir stabil pada jam 18
                \n- Pada jam ini perlu diperhatikan ketersedian sepeda dan pelayanan mengingat ini merupakan jam krusial
                """
            )

    ############################
    #THIS PART FOR 4th Question#
    ############################    

    st.subheader('Average Rent per Hour Trends')

    fig, ax = plt.subplots(figsize=(16,8))
    ax.plot(
        RentTrend_perHour['hour'],
        RentTrend_perHour['rented'],
        marker = 'o',
        color="blue",

    )

    ax.set_xlabel('hour',fontsize=16)
    ax.set_ylabel('rented',fontsize=16)
    
    ax.set_title("Average Rent per Hour", fontsize=28, fontweight='bold')
    
    ax.set_xticks(RentTrend_perHour['hour'])
    ax.set_yticks([x for x in range(0,500,20)])

    ax.grid()

    st.pyplot(fig)

    if previewMode == 'See Insight':
        with st.expander("See Explanation"):
            st.write(
                """Insight:
                \n- Penyewaan sepeda paling banyak terjadi pada jam 17 dan hampir stabil pada jam 18
                \n- Pada jam ini perlu diperhatikan ketersedian sepeda dan pelayanan mengingat ini merupakan jam krusial
                \n- Dengan memperhatikan tren, maka jam 4-5 merupakan waktu yang baik untuk maintenance karena demand paling rendah dan akan terjadi lonjakan sewa pada jam 5. Jika terjadi kerusakan yang urgent setelah puncak sewa jam 5-8, dapat dilakukan perbaikan pada jam 10 karena akan segera terjadi kenaikan rate sewa pada jam sebelumnya dan jam 10 rate sewa menurun dibanding sebelumnya.
                """
            )

def main_view_CustomDate():
    
    
    main_df = day_df[(day_df["date"] >= str(start_date)) & 
        (day_df["date"] <= str(end_date))]

    main_hour_notGrouped_df = hour_df[(hour_df["date"] >= str(start_date)) & 
        (hour_df["date"] <= str(end_date))]

    main_hour_rented_sum_df = main_hour_notGrouped_df.groupby(by='hour').agg({'rented': 'sum'}).reset_index()
        
    main_hour_df = main_hour_notGrouped_df.groupby(by='hour').agg({'rented' : 'mean'}).reset_index()
    
    ###############
    # FIRST GRAPH #
    ###############

    st.subheader('Rent per month trends')
    col1, col2, col3 = st.columns(3)

    with col1:
        total_rent = main_df.rented.sum()
        st.metric("Total Rented", value=total_rent)

    with col2:
        average_rent =  main_df.rented.mean()
        average_rent = f"{average_rent:.2f}"
        st.metric("Average Daily Rented", value=average_rent)

    with col3:
        highest_rent = main_df.rented.max()
        st.metric("Highest Daily Rented", value=highest_rent)

    fig, ax = plt.subplots(figsize = (16,8))
    ax.plot(
        main_df['date'],
        main_df['rented'],
        marker='o',
        linewidth=2,
        color="#90CAF9",
    )

    ax.set_xlabel('Date',fontsize=16)
    ax.set_ylabel('Rented',fontsize=16)
    
    ax.set_title("Rent Overview", fontsize=28, fontweight='bold')
    
    #ax.set_xticks(RentTrend_perHour['hour'])
    #ax.set_yticks([x for x in range(0,500,20)])

    ax.grid()

    st.pyplot(fig)

    ###########
    #2nd Graph#
    ###########

    st.subheader('Rent per month trends')
    with st.container():

        col1, col2,  = st.columns(2)
        with col1:
            total_RentCasual= main_df.casual.sum()
            st.metric("Total Rental Casual: ", total_RentCasual)
            
        with col2:
            total_RentRegistered= main_df.registered.sum()
            st.metric("Total Rental Registered: ", total_RentRegistered)
            
        col3, col4,  = st.columns(2)
        with col3:
            percent_RentCasual= main_df.casual.sum()*100/main_df.rented.sum()
            percent_RentCasual = f"{percent_RentCasual:.2f}%"
            st.metric("Rented Casual: ", percent_RentCasual)
            
        with col4:
            percent_RentRegistered= main_df.registered.sum()*100/main_df.rented.sum()
            percent_RentRegistered = f"{percent_RentRegistered:.2f}%"
            st.metric("Rented Registered: ", percent_RentRegistered)

    main_df_melted = main_df.melt(id_vars='date', value_vars=['casual', 'registered'],
                    var_name='customers_type', value_name='Bike Rented')
    
    #print(main_df_melted)

    fig, ax = plt.subplots(figsize=(16,8))
    sns.barplot(data=main_df_melted, x = 'date', y='Bike Rented', hue='customers_type')
    ax.set_title("Grafic of Casual vs Rented Customers", fontsize=28, fontweight='bold')

    plt.xticks(rotation=45, ha='right')
    
    st.pyplot(fig)

    ############
    # 3rd Graph#
    ############

    #print(RentTrend_perHour)


    st.subheader('Average Hourly Rent trends')

    col1, col2, col3 = st.columns(3)

    with col1:
        max_avg_hour_rent = main_hour_rented_sum_df.rented.max()
        st.metric("Max Bike Rented per Hour: ", value=max_avg_hour_rent)

    with col2:
        max_average_hourly_rent =  main_hour_df.rented.max()
        max_average_hourly_rent = f"{max_average_hourly_rent:.2f}"
        st.metric("Max Average Bike Rented per Hour", value=max_average_hourly_rent)

    with col3:
        max_average_hourly_rent =  main_hour_df.rented.mean()
        max_average_hourly_rent = f"{max_average_hourly_rent:.2f}"
        st.metric("Average Bike Rented per Hour", value=max_average_hourly_rent)

    colors_2 = ['#D3D3D3' if value != main_hour_df['rented'].max() else '#72BCD4' for value in main_hour_df['rented']]

    fig, ax = plt.subplots(figsize=(16,8))
    sns.barplot(data=main_hour_df, x='hour', hue = 'hour', y='rented', palette=colors_2, legend=False)
    
    ax.set_title("Average Bike Rented per Hour", fontsize=28, fontweight='bold')

    #ax.set_xticks(RentTrend_perHour['hour'])

    st.pyplot(fig)

    ###########
    #4th Graph#
    ########### 

    #print(main_hour_df)

    st.subheader('Average Rent per Hour Trends')

    fig, ax = plt.subplots(figsize=(16,8))
    ax.plot(
        main_hour_df['hour'],
        main_hour_df['rented'],
        marker = 'o',
        color="blue",

    )

    ax.set_xlabel('hour',fontsize=16)
    ax.set_ylabel('bike rented',fontsize=16)
    
    ax.set_title("Average Rent per Hour", fontsize=28, fontweight='bold')
    ax.set_xticks(main_hour_df['hour'])
    #ax.set_yticks([x for x in range(0,500,20)])

    ax.grid()

    st.pyplot(fig)



st.header("Feb's Bike Rentals")

min_date = day_df["date"].min()
max_date = day_df["date"].max()

#print(RentTrend_2012)
#print(type(RentTrend_2011))
#print(RentTrend_2011['rented'])

with st.sidebar:
    st.image("https://cdn2.vectorstock.com/i/1000x1000/21/31/logo-for-bicycle-rental-vector-25512131.jpg")

    preview = st.selectbox(
        label = "View Mode",
        options = ('Custom Date', 'See 2011-2012 overview with Insight', 'See 2011-2012 overview (Graph)')
    )

if preview == 'See 2011-2012 overview with Insight' or preview == 'Graph Only':
    mainView(preview)

else:

    min_date = day_df["date"].min()
    max_date = day_df["date"].max()

    with st.sidebar:
        start_date, end_date = st.date_input(
        label='Date Range',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
        )
        st.text('Warning!\nRange tanggal yang terlalu jauh \ndapat mengakibatkan \ngrafik sulit dipahami.\n\nJika ingin melihat \nketerangan secara keseluruhan,\nubah \'view modde\'')       

    main_view_CustomDate()
    
