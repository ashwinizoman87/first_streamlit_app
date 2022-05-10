
import streamlit
import pandas
import requests
import snowflake.connector
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

#create a repeatable code block(called a function)
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
  fruityvice_normalised = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalised
  
#new section to display fruitvice api responce
streamlit.header('Fruityvice Fruit Advice')
try:
  fruit_choice = streamlit.text_input('what fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()
    
#streamlit.write('The user entered', fruit_choice)  #take the json version of the response and normalize it

streamlit.header("View Our Fruit List - Add Your Favourites")
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * from fruit_load_list")
    return my_cur.fetchall()
  
# Add button to load the fruit
if streamlit.button('Get Fruit Load List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  my_cnx.close()
  streamlit.dataframe(my_data_rows)           #streamlit.stop()    #dont run anything Past
                                     
#allow the end user to add fruit to the list
def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into fruit_load_list values ('Papaya')")
    return "Thanks for adding " + new_fruit
  
add_my_fruit = streamlit.text_input('what fruit would you like add?')
if streamlit.button('Add a Fruit to the List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_function = insert_row_snowflake(add_my_fruit)
  streamlit.text(back_from_function)
    
  
#streamlit.write('Thanks for adding', add_fruit_list)

