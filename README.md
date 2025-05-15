# summative-lab-inventory-management-system
Summative Lab: Python REST API with Flask- Inventory Management System 
By completing this lab, you will:

Introduce advanced state management techniques.
Implement client side routing.
Manipulate data through a simulated backend to maintain persistence.
Test React components and interactions.
Scenario
You have been hired by a small retail company to develop an inventory management system. This system will allow employees to add, edit, view, and delete inventory items. Additionally, the system will fetch real-time product data from an external API (e.g., OpenFoodFacts API) to supplement product details.

You are tasked with creating an administrator portal for an e-commerce website which will include.

A Flask-based REST API with CRUD operations for managing inventory.
An external API integration to fetch product details by barcode or name.
A CLI-based interface to interact with the API.
Unit tests to validate functionality and interactions.
Tools and Resources
Development Tools: A text editor or IDE (e.g., VS Code), browser developer tools, Node.js, and GitHub.
OpenFoodFacts APILinks to an external site.

Instructions

Task 1: Define the Problem
Analyze and plan each necessary route.
Build a user interface to interact with each route.
Build flask endpoints to trigger upon user action.
Connect to OpenFoodFacts api to get specific data from the database.
Update simulated data storage by updating an array.

Task 2: Determine the Design
For each planned route determine the necessary route inputs as well as the output of each route.

Determine what it will change in regards to the data given.
Determine when each route will be triggered within CLI application
Utilizing OpenFoodFacts database, build a mock database in an array.
 The data should resemble what the OpenFoodFacts API may contain: 
{
  "status": 1,
  "product": {
    "product_name": "Organic Almond Milk",
    "brands": "Silk",
    "ingredients_text": "Filtered water, almonds, cane sugar, ..."
    // Additional product information
  }
It is up to you to determine what data you may want to store store, ensure each item in your database array contains an ID.

Task 3: Develop the Code
Step 1: File Setup
Initialize or clone new python project. 
Install necessary python installs like flask.
Use Github. 
Step 2: API Design
Define API endpoints following RESTful conventions:
GET /inventory → Fetch all items
GET /inventory/<id> → Fetch a single item
POST /inventory → Add a new item
PATCH /inventory/<id> → Update an item
DELETE /inventory/<id> → Remove an item
Implement Flask routing and request handling.
Update temporary array to simulate storage.
Step 3: Fetch Data
Use the OpenFoodFacts API to fetch product details.
Implement a function that queries the external API using a barcode or product name.
Enhance stored inventory data with additional details from the API.
Step 4: CLI Frontend
Develop a CLI tool to interact with the API.
Allow users to:
Add new inventory items.
View inventory details.
Update item prices or stock levels.
Delete products.
Find item on api.
Ensure error handling for invalid inputs and API failures.

Task 4: Test and Debug
Write unit tests for:
API endpoints (GET, POST, PATCH, DELETE)
CLI commands
External API interactions
Use pytest and unittest.mock to simulate API responses.
Debug with Flask Debug Mode and Postman for API validation.

Task 5: Document and Maintain
Write a README.md with:
Installation and setup instructions
API endpoint details
Example usage of CLI commands
Ensure clear code comments and maintainability.
Push the project to GitHub with a structured repository.

Submission and Grading Criteria
Review the rubric below as a guide for how this lab will be graded.
Complete your assignment using your preferred IDE.
When you are ready, push your final script to GitHub.
Your GitHub repository should include:
Complete source code.
A README.md file with project details and instructions.
Mock-up references or additional documentation if applicable.
To submit your assignment, share the link to your GitHub repo below. 
