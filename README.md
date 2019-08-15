# MeterAnalyser
Program that allows users ti add/delete meter reads to a database and summarises the data.

In my day job I have to monitor energy consumption and thought I would write a program to further my coding skills. I wanted to use a database to get practice using one, so I opted for SQLite with a Tkinter front end. I created a dashboard to display basic information such as averages, min/max values and listing the calculated consumption values rather than just the raw reads. I made it slightly harder by breaking the records into years and giving the user the ability to select the data across three meters per year.
I used Matlibplot to practice using graphs to show the consumption trends, again the user has the ability to choose different meters to show.
The user has the ability to add/remove meter reads into the database. This was slightly complex as the user has to make sure they enter a month, year and meter name. I had to put conditionals in to cater for any errors that may arise such as missing data, no data, incorrect data if the user enters a value that is less than previous etc. I created a label at the top to display error messages and also success messages.

<b>Learning Concepts</b>
<ol>
  <li>String Formatting/Manipulation</li>
  <li>Conditionals</li>
  <li>Loops</li>
  <li>Tkinter GUI</li>
  <li>Matlibplot Graphs</li>
  <li>Database SQLite</li>
  <li>Data Structures - Lists</li>
