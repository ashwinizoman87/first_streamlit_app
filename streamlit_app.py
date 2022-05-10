
import streamlit


streamlit.title('My Mom\'s Healthy Diner')
streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')


streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

#Choose the Fruit Name Column as the Index
my_fruit_list = my_fruit_list.set_index('Fruit')

#filter the table data based on the fruits a customer will choose, so we'll pre-populate the list to set an example for the customer. 
#streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])

#We'll ask our app to put the list of selected fruits into a variable called fruits_selected.
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries']) #after removing ['Avocado','Strawberries]
#fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))
fruits_to_show = my_fruit_list.loc[fruits_selected]
#Then, we'll ask our app to use the fruits in our fruits_selected list to pull rows from the full data set
streamlit.dataframe(fruits_to_show)

#Put a picklist
#streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))

#display fruit table on page
#streamlit.dataframe(my_fruit_list)


streamlit.header('Fruityvice Fruit Advice')



fruit_choice = streamlit.text_input('what fruit would you like information about?', 'kiwi')
streamlit.write('The user entered', fruit_choice)

import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)


#take the json version of the response and normalize it
fruityvice_normalised = pandas.json_normalize(fruityvice_response.json())
#output it the screen as a table
streamlit.dataframe(fruityvice_normalised)

import snowflake.connector

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit_load_list contains:")
streamlit.dataframe(my_data_rows)

add_fruit_list = streamlit.text_input('what fruit would you like information about?', 'jackfruit')
streamlit.write('The user entered', add_fruit_list)
