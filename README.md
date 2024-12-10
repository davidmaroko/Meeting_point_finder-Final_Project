# Meeting Point Finder  
<h4>Current use case: Minyan Finder</h4>
<img src="demonstration_gif.gif" alt="description" />


<h3>Description:</h3>  

Meeting Point Finder is a web application designed to help groups of individuals from different locations find the nearest optimal meeting point. The project addresses an **optimization** of the open NP problem, the <a href="https://en.wikipedia.org/wiki/Metric_k-center">Vertex-k-Center Problem (also known as metric k-center)</a>
The application models the map as a graph and performs a search across all graph nodes within the area where the participants are located, identifying the most suitable meeting point.  

This is a full **end-to-end system** built with a **REST API**:  
- **Back-end:** Developed in **Python** using **Flask**.  
- **Front-end:** Built with **React.js**.  

---

### Current use case: Minyan Finder
Currently, the front-end (and part of the back-end) is customized for a specific use case: helping individuals find a **Minyan**—a quorum of at least 10 people required for Jewish prayer according to Torah rules.  

This implementation introduces additional challenges, such as dynamically grouping users from random locations worldwide into clusters within reasonable driving distances. For instance, someone in Paris wouldn't travel all the way to London to join a Minyan. The system intelligently assigns users to local clusters to ensure practicality and efficiency.  

---

## How to Run the Server  
1. Install the required Python dependencies:  
   ```bash
   pip install -r requirements.txt
   ```
   or
  ```bash
  pip install -r req .\requirement.txt
```  
2. Start the Flask server
```bash
python app.py
```
## How to Run the Client
1.Set Up API Keys:

Obtain a Google Maps API key from Google Maps Documentation: https://developers.google.com/maps/documentation/javascript/get-api-key

Obtain a Mapbox API key from Mapbox Documentation: https://docs.mapbox.com/help/getting-started/access-tokens/

Paste both keys into the file:
```bash
frontend-Minian_finder/src/components/util/data.js
```
2.Install Dependencies and Run the Client:
Navigate to the frontend directory:
```bash
frontend-Minian_finder
```
Install the required dependencies:
```bash
npm install
```
Start the development server:
```bash
npm start
```
(or npm run)
# Open your browser and navigate to the front-end adress:
```bash
http://localhost:3000
```
## Notes
Make sure your API keys are valid and have the necessary permissions enabled for the application to work correctly.
 
---
**Written by:** David Maroko, Mendel Bismut  
**Contact:** [dmaroko21@gmail.com](mailto:dmaroko21@gmail.com)  
For any issues, feel free to contact us at the email provided above.

