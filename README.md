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
    GET /listMeals?is_vegetarian=true
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
    curl -d "meal_id=1&rice=low" -X POST http://localhost:8080/quality
    ```
- /price: Calculates the price of a specific meal based on ingredient qualities.
  - Example:
    ```shell
    curl -d "meal_id=1&rice=low" -X POST http://localhost:8080/price
    ```
- /random: Retrieves a random meal within a specified budget.
  - Example:
    ```shell
    curl -d "budget=3.3" -X POST http://localhost:8080/random
    ```

## Function Descriptions
## functions.py

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

- ### calculate_quality_for_random: Calculates the overall quality of a specific meal based on ingredient qualities.
  - Parameters:
    - meal_id (int): The ID of the meal.
    - ingredient_qualities (dict, optional): A dictionary of ingredient qualities.
  - Returns:
    - A tuple containing the overall quality score and a list of ingredients with their respective qualities.

- ### calculate_price_for_random: Calculates the total price of a specific meal based on ingredient qualities.
  - Parameters:
    - meal_id (int): The ID of the meal.
    - ingredient_qualities (dict, optional): A dictionary of ingredient qualities.
  - Returns:
    - A tuple containing the total price and a list of ingredients with their respective qualities.

- ### random_meal: Retrieves a random meal within a specified budget.
  - Parameters:
    - budget (float): The budget for the meal (default is infinity).
  - Returns:
    - A dictionary containing the selected meal's details, including price and quality score.

- ### find_affordable_meal: Finds an affordable meal within a specified budget.
  - Parameters:
    - budget (float): The budget for the meal.
  - Returns:
    - The affordable meal details if found, otherwise None.

- ### _get_meal_by_id: Retrieves a meal by its ID.
  - Parameters:
    - meal_id (int): The ID of the meal.
  - Returns:
    - The meal data if found, otherwise None.
   
- ### _get_quality_score: Converts a quality level to a numerical score.
  - Parameters:
    - quality (str): The quality level ('high', 'medium', 'low').
  - Returns:
    - The numerical score corresponding to the quality level.

- ### _get_price: Retrieves the price per unit of an ingredient based on its quality.
  - Parameters:
    - quality (str): The quality level ('high', 'medium', 'low').
    - ingredient_name (str): The name of the ingredient.
  - Returns:
    - The price per unit for the specified ingredient and quality, or None if not found.

- ### calculate_quality: Calculates the overall quality of a specific meal based on ingredient qualities.
  - Parameters:
    - meal_id (int): The ID of the meal.
    - ingredient_qualities (dict, optional): A dictionary of ingredient qualities.
  - Returns:
    - The overall quality score of the meal.

- ### calculate_price: Calculates the total price of a specific meal based on ingredient qualities.
  - Parameters:
    - meal_id (int): The ID of the meal.
    - ingredient_qualities (dict, optional): A dictionary of ingredient qualities.
  - Returns:
    - The total price of the meal.
   

- ### search_meals: Searches for meals based on a query string.
  - Parameters:
    - query (str): The search query.
  - Returns:
    - A list of meals that match the query string.
### http_server.py

- ### _set_headers: Sets the HTTP response headers.
  - Parameters:
    - status_code (int): The HTTP status code to send (default is 200).
  - Behavior:
    - Sends the response status code and ends the headers.

- ### _send_error_response: Sends an error response.
  - Parameters:
    - message (str): The error message to send.
    - status_code (int): The HTTP status code to send (default is 400).
  - Behavior:
    - Sends an error message with the specified status code.
   
- ### _send_response: Sends a JSON response.
  - Parameters:
    - message (dict): The message to send.
    - status_code (int): The HTTP status code to send (default is 200).
  - Behavior:
    - Sends the specified message with the status code as a JSON-encoded response.

- ### do_GET: Handles GET requests.
  - Behavior:
    - Parses the request URL and query parameters, and routes the request to the appropriate handler (handle_list_meals, handle_get_meal, or handle_search). If the endpoint is not found, sends a "Endpoint not found" message.

- ### handle_list_meals: Handles requests to list meals based on dietary preferences.
  - Parameters:
    - query_params (dict): The query parameters from the request URL.
  - Behavior:
    - Filters meals based on is_vegetarian and is_vegan query parameters and sends the list of filtered meals as a JSON response. Sends an error response if query parameters are invalid.
   
- ### handle_get_meal: Handles requests to get information about a specific meal.
  - Parameters:
    - query_params (dict): The query parameters from the request URL.
  - Behavior:
    -  Retrieves the meal information based on the id query parameter and sends it as a JSON response. Sends an error response if the meal ID is invalid or not provided, or if the meal is not found.
   
- ### handle_search: Handles requests to search for meals based on a query string.
  - Parameters:
    - query_params (dict): The query parameters from the request URL.
  - Behavior:
    - Searches for meals that match the query string and sends the results as a JSON response. Sends an error response if the query parameter is missing.
   
- ### get_query_param_as_bool: Converts a query parameter to a boolean value.
  - Parameters:
    - query_params (dict): The query parameters from the request URL.
    - param_name (str): The name of the query parameter to convert.
  - Returns:
    - The boolean value of the specified query parameter.
  - Behavior:
    - Converts the query parameter value to lowercase and checks if it is "true".
   
- ### is_vegan_ingredient: Checks if an ingredient is vegan.
  - Parameters:
    - ingredient_name (str): The name of the ingredient.
  - Returns:
    - True if the ingredient is vegan, otherwise False.
  - Behavior:
    - Checks if the ingredient is in the vegan group in the restaurant data.
   
- ### is_vegetarian_ingredient: Checks if an ingredient is vegetarian.
  - Parameters:
    -ingredient_name (str): The name of the ingredient.
  - Returns:
    - True if the ingredient is vegetarian or vegan, otherwise False.
  - Behavior:
    - Checks if the ingredient is in the vegetarian or vegan group in the restaurant data.
   
- ### do_POST: Handles POST requests.
  - Behavior:
    - Parses the request body and routes the request to the appropriate handler based on the request path (/quality, /price, or /random). Sends error responses for invalid or missing parameters.
   
- ### run: Starts the HTTP server.
  - Parameters
    - server_class (class): The HTTP server class (default is HTTPServer).
    - handler_class (class): The request handler class (default is RequestHandler).
    - port (int): The port number to run the server on (default is 8080).
  - Behavior:
    - Initializes and starts the HTTP server, printing a message to indicate that the server has started.

## Example Usage

### For price endpoint

![fiyat](https://github.com/GulzadeEvni/gulzade-evni-otsimo-internship-task-2024/assets/111283320/54a867ef-8c9c-44a4-a231-a101b73a2bab)

### For quality endpoint

![kalite](https://github.com/GulzadeEvni/gulzade-evni-otsimo-internship-task-2024/assets/111283320/151e5357-091c-47a2-8378-445b378e7ad5)

### For random endpoint

![random](https://github.com/GulzadeEvni/gulzade-evni-otsimo-internship-task-2024/assets/111283320/92106732-880a-43b7-a10e-23bd4cff0aad)

### Incorrect use of listMeals

![list_hatalı](https://github.com/GulzadeEvni/gulzade-evni-otsimo-internship-task-2024/assets/111283320/6451f106-4eaf-4e53-aa6a-2b470bb16064)

### Incorrect use of getMeal

![get_hatalı](https://github.com/GulzadeEvni/gulzade-evni-otsimo-internship-task-2024/assets/111283320/2e2e3a3b-bd99-43a2-a37a-bc4f4ddf522e)

