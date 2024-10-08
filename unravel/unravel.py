# -*- coding: utf-8 -*-

# **Required Modules**
"""

import requests as r
import json 
import pandas as pd
import numpy as np

"""# **UNRAVEL PACK**

"""
########################################
##### Verify if the object is a dict ### V1.0
########################################

def is_dict(mydic):
  if type(mydic)==dict:
    return True
  else:
    return False

########################################
####  Verify if the object is a list ### V1.0
########################################

def is_list(mylist):
  if type(mylist)==list:
    return True
  else:
    return False


########################################
## Return the first dict in a column ### v1.1
########################################

def first_dict(column):

  column=column[contains_dict(column)]
  
  return column.iloc[0]

########################################
## Return the first list in a column ### v1.1
########################################

def first_list(column):

  column=column[contains_list(column)]
  
  return column.iloc[0]

########################################
##### Verify if exists in both list #### v1.1
########################################

def it_contains(list1,list2):

  if any((match := item) in list1 for item in list2):
    return True

  else:
    return False

########################################
######### Restructure a DataFrame ###### V1.1
########################################

def dataframe_res(Df1,location,Df2):
    
    Df=Df1.copy()
    Df2_names=Df2.columns.tolist()
    for i in Df2_names:
      Df.insert(loc=location, column=i,value=Df2[i])
      location+=1
    
    return Df


########################################
# Verify if a columns contains a dict #  V1.0
########################################

def contains_dict(interest_column):

  boolean_list=[]

  for i in range(len(interest_column)):

    if is_dict(interest_column[i]):
      boolean_list.append(True)
    else:
      boolean_list.append(False)

  return boolean_list

########################################
## Verify if a columns contains a list #  V1.0
########################################

def contains_list(interest_column):

  boolean_list=[]

  for i in range(len(interest_column)):

    if is_list(interest_column[i]):
      boolean_list.append(True)
    else:
      boolean_list.append(False)

  return boolean_list

########################################
######### Dict to Columns   ############ V1.0
########################################

def expand(chosen_column,prefix):

    f_dict=first_dict(chosen_column)
    dictionaries = []
    
    len_dict=len(f_dict)
    empty_dict=dict(zip(f_dict.keys(), [np.nan]*len_dict))


    for i in chosen_column:

        if pd.isnull(i)==True:
            i=empty_dict
        elif i:
            new_dict = {**i}
            dictionaries.append(new_dict)

            Df=pd.DataFrame(dictionaries)
            Df_names=Df.columns.tolist()

    for i in Df_names:  
      Df.rename(columns={i:prefix+'_'+i}, inplace=True)

    return Df

########################################
######### Dict to Columns nokey ######## V1.0
########################################

def expand_noKey(chosen_column):
    
    f_dict=first_dict(chosen_column)
    dictionaries = []

    len_dict=len(f_dict)
    empty_dict=dict(zip(f_dict.keys(), [np.nan]*len_dict))


    for i in chosen_column:

        if pd.isnull(i)==True:
            i=empty_dict
        elif i:
            new_dict = {**i}
            dictionaries.append(new_dict)

            Df=pd.DataFrame(dictionaries)
            Df_names=Df.columns.tolist()

    return Df

########################################
##      Return structed columns       ##  V1.0
########################################

def st_df(Df):

 structure_columns_names=[]
 columns_names= Df.columns.tolist()

 for i in columns_names:

    if True in (contains_dict(Df[i]) or contains_list(Df[i])):
      structure_columns_names.append(i)
  
 return structure_columns_names

########################################
#########  All the columns   ########### v1.1
########################################

def unravel(Df,inplace=False): 

  if inplace==False:
       Df=Df.copy()  
  expand_names=st_df(Df)
  if it_contains(expand_names,Df.columns.tolist())==True:
       for i in expand_names:

         df_aux=expand(Df[i],i)   

         position_insert=Df.columns.get_loc(i)
         Df=dataframe_res(Df,position_insert+1,df_aux)
         Df.drop(i, inplace=True, axis=1)

         unravel(Df)
  else:
         return Df
