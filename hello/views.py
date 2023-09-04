from django.shortcuts import render
import requests

# Create your views here.
from django.http import JsonResponse
from .forms import NutritionForm


def index(request):
    context = {}  # Initialize context
    logged_foods = []  # Initialize an empty list for logged foods
    if request.method == "POST":
        form = NutritionForm(request.POST)
        if form.is_valid():
            serving_size = form.cleaned_data["serving_size"]
            food = form.cleaned_data["food"]

            api_key = "fAWMZKRNMAXfaSVc20I0rw==SqaWeWZOtOXPLc5v"
            base_url = "https://api.calorieninjas.com/v1/nutrition"
            food_item = f"{serving_size} of {food}"

            headers = {"X-Api-Key": api_key}
            url = f"{base_url}?query={food_item}"
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                context = {
                    "form": form,
                    "nutrition_data": data["items"][0],
                    "logged_foods": logged_foods,
                }

                # Retrieve the logged foods from the session or initialize an empty list
                logged_foods = request.session.get("logged_foods", [])

                # Append the new food item to the list of logged foods

                found_food = False
                for foods in logged_foods:
                    if data["items"][0]["name"] == foods:
                        found_food = True
                        break
                    else:
                        found_Food = False
                if found_food == False:
                    logged_foods.append(
                        {
                            "name": data["items"][0]["name"],
                            "calories": data["items"][0]["calories"],
                            "fats": data["items"][0]["fat_total_g"],
                            "proteins": data["items"][0]["protein_g"],
                            "carbs": data["items"][0]["carbohydrates_total_g"],
                            "serving_size": data["items"][0]["serving_size_g"],
                        }
                    )
                # logged_foods.clear()
                total_calories = sum(food["calories"] for food in logged_foods)
                total_fats = sum(food.get("fats", 0) for food in logged_foods)
                total_proteins = sum(food.get("proteins", 0) for food in logged_foods)
                total_carbs = sum(food.get("carbs", 0) for food in logged_foods)
                # Store the updated list of logged foods in the session
                request.session["logged_foods"] = logged_foods
                request.session["total_calories"] = total_calories
                request.session["total_fats"] = total_fats
                request.session["total_proteins"] = total_proteins
                request.session["total_carbs"] = total_carbs

                # Include the list of logged foods in the JSON response
                context["logged_foods"] = logged_foods
                context["total_calories"] = total_calories
                context["total_fats"] = total_fats
                context["total_proteins"] = total_proteins
                context["total_carbs"] = total_fats
            else:
                context = {
                    "form": form,
                    "error_message": "Failed to fetch nutrition data.",
                }

            # Check if it's an AJAX request
            if request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest":
                return JsonResponse(context)  # Return JSON response for AJAX requests
    else:
        form = NutritionForm()
        context = {
            "form": form,
            "logged_foods": request.session.get("logged_foods", []),
        }

    return render(request, "hello/index.html", context)
