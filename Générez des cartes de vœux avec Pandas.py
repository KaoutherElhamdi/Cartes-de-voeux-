#!/usr/bin/env python
# coding: utf-8

# <hr>
# <p><font color='crimson'><h1 align="center">Générez des cartes de vœux avec Pandas</h1></font><a
#                                                                                                  href="https://openclassrooms.com/fr/courses/4452741-decouvrez-les-librairies-python-pour-la-datascience/exercises/3040#/step1">Lien vers l'énoncé</a>.</p>

# <h2><font color='palevioletred'>Scénario</font></h2>
# Vous avez une idée de start-up ! Vous souhaitez vendre des cartes de vœux pour les anniversaires... Ca parait simple, mais attention, il y a un twist !
# 
# Vous voulez faire un type de cartes de vœux pour le jour de la semaine de naissance du destinataire. Vous aurez ainsi 7 types de cartes différents.
# 
# <h2><font color='palevioletred'>Les données</font></h2>
# Vous aimeriez prévoir la quantité de cartes à créer. Malheureusement, vous ne savez pas quelle quantité commander pour chaque jour. Mais vous avez accès aux données de naissance aux États-Unis dans ce </font><a href="http://www.pnas.org/content/15/3/168.full">fichier</a>.</p> (eh oui, vous partez directement à l'international !)

# <h2><font color='palevioletred'>Solution proposée</font></h2>

# In[1]:


#Importation des librairies nécessaires
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# In[2]:


#Importation des données
df=pd.read_csv("https://raw.githubusercontent.com/jakevdp/data-CDCbirths/master/births.csv")


# <h3><font color='cadetblue'>Visualisation des données</font></h3>

# In[3]:


df.head()


# In[4]:


df.describe(include="all")


# In[5]:


df.info()


# In[6]:


#Savoir s'il y a des Nans 
df.isnull().values.any()


# <h3><font color='cadetblue'>Nettoyage de données</font></h3>

# In[7]:


#On supprime les lignes contenants des Nans
df=df.dropna()
#Modifier les valeurs du colonne 'day' en entier
df["day"]=df["day"].astype(int)
#Supprimer les lignes où les jours supérieures à 31 ou négatives
df=df.drop(df[(df["day"]>31)|(df["day"]<1)].index)


df.info()


# In[8]:


df.index=pd.to_datetime(10000 * df.year +100 * df.month +df.day, format='%Y%m%d',errors='coerce')


# In[9]:


df.head()


# In[10]:


df.tail()


# <h3><font color='cadetblue'>Suite du Travail</font></h3>

# In[11]:


df['dayofweek']=df.index.dayofweek
df=df.dropna()
df['dayofweek']=df['dayofweek'].astype(int)
df.head()


# In[12]:


df['day_of_week'] = df.index.weekday_name
df.head()


# In[13]:


def decade(year):
    return 10*(year//10)

df['decade']=decade(df['year'])
df.head()


# In[14]:


dg=df[['decade','day_of_week','births']].groupby(['decade','day_of_week']).sum()


# In[15]:


sns.set_style("whitegrid")
sns.boxplot(x='day_of_week',y='births',hue='decade',data=df)
plt.title("whitegrid")


# In[16]:


sns.barplot(x='day_of_week', y='births', data=dg.reset_index(),hue='decade')


# In[17]:


sns.catplot(x="day_of_week", y="births",  hue="decade", kind="point", data=dg.reset_index())


# In[18]:


dg.reset_index().pivot(index='day_of_week',values='births',columns='decade').plot(kind='bar',stacked=True,figsize=(8,8))


# In[19]:


df.pivot_table('births', index='dayofweek',columns='decade', aggfunc='sum').plot()
plt.ylabel('births');


# <h4><font color='green'>NB:</font></h4>
# C'est vrai que les résultats obtenues sont claires mais on peut travailler avec le nombre moyen de naissances par jour :

# In[20]:


dq=df[['decade','day_of_week','births']].groupby(['decade','day_of_week']).mean()
dq=dq.rename(columns={"births":"moyen births per day"})
dq.head()


# In[21]:


sns.barplot(x='day_of_week', y='moyen births per day', data=dq.reset_index(),hue='decade')


# In[22]:


sns.catplot(x="day_of_week", y="moyen births per day",  hue="decade", kind="point", data=dq.reset_index())


# In[23]:


dq.reset_index().pivot(index='day_of_week',values='moyen births per day',columns='decade').plot(kind='bar',stacked=True,figsize=(8,8))


# In[24]:


df.pivot_table('births', index='day_of_week',columns='decade', aggfunc='mean').plot()
plt.ylabel('Moyen births per day');

