import pickle
import streamlit as st
import pandas as pd
from datetime import datetime as dt


hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)

st.markdown('<h1 style="color:white;">Traffi AI</h1>', unsafe_allow_html=True)
st.markdown('<h2 style="color:gray;">Traffic jam solution</h2>', unsafe_allow_html=True)


with open ('model.pkl', 'rb') as f:
    clf = pickle.load(f)

def main():

    left, right = st.columns(2)   
    with left:     
  # add element on the left side   
     with right:     
  # add element on the right side
        Junction = st.radio('Junction', options=['1', '2', '3', '4'], 
          horizontal=True)
        ID = st.number_input('ID')
        Vehicles = st.number_input('Vehicles')
    
        if st.button('Predict'):
            DateTime= dt.today()
            DateTime= DateTime.toordinal()
            prediction = clf.predict([[Junction, Vehicles, DateTime]])
            st.success(prediction)



if __name__=='__main__':
    main()