#!/usr/bin/env python
# coding: utf-8

# In[28]:


import os
os.environ['GOOGLE_API_KEY'] = 'your-google-ai-api-key'

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro", temperature=0.9)

prompt = PromptTemplate.from_template("I want to open an Indian restrobar, suggest me a fancy name for it and a {cuisine} dish.")
# response = llm.invoke(prompt)

chain = prompt | llm

# Run the chain
response = chain.invoke({"restro":"Italian", "cuisine":"Chinese"})

# Print the result
print(response.content)


# In[23]:


import google.generativeai as genai

genai.configure(api_key="your-google-ai-api-key")

models = genai.list_models()

for model in models:
    print(model.name)


# In[ ]:




