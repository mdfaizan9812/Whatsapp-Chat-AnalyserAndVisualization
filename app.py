import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')



html_temp="""
    <div style="background-color:springgreen;padding:15px;">
    <h1>WHATSAPP DATA VISUALIZATION AND ANALYSIS</h1>
    </div>
    """
html_temp1="""
    <div style="background-color:springgreen;padding:5px;">
    <h1>Choose->Analyse or Visualize</h1>
    </div>
    """

st.markdown(html_temp,unsafe_allow_html=True)
img=Image.open("images/whatsapp.jpg")
st.image(img,width=700)

st.sidebar.subheader("Files for chat are temporarily uploaded to app, and no data is stores, you data file remains private, and nothing is shared to server")


st.sidebar.markdown(html_temp1,unsafe_allow_html=True)
img2=Image.open("images/whats2.jpg")
st.sidebar.image(img2,width=305)

def process_data(data):
    filename=data
    df=pd.read_csv(filename,header=None,error_bad_lines=False,encoding='utf-8')
    df=df.drop(0)
    df.columns=['Date','Chat']
    messages=df["Chat"].str.split("-",n=1,expand=True)
    df['Time']=messages[0]
    df['Text']=messages[1]
    messages1=df['Text'].str.split(":",n=1,expand=True)
    df['Name']=messages1[0]
    df['Text']=messages1[1]
    df.drop(columns=['Chat'],inplace=True)
    df['Text']=df['Text'].str.lower()
    df['Text']=df['Text'].str.replace('<media omitted>','media shared')
    df['Text']=df['Text'].str.replace('this message was deleted','deletedmsg')
    null_name=df[df['Name'].isnull()]
    df.drop(null_name.index,inplace=True)
    df.dropna(inplace=True)
    df['Date']=pd.to_datetime(df['Date'])
    df['day_of_the_week']=df['Date'].dt.day_name()
    return df

def char_counter(msg):
    if msg==' media shared':
        return 0
    return len(msg)

def word_counter(msg):
    if msg==" media shared":
        return 0
    else:
        words=len(msg.split())
    return words 
def steps():
    st.info("STEPS TO USE")
    
    st.subheader("1-> Open the WhatsApp conversation you would like to have visualized and tap on the group subject or contact name in the navigation bar")
    st.subheader("2-> Scroll to the bottom and tap on 'Export chat' ")
    st.subheader("3-> Select without media")
    st.subheader("4-> Select 'Mail'")
    st.subheader("5-> Enter ur email into the 'To' field , Tap on Send")
    st.subheader("6-> Download your chat from the mail and browse here from that location")
    st.subheader("7-> That's It, now ready to analyse and visualize your chat")

def main():
    activities=['Analysis and Statistics of Chat','Visualization of chat']
    choice=st.sidebar.selectbox("Select Activity",activities)
    if choice=='Analysis and Statistics of Chat':
        st.header("ANALYSIS OF CHAT")
        data=st.file_uploader("Upload a file",type=['txt','csv'])
        if data is None:
            steps()
        else:
            df=process_data(data)
            ##Show processed data
            if st.checkbox("Processed Data"):
                st.write(df)

            #media msg info
            if st.checkbox("Media msgs info"):
                mediamsg=df[df['Text']==' media shared']
                if st.button('Show media messages info'):
                    st.write(mediamsg)

                no_mediamsg=mediamsg['Name'].value_counts()
                if st.button("Number of media msg by each user"):
                    st.write(no_mediamsg)
                if st.button("Number of media msg by each user in graph"):
                    st.bar_chart(no_mediamsg)

            ##word and letter count
            if st.checkbox("Words and Letters used by Each person"):
                df['Letter_Count']=df['Text'].apply(char_counter)
                df['Word_Count']=df['Text'].apply(word_counter)
                st.write(df[['Text','Letter_Count','Word_Count']])

            ##most active user
            if st.checkbox("most active user"):
                active_user=df['Name'].mode()
                st.info(active_user.iloc[0])

            #Number of messages send by each user
            if st.checkbox("Number of messages send by each user"):
                st.write(df[['Name','Text']].groupby('Name').count())

            #Words used by each person
            if st.checkbox("Words used by each person: "):
                name_value_count=df[['Name','Word_Count']].groupby('Name').sum()
                st.write(name_value_count)
            
            #Average msg in a day
            if st.checkbox("Average msg in a day"):
                dth=df[['Date','Text']].groupby('Date').count()
                st.write(dth['Text'].mean())
            if st.checkbox("Number of msg per day"):
                dth1=df[['Date','Text']].groupby('Date').count()
                st.write(dth1)
            
            
            df.set_index('Date',inplace=True) # set date as index 
            # Number of msg per week
            if st.checkbox("Number of msg per week"):
                dth2=df.Text.resample('W').count()
                st.write(dth2)

            # Number of msg per month
            if st.checkbox("Number of msg per month"):
                dth3=df.Text.resample('M').count()
                st.write(dth3)


    else:
        st.header("CHAT VISUALIZATION")
        data=st.file_uploader("Upload a file",type=['txt','csv'])
        if data is None:
            steps()
        else:
            df=process_data(data)
            df['Letter_Count']=df['Text'].apply(char_counter)
            df['Word_Count']=df['Text'].apply(word_counter)
            all_columns_name=df.columns.tolist()

            
            #pie chart for word and letter count
            if st.checkbox("Visualize word and letter count and media msg"):
                all_columns_name=df.columns.tolist()

                # word count
                if st.button("Generate pie plot for word count"):
                    st.write('0 mean media shared')
                    st.write('1 mean message has 1 word')
                    st.write('2 mean message has 2 word & so on')
                    words_count_count=df.iloc[0:40,-1].value_counts()
                    plt.pie(words_count_count,labels=words_count_count.index,autopct="%0.2f%%")
                    st.pyplot()

                # Letter count
                if st.button("Generate pie plot for letter count"):
                    st.write('0 mean media shared')
                    st.write('1 mean message has 1 letter')
                    st.write('2 mean message has 2 letter & so on')
                    letters_count_count=df.iloc[0:30,-2].value_counts()
                    plt.pie(letters_count_count,labels=letters_count_count.index,autopct="%0.2f%%")
                    st.pyplot()
            
            # Message shared by each user
            if st.checkbox("Message shared by each user"):
                msg_by_each_user=df.groupby("Name").count()
                graphm=st.selectbox("Select Graph",('','bar','pie','pie_bar'))
                if graphm == 'bar':
                    plt.title("Message shared by each user",fontsize=15)
                    plt.xlabel("User Name",fontsize=12)
                    plt.ylabel("Number of message",fontsize=12)
                    plt.bar(msg_by_each_user.index,msg_by_each_user['Text'])
                    st.pyplot()
                if graphm == 'pie':
                    plt.title("Message shared by each user",fontsize=15)
                    plt.pie(msg_by_each_user['Text'],labels=msg_by_each_user.index,autopct="%0.2f%%")
                    st.pyplot()

                if graphm == 'pie_bar':
                    plt.subplot(2,1,1)
                    plt.bar(msg_by_each_user.index,msg_by_each_user['Text'])
                    plt.title("Message shared by each user",fontsize=15)
                    plt.xlabel("User Name",fontsize=12)
                    plt.ylabel("Number of message",fontsize=12)
                    st.pyplot()
                    plt.subplot(2,1,2)
                    plt.pie(msg_by_each_user['Text'],labels=msg_by_each_user.index,autopct="%0.2f%%")
                    plt.title("Message shared by each user",fontsize=15)
                    st.pyplot()

            # Media Message shared by each user
            if st.checkbox("Media Message shared by each user"):
                media_msg_by_each_user=df[df["Text"]==" media shared"].groupby("Name").count()
                graphm=st.selectbox("Select Graph",('','bar','pie','pie_bar'))
                if graphm == 'bar':
                    plt.title("Media message shared by each user",fontsize=15)
                    plt.xlabel("User Name",fontsize=12)
                    plt.ylabel("Number of media message",fontsize=12)
                    plt.bar(media_msg_by_each_user.index,media_msg_by_each_user['Text'])
                    st.pyplot()
                if graphm == 'pie':
                    plt.title("Media message shared by each user",fontsize=15)
                    plt.pie(media_msg_by_each_user['Text'],labels=media_msg_by_each_user.index,autopct="%0.2f%%")
                    st.pyplot()

                if graphm == 'pie_bar':
                    plt.subplot(2,1,1)
                    plt.title("Media message shared by each user",fontsize=15)
                    plt.xlabel("User Name",fontsize=12)
                    plt.ylabel("Number of media message",fontsize=12)
                    plt.bar(media_msg_by_each_user.index,media_msg_by_each_user['Text'])
                    st.pyplot()

                    plt.subplot(2,1,2)
                    plt.title("Media message shared by each user",fontsize=15)
                    plt.pie(media_msg_by_each_user['Text'],labels=media_msg_by_each_user.index,autopct="%0.2f%%")
                    st.pyplot()

            # Message shared per day
            if st.checkbox("Message shared per day"):
                msg=df.groupby("Date").count()
                graphm=st.selectbox("Select Graph",('','bar','pie','pie_bar'))
                if graphm == 'bar':
                    plt.title("Message shared per day",fontsize=15)
                    plt.xlabel("Date",fontsize=12)
                    plt.ylabel("Number of message",fontsize=12)
                    plt.bar(msg[:20].index,msg[:20]['Text'])
                    st.pyplot()
                if graphm == 'pie':
                    plt.title("Message shared per day",fontsize=15)
                    plt.pie(msg[:20]['Text'],labels=msg[:20].index,autopct="%0.2f%%")
                    st.pyplot()

                if graphm == 'pie_bar':
                    plt.subplot(2,1,1)
                    plt.title("Message shared per day",fontsize=15)
                    plt.xlabel("Date",fontsize=12)
                    plt.ylabel("Number of message",fontsize=12)
                    plt.bar(msg[:20].index,msg[:20]['Text'])
                    st.pyplot()

                    plt.subplot(2,1,2)
                    plt.title("Message shared per day",fontsize=15)
                    plt.pie(msg[:20]['Text'],labels=msg[:20].index,autopct="%0.2f%%")
                    st.pyplot()

            # Media message shared per day
            if st.checkbox("Media message shared per day"):
                msg=df[df["Text"]==" media shared"].groupby("Date").count()
                graphm=st.selectbox("Select Graph",('','bar','pie','pie_bar'))
                if graphm == 'bar':
                    plt.title("Media message shared per day",fontsize=15)
                    plt.xlabel("Date",fontsize=12)
                    plt.ylabel("Number of media message",fontsize=12)
                    plt.bar(msg[:20].index,msg[:20]['Text'])
                    st.pyplot()
                
                if graphm == 'pie':
                    plt.title("Media message shared per day",fontsize=15)
                    plt.pie(msg[:20]['Text'],labels=msg[:20].index,autopct="%0.2f%%")
                    st.pyplot()

                if graphm == 'pie_bar':
                    plt.subplot(2,1,1)
                    plt.title("Media message shared per day",fontsize=15)
                    plt.xlabel("Date",fontsize=12)
                    plt.ylabel("Number of media message",fontsize=12)
                    plt.bar(msg[:20].index,msg[:20]['Text'])

                    plt.subplot(2,1,2)
                    plt.title("Media message shared per day",fontsize=15)
                    plt.pie(msg[:20]['Text'],labels=msg[:20].index,autopct="%0.2f%%")
                    st.pyplot()
            
            if st.button("It's Completed"):
                st.balloons()
   
if __name__ == "__main__":
    main()
