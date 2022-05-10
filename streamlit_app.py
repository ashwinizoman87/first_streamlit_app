
import streamlit
#import pandas
#import requests
#import snowflake.connector
from urllib.error import URLError

streamlit.title('My Mom\'s Healthy Diner')
streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')          #Choose the Fruit Name Column as the Index

#filter the table data based on the fruits a customer will choose, so we'll pre-populate the list to set an example for the customer. 
#streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])

#We'll ask our app to put the list of selected fruits into a variable called fruits_selected.
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Banana','Strawberries'])   #after removing ['Avocado','Strawberries]
#fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)   #to display fruit on table

#Put a picklist
#streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))

#display fruit table on page
#streamlit.dataframe(my_fruit_list)

#new section to display fruitvice api responce
streamlit.header('Fruityvice Fruit Advice')
fruit_choice = streamlit.text_input('what fruit would you like information about?', 'Banana')
streamlit.write('The user entered', fruit_choice)


fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)


#take the json version of the response and normalize it
fruityvice_normalised = pandas.json_normalize(fruityvice_response.json())
#output it the screen as a table
streamlit.dataframe(fruityvice_normalised)

streamlit.stop()    #dont run anything Past


my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit_load_list contains:")
streamlit.dataframe(my_data_rows)

add_fruit_list = streamlit.text_input('what fruit would you like information about?','Plum')
streamlit.write('Thanks for adding', add_fruit_list)
my_cur.execute("insert into fruit_load_list values ('from streamlit')")
