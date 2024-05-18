# gulzade-evni-otsimo-internship-task-2024

## Installation
1. Clone the repository:
```shell
git clone https://github.com/GulzadeEvni/gulzade-evni-otsimo-internship-task-2024.git
```
2. Navigate to the project directory:
```shell
cd gulzade-evni-otsimo-internship-task-2024
```
3. After downloading the project files to your local environment, start the API server by running the following command:
```shell
python3 http_server.py
```
Once the server is started, you can send HTTP requests to the API.

## Usage
### Available Endpoints  

GET Endpoints

- /listMeals:
  - Query Parameters:
    - is_vegetarian (boolean): Filter for vegetarian meals.
    - is_vegan (boolean): Filter for vegan meals.
  - Example:
    ```shell
    GET /listMeals?is_vegetarian=true&is_vegan=false
    ```
- /getMeal: Retrieves information about a specific meal.
  - Query Parameters:
    - id (integer): The ID of the meal.
  - Example:
    ```shell
    GET /getMeal?id=1
    ```
- /search: Searches for meals based on a query string.
  - Query Parameters:
    - query (string): The search query.
  - Example:
    ```shell
    GET /search?query=pasta
    ```
POST Endpoints

- /quality: Calculates the quality of a specific meal based on ingredient qualities.
  - Example:
    ```shell
    curl -d "meal_id=1&garlic=low" -X POST http://localhost:8080/quality
    ```
- /price: Calculates the price of a specific meal based on ingredient qualities.
  - Example:
    ```shell
    curl -d "meal_id=1&garlic=low" -X POST http://localhost:8080/price
    ```
- /random: Retrieves a random meal within a specified budget.
  - Example:
    ```shell
    curl -d "budget=3.3" -X POST http://localhost:8080/random
    ```

## Function Descriptions

- ### load_menu: Loads menu data from a specified JSON file.
  - Parameters:
    - menu_file (str) -> The path to the JSON file containing menu data.
  - Returns:
    - The first item in the loaded menu data.

- ### list_meals: Lists meals based on specified dietary preferences.
  - Parameters:
    - is_vegetarian (bool): Filter for vegetarian meals (default is False).
    - is_vegan (bool): Filter for vegan meals (default is False).
  - Returns:
    - A list of meals that match the specified dietary preferences.

- ### get_meal: Retrieves information about a specific meal.
  - Parameters:
    - meal_id (int): The ID of the meal.
  - Returns:
    - The meal information if found, otherwise None.
   
- ### get_meal_info:  Retrieves detailed information about a specific meal, including ingredients.
  - Parameters:
    - meal_id (int): The ID of the meal.
  - Returns:
    - A dictionary containing the meal's ID, name, and detailed ingredients information.

- ### is_meal_vegetarian: Checks if a meal is vegetarian.
  - Parameters:
    - meal (dict): The meal data.
  - Returns:
    - True if the meal is vegetarian, otherwise False.
   
- ### is_meal_vegan: Checks if a meal is vegan.
  - Parameters:
    - meal (dict): The meal data.
  - Returns:
    - True if the meal is vegan, otherwise False.
