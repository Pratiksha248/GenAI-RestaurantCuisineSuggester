import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from secretkey import google_ai_api_key

os.environ["GOOGLE_API_KEY"] = google_ai_api_key

llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro", temperature=0.8)

# Prompt to return structured text (not JSON)
restaurant_prompt = PromptTemplate(
    input_variables=["cuisine", "diet"],
    template="""
You are a restaurant consultant. Given a cuisine: "{cuisine}" and a diet preference: "{diet}", suggest:

1. A unique and catchy restaurant name.
2. 5 top dishes, each with:
   - Name
   - Ingredients
   - Calories
   - Recipe

Respond only in this format:

Restaurant Name: <your name>

Dishes:
1. Dish Name: ...
   Ingredients: ...
   Calories: ...
   Recipe: ...

2. Dish Name: ...
   ...
"""
)

def generate_restaurant_name_and_items(cuisine: str, diet: str) -> dict:
    prompt = restaurant_prompt.format(cuisine=cuisine, diet=diet)

    try:
        response = llm.invoke(prompt)
        content = response.content if hasattr(response, "content") else str(response)
        lines = content.strip().splitlines()

        # Extract restaurant name
        restro_name = "Name unavailable"
        for line in lines:
            if line.lower().startswith("restaurant name"):
                restro_name = line.split(":", 1)[-1].strip()
                break

        # Extract dishes
        dishes = []
        current_dish = {}
        for line in lines:
            line = line.strip()
            if any(line.startswith(f"{i}.") for i in range(1, 10)) and "Dish Name" in line:
                if current_dish:
                    dishes.append(current_dish)
                current_dish = {"name": line.split(":", 1)[-1].strip()}
            elif "Ingredients" in line:
                current_dish["ingredients"] = line.split(":", 1)[-1].strip()
            elif "Calories" in line:
                current_dish["calories"] = line.split(":", 1)[-1].strip()
            elif "Recipe" in line:
                current_dish["recipe"] = line.split(":", 1)[-1].strip()

        if current_dish:
            dishes.append(current_dish)

        return {
            "restaurant_name": restro_name,
            "structured_dishes": dishes
        }

    except Exception as e:
        return {
            "restaurant_name": "Name unavailable",
            "structured_dishes": [],
            "warning": f"⚠️ Could not extract structured data: {str(e)}"
        }