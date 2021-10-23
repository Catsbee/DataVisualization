import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
import seaborn as sns


st.header("A journey throught my google fit data")
st.subheader("Charlotte Mauvezin")
"""
github : [Catsbee](https://github.com/Catsbee)
"""
###########################Code de base#############################
"""
## Getting the data
Let's beggin by getting the data and have a look at it
"""
# Information sur les données
df = pd.read_csv("fit.csv")
#df.info()
st.write(df.describe())
#df.describe()
df.shape
"""
As we can see there is a lot of columns that are not usefull nor explicit
Tho we can also see that we have a register of 1165 day which is a lot so let's get cleaning
"""
"""
PS : before continuing let's look at the hash value of the dataframe and stock it
"""
## Créating hash value
st.write(hash(df.values.tobytes()))

# Traitement des données
df.head()
# Plusieurs colonnes ne servent à rien, sont vide ou ont des valeurs qui n'ont
# pas le bon type ou pas la bonne échelle
# Bref il faut nettoyer les données
"""
## Cleaning
We said that there was a lot of column which were useless so drop them
Here is the new (but not yet improved dataframe
"""
df.drop(['Poids moyen (kg)', 'Poids maximal (kg)','Poids minimal (kg)','Basse latitude (°)','Basse longitude (°)','Haute latitude (°)','Haute longitude (°)'], axis=1, inplace = True)
st.dataframe(df)
st.write(df.shape)


"""
Now let's get usefull and standardize value
## Formating
* a better name for data
* propper date format
* deleting none data
* having better dimension
"""
df.columns = ['Date','NbMinAct','Cal(kcal)','Dist(m)','PtsCard','MinCard','VitMoy(m/s)','VitMax(m/s)','VitMin(m/s)','NbPas','Velo(ms)','Inactif(ms)','Marche(ms)','Course(ms)','Elliptique(ms)','EntFracHautInt(ms)']

# dealing with date format
df['Date'] = pd.to_datetime(df['Date'], dayfirst = True)

# dealing with none data
df.fillna(0, inplace = True)

# dealing with better dimensions
df['Cal(kcal)'] = (df['Cal(kcal)'] // 1).astype(int)
df['Dist(m)'] = (df['Dist(m)'] // 1).astype(int)
df['VitMoy(m/s)'] = round(df['VitMoy(m/s)'] * 3600 / 1000, 1)
df['VitMax(m/s)'] = round(df['VitMax(m/s)'] * 3600 / 1000, 1)
df['VitMin(m/s)'] = round(df['VitMin(m/s)'] * 3600 / 1000, 1)
df['NbPas'] = df['NbPas'].astype(int)
df['NbMinAct'] = df['NbMinAct'].astype(int)
df['Velo(ms)'] = (df['Velo(ms)'] // 1000 // 60).astype(int)
df['Inactif(ms)'] = (df['Inactif(ms)'] // 1000 // 60).astype(int)
df['Marche(ms)'] = (df['Marche(ms)'] // 1000 // 60).astype(int)
df['Course(ms)'] = (df['Course(ms)'] // 1000 // 60).astype(int)
df['Elliptique(ms)'] = (df['Elliptique(ms)'] // 1000 // 60).astype(int)
df['EntFracHautInt(ms)'] = (df['EntFracHautInt(ms)'] // 1000 // 60).astype(int)

# new better name
df.columns = ['Date','NbMinAct','Cal(kcal)','Dist(m)','PtsCard','MinCard','VitMoy(km/h)','VitMax(km/h)','VitMin(km/h)','NbPas','Velo(min)','Inactif(min)','Marche(min)','Course(min)','Elliptique(min)','EntFracHautInt(min)']
"""
### My new dataframe
"""
st.dataframe(df)
"""
The date is still iffy so let's focus on better period
# Better date
"""

df['Jour'] = df['Date'].dt.dayofweek
days_of_week = {0: 'Lundi', 1: 'Mardi', 2: 'Mercredi', 3: 'Jeudi', 4: 'Vendredi', 5: 'Samedi', 6:'Dimanche'}
df['Jour'].replace(days_of_week, inplace = True)
cols = ['Date','Jour','NbMinAct','Cal(kcal)','Dist(m)','PtsCard','MinCard','VitMoy(km/h)','VitMax(km/h)','VitMin(km/h)','NbPas','Velo(min)','Inactif(min)','Marche(min)','Course(min)','Elliptique(min)','EntFracHautInt(min)']
df = df[cols]

# The information start to be really interesting by 2018-08-14 (I got my new phone)
df2 = df[df['Date'] > '2018-08-14']
df2
"""
## Let's explore the data to see what is correlated

"""
#fig = sns.pairplot(df)
#st.pyplot(fig)
"""
Lots and lots of datas which don't explicitly show us interesting stuff
Let's focus on my diferent activity throught time

### First my activity in minute per day
"""
#fig = plt.figure(figsize=(8,5))
#plt.plot(df2['Date'], df2['NbMinAct'], color = 'y')
#plt.title('Minute active par jour', fontsize = 16)
#plt.ylabel('Nombre de minutes actives',fontsize =12)
#plt.xlabel('Jour')
#plt.xticks(rotation=45)
#plt.tick_params(bottom=False, top=False, left=False, right=False)
#plt.gca().spines['top'].set_visible(False)
#plt.gca().spines['bottom'].set_visible(False)
#plt.gca().spines['right'].set_visible(False)
#plt.gca().spines['left'].set_visible(False)
#plt.grid()
#plt.show()
#st.pyplot(fig)

st.write(alt.Chart(df2, title='Number of activity each day').mark_trail().encode(
    x='Date:T',
    y='NbMinAct:Q',
    color=alt.value('pink')
).properties(
    width=700,
    height=400
))
"""
### Now let's see if i do the appropriate minute of activity
"""
week_activity = []
week_start = []
df2.reset_index(inplace = True)
#print(df2['Date'])
for day in range(0, len(df2['Date']), 7):
    week = df2['NbMinAct'][day:day+6].sum()
    week_activity.append(week)
    week_start.append(df2['Date'][day])

fig = plt.figure(1, figsize = (6, 3))
##########################################################plt.style.use('dark_background')
fig.add_axes([0, 0, 1, 1])
ax = plt.gca()

plt.plot(week_start[:-1], week_activity[:-1], color = 'b')
plt.axhline(150, linestyle = '--', color = 'r')
plt.title("Weekly activity in minute", fontsize = 16)
plt.ylabel("Activity in minutes", fontsize = 12)
plt.xticks(rotation = 45)
plt.ylim(0, 700)
plt.tick_params(bottom=False, top=False, left=False, right=False)#plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['bottom'].set_visible(False)
plt.gca().spines['left'].set_visible(False)
plt.grid()
plt.text(0.82, 0.25, '150 minutes', transform=ax.transAxes, fontsize=12)
plt.show()
st.pyplot(fig)



"""
### how many minutes of sport I do usually
"""
fig = plt.figure(figsize=(7,5))
plt.hist(df2['NbMinAct'], 7, alpha=0.3, color='b', edgecolor='b')
plt.xticks(range(0, 240, 30))
plt.title('Intervals in minutes', fontsize=15)
plt.ylabel('Number of days', fontsize=12)
plt.tick_params(bottom=False, top=False, left=False, right=False)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['bottom'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['left'].set_visible(False)
plt.show()
st.pyplot(fig)

#st.write(alt.Chart(df2).mark_bar().encode(
#    alt.X("NbMinAct:Q", bin=alt.Bin(maxbins=7)),
#    y='count()',
#).properties(
#    width=800,
#    height=400
#))

#df2

days_of_week = ['Sunday','Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
active_minutes_per_day_of_week = df2.groupby('Jour')['NbMinAct'].sum()
number_of_days = df2['Jour'].value_counts()
for day in days_of_week:
    average_active_minutes_per_day_of_week = active_minutes_per_day_of_week // number_of_days

# Average active minutes per day of week

#fig = plt.figure(figsize=(7,3))
#plt.plot(range(7), average_active_minutes_per_day_of_week, color='b')
#plt.ylabel('Activity in minutes', fontsize=12)
#plt.title('Average active Minutes per Day of Week', fontsize=15)
#plt.xticks(range(7), days_of_week, rotation='45')
#plt.yticks(range(0, 120, 20))
#plt.tick_params(bottom=False, top=False, left=False, right=False)
#plt.gca().spines['top'].set_visible(False)
#plt.gca().spines['right'].set_visible(False)
#plt.gca().spines['bottom'].set_visible(False)
#plt.gca().spines['left'].set_visible(False)
#plt.show()
#st.pyplot(fig)
"""
### My physical activity
"""
marcher = df2['Marche(min)'].sum()
courrir = df2['Course(min)'].sum()
rouler = df2['Velo(min)'].sum()
tourner = df2['Elliptique(min)'].sum()
franction = df2['EntFracHautInt(min)'].sum()

activities_array = [marcher, courrir, rouler, tourner, franction]
activities_labels = ['Marcher', 'Courrir', 'Vélo', 'Elliptique', 'EntFrac']

frame = {'Activity': activities_labels, 'Duration': activities_array}

activities = pd.DataFrame(frame)
activities.sort_values(by=['Duration'], inplace=True)

fig = plt.figure(figsize=(10,5))
plt.barh(activities['Activity'], activities['Duration'], alpha=0.3, color='b', edgecolor='b')
plt.barh(activities['Activity'][0], activities['Duration'][0], alpha=0.3, color='r', edgecolor='r')
plt.title('Different Activities', fontsize=15)
plt.tick_params(bottom=False, top=False, left=False, right=False)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['left'].set_visible(False)
plt.gca().spines['bottom'].set_visible(False)
plt.ylabel('Activity in minutes', fontsize=12)
plt.show()
st.pyplot(fig)
"""
We can see that I walk way more than any other activity 
### Let's analyse the specificity of this activity

"""

#On peut remarquer que je marcher beaucoup trop comparer aux autres activité physique
### Cet marche est beaucoup trop extrème, analysons la
df2['Marche(min)'].describe()

# what’s the distance I walked through all those days?
df2['Dist(m)'].describe()



# how many kilometers did I walk during those three months in general?
"""I walked a total of :"""
st.write(df2['Dist(m)'].sum())

# Number of steps per Day
fig = plt.figure(figsize=(10,5))

plt.plot(df2['Date'], df2['NbPas'], color='b')
plt.title('Number of Steps per Day', fontsize=15)
plt.ylabel('Number of Steps', fontsize=12)
plt.axhline(7500, linestyle='--', color='r', label = '7 500 steps', linewidth=0.5)
plt.xticks(rotation=45)
plt.tick_params(bottom=False, top=False, left=False, right=False)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['bottom'].set_visible(False)
plt.gca().spines['left'].set_visible(False)
plt.legend(loc='upper left', fontsize=12)

plt.show()
st.pyplot(fig)


# when it happened
"""The most of meter I walked in a day was in :"""
row = df2.loc[df2['Dist(m)'] == df2['Dist(m)'].max()]
st.write(row[['Date', 'Jour', 'Dist(m)']])

# Let’s count what percentage of days did I fulfilled this condition.
#more_then_10000_steps = sum(df2['NbPas'] > 10000)
#print('{}%'.format(more_then_10000_steps / 92 * 100))
"""
New hash value
"""
st.write(hash(df.values.tobytes()))
