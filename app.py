import streamlit as st
from logic import offer_convert, hotel_recommender

st.set_page_config(page_title='Indian Hotel Recommendation', layout='wide')
st.title('Hotel Recommender')

with st.form('form'):
    city = st.text_input(label="City", value="Mumbai")
    location = st.text_input(label="Location", value="Dadar")
    requirements = st.text_input(label="Your Requirements")
    min_no_of_ratings = st.number_input(label="Minimum number of ratings",value=10)
    min_price = st.number_input(label="Minimum Price in Rupees",value=500)
    max_price = st.number_input(label="Maximum Price in Rupees",value=2000)
    offer = st.radio(label="Do you want a Discounted offer included?",options=["Yes","No"])
    submitted = st.form_submit_button('Submit')
    if submitted:
        offer = offer_convert(offer)
        df = hotel_recommender(city=city,location=location,min_no_of_ratings=min_no_of_ratings,min_price=min_price\
            ,max_price=max_price,offer=offer,requirements=requirements)
        st.dataframe(df,use_container_width=True)
    

