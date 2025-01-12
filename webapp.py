import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("data_temp.txt")
figure = px.line(x=df["date"], y=df["temperature"], labels={"x": "Date", "y": "Temp"})
st.plotly_chart(figure)