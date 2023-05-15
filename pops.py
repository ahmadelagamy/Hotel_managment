""" this is a streamlit webapp that enables users to enter a url and it scrapes conference websites for hotel name and reservation number and links to the hotel website."""
# the app has a sidebar with a title and a text box for the url
# the main page has a title and a button to scrape the url
# when the user clicks the button, the app scrapes the conference website for the hotel name and reservation number
# the app displays the hotel name and reservation number in a table
import streamlit as st
import pandas as pd
import requests
import re
import json
import time
import os
import sys
import base64
from bs4 import BeautifulSoup as bs

st.title('Conference Hotel Scraper')
st.sidebar.title('Conference Hotel Scraper')
st.sidebar.markdown('A webapp that scrapes conference websites for hotel name and reservation number.')
st.sidebar.markdown('Enter the url of the conference website below:')
url = st.sidebar.text_input('Enter the url of the conference website here:')

#don't run the code until a url is provided
if url == '':
    st.stop()
    
# declarong global variables to store the results of the scraping function
hotel_name = ''
reservation_number = ''
hotel_address = ''
hotel_phone_number = ''
hotel_website = ''
room_rate = ''
room_rate_expiration_date = ''
room_rate_expiration_time = ''
room_rate_disclaimer = ''

# function for scraping the conference website for the hotel name and reservation number
def scrape(url):
    response = requests.get(url)
    soup = bs.BeautifulSoup(response.text, 'html.parser')
    # find the hotel name
    hotel_name = soup.find_all('h4', class_ = 'hotel-name')
    # find the reservation number
    reservation_number = soup.find_all('span', class_ = 'reservation-number')
    # find the hotel address
    hotel_address = soup.find_all('p', class_ = 'hotel-address')
    # find the hotel phone number
    hotel_phone_number = soup.find_all('p', class_ = 'hotel-phone')
    # find the hotel website
    hotel_website = soup.find_all('a', class_ = 'hotel-website')
    # find the hotel room rate
    room_rate = soup.find_all('p', class_ = 'room-rate')
    # find the hotel room rate expiration date
    room_rate_expiration_date = soup.find_all('p', class_ = 'room-rate-expiration-date')
    # find the hotel room rate expiration time
    room_rate_expiration_time = soup.find_all('p', class_ = 'room-rate-expiration-time')
    # find the hotel room rate disclaimer
    room_rate_disclaimer = soup.find_all('p', class_ = 'room-rate-disclaimer')
    return hotel_name, reservation_number, hotel_address, hotel_phone_number, hotel_website, room_rate, room_rate_expiration_date, room_rate_expiration_time, room_rate_disclaimer

# display results of the above function in a table
if st.sidebar.button('Scrape'):
    st.header('Hotel Information')
    st.subheader('Hotel Name')
    st.write(hotel_name)
    st.subheader('Reservation Number')
    st.write(reservation_number)
    st.subheader('Hotel Address')
    st.write(hotel_address)
    st.subheader('Hotel Phone Number')
    st.write(hotel_phone_number)
    st.subheader('Hotel Website')
    st.write(hotel_website)
    st.subheader('Room Rate')
    st.write(room_rate)
    st.subheader('Room Rate Expiration Date')
    st.write(room_rate_expiration_date)
    st.subheader('Room Rate Expiration Time')
    st.write(room_rate_expiration_time)
    st.subheader('Room Rate Disclaimer')
    st.write(room_rate_disclaimer)
    
# Write code to save the results of the scraping function to a google sheet
df= pd.DataFrame({'Hotel Name': hotel_name, 'Reservation Number': reservation_number, 'Hotel Address': hotel_address, 'Hotel Phone Number': hotel_phone_number, 'Hotel Website': hotel_website, 'Room Rate': room_rate, 'Room Rate Expiration Date': room_rate_expiration_date, 'Room Rate Expiration Time': room_rate_expiration_time, 'Room Rate Disclaimer': room_rate_disclaimer})
df.to_csv('hotel_information.csv', index=False)

#show csv in smart table format
#create download button
def csv_downloader(data):
    csvfile = data.to_csv(index=False)
    b64 = base64.b64encode(csvfile.encode()).decode()
    new_filename = "new_text_file.csv"
    st.markdown("### ** Download CSV File **")
    href = f'<a href="data:file/csv;base64,{b64}" download="{new_filename}">Click Here!!</a>'
    st.markdown(href,unsafe_allow_html=True)
    
if st.sidebar.button('Download CSV'):
    csv_downloader(df)
    
    