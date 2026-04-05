#Full Programme to Show NPS
import streamlit as st
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import datetime
import mysql.connector
import pymysql
pymysql.install_as_MySQLdb()

st.title("NPS Calculator!")

# Initialize connection.
conn = st.connection("neon", type="sql")

# Perform query.
df = conn.query('SELECT user_id, score FROM survey WHERE date = CURRENT_DATE')

st.write("Scores for Today ", df)

# Get today's date
today = datetime.date.today()

fig, ax = plt.subplots()
ax.plot(df.user_id, df.score) 
ax.set_ylabel('Score')
ax.set_xlabel('User ID')
ax.grid()
#Python’s f‑strings, short for formatted string literals.
ax.set_title(f"Today's User Ratings ({today})")
st.pyplot(fig)

#Run query with pandas for NPS calculation
df_nps = pd.read_sql("SELECT user_id, score FROM survey WHERE date = CURRENT_DATE", con=conn.engine)

# Convert to NumPy array
data = df_nps.to_numpy()

# Save as .npy file
np.save("survey.npy", data)

# Later, load it back with np.load
score = np.load("survey.npy", allow_pickle = True)
len(score)

#Calculate Detractor %
detractors = score[score<=6]
len(detractors)
percentage_detractors = (len(detractors)/len(score))*100

#Calculate Promoter %
promoters = score[score>=9]
len(promoters)
percentage_promoters = (len(promoters)/len(score))*100

#NPS CAlculation
NPS = percentage_promoters - percentage_detractors
st.write("Today's NPS for the company is", NPS)






##########################################################################################
# engine = create_engine("mysql+pymysql://root:aadi123@127.0.0.1:3306/smita_database")

# #Run query with pandas to get both score & userId for Visualisation using MATLABLIB
# df_visualisation = pd.read_sql("SELECT user_id, score FROM survey WHERE date = CURDATE()", engine)
# st.write("Scores for Today ", df_visualisation)

# # Get today's date
# today = datetime.date.today()

# fig, ax = plt.subplots()
# ax.plot(df_visualisation.user_id, df_visualisation.score) 
# ax.set_ylabel('Score')
# ax.set_xlabel('User ID')
# ax.grid()
# #Python’s f‑strings, short for formatted string literals.
# ax.set_title(f"Today's User Ratings ({today})")
# st.pyplot(fig)

# #Run query with pandas for NPS calculation
# df_nps = pd.read_sql("SELECT score FROM survey WHERE date = CURDATE()", engine)

# # Convert to NumPy array
# data = df_nps.to_numpy()

# # Save as .npy file
# np.save("survey.npy", data)

# # Later, load it back with np.load
# score = np.load("survey.npy", allow_pickle = True)
# len(score)

# #Calculate Detractor %
# detractors = score[score<=6]
# len(detractors)
# percentage_detractors = (len(detractors)/len(score))*100

# #Calculate Promoter %
# promoters = score[score>=9]
# len(promoters)
# percentage_promoters = (len(promoters)/len(score))*100

# #NPS CAlculation
# NPS = percentage_promoters - percentage_detractors
# st.write("Today's NPS for the company is", NPS)


