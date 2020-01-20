---
layout: post
title: Which people do I share the most classes with?
published: false
---

Every student thinks about this at the beginning of a semester.
They might ask their friends about the classes they're taking, and they'll probably notice a few people who they share a bunch of classes with.

However, I wanted to know

This project involved scraping my school's coursesite (similar to blackboard) using [selenium](https://selenium.dev/projects/).
Afterwards, I created an [UpSet plot](https://caleydo.org/tools/upset/), which is a type of graph designed to visualize relationships between a large number of sets.
Oringinally developed for visualizing the similarities between the genomes of different organisms, I thought It would be perfect for this project.
Needless to say, a venn diagram with more than three sets quickly gets out of hand.


Lehigh's coursesite is a [moodle](https://moodle.org/) based learning platform.
Every class you're enrolled in has a page which allows you to see all of the classes participants.
I was able to scrape those tables in to a list of dicts.
INCLUDE IMAGE of class participants
INCLUDE IMAGE of list of dicts
From this, I turned each class into a list of the participant ID's in that class and fed it into the [python UpSet library](https://pypi.org/project/UpSetPlot/).
INCLUDE UPSETPLOT HERE

Talk about how to read the graph. Do a single point, and then multiple points.
I'm the only person who was in all five of my classes.
30 way tie for people who share 3 classes with me
- Name some of them (WILL NEED NEW SCRIPT FOR THAT)

Show the grad year version of the visualization, and talk about how I was unhappy with it and created a 100% bar chart.
INSERT BAR CHART
I wasn't very happy with how readable the bar chart was either. Unfortunately other than several pie charts, I'm not
really sure how to express percentages for several different groups well.


Aside:
> While I kind of breeze past the initial scraping stuff. 
> Even beginning to scrape coursesite was a massive hurdle for me.
> I attempted to use requests, scrapy + splash, and then scrapy + selenium.
> I tried all kinds of different ways to save cookies and headers, 
> but eventually I started using selenium alone because it just worked, and performance wasn't a concern for this project.
> Maybe in the future I'll come back to scrapy and see if it clicks.

Reflections:
- learned: selenium, xpath
- learned some of: pandas, seaborn, matplotlib
- While I didn't do it in this project. I really should have defined classes or namedtuples which represented the data I was scraping.
  It eventually became quite annoying when every object, whether it was a user profile, or a course, or an entry in a
  participants list was a dict instead of a class.