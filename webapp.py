import streamlit as st
import sqlite3
import plotly.express as px

connection = sqlite3.connect("data_temp.db")
cursor = connection.cursor()
cursor.execute("SELECT date FROM temperature")
date = cursor.fetchall()
date = [item[0] for item in date]

cursor.execute("SELECT temperature FROM temperature")
temperature = cursor.fetchall()
temperature = [item[0] for item in temperature]
print(temperature)

figure = px.line(x=date, y=temperature, labels={"x": "Date", "y": "Temp"})
st.plotly_chart(figure)