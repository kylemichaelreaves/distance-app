# Coding Test

The challenge was to design an API which would call a Google API to display the distance between two addresses. 

They specified several requirements:

- Make it scalable. 
- The addresses had to be displayed properly formatted.
- Display the distance between the two addresses
- Those addresses had to be geocoded.
- Make it usable for placenames. 

I chose the Google Places API because it fit those requirements perfectly. 

According to their feedback, I was rejected for calling Google Places API from the frontend.

I've since refactored to hide the key, to learn from my error. 

Overall, this was an exercise from which I learned a lot.
