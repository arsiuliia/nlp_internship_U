#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import string
import re
import xml.etree.ElementTree as ET


# In[ ]:


df_cat = df[['code', 'UGC_eanPrincipal', 'UGC_libEcommerce','PIM_nomFonctionnel']]
df_cat

#ajouter ean, ids
#UGC_libProduit - à supprimer
#noms foncti
#


# In[ ]:


df_cat['UGC_libEcommerce']=df_cat['UGC_libEcommerce'].apply(str)
df_cat['UGC_eanPrincipal']=df_cat['UGC_eanPrincipal'].apply(str)
df_cat['code']=df_cat['code'].apply(str)


# In[1]:


common_phrases = set()
settings_path='/content/drive/MyDrive/search engine/search-settings.xml'
with open(settings_path, 'r') as f:
    tree = ET.parse(f)
    root = tree.getroot()
    for common_phrase_list in root.iter('{http://www.demandware.com/xml/impex/search2/2010-02-19}common-phrase-list'):
        for common_phrase in common_phrase_list.iter('{http://www.demandware.com/xml/impex/search2/2010-02-19}common-phrases'):
            if common_phrase.attrib.get('match-mode') == 'exact-match':
                common_phrases.add(common_phrase.text.lower())


# In[ ]:


def search_products(search_term, max_results=10):
    matches = df_cat[df_cat.apply(lambda row: row['UGC_libEcommerce'].lower().startswith(search_term.lower())
    and not any(phrase in row['UGC_libEcommerce'].lower() for phrase in common_phrases), axis=1)]
    matches['sort_key'] = matches['PIM_nomFonctionnel'].apply(lambda val: 0 if pd.isna(val) else 1)
    matches = matches.sort_values(by='sort_key', ascending=False).head(max_results)
    results = matches.to_dict('records')
       return results


# In[ ]:


search_term = input("🔎: ")


# In[ ]:


results = search_products(search_term, max_results=10)


# In[ ]:


for result in results:
    print(f"{result['UGC_libEcommerce']} - [{result['UGC_eanPrincipal']}]")

