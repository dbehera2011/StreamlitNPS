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
df = conn.query('SELECT * FROM survey')
st.write(df)

#Run query with pandas for NPS calculation
df_nps_today = pd.read_sql("SELECT user_id, score FROM survey WHERE date = CURRENT_DATE", con=conn.engine)

# Get today's date
today = datetime.date.today()
st.write(f"Scores for Today ({today})", df_nps_today)

fig, ax = plt.subplots()
ax.plot(df_nps_today.user_id, df_nps_today.score) 
ax.set_ylabel('Score')
ax.set_xlabel('User ID')
ax.grid()
#Python’s f‑strings, short for formatted string literals.
ax.set_title(f"Today's User Ratings ({today})")
st.pyplot(fig)

# Convert to NumPy array
data = df_nps_today.score.to_numpy()

# Save as .npy file
np.save("survey.npy", data)

# Later, load it back with np.load
score_file = np.load("survey.npy", allow_pickle = True)
len(score_file)

#Calculate Detractor %
detractors = score_file[score_file<=6]
len(detractors)
percentage_detractors = (len(detractors)/len(score_file))*100

#Calculate Promoter %
promoters = score_file[score_file>=9]
len(promoters)
percentage_promoters = (len(promoters)/len(score_file))*100

#NPS CAlculation
NPS = percentage_promoters - percentage_detractors
#st.write("Today's NPS for the company is", NPS)


with st.popover("Check Today's NPS"):
    st.markdown("👋Today's NPS for the company is", NPS)