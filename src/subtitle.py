import streamlit as st

def makesubtitle(text, size="30px", color='g', weight='regular'):
   
    # GLOBAL PARAMS
    Green = "#1DB954"
    Black = "#191414"
    
    if color == 'g':
        
        color = Green
    elif 'b':
        color = Black
     # Defaulting 
    else: 
        
        color = Black


    st.markdown(f'''<span style="font-family: 'Circular Std'; font-size: {size}; color: {color}; font-weight: {weight}">{text}</span>''', unsafe_allow_html=True)