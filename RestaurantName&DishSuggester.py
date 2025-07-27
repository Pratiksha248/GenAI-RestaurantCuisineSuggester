#!/usr/bin/env python
# coding: utf-8

# In[23]:


import google.generativeai as genai

genai.configure(api_key="your-google-ai-api-key")

models = genai.list_models()

for model in models:
    print(model.name)


# In[12]:


import os
os.environ['GOOGLE_API_KEY'] = 'your-google-ai-api-key'

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro", temperature=0.8)

prompt = PromptTemplate.from_template("I want to open an {restro} restrobar, suggest me a fancy name for it and a {cuisine} dish.")
# response = llm.invoke(prompt)

chain = prompt | llm

# Run the chain
response = chain.invoke({"restro":"Arabic", "cuisine":"Chinese"})

# Print the result
print(response.content)


# In[5]:


import os
os.environ['GOOGLE_API_KEY'] = 'your-google-ai-api-key'

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda, RunnableMap

llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro", temperature=0.8)

# 1) Generate restrobar name
prompt_name = PromptTemplate.from_template("Suggest a fancy {cuisine} restrobar name.")
name_chain = prompt_name | llm

# 2) Function to generate dietary-based prompt
def make_diet_prompt(inputs):
    cuisine = inputs["cuisine"]
    diet = inputs["diet"]
    restro = inputs["restro_name"]
    
    if diet == "vegan":
        prompt_text = f"Suggest 5 best-selling vegan {cuisine} dishes for the restrobar named {restro}."
    elif diet == "non-vegan":
        prompt_text = f"Suggest 5 best-selling non-vegan {cuisine} dishes for the restrobar named {restro}."
    else:
        prompt_text = f"Suggest 5 best-selling {cuisine} dishes for the restrobar named {restro} that suit both vegan and non-vegan preferences."
    
    return {"prompt": prompt_text}

diet_router = RunnableLambda(make_diet_prompt)
prompt_dishes = PromptTemplate.from_template("{prompt}")
dishes_chain = diet_router | prompt_dishes | llm

# Full pipeline using RunnableLambda instead of RunnableMap
full_chain = (
    RunnableLambda(lambda x: {"cuisine": x["cuisine"], "diet": x["diet"]})
    | RunnableLambda(lambda x: {
        "cuisine": x["cuisine"],
        "diet": x["diet"],
        "restro_name": name_chain.invoke({"cuisine": x["cuisine"]}).content
    })
    | RunnableLambda(lambda x: {
        "restro_name": x["restro_name"],
        "dishes": dishes_chain.invoke({
            "restro_name": x["restro_name"],
            "cuisine": x["cuisine"],
            "diet": x["diet"]
        }).content
    })
)

# Run the chain
input_data = {"cuisine": "Indian", "diet": "vegan"}
result = full_chain.invoke(input_data)

# Output
print("Restaurant name: ", result["restro_name"])
print("\nDiet-based dishes: \n", result["dishes"])


# In[ ]:




