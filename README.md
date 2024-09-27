# ChannelFactory Coding Test

The challenge was to design an API which would call a Google API to display the distance between two addresses. 

They specified several requirements:
Make it scalable. 
The addresses had to be displayed properly formatted. 
Those addresses had to be geocoded. 
Make it usable for placenames. 

I chose the Google Places API because it fit those requirements perfectly. According to their feedback, I was for calling Google Places API from the front end. 
It did not matter to them whether this API was designed to be called from the frontend or not. Google's documentation is almost exclusively composed of examples of this usecase. In fact, they have code examples in JavaScript and TypeScript. 

I thought I built a lovely reusable component, which I'm proud of.
