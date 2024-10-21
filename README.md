Weather Monitoring System
This weather monitoring system collects real-time weather data from the OpenWeatherMap API for several Indian cities. It stores the data in an SQLite database, generates daily rollups of average, maximum, and minimum temperatures, and visualizes the data in separate graphs for each city. The system also sends email alerts when the temperature exceeds a specified threshold.

                                            Running the Application

Simulate Weather Data: The application simulates weather data for 7 days. To begin the simulation:
Code
python weather_monitor.py
View Graphs: After simulation, the application will generate and display visual graphs showing the weather summary (temperature, humidity, wind speed) for each city over the simulation period.

Simulating Weather Updates

The simulate_weather_updates() function generates mock weather data for multiple cities and stores it in an SQLite database. The process includes:
Randomly generating weather parameters such as temperature, humidity, and wind speed.
Storing the generated data in the database.
Rolling up daily summaries for each city.
Example:
Python Code
simulate_weather_updates()

Features
Real-time Weather Data: Fetches current weather data (temperature, "feels like" temperature, weather conditions) for multiple cities.
Temperature Conversion: Converts temperatures from Kelvin to Celsius.
Data Persistence: Stores fetched weather data in an SQLite database.
Daily Rollup: Computes daily average, maximum, and minimum temperatures, along with the most dominant weather condition.
Threshold Alerts: Sends email alerts when a city’s temperature exceeds a set threshold.
Graph Visualization: Displays temperature data for each city in separate graphs.
Prerequisites
Before you start, ensure you have:

Python 3.6 or later installed
An OpenWeatherMap API key
Required Python packages (requests, sqlite3, matplotlib, smtplib)
Installation
Clone the repository:

Code
git clone https://github.com/yourusername/weather-monitoring-system.git
cd weather-monitoring-system
Install required Python libraries:

bash
Copy code
pip install requests matplotlib
Set up environment variables for the OpenWeatherMap API key and email credentials in a .env file (optional for security):

Code

OPENWEATHER_API_KEY="your_openweathermap_api_key"
SENDER_EMAIL="your_email@example.com"
SENDER_PASSWORD="your_email_password"

Configuration

API_KEY: OpenWeatherMap API key. Replace 'your_api_key_here' in the code.
CITIES: List of cities to monitor.
INTERVAL: Time interval (in seconds) between data fetches (default is 300 seconds).
THRESHOLD_TEMP: Temperature threshold for sending alerts (default is 35°C).
You can modify these in the script to suit your needs.

                                                 How to Run

Open the terminal and navigate to the project directory.

Run the script:

Code

python weather_monitoring.py

The system will fetch weather data at regular intervals, store it in the SQLite database (weather.db), check for temperature thresholds, and visualize data in separate graphs for each city.

To stop the system, press Ctrl + C in the terminal.

Email Alerts
The system sends email alerts if the temperature exceeds the defined threshold (THRESHOLD_TEMP). Email credentials are required for sending alerts via SMTP.

Update the following variables in the script for email functionality:

Code

sender = 'your_email@example.com'
receivers = ['alert_receiver@example.com']
Ensure you have configured the sender's email account for SMTP and allowed less secure apps (if needed).

Data Storage
Weather data is stored in two SQLite tables:

weather: Stores real-time weather data (city, temperature, feels like, condition, and timestamp).
daily_summary: Stores daily summaries (average, max, min temperatures, dominant condition, and date).
Graph Visualization
For each city, the system generates a graph showing the daily average, maximum, and minimum temperatures. The graphs are displayed in separate windows using Matplotlib.

                                              Directory Structure

Code
weather-monitoring/
├── weather_monitor.py      # Main Python script to run the simulation and visualization
├── requirements.txt        # File containing required Python libraries
├── weather_simulation.db    # SQLite database (created after the first run)
├── README.md               # Project documentation

                                                  Design Choices

SQLite for Data Storage: SQLite was chosen as it is lightweight, requires no additional setup, and is sufficient for simulating weather data for a limited time frame. It supports all the SQL operations needed to store, retrieve, and roll up the weather data.
Matplotlib for Visualization: The matplotlib library was chosen for data visualization due to its flexibility and ease of use in generating various types of plots (line charts for weather data). It also allows for extensive customization of the appearance of the plots.
Separation of Concerns: The system is divided into key functions:
generate_mock_weather_data(): Responsible for simulating random weather data.
store_weather_data(): Handles storage of the generated data.
rollup_daily_summary(): Processes daily weather data to create meaningful summaries.
visualize_daily_summary(): Visualizes the summarized weather data in easy-to-read charts.
Data Simulation: Random weather conditions and parameters (temperature, humidity, wind speed) are generated using the Python random library. The simulated data is designed to imitate real-world weather variations across different Indian cities.

Daily Summaries: Each city’s weather data is rolled up into daily summaries that show:

Average, minimum, and maximum temperature
Average humidity
Maximum wind speed
Dominant weather condition

                                            Non-Functional Considerations
1. Security
API Key & Email Credentials: Store sensitive credentials in environment variables or use a .env file.
TLS for Email: Email alerts are sent using TLS encryption via the smtplib module.
2. Performance
Efficient Data Fetching: Weather data is fetched at configurable intervals to avoid API rate limits.
Lightweight Database: SQLite is used to store and retrieve weather data efficiently.
3. Scalability
Flexible Configuration: The system can monitor additional cities and use a more scalable database if needed.
Database Scalability: The system can switch to PostgreSQL or MySQL for larger deployments.
4. Error Handling
API Error Handling: The system handles API errors and prints meaningful messages.
Database Transactions: Data is stored using transactions (commit()) to ensure consistency.
5. Maintainability
Modular Structure: Each function is responsible for a specific task (fetching, storing, processing, visualizing), making the code easy to maintain and extend.
6. Reliability
Persistent Storage: Weather data is stored in the SQLite database, ensuring data is not lost between runs.
Alert System: The system reliably sends email alerts when temperature thresholds are exceeded.
Future Improvements
Caching: Implement caching to reduce redundant API calls.
Asynchronous Data Fetching: Use asynchronous programming to fetch data for multiple cities in parallel.
Cloud Deployment: Deploy the system on a cloud platform for better scalability and availability.
Advanced Monitoring: Integrate Prometheus and Grafana for real-time monitoring and alerting.
