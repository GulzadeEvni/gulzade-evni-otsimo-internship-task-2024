from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from functions import Restaurant
import json

class RequestHandler(BaseHTTPRequestHandler):

    restaurant = Restaurant("menu.json")

    def __init__(self, request, client_address, server):
        self.restaurant = Restaurant("menu.json")
        super().__init__(request, client_address, server)

    def _set_headers(self, status_code=200):
        self.send_response(status_code)
        self.end_headers()

    def _send_error_response(self, message, status_code=400):
        error_response = {
               "error": message
        }
        self.end_headers()
        self.wfile.write(json.dumps(error_response).encode())

    def _send_response(self, message, status_code=200):
        self.send_response(status_code)
        self.end_headers()
        self.wfile.write(json.dumps(message).encode())

    def do_GET(self):
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        if parsed_url.path == '/listMeals':
            self.handle_list_meals(query_params)
        elif parsed_url.path == '/getMeal':
            self.handle_get_meal(query_params)
        elif parsed_url.path == '/search':
            self.handle_search(query_params)
        else:
            self.wfile.write(b'Endpoint not found')

    def handle_list_meals(self, query_params):

        expected_params = ['is_vegetarian', 'is_vegan']
        for param, value in query_params.items():
            if param not in expected_params or value[0].lower() not in ['true', 'false']:
                self._send_error_response(f"Invalid query parameter: {param}={value[0]}")
                return

        is_vegetarian = self.get_query_param_as_bool(query_params, 'is_vegetarian')
        is_vegan = self.get_query_param_as_bool(query_params, 'is_vegan')


        filtered_meals = []

        for meal in self.restaurant.data[0]['meals']:
            ingredients = [ingredient['name'] for ingredient in meal['ingredients']]

            if is_vegan:
                if all(self.is_vegan_ingredient(ingredient) for ingredient in ingredients):
                    filtered_meals.append({
                        'id': meal['id'],
                        'name': meal['name'],
                        'ingredients': ingredients
                    })
            elif is_vegetarian:
                if all(self.is_vegetarian_ingredient(ingredient) for ingredient in ingredients):
                    filtered_meals.append({
                        'id': meal['id'],
                        'name': meal['name'],
                        'ingredients': ingredients
                    })
            else:
                filtered_meals.append({
                    'id': meal['id'],
                    'name': meal['name'],
                    'ingredients': ingredients
                })

        self.wfile.write(json.dumps(filtered_meals).encode())

    def handle_get_meal(self, query_params):
        meal_id = query_params.get('id', [''])[0]

        if meal_id:
            try:
                meal_id = int(meal_id)
            except ValueError:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Invalid meal ID."}).encode())
                return
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Meal ID is required."}).encode())
            return

        
        meal_info = self.restaurant.get_meal_info(meal_id)
        if meal_info:
            self.wfile.write(json.dumps(meal_info).encode())
        else:
            self.send_response(404)
            self.wfile.write(json.dumps({"error": "Meal not found."}).encode())

    def handle_search(self, query_params):
        query = query_params.get('query', [''])[0]

        if query:
            search_results = self.restaurant.search_meals(query.lower())
            self._send_response(search_results)
        else:
            self._send_error_response('Missing query parameter.', 400)




    def get_query_param_as_bool(self, query_params, param_name):
        param_value = query_params.get(param_name, [''])[0].lower()
        return param_value == 'true'

    def is_vegan_ingredient(self, ingredient_name):
        for ingredient in self.restaurant.data[0]['ingredients']:
            if ingredient['name'] == ingredient_name and 'vegan' in ingredient['groups']:
                return True
        return False

    def is_vegetarian_ingredient(self, ingredient_name):
        for ingredient in self.restaurant.data[0]['ingredients']:
            if ingredient['name'] == ingredient_name and ('vegetarian' in ingredient['groups'] or 'vegan' in ingredient['groups']):
                return True
        return False


    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        post_params = parse_qs(post_data, keep_blank_values=True)

        parsed_path = urlparse(self.path)

        meal_id = int(post_params.get('meal_id', [0])[0])
        specified_qualities = {param: value[0] for param, value in post_params.items() if param != 'meal_id'}

        if parsed_path.path == '/quality':
            result = self.restaurant.calculate_quality(meal_id, specified_qualities)
            self._send_response(result)
        elif parsed_path.path == '/price':
            result = self.restaurant.calculate_price(meal_id, specified_qualities)
            self._send_response(result)
        elif parsed_path.path == '/random':
            budget_param = post_params.get('budget', None)
            if budget_param is not None:
                if list(post_params.keys()) == ['budget']:
                    try:
                        budget = float(budget_param[0])
                        if budget <= 0:
                            self._send_response("Budget should be a positive number", status_code=400)
                        else:
                            result = self.restaurant.random_meal(budget)
                            formatted_result = {
                                "id": result['id'],
                                "name": result['name'],
                                "price": result['price'],
                                "quality_score": result['quality_score'],
                                "ingredients": result['ingredients']
                            }
                            self._set_headers()
                            self.wfile.write(json.dumps(formatted_result, indent=2).encode())
                    except ValueError:
                        self._send_response("Invalid budget format. Please provide a valid number", status_code=400)
                else:
                    self._send_response("Only 'budget' parameter is allowed", status_code=400)
            else:
                self._send_response("Budget parameter is missing", status_code=400)
        else:
            self._send_response("Invalid endpoint", status_code=400)

    

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()