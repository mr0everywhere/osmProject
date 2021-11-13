# osmProject
Udacity Project 2: Wrangle OpenStreetMap Data


#################################

<strong>WARNING: this project pulls 2.7GB from an online resource as well as creates some other local files taking up a total of 5.5GB local storage</strong>

#################################

Please run from main.py and store all other files in the same directory.

It was written to run on python 2.7 with the default pip installs of pandas, humanize, and sqlite3

This program pulls OpenStreetMaps OSM data for the Phoenix Metro and surrounding area.

It attempts to automate many corrections of the data before creating a few CSV files and a sqlite3 DB file.

The audit.py file runs an audit of street names to show if any have errors or are formatted differently than expected.

The fix.py file fixes the postcode, state and street info, it also contains the shape and process map elements taken from the lessons and adapted for use in this project.

The getset.py file has many variables declared that are used throughout the other py files for this project as well as the creation script for smaller osm files from the main larger osm file

The pullphoenixosm.py file pulls the whole large osm that was used for this data set.

The main.py file is the primary file for running this data it includes the sql queries to get stats for the osm

The output of full run file shows the console output of my pc when ran in its entirety including pulling the large osm file and parsing it in the database.

The PhoenixSmall.osm is included as a small sample of data from the larger set if someone so chooses to run against it.

The database contains tables for nodes, node tags, ways, way nodes, and way tags.

At the time of writing this program, the database has slightly more than 34 Million total rows of information.

There were a total of 3437 users that contributed to the data.

A single user '_jcaruso' is responsible for 26.26% of the total information in the data.

The most common node tags are highways.

The top 3 most common brands in this area are Starbucks, Subway, and Circle K in that order.

The top 3 most common cuisines are Pizza, Mexican, and American.

Further info is included in the 'output of full run' file

The biggest limitations of these statistics are the following:
<li>The brands' data is very dirty and does not lend itself to automated cleanup containing errors like names starting with 'The' that should not, misspellings, and brands with subtext or subbrands attached to them. I suspect that a good way to fix this is by dropping the word The if present at the begning of the name and then comparing the first word or 2 to brands already on the list the if they match increment the non "The" brand name count</li>
<li>The Cuisines data is very skewed because in the top 10 there are 6 different types of Asian cuisines including a catchall Asian type and if combined would be far more than the number one spot, The query that lists the top 10 shows that the data has issues Getting a list of all the cuisines and figuring out which ones can be merged then using a dictionary based system like the street abbreviation to full name function would work to fix this.</li>

Problems encountered:
<li>Formatting the data to pull from open street maps on separate occasions I pulled a stripe going around the globe either north and south or east and west that specifically excluded the data I was trying to pull and it pulled very large files with none of the data I needed. </li>
<li>It is very common for streets to not have a suffix in the area I looked into so there is a lot of noise regarding street name cleaning</li>

Benefits of making corrections:
<li>The fixes already performed would make the data more congruent if it were uploaded to the open street maps system and would would lead to a heightened accuracy of the data set. </li>
<li>Regarding the cuisines data I think it would be beneficial if there were a primary cuisine like Asian, American and similair broad cuisine types followed by a more granular type like Korean, Japanese, Burger, Bar and Grill</li>

Problems with these corrections:
<li>I suspect that in many cases if a node or way is on a boarder of some kind it shows 2 values in the following format taga:tagb and therefore both are correct for that element</li>
<li>Programatically correcting the Cuisine types may lead to some bias or catagorization problems, questions like are burgers American food, is Indian food Asian, is Pakistani food Asian, does everything need that secondary tag or is it optional?</li>

This program was written in PyCharm IDE Education Edition and all atempts to meet pep standards were made in earnest. 
