# MinyanFinder
MinyanFinder is a web application that helps you find the nearest minyan to your location.
We built a system for finding an optimal meeting place between people from different locations. 
This is an open computational problem from the field of computer science.  
We optimized and reduced the computation time by representing maps as a graph and finding the region where the optimal point is.  
We also built a rest api server in Python language that uses the system to find a minyan for prayer for worshipers around the world.  
The server also deals with the analysis of the geographical proximity between different 
worshipers and their storage in a way that will shorten the search and comparison times.
# writed by: David Maroko, Mendel bismut
# contact us: dmaroko21@gmail.com
# run server: 
pip install -r req .\requirement.txt  
then:
python app.py,  
# run client:
first you should create a personal keys,
to google in  https://developers.google.com/maps/documentation/javascript/get-api-key
and for map-box in https://docs.mapbox.com/help/getting-started/access-tokens/, 
and paste them in frontend/src/components/util/data.js.  
then:
from frontend directory:
npm install,  
npm run,  
then:   
go to localhost:3000 in your browser
