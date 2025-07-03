AI Powered Pro Travel Planner

Plan your perfect trip, personalized by AI. This project is an AI-powered travel planner built with Streamlit. When a user enters their desired city and date, it generates a custom, expert-level travel itinerary.

* Key Features
  
Expert-Level AI Itineraries: An AI with the persona of a "Senior Travel Columnist for Lonely Planet" generates unique itineraries that go beyond simple place-listing to include hidden tips and storytelling.

Multi-language Support: Supports English, Korean and Japanese. The UI text and the generated travel plan are all provided in the user's selected language.

Date-Based Weather Tips: Provides historical weather averages and appropriate packing tips (e.g., bring an umbrella, heavy coat) based on the user's selected travel month.

Real-World Imagery: Integrates with the Unsplash API to display high-quality, real photos of the destination, adding to the travel excitement (Optional).

Interactive Map Links: Every location mentioned in the generated plan includes a link to view its exact location on Google Maps.

* Tech Stack
  
Framework: Streamlit

Language: Python

APIs: OpenAI API, Unsplash API

Core Libraries: requests, re

* Getting Started
  
1. Clone the Repository
   
Bash

git clone https://github.com/your-username/your-repository-name.git
cd your-repository-name

2. Create and Activate a Virtual Environment
   
Using a virtual environment is highly recommended to manage project dependencies independently.

Bash

# Create the environment
python -m venv venv

# On Windows
.\venv\Scripts\activate

# On macOS / Linux
source venv/bin/activate

3. Install Dependencies
   
Create a requirements.txt file in the project's root directory with the following content:

requirements.txt

streamlit
openai
requests

Then, run the following command in your terminal to install the necessary libraries:

Bash

pip install -r requirements.txt

4. Configure API Keys
   
This application uses two external APIs. You will need to enter the keys in the sidebar after launching the app.

OpenAI API Key (Required): Needed to generate travel plans using the AI model. Get your key here.

Unsplash Access Key (Optional): Needed to display real-world photos of the destination. The app will still function without it. Get your key here.

Please be assured that the keys you enter are not stored or transmitted anywhere. They are only held in memory for the duration of your session.

5. Run the Application
   
Enter the following command in your terminal to launch the Streamlit app:

Bash

streamlit run main.py

(If your Python script has a different name, replace main.py accordingly.)
