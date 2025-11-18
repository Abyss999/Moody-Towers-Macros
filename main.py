from imports import *

today = date.today()
menuType = ["breakfast", "lunch", "dinner"]
menu = "dinner"
foodMaps = []

# filters 
search = ["all", "P", "V", "VG", "CF"]
# all = all items
# P = PR - Good Source of Protein
# V = Vegetarian
# VG = Vegan
# CF = Climate Friendly

# min-w-full = station tables 

# View nutritional information for [Stir Fry Vegetables]

nutNameMap = {
    "Protein (g)": "protein",
    "Total Carbohydrates (g)": "carbs",
    "Total Fat (g)": "fats",
    "Calories": "calories",
    "Sugar (g)": "sugar",
    "Serving Size": "serving_size",
}

def run(playwright: Playwright):
    chromium = playwright.chromium
    browser = chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(f"https://new.dineoncampus.com/uh/whats-on-the-menu/moody-towers-dining-commons/{today}/dinner")

    page.wait_for_selector(".min-w-full") # wait for each station to load 

    # foods  = page.query_selector_all(".text-lg.font-semibold.pl-2") # text-lg font-semibold pl-2
    foods = page.query_selector_all(".max-w-0.py-5.pl-4.pr-3")
    print(f"Found {len(foods)} foods")

    for count, food in enumerate(foods):
        text_split = food.inner_text().split("\n")
        text = text_split[0] if len(text_split) > 0 else "N/A"
        description = text_split[1] if len(text_split) > 1 else "N/A"
        # scroll if needed 
        food.scroll_into_view_if_needed()
        # click the food 
        food.click()
        # wait for popup 
        page.wait_for_selector("span.font-bold:has-text('Protein (g)')") # <span class="font-bold">Protein (g)</span>
        # nutrition = page.query_selector_all("span.font-bold")
        serving = page.query_selector(".text-sm.font-bold.border-b")
        nutrition = page.query_selector_all(".flex.justify-between.py-1")

        nutritionMap = {}

        serving_split = serving.inner_text().split(": ")
        nutritionMap["serving_size"] = serving_split[1] if len(serving_split) > 1 else "N/A"

        for i in range(len(nutrition) - 1):
            key = nutrition[i].inner_text()
            arr = key.split("\n") # key : value // ex. protein : 10
            if arr[0] in nutNameMap.keys():
                nutritionMap[nutNameMap[arr[0]]] = handleNutritionMap(arr[1])
            else:
                nutritionMap[arr[0]] = handleNutritionMap(arr[1])

        protein = nutritionMap.get("protein", "N/A")
        carbs = nutritionMap.get("carbs", "N/A")
        fats = nutritionMap.get("fats", "N/A")
        calories = nutritionMap.get("calories", "N/A")
        sugar = nutritionMap.get("sugar", "N/A")
        serving_size = nutritionMap.get("serving_size", "N/A")
        description = nutritionMap.get("description", "N/A")

        print(f"Food {count + 1}: {text}")

        close_button = page.query_selector(".svg-inline--fa.fa-xmark")
        close_button.click()
        # page.wait_for_timeout(50) # wait for popup to close


        foodMaps.append({
            "name": text,
            "description": description,
            "serving_size": serving_size,
            "calories": int(calories) if calories.isnumeric() else 0,
            "protein": int(protein) if protein.isnumeric() else 0,
            "carbs": int(carbs) if carbs.isnumeric() else 0,
            "fats": int(fats) if fats.isnumeric() else 0,
            "sugar": int(sugar) if sugar.isnumeric() else 0,
        })

    print("Final Food Maps:")

    sortArr = sorted(foodMaps, key=lambda x: x["protein"], reverse=False)
    for foodMap in sortArr:
        print(foodMap)



def handleNutritionMap(nutritionAmount):
    if nutritionAmount.endswith("g"):
        return nutritionAmount[:-2]
    if nutritionAmount.endswith("kcal"):
        return nutritionAmount[:-5]
    return nutritionAmount

__init__ = "__main__"
if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)