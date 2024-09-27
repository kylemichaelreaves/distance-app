# ChannelFactory Coding Test

#### By: Kyle M Reaves

### Specifications

- [x] An input for an origin location
- [x] An input for a destination location
- [x] Display the properly formatted address of both
- [x] Build database models and queries using Django
- [ ] Optimize database and queries to scale and be as efficient as possible; don't use any external caching services
- [x] Use Google's Geocoding API to geocode both addresses

***

### My Implementation

- [x] frontend form validation: Watch or listen to both addresses are for changes to their truthiness (and we know both
  will be valid since we are using the Places API) before sending the request to Django
- [x] Check if both addresses already exist in the database
- [x] If they do, return the distance from the database
- [x] If they don't, use postgis to calculate the distance and save it to the database
- [x] I opted for using the Places API instead of the Geocoding API because it offers validations of places and
  addresses
- [x] I created a reusable component for the autocomplete inputs

***

### Conflicting instructions?

There seems to be a conflict in the instructions.

Under Specifications:

`Get the distance between the two locations using the Google Maps API.`

But then under Instructions, it says:

`You will need to do this calculation yourself.`

Based on the requirements, I opted for the Google Places API, which returns the lat and lng coordinates as well as
properly formatted addresses. 

With the lat and log of the addresses already taken care of, I was able to directly create
Point objects in Django, and then query those coordinates in postgres. 

I think directly querying the database with an actual SQL query, as opposed to ORM, is more scalable and efficient.
***

### Running Locally

1. Create a python virtual environment — I used version 3.12.5 `python3 -m venv env`
2. Activate that environment `source env/bin/activate`
3. Install the requirements for both front and back ends `pip install -r requirements.txt`
4. This app depends on a Google API key — ensure it is injected on the front end's index.html header script
5. Run the Django server `python manage.py runserver`
6. Run the front end `npm run dev`