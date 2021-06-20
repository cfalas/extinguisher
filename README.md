# Extinguisher

Fires are disastrous– it seems like every day, we scroll down our News Feed only to find out another part of our ecosystem is on fire, with hundreds of years of growth, millions of Euros and human lives lost in minutes. In order to prevent this, fires need to be contained quickly.

---

### What

When thinking of the problem at hand, a question that arises is where should fire stations be placed.
Extinguisher suggests locations for new emergency-response hubs so as to optimize the emergency response system and decrease response times, hence protecting the rural areas.


### How

Step 1: Extinguisher collects historical fire data from satellite data, and clusters fires which are close to each other as one, larger fire to make computation faster.

Step 2: The weight of each fire is calculated. This represents the danger a fire in that region poses. This is calculated using the fire intensity as reported by satellite data, as well as a risk assessment of the surrounding area.
The risk of a specific area depends on:

* The slope of the area

   * While fires spread faster on hills than flat ground, not a lot of fires are initiated on very steep hills.
   * Elevation data is collected from a custom Valhalla instance and OpenStreetMap data.

* Vegetation type:
    * Fires can spread up to 40% faster on grasslands than forests. Satellite data from Sentinel-2 are collected, to differentiate between types of vegetation.

* Population density around the region:
Fires endangering people need to be contained faster. In order to approximate this, the distance from the nearest village is measured.

Step 3: The fires and existing fire stations are plotted on the user interface

Step 4: Extinguisher finds optimal locations for new fire stations. using a modified k-means clustering algorithm which tries to maximise the total fitness of each fire station, slightly moving the fire stations in each iteration.

The fitness of each fire station in our model depends on:
* The total weight of fires historically around that station
* The distance from each fire. In this way, fires which were further away contribute less to the fitness, so that the fire station is placed as close to all fires as possible.

All distances used were the time needed by car, as reported by a custom instance of Open Source Routing Machine.

### Impact
The impact that this project can have is huge. Not only can it help save large areas of precious green sites, and by extension the lives of people, the data collected, especially the risk assessment by location, can be extremely valuable to insurance companies.

### Future plans
In the future, the functionality of Extinguisher can be extended heavily. On the aspect of fires, additional factors can be included in the model, such as the location of dams / water refilling stations. Additionally, the platform can be made more customizable to allow more control over the model.
The models can be refined by field experts for a better reflection of the real world.

However, beyond this, the project can be extended to other emergencies.
