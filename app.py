import streamlit as st
import preprocesser,helper
import matplotlib.pyplot as plt

st.sidebar.title("Choose a .txt file")
uploaded_file = st.sidebar.file_uploader("Select a whatsapp chat and click on export, then upload it here.")

if uploaded_file is None:
    st.markdown('<h1 style="color: #128C7E;">{}</h1>'.format("Whatsapp Chat Analyzer"), unsafe_allow_html=True)
    st.markdown('<h3 style="color: #DCF8C6;">{}</h2>'.format("Upload your whatsapp chat to see analysis on it."), unsafe_allow_html=True)


if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    try:
        df = preprocesser.preprocess(data)
    
        # fetch unique users
        user_list = df['user'].unique().tolist()
        if "group_notification" in user_list:
            user_list.remove('group_notification')
        user_list.sort()
        user_list.insert(0,"Overall")
    
        selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)
    
        if st.sidebar.button("Show Analysis"):
            
            plt.style.use('dark_background')
            # Stats Area
            num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user,df)
            st.markdown('<h1 style="color: #128C7E;">{}</h1>'.format("Top Statistics"), unsafe_allow_html=True)
            col1, col2, col3, col4 = st.columns(4)
    
            with col1:
                st.markdown('<h2 style="color: #DCF8C6;">{}</h2>'.format("Total Messages"), unsafe_allow_html=True)
                st.markdown('<h3 style="color: #25D366;">{}</h3>'.format(num_messages), unsafe_allow_html=True)
    
            with col2:
                st.markdown('<h2 style="color: #DCF8C6;">{}</h2>'.format("No. of words"), unsafe_allow_html=True)
                st.markdown('<h3 style="color: #25D366;">{}</h3>'.format(words), unsafe_allow_html=True)
            with col3:
                st.markdown('<h2 style="color: #DCF8C6;">{}</h2>'.format("Media shared"), unsafe_allow_html=True)
                st.markdown('<h3 style="color: #25D366;">{}</h3>'.format(num_media_messages), unsafe_allow_html=True)
            with col4:
                st.markdown('<h2 style="color: #DCF8C6;">{}</h2>'.format("Links shared"), unsafe_allow_html=True)
                st.markdown('<h3 style="color: #25D366;">{}</h3>'.format(num_links), unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
    
            with col1:
    
                emoji_df,emoji_count= helper.emoji_counter(selected_user,df)
    
                st.markdown('<h2 style="color: #DCF8C6;">{}</h2>'.format("Total Emojis used"), unsafe_allow_html=True)
                st.markdown('<h3 style="color: #25D366;">{}</h3>'.format(emoji_count), unsafe_allow_html=True)
            
            with col2:
    
                st.markdown('<h2 style="color: #DCF8C6;">{}</h2>'.format("Average number of words per message"), unsafe_allow_html=True)
                st.markdown('<h3 style="color: #25D366;">{}</h3>'.format(round(words/num_messages,1)), unsafe_allow_html=True)
    
            st.markdown("<hr>", unsafe_allow_html=True)
    
            #Monthly timeline
            st.markdown('<h1 style="color: #128C7E;">{}</h1>'.format("Timeline"), unsafe_allow_html=True)
            col1,col2=st.columns(2)
            with col1:         
                st.markdown('<h2 style="color: #DCF8C6;">{}</h2>'.format("Monthly"), unsafe_allow_html=True)  
                timeline=helper.monthly_timeline(selected_user,df)
                fig,ax=plt.subplots()
                ax.plot(timeline['time'],timeline['message'],color='#25D366')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
    
            #Daily timeline
            with col2:
                st.markdown('<h2 style="color: #DCF8C6;">{}</h2>'.format("Daily"), unsafe_allow_html=True)
                daily_timeline=helper.daily_timeline(selected_user,df)
                fig,ax=plt.subplots()
                ax.plot(daily_timeline['only_date'],daily_timeline['message'],color='#25D366')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
    
            st.markdown("<hr>", unsafe_allow_html=True)
    
            # activity map
            st.markdown('<h1 style="color: #128C7E;">{}</h1>'.format("Activity Map"), unsafe_allow_html=True)
            col1,col2 = st.columns(2)
    
            with col1:
                st.markdown('<h2 style="color: #DCF8C6;">{}</h2>'.format("Busiest day"), unsafe_allow_html=True)
                busy_day = helper.week_activity_map(selected_user,df)
                fig,ax = plt.subplots()
                ax.bar(busy_day.index,busy_day.values,color='#25D366')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
    
            with col2:
                st.markdown('<h2 style="color: #DCF8C6;">{}</h2>'.format("Busiest Month"), unsafe_allow_html=True)
                busy_month = helper.month_activity_map(selected_user, df)
                fig, ax = plt.subplots()
                ax.bar(busy_month.index, busy_month.values,color='#25D366')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            st.markdown("<hr>", unsafe_allow_html=True)
    
            #Busiest users
            if selected_user=="Overall":
                st.markdown('<h1 style="color: #128C7E;">{}</h1>'.format("Most Active Users"), unsafe_allow_html=True)
                x,new_df=helper.most_active_users(df)
                fig, ax=plt.subplots()
    
                col1, col2 = st.columns(2)
    
                with col1:
                    ax.bar(x.index,x.values,color='#25D366')
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)
                with col2:
                    st.dataframe(new_df)
                st.markdown("<hr>", unsafe_allow_html=True)
    
            #Word cloud
            st.markdown('<h1 style="color: #128C7E;">{}</h1>'.format("Text Analysis"), unsafe_allow_html=True)
            col1,col2=st.columns(2)
            most_used_words_df,wc=helper.most_used_words(selected_user,df)
            with col1:
                st.markdown('<h2 style="color: #DCF8C6;">{}</h2>'.format("Word Cloud"), unsafe_allow_html=True)
                fig, ax = plt.subplots()
                ax.imshow(wc)
                st.pyplot(fig)
    
            # Most common words
            with col2:
                st.markdown('<h2 style="color: #DCF8C6;">{}</h2>'.format("Most Used Words"), unsafe_allow_html=True)
        
                fig, ax = plt.subplots()
    
                ax.barh(most_used_words_df[0],most_used_words_df[1],color='#25D366')
                st.pyplot(fig)
            st.markdown("<hr>", unsafe_allow_html=True)
    
            # Emoji analysis
            st.markdown('<h1 style="color:#128C7E;">{}</h1>'.format("Emoji Analysis"), unsafe_allow_html=True)
                
            col1,col2 = st.columns(2)
    
            with col1:
                st.markdown('<h2 style="color: #DCF8C6;">{}</h2>'.format("Emoji count"), unsafe_allow_html=True)
                st.dataframe(emoji_df)
            with col2:
            # Users that use the most emojis
                if selected_user=="Overall":
                    st.markdown('<h2 style="color:#DCF8C6;">{}</h2>'.format("Users that use the emojis most"), unsafe_allow_html=True)
                    df['emoji_count']=df['message'].apply(helper.most_emoji_user)
                    user_emoji_count = df.groupby('user')['emoji_count'].sum().reset_index()
                    st.dataframe(user_emoji_count[user_emoji_count['emoji_count']>0].sort_values("emoji_count",ascending=False)) 
    except:
        st.markdown('<h1 style="color: #128C7E;">{}</h1>'.format("Whatsapp Chat Analyzer"), unsafe_allow_html=True)
        st.markdown('<h3 style="color: red">{}</h2>'.format("There seems to be an error, Try uploading the file with correct format."), unsafe_allow_html=True)
