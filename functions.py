import json
import random
import logging

logging.basicConfig(filename='restaurant.log', level=logging.INFO)

class Restaurant:

    def __init__(self, data_file):
        try:
            with open(data_file, 'r') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            logging.error(f"Error: File '{data_file}' not found.")
            raise
        except json.JSONDecodeError:
            logging.error(f"Error: '{data_file}' is not a valid JSON file.")
            raise

    def load_menu(self, menu_file):
        with open(menu_file, 'r') as file:
            menu_data = json.load(file)
        return menu_data[0]

    def list_meals(self, is_vegetarian=False, is_vegan=False):
        meals = self.data.get("meals", [])
        filtered_meals = []
        for meal in meals:
            if (not is_vegetarian or self.is_meal_vegetarian(meal)) and \
               (not is_vegan or self.is_meal_vegan(meal)):
                filtered_meals.append({
                    "id": meal["id"],
                    "name": meal["name"],
                    "ingredients": [ingredient["name"] for ingredient in meal["ingredients"]]
                })
        return filtered_meals

    def get_meal(self, meal_id):
            meals = self.data[0].get("meals", [])
            for meal in meals:
                if meal["id"] == meal_id:
                    return meal
            return None
        
    def get_meal_info(self, meal_id):
        meal = self.get_meal(meal_id)
        if meal:
            ingredients_info = []
            for ingredient in meal["ingredients"]:
                ingredient_info = {
                    "name": ingredient["name"],
                    "groups": [],
                    "options": []
                }
                for item in self.data[0]["ingredients"]:
                    if item["name"] == ingredient["name"]:
                        ingredient_info["groups"] = item["groups"]
                        ingredient_info["options"] = item["options"]
                        break
                ingredients_info.append(ingredient_info)

            return {
                "id": meal["id"],
                "name": meal["name"],
                "ingredients": ingredients_info
            }
        else:
            return None
    
    def is_meal_vegetarian(self, meal):
        for ingredient in meal["ingredients"]:
            if "vegetarian" not in ingredient["groups"]:
                return False
        return True

    def is_meal_vegan(self, meal):
        for ingredient in meal["ingredients"]:
            if "vegan" not in ingredient["groups"]:
                return False
        return True

    def calculate_quality_for_random(self, meal_id, ingredient_qualities=None):
        meal = self._get_meal_by_id(meal_id)
        if not meal:
            return "Meal not found"
        
        ingredient_scores = []
        ingredients = []
        for ingredient in meal['ingredients']:
            ingredient_quality = ingredient_qualities.get(ingredient['name'], 'high') if ingredient_qualities else 'high'
            score = self._get_quality_score(ingredient_quality)
            ingredient_scores.append(score)
            ingredients.append({"name": ingredient['name'], "quality": ingredient_quality})
        
        overall_quality = sum(ingredient_scores) / len(ingredient_scores)
        return overall_quality, ingredients

    def calculate_price_for_random(self, meal_id, ingredient_qualities=None):
        meal = self._get_meal_by_id(meal_id)
        if not meal:
            return "Meal not found"
        
        total_price = 0
        ingredients = []
        for ingredient in meal['ingredients']:
            ingredient_quality = ingredient_qualities.get(ingredient['name'], 'high') if ingredient_qualities else 'high'
            price_per_unit = self._get_price(ingredient_quality, ingredient['name'])
            if price_per_unit is None:
                price_per_unit = 0
            quantity = ingredient.get('quantity', 0)
            total_price += (quantity * price_per_unit)
            ingredients.append({"name": ingredient['name'], "quality": ingredient_quality})
        
        if ingredient_qualities:
            for ingredient_name, quality in ingredient_qualities.items():
                if quality == 'medium':
                    total_price += 0.05
                elif quality == 'low':
                    total_price += 0.10
        
        return total_price, ingredients

    def random_meal(self, budget=float('inf')):
        selected_meal = random.choice(self.data[0]['meals'])
        ingredient_qualities = {ingredient['name']: random.choice(['high', 'medium', 'low']) for ingredient in selected_meal['ingredients']}
        price, _ = self.calculate_price_for_random(selected_meal['id'], ingredient_qualities)
        quality, ingredients_quality = self.calculate_quality_for_random(selected_meal['id'], ingredient_qualities)
        
        if price > budget:
            selected_meal['price'] = budget
        else:
            selected_meal['price'] = price
        
        selected_meal['quality_score'] = quality
        selected_meal['ingredients'] = ingredients_quality
        return selected_meal
    
    def find_affordable_meal(self, budget):
        affordable_meal = None
        
        for meal_group in self.data:
            for meal in meal_group['meals']:
                ingredient_qualities = {ingredient['name']: random.choice(['high', 'medium', 'low']) for ingredient in meal['ingredients']}
                price, ingredients_quality = self.calculate_price_for_random(meal['id'], ingredient_qualities)
                if price <= budget:
                    quality, _ = self.calculate_quality_for_random(meal['id'], ingredient_qualities)
                    
                    return affordable_meal 
                
        return affordable_meal

    
    def _get_meal_by_id(self, meal_id):
        for meal_group in self.data:
            for meal in meal_group['meals']:
                if meal['id'] == meal_id:
                    return meal
        return None
    

    def get_meal(self, meal_id):
            meals = self.data[0].get("meals", [])
            for meal in meals:
                if meal["id"] == meal_id:
                    return meal
            return None

    def _get_quality_score(self, quality):
        if quality == 'high':
            return 30
        elif quality == 'medium':
            return 20
        elif quality == 'low':
            return 10

    def _get_price(self, quality, ingredient_name):
        for ingredient in self.data[0]['ingredients']:
            if ingredient['name'] == ingredient_name:
                for option in ingredient['options']:
                    if option['quality'] == quality:
                        return option['price'] / 1000
        return None

    def calculate_quality(self, meal_id, ingredient_qualities=None):
        meal = self._get_meal_by_id(meal_id)
        if not meal:
            return "Meal not found"
        
        total_quality_score = 0
        total_ingredients = 0
        for ingredient in meal['ingredients']:
            total_ingredients += 1
            ingredient_name = ingredient['name'].lower() 
            ingredient_quality = ingredient_qualities.get(ingredient_name, 'high') if ingredient_qualities else 'high'
            score = self._get_quality_score(ingredient_quality)
            total_quality_score += score
        
        if total_ingredients == 0:
            return "No ingredients found for this meal"
        
        overall_quality = total_quality_score / total_ingredients
        return overall_quality
    

    def calculate_price(self, meal_id, ingredient_qualities=None):
        meal = self._get_meal_by_id(meal_id)
        if not meal:
            return "Meal not found"
        
        total_price = 0
        for ingredient in meal['ingredients']:
            ingredient_quality = ingredient_qualities.get(ingredient['name'].lower(), 'high') if ingredient_qualities else 'high'
            price_per_unit = self._get_price(ingredient_quality, ingredient['name'])
            quantity = ingredient['quantity']
            total_price += (quantity * price_per_unit)
        
        
        if ingredient_qualities:
            for ingredient_name, quality in ingredient_qualities.items():
                if quality == 'medium':
                    total_price += 0.05
                elif quality == 'low':
                    total_price += 0.10
        
        return total_price
        
    def search_meals(self, query):
        results = []
        for meal in self.data[0]['meals']:
            if query.lower() in meal['name'].lower():
                results.append({
                    "id": meal['id'],
                    "name": meal['name'],
                    "ingredients": [ingredient['name'] for ingredient in meal['ingredients']]
                })
        return results