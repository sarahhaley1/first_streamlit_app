import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError
streamlit.title("My Mom's New Healthy Diner")

streamlit.header('Breakfast Favorites')
streamlit.text('🫐 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥬 Kale, Spinach & Rocket Smoothie')
streamlit.text('🥚 Hard-Boiled Free Range Egg')
streamlit.text('🥑 Avocado Toast')


streamlit.title("🍌🍓 Build Your Own Fruit Smoothie 🥝🍇")


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Adding a Pick List here so they can pick what they want to include in their smoothie 
# Adding an automated example for display 
# created a variable to hold the fruits selected
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])

#filtering the table to only show fruits selected 
fruits_to_show = my_fruit_list.loc[fruits_selected]

#display the table on the page
streamlit.dataframe(fruits_to_show)

#create funciton to pull in fruit choices
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized
  
#New Section to display fruityvice api response
streamlit.header('Fruityvice Fruit Advice!')
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
    
except URLError as e:
  streamlit.error()
streamlit.write('The user entered', fruit_choice)







# dont run anything past here while we troubleshoot
streamlit.stop()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)

add_my_fruit = streamlit.text_input('What fruit would you like to add?', 'jackfruit')
streamlit.write('Thanks for adding', add_my_fruit)
my_cur.execute("insert into fruit_load_list values ('from streamlit')")
