#Full Programme to Show NPS
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import mysql.connector
import pymysql
import seaborn as sns
from sqlalchemy import text
from sqlalchemy import create_engine
pymysql.install_as_MySQLdb()


st.title("NPS Calculator!")

# Initialize connection.
conn = st.connection("neon", type="sql")

# Perform query.
df = conn.query('SELECT * FROM nps_survey')
st.write(df)

#Run query with pandas for NPS calculation
df_nps_today = pd.read_sql("SELECT user_id, score FROM nps_survey WHERE date = CURRENT_DATE", con=conn.engine)

# Get today's date
today = datetime.date.today()
#st.write(f"Scores for Today ({today})", df_nps_today)

fig, ax = plt.subplots()
ax.plot(df_nps_today.user_id, df_nps_today.score) 
ax.set_ylabel('Score')
ax.set_xlabel('User ID')
ax.grid()
#Python’s f‑strings, short for formatted string literals.
ax.set_title(f"Today's User Ratings ({today})")
#st.pyplot(fig)

# Convert to NumPy array
data = df_nps_today.score.to_numpy()

# Save as .npy file
np.save("nps_survey.npy", data)

# Later, load it back with np.load
score_file = np.load("nps_survey.npy", allow_pickle = True)
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



#######################################################################
#1. add new column user_type
#	promoter>=9, detractor<=6, passives<=6 & >=9
#2. Draw the graph bar chat using Seaborn
#######################################################################
def assign_user_type(score):
  if score <= 6: return 'detractor'
  elif score >= 9: return 'promoter'
  else: return 'passives'

# Example for SQLite
conn = st.connection("neon", type="sql")
df = pd.read_sql("SELECT * FROM nps_survey", con=conn.engine)

#new column added user_type
df['user_type'] = df['score'].apply(assign_user_type)
#st.write("df_nps_today new column: ", df)

with conn.session as session:
    # 1. Add the column (if needed)
    session.execute(text("ALTER TABLE nps_survey ADD COLUMN IF NOT EXISTS user_type VARCHAR(255)"))
    
    # 2. Run the update in bulk (avoids hitting the pool limit)
    params = [{"val": row["user_type"], "id": row["user_id"]} for _, row in df.iterrows()]
    session.execute(
        text("UPDATE nps_survey SET user_type = :val WHERE user_id = :id"),
        params
    )
    session.commit()

st.write(df)

st.write(df['user_type'].value_counts())


fig, ax = plt.subplots()
sns.countplot(data=df, x='user_type', ax=ax, palette='viridis')

custom_colors = {"promoter": "green", "passive": "gray", "detractor": "red"}
sns.countplot(data=df, x='user_type', palette=custom_colors, ax=ax)

# 3. Add labels (Optional)
ax.set_title("Distribution of User Types")
ax.set_xlabel("User Category")
ax.set_ylabel("Count")

# 4. Display in Streamlit
st.pyplot(fig)









