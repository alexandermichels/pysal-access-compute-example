#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import geopandas as gpd
from access import Access, weights, Datasets
import os


# In[2]:

RESULTS_FOLDER = os.getenv('result_folder')
print(f"The results folder is: {RESULTS_FOLDER}")

print("Hit the beginning of ChicagoAccess.py")
# Datasets.available_datasets()


# In[3]:


chicago_pop = Datasets.load_data("chi_pop")


# In[4]:


chi_doc = Datasets.load_data("chi_doc_geom")


# In[5]:


chi_times = Datasets.load_data('chi_times')
print("All data loaded successfully")

# In[6]:


A = Access(demand_df            = chicago_pop,
           demand_index         = 'geoid',
           demand_value         = 'pop',
           supply_df            = chi_doc,
           supply_index         = 'geoid',
           supply_value         = 'doc',
           cost_df              = chi_times,
           cost_origin          = 'origin',
           cost_dest            = 'dest',
           cost_name            = 'cost',
           neighbor_cost_df     = chi_times,
           neighbor_cost_origin = 'origin',
           neighbor_cost_dest   = 'dest',
           neighbor_cost_name   = 'cost')
print("Access object created")

# In[7]:


fn30 = weights.step_fn({10 : 1, 20 : 0.68, 30 : 0.22})
fn60 = weights.step_fn({20 : 1, 40 : 0.68, 60 : 0.22})
gaussian = weights.gaussian(20)
gravity = weights.gravity(scale = 60, alpha = -1)

# In[8]:

print("Beginning Accessibility calculations")
A.weighted_catchment    (name = "gravity",  weight_fn = gravity)
A.fca_ratio             (name = "fca",      max_cost = 15)
A.fca_ratio             (name = "fca",      max_cost = 30) # Note - the warning -- good!
A.fca_ratio             (name = "fca60",    max_cost = 60)
A.fca_ratio             (name = "fca90",    max_cost = 90)
A.two_stage_fca         (name = "2sfca",    max_cost = 60)
A.enhanced_two_stage_fca(name = "2sfca30",  weight_fn = fn30)
A.enhanced_two_stage_fca(name = "2sfca60",  weight_fn = fn60)
A.enhanced_two_stage_fca(name = "g2sfca",   weight_fn = gaussian)
A.three_stage_fca       (name = "3sfca")
A.raam(name = "raam", tau = 60)
A.raam(name = "raam30", tau = 30)
print("Accessibility calculations finished")

# In[9]:


A.access_df.head()


# In[10]:


A.access_df.to_csv(os.path.join(RESULTS_FOLDER, "access_result.csv"))
print("Saved result to access_result.csv")


# In[ ]:




