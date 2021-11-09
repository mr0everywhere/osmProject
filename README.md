# osmProject
Udacity Project 2: Wrangle OpenStreetMap Data


#################################

<strong>WARNING: this project pulls 2.7GB from an online resource as well as creates some other local files taking up a total of 5.5GB local storage</strong>

#################################


It was written to run on python 2.7 with the default pip installs of pandas, humanize, and sqlite3

This program pulls OpenStreetMaps OSM data for the Phoenix Metro and surrounding area.

It attempts to automate many corrections of the data before createing a few csv files and a sqlite3 db file.

The database contains tables for nodes, node tags, ways, way nodes, and way tags.

At the time of writing this program the database has slightly more than 34 Million total rows of information.

There were a total of 3437 users that contributed to the data.

A single user '_jcaruso' is responsible for 26.26% of the total information in the data.

The most common node tags are highways.

The top 3 most common brands in this area are Starbucks, Subway, and Circle K in that order.

The top 3 most common cuisines are Pizza, Mexican, and American.

Further Statistics are included in the jupyter notebook

The biggest limitations of these statistics are the following:
<li>The brands data is very dirty and does not lend itself to automated cleanup containing errors like names starting with 'The' that should not, misspellings, and brands with subtext or subbrands attached to them </li>
<li>The Cuisines data is very skewed because in the top 10 there are 6 different types of asian cuisines including a catchall asian type and if combined would be far more than the number one spot</li>
