
# coding: utf-8

# # Capstone Project 1: MuscleHub AB Test

# ## Step 1: Get started with SQL

# Like most businesses, Janet keeps her data in a SQL database.  Normally, you'd download the data from her database to a csv file, and then load it into a Jupyter Notebook using Pandas.
# 
# For this project, you'll have to access SQL in a slightly different way.  You'll be using a special Codecademy library that lets you type SQL queries directly into this Jupyter notebook.  You'll have pass each SQL query as an argument to a function called `sql_query`.  Each query will return a Pandas DataFrame.  Here's an example:

# In[1]:


# This import only needs to happen once, at the beginning of the notebook
from codecademySQL import sql_query


# In[2]:


# Here's an example of a query that just displays some data
sql_query('''
SELECT *
FROM visits
LIMIT 5;
''')


# In[3]:


# Here's an example where we save the data to a DataFrame
df = sql_query('''
SELECT *
FROM applications
LIMIT 5;
''')


# ## Step 2: Get your dataset

# Let's get started!
# 
# Janet of MuscleHub has a SQLite database, which contains several tables that will be helpful to you in this investigation:
# - `visits` contains information about potential gym customers who have visited MuscleHub
# - `fitness_tests` contains information about potential customers in "Group A", who were given a fitness test
# - `applications` contains information about any potential customers (both "Group A" and "Group B") who filled out an application.  Not everyone in `visits` will have filled out an application.
# - `purchases` contains information about customers who purchased a membership to MuscleHub.
# 
# Use the space below to examine each table.

# In[4]:


# Examine visits here
sql_query('''
SELECT * 
FROM visits
LIMIT 5;
''')


# How many records are there in the visits csv file?

# In[5]:


print('Total number of entries in visits:\n', sql_query('''SELECT COUNT(*) AS 'Number' FROM visits;'''))


# In[6]:


# Examine fitness_tests here
sql_query('''
SELECT * 
FROM fitness_tests
LIMIT 5;
''')


# In[7]:


# How many records are there in fitness_tests?
print('Total number of entries in fitness_tests:\n', sql_query('''SELECT COUNT(*) AS 'Number' FROM fitness_tests;'''))


# In[8]:


# Examine applications here
sql_query('''
SELECT *
FROM applications
LIMIT 5;
''')


# In[9]:


print('Total number of entries in applications:\n', sql_query('''SELECT COUNT(*) AS 'Number' FROM applications;'''))


# In[10]:


# Examine purchases here
sql_query('''
SELECT *
FROM purchases
LIMIT 5;
''')


# In[11]:


print('Total number of entries in purchases:\n', sql_query('''SELECT COUNT(*) AS 'Number' FROM purchases;'''))


# We'd like to download a giant DataFrame containing all of this data.  You'll need to write a query that does the following things:
# 
# 1. Not all visits in  `visits` occurred during the A/B test.  You'll only want to pull data where `visit_date` is on or after `7-1-17`.
# 
# 2. You'll want to perform a series of `LEFT JOIN` commands to combine the four tables that we care about.  You'll need to perform the joins on `first_name`, `last_name`, and `email`.  Pull the following columns:
# 
# 
# - `visits.first_name`
# - `visits.last_name`
# - `visits.gender`
# - `visits.email`
# - `visits.visit_date`
# - `fitness_tests.fitness_test_date`
# - `applications.application_date`
# - `purchases.purchase_date`
# 
# Save the result of this query to a variable called `df`.
# 
# Hint: your result should have 5004 rows.  Does it?

# In[12]:


df = sql_query('''
SELECT visits.first_name,
    visits.last_name,
    visits.email,
    visits.gender,
    visits.visit_date,
    fitness_tests.fitness_test_date,
    applications.application_date,
    purchases.purchase_date
FROM visits
LEFT JOIN fitness_tests
    ON visits.first_name = fitness_tests.first_name
    AND visits.last_name = fitness_tests.last_name
    AND visits.email = fitness_tests.email
LEFT JOIN applications
    ON visits.first_name = applications.first_name
    AND visits.last_name = applications.last_name
    AND visits.email = applications.email
LEFT JOIN purchases
    ON visits.first_name = purchases.first_name
    AND visits.last_name = purchases.last_name
    AND visits.email = purchases.email
WHERE visits.visit_date >= '7-1-17'
''')

pre_df = sql_query('''
SELECT visits.first_name,
    visits.last_name,
    visits.email,
    visits.gender,
    visits.visit_date,
    fitness_tests.fitness_test_date,
    applications.application_date,
    purchases.purchase_date
FROM visits
LEFT JOIN fitness_tests
    ON visits.first_name = fitness_tests.first_name
    AND visits.last_name = fitness_tests.last_name
    AND visits.email = fitness_tests.email
LEFT JOIN applications
    ON visits.first_name = applications.first_name
    AND visits.last_name = applications.last_name
    AND visits.email = applications.email
LEFT JOIN purchases
    ON visits.first_name = purchases.first_name
    AND visits.last_name = purchases.last_name
    AND visits.email = purchases.email
WHERE visits.visit_date < '7-1-17'
''')

big_df = sql_query('''
SELECT visits.first_name,
    visits.last_name,
    visits.email,
    visits.gender,
    visits.visit_date,
    fitness_tests.fitness_test_date,
    applications.application_date,
    purchases.purchase_date
FROM visits
LEFT JOIN fitness_tests
    ON visits.first_name = fitness_tests.first_name
    AND visits.last_name = fitness_tests.last_name
    AND visits.email = fitness_tests.email
LEFT JOIN applications
    ON visits.first_name = applications.first_name
    AND visits.last_name = applications.last_name
    AND visits.email = applications.email
LEFT JOIN purchases
    ON visits.first_name = purchases.first_name
    AND visits.last_name = purchases.last_name
    AND visits.email = purchases.email
''')


# Let's look at the range of dates of the visits for which we have records.

# In[13]:


print(pre_df.head())
print("First visit in records was on", big_df.iloc[:, 4].min())
print("Last visit before study started was on", pre_df.iloc[:, 4].max())
print("First visit during A/B test period was on", df.iloc[:, 4].min())
print("Last visit in records was on", big_df.iloc[:, 4].max())

# print("Look at years: min:", big_df.iloc[:, 4][-2,-1].min(), "max:", big_df.iloc[:, 4][-2,-1].max())
# big_df['visit_year'] = big_df.visit_date.apply(lambda date: date[-2,-1])
# print(big_df.head())


# OK, it looks like the range of dates is from 5-1-17 to 9-9-17.
# Also the records from before A/B test are a bit suspect.

# Let's see if I can find the people for whom we have interviews:

# In[14]:


big_df[big_df.first_name == 'Cora']


# Hm, no record of any Cora visiting.

# In[15]:


big_df[big_df.first_name == 'Jesse']


# Seven possible matches for Jesse.

# In[16]:


big_df[big_df.first_name == 'Sonny']


# No record of any Sonny.

# In[17]:


big_df[big_df.first_name == 'Shirley']


# Only one Shirley purchased membership, as implied by the interview, but the Shirley that signed up also took the fitness test, which is inconsistent with the interview.

# ## Step 3: Investigate the A and B groups

# We have some data to work with! Import the following modules so that we can start doing analysis:
# - `import pandas as pd`
# - `from matplotlib import pyplot as plt`

# In[18]:


import pandas as pd
from matplotlib import pyplot as plt
get_ipython().magic('matplotlib inline')


# We're going to add some columns to `df` to help us with our analysis.
# 
# Start by adding a column called `ab_test_group`.  It should be `A` if `fitness_test_date` is not `None`, and `B` if `fitness_test_date` is `None`.

# In[19]:


df['ab_test_group'] = df.fitness_test_date.apply(lambda date: 'A' if pd.notnull(date) else 'B')


# Let's do a quick sanity check that Janet split her visitors such that about half are in A and half are in B.
# 
# Start by using `groupby` to count how many users are in each `ab_test_group`.  Save the results to `ab_counts`.

# In[20]:


ab_counts = df.groupby('ab_test_group').count().reset_index()
ab_counts


# We'll want to include this information in our presentation.  Let's create a pie cart using `plt.pie`.  Make sure to include:
# - Use `plt.axis('equal')` so that your pie chart looks nice
# - Add a legend labeling `A` and `B`
# - Use `autopct` to label the percentage of each group
# - Save your figure as `ab_test_pie_chart.png`

# In[21]:


plt.pie(ab_counts.first_name.values, autopct='%0.2f%%')
plt.axis('equal')
plt.legend(['Group A (control)', 'Gropu B (experimental)'], fontsize=11, loc=(.8,.8))
plt.title('Relative Experimental Group Size', fontsize=20)

plt.show()
plt.savefig('ab_test_pie_chart.png')


# I would like to look at the gender make up of the visitors.

# In[22]:


mf_counts = df.groupby('gender').count().reset_index()
mf_counts


# I'll create a pie chart of the relative gender split.

# In[23]:


plt.pie(mf_counts.first_name.values, autopct='%0.2f%%')
plt.axis('equal')
plt.legend(['Female', 'Male'], fontsize=11, loc=(.8,.8))
plt.title('Gender Makeup of Total Population', fontsize=20)

plt.show()
plt.savefig('mf_pie_chart.png')


# And are the males and females evenly split between the two groups?

# In[24]:


mf_ab_counts = df.groupby(['ab_test_group', 'gender']).count().reset_index()
mf_ab_counts


# Uh, oh. It looks like there are disproportionately more females in group B.

# In[25]:


mf_ab_pivot = mf_ab_counts.pivot(columns='gender',
                             index='ab_test_group',
                             values='first_name').reset_index()
mf_ab_pivot['Total'] = mf_ab_pivot.female + mf_ab_pivot.male
mf_ab_pivot['Percent Female'] = 100.0 * mf_ab_pivot.female / mf_ab_pivot.Total
mf_ab_pivot['Percent Male'] = 100.0 * mf_ab_pivot.male / mf_ab_pivot.Total

mf_ab_pivot


# In[26]:


plt.figure(figsize=(8,5))
plt.subplot(1, 2, 1)
plt.pie(mf_ab_counts.first_name.values[0:2], autopct='%0.2f%%')
plt.axis('equal')
plt.legend(['Female', 'Male'], fontsize=11, loc=(.8,.8))
plt.title('Gender Makeup of Group A', fontsize=16)

plt.subplot(1, 2, 2)
plt.pie(mf_ab_counts.first_name.values[2:4], autopct='%0.2f%%')
plt.axis('equal')
plt.legend(['Female', 'Male'], fontsize=11, loc=(.8,.8))
plt.title('Gender Makeup of Group B', fontsize=16)

plt.subplots_adjust(wspace=.5)

plt.show()
plt.savefig('mf_ab_pie_chart.png')


# Let's check how significant the difference is.

# In[27]:


from scipy.stats import chi2_contingency
X = [[1255, 1249],
     [1309, 1191]]
chi2, pval, dof, expected = chi2_contingency(X)
pval


# Phew, we cannot reject the null hypothesis, that there is not a significant diference between the gender makeup of the two groups.

# ## Step 4: Who picks up an application?

# Recall that the sign-up process for MuscleHub has several steps:
# 1. Take a fitness test with a personal trainer (only Group A)
# 2. Fill out an application for the gym
# 3. Send in their payment for their first month's membership
# 
# Let's examine how many people make it to Step 2, filling out an application.
# 
# Start by creating a new column in `df` called `is_application` which is `Application` if `application_date` is not `None` and `No Application`, otherwise.

# In[28]:


df['is_application'] = df.application_date.apply(lambda date: 'Application' if pd.notnull(date) else 'No Application')


# Now, using `groupby`, count how many people from Group A and Group B either do or don't pick up an application.  You'll want to group by `ab_test_group` and `is_application`.  Save this new DataFrame as `app_counts`

# In[29]:


app_counts = df.groupby(['ab_test_group', 'is_application']).count().reset_index()
app_counts


# We're going to want to calculate the percent of people in each group who complete an application.  It's going to be much easier to do this if we pivot `app_counts` such that:
# - The `index` is `ab_test_group`
# - The `columns` are `is_application`
# Perform this pivot and save it to the variable `app_pivot`.  Remember to call `reset_index()` at the end of the pivot!

# In[30]:


app_pivot = app_counts.pivot(columns='is_application',
                             index='ab_test_group',
                             values='first_name').reset_index()
# app_pivot


# Define a new column called `Total`, which is the sum of `Application` and `No Application`.

# In[31]:


app_pivot['Total'] = app_pivot.Application + app_pivot['No Application']
# app_pivot


# Calculate another column called `Percent with Application`, which is equal to `Application` divided by `Total`.

# In[32]:


app_pivot['Percent with Application'] = 100.0 * app_pivot.Application / app_pivot.Total
app_pivot


# It looks like more people from Group B turned in an application.  Why might that be?
# 
# We need to know if this difference is statistically significant.
# 
# Choose a hypothesis tests, import it from `scipy` and perform it.  Be sure to note the p-value.
# Is this result significant?

# In[33]:


# from scipy.stats import chi2_contingency
X = [[250, 2254],
     [325, 2175]]
chi2, pval, dof, expected = chi2_contingency(X)
pval


# ## Step 5: Who purchases a membership?

# Of those who picked up an application, how many purchased a membership?
# 
# Let's begin by adding a column to `df` called `is_member` which is `Member` if `purchase_date` is not `None`, and `Not Member` otherwise.

# In[34]:


df['is_member'] = df.purchase_date.apply(lambda date: 'Member' if pd.notnull(date) else "Not Member")
# df


# Now, let's create a DataFrame called `just_apps` the contains only people who picked up an application.

# In[35]:


just_apps = df[df.is_application == "Application"]
# just_apps


# Great! Now, let's do a `groupby` to find out how many people in `just_apps` are and aren't members from each group.  Follow the same process that we did in Step 4, including pivoting the data.  You should end up with a DataFrame that looks like this:
# 
# |is_member|ab_test_group|Member|Not Member|Total|Percent Purchase|
# |-|-|-|-|-|-|
# |0|A|?|?|?|?|
# |1|B|?|?|?|?|
# 
# Save your final DataFrame as `member_pivot`.

# In[36]:


member_count = just_apps.groupby(['ab_test_group', 'is_member']).first_name.count().reset_index()
member_pivot = member_count.pivot(columns='is_member',
                                  index='ab_test_group',
                                  values='first_name').reset_index()
member_pivot['Total'] = member_pivot.Member + member_pivot['Not Member']
member_pivot['Percent Purchase'] = 100.0 * member_pivot.Member / member_pivot.Total
member_pivot


# It looks like people who took the fitness test were more likely to purchase a membership **if** they picked up an application.  Why might that be?
# 
# Just like before, we need to know if this difference is statistically significant.  Choose a hypothesis tests, import it from `scipy` and perform it.  Be sure to note the p-value.
# Is this result significant?

# In[37]:


X = [[200, 50],
     [250, 75]]
chi2, pval, dof, expected = chi2_contingency(X)
pval


# Previously, we looked at what percent of people **who picked up applications** purchased memberships.  What we really care about is what percentage of **all visitors** purchased memberships.  Return to `df` and do a `groupby` to find out how many people in `df` are and aren't members from each group.  Follow the same process that we did in Step 4, including pivoting the data.  You should end up with a DataFrame that looks like this:
# 
# |is_member|ab_test_group|Member|Not Member|Total|Percent Purchase|
# |-|-|-|-|-|-|
# |0|A|?|?|?|?|
# |1|B|?|?|?|?|
# 
# Save your final DataFrame as `final_member_pivot`.

# In[38]:


final_member_count = df.groupby(['ab_test_group', 'is_member']).first_name.count().reset_index()
final_member_pivot = final_member_count.pivot(columns='is_member',
                                              index='ab_test_group',
                                              values='first_name').reset_index()
final_member_pivot['Total'] = final_member_pivot.Member + final_member_pivot['Not Member']
final_member_pivot['Percent Purchase'] = 100.0 * final_member_pivot.Member / final_member_pivot.Total
final_member_pivot


# Previously, when we only considered people who had **already picked up an application**, we saw that there was no significant difference in membership between Group A and Group B.
# 
# Now, when we consider all people who **visit MuscleHub**, we see that there might be a significant different in memberships between Group A and Group B.  Perform a significance test and check.

# In[39]:


X = [[200, 2304],
     [250, 2250]]
chi2, pval, dof, expected = chi2_contingency(X)
pval


# ## Step 6: Summarize the acquisition funel with a chart

# We'd like to make a bar chart for Janet that shows the difference between Group A (people who were given the fitness test) and Group B (people who were not given the fitness test) at each state of the process:
# - Percent of visitors who apply
# - Percent of applicants who purchase a membership
# - Percent of visitors who purchase a membership
# 
# Create one plot for **each** of the three sets of percentages that you calculated in `app_pivot`, `member_pivot` and `final_member_pivot`.  Each plot should:
# - Label the two bars as `Fitness Test` and `No Fitness Test`
# - Make sure that the y-axis ticks are expressed as percents (i.e., `5%`)
# - Have a title

# In[40]:


# plot the percent of visitors who apply from each group
ax = plt.subplot()
plt.bar(range(len(app_pivot)), app_pivot['Percent with Application'])

plt.title('Percent of Visitors who Apply', fontsize=19)

plt.xlabel('Test Groups', fontsize=16)
ax.set_xticks([0,1])
x_labels = ['Fitness Test', 'No Fitness Test']
ax.set_xticklabels(x_labels, fontsize=16)

plt.ylabel('Percent', fontsize=16)
ax.set_yticks([0, 5, 10, 15, 20])
ax.set_yticklabels(['0%', '5%', '10%', '15%', '20%'])

plt.show()
plt.savefig('percent_visitors_apply_bar.png')


# In[41]:


# plot the percent of applicants who purchase membership from each group
ax = plt.subplot()
plt.bar(range(len(member_pivot)), member_pivot['Percent Purchase'])

plt.title('Percent of Applicants who Purchase Membership', fontsize=19)

plt.xlabel('Test Groups', fontsize=16)
ax.set_xticks(range(len(member_pivot)))
ax.set_xticklabels(x_labels, fontsize=16)

plt.ylabel('Percent', fontsize=16)
ax.set_yticks([0, 20, 40, 60, 80, 100])
ax.set_yticklabels(['0%', '20%', '40%', '60%', '80%', '100%'])

plt.show()
plt.savefig('percent_applicants_purchase_bar.png')


# In[42]:


# plot the percent of visitors who purchase membership from each group
ax = plt.subplot()
plt.bar(range(len(final_member_pivot)), final_member_pivot['Percent Purchase'])

plt.title('Percent of Visitors who Purchase Membership', fontsize=19)

plt.xlabel('Test Groups', fontsize=16)
ax.set_xticks(range(len(final_member_pivot)))
ax.set_xticklabels(x_labels, fontsize=16)

plt.ylabel('Percent', fontsize=16)
ax.set_yticks([0, 5, 10, 15, 20])
ax.set_yticklabels(['0%', '5%', '10%', '15%', '20%'])

plt.show()
plt.savefig('percent_visitors_purchase_bar.png')

