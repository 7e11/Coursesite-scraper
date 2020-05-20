# Which people do I share the most classes with?

Most students think about this question at the beginning of a semester.
They might ask their friends about the classes they're taking, and they'll probably notice a few people who they share a bunch of classes with.
However, I wanted to know the answer to this question definitively, so I decided to scrape my school's coursesite (similar to blackboard) 
using [selenium](https://selenium.dev/projects/).

Firstly, a bit about me: 

I'm currently a Junior at Lehigh University where I'm studying Computer Science & Engineering. My Fall 2019 Schedule was packed with the hard hitting classes which are to be expected as a Junior in CSE.

| ID       | Name                              |
|----------|-----------------------------------|
| POLS-106 | Environmental Values & Ethics     |
| CSE-337  | Reinforcement Learning            |
| CSE-216  | Software Engineering              |
| CSE-303  | Operating System Design           |
| CSE-340  | Design and Analysis of Algorithms |

Onto the scraping:

Every Lehigh student's user page on coursesite contains their ID in the url.
 
 `https://coursesite.lehigh.edu/user/view.php?id=#####`

Every class you're enrolled in has a page which allows you to see all of the class's participants, 
and links to all of their user pages. 


![Anonymized participants list](./coursesite/images/participants.png)

I was able to scrape these participant pages and create a list of participant IDs for each class I was enrolled in.
After cleaning, I plotted the data using the [python UpSet library](https://pypi.org/project/UpSetPlot/).

**NB:** An [UpSet plot](https://caleydo.org/tools/upset/) is a type of graph designed to visualize relationships between a large number of sets.
Oringinally developed for visualizing the similarities between the genomes of organisms, 
it's perfect for this project becuase a venn diagram with more than three sets (classes) would be difficult to read.

![UpSet plot of Fall 2019](./coursesite/images/F2019.png)

**UpSet 101:**
- The horizontal bars to the left of the course IDs are the **total enrollment** for that course.
- A filled dot in a row and column means that everyone in that intersection **took that course**.
  - Multiple filled dots means that everyone in the intersection took all of those courses.
- A empty dot in a row and column means that everyone in that intersection **did not take that course**.
  - Multiple empty dots means that everyone in the intersection did not take any of those courses.
  
For example, we can see that there were four people who took `CSE-337` and `CSE-340`, and did not take any of the other three classes.

**Brief Analysis:**
- I'm the only person who was in all five of my classes.
- No one had four classes with me.
- There was a 17 way tie for people who took three classes with me.

One problem with this graphic is that it doesn't really tell you anything about the people who are in these intersections.

I noticed that some people had added their school emails to their coursesite user page.
Lehigh emails have a format of `INITIALS|NUM|GRAD_YEAR@lehigh.edu`. For example, my email is `ezh221@lehigh.edu`
By scraping people user pages for their emails, 
I was able to determine their graduation years and add this data to the graph as a series of violin plots.

![UpSet plot of Fall 2019 with grad_year](./coursesite/images/F2019_gradyear.png)

**Brief Analysis:**
- The four people taking only Algorithms & Reinforcment Leaning are all grad students.
- Most people taking Operating Systems and Algorithms are seniors (Class of 2020)
- However, most people taking Software Engineering and Algorithms are juniors (Class of 2021)

Ultimately, I was unhappy with how this graphic displayed the grad year data, so I created a percentage bar chart as well.

![Percentage bar chart of courses by grad_year](./coursesite/images/F2019_percentage_bar.png)

**Brief Analysis:**
- Reinforcement Learning is very popular with grad students.
- Operating Systems is made up of almost all seniors.
- There were no first years in any of my classes.


Unfortunately, I don't think this is very readable. Other than a series of pie charts, I'm not
really sure how to express percentages for several different groups well.


### Spring 2020 classes

Here is my spring schedule. 
It's my first time taking a grad class so we'll see how that goes.

| ID      | Name                       |
|---------|----------------------------|
| CSE-398 | Software Verification      |
| CSE-403 | Advanced Operating Systems |
| CSE-280 | Capstone Project I         |
| CSE-327 | Artificial Intelligence    |
| CSE-318 | Theory Of Computation      |

_Software Verification doesn't have a coursesite to scrape, but Professor Michael Spear
was kind enough to email me the participants list._

![UpSet plot of Spring 2020](./coursesite/images/S2020_gradyear.png)

**Brief Analysis:**
- Software Verification and Advanced Operating Systems have a surprisingly high amount of overlap.
- Similar to the Fall, There is a 11 way tie for people who share three classes with me.

![Percentage bar chart of courses by grad_year for Spring 2020](./coursesite/images/S2020_percentage_bar.png)

**Brief Analysis:**
- The small percentage of "grad students" who are taking Capstone I are likely
  super-super seniors which I misclassified.
- The large amount of unknowns in Advanced Operating Systems are likely grad students
  who never added their email address to coursesite.

### All together now

By combining my Fall 2019 and Spring 2020 data I was able to produce this monster.
The set intersections of my entire 2019-2020 school year.

![UpSet plot of 2019-2020](./coursesite/images/FullYear_gradyear.png)

_Try popping out the image to make it easier to read_

While I'm sure there's some crazy analysis I could do with this graph,
I'm going to settle for answering the question I posed in the beginning of this article.
Which people share the most classes with me?

6 classes (2 people)
- Shane Acoveno
- Letong (Simon) Zhang

5 classes (9 people)
- Daniel Yu
- Reilly Yankovich
- _Jitong Ding_
- _Emir Anda_
- _Hansen Lukman_
- _Bradford (Brad) DeMassa_
- _Olivia Grimes_
- Thomas (Kingsley) Leighton
- Nathan Tokala

The five who are in italics all took the exact same courses:
- Fall: CSE-216, CSE-340
- Spring: CSE-280, CSE-327, CSE-318

When beginning this project, I expected that I would not know the person who shares
the most classes with me, and I was right. I don't know either of those people.

What is surprising though is that I'm well acquainted with three of the people who share five classes with me.



Reflections:
- learned about scraping: selenium, xpath
- learned about graphing: pandas, seaborn, matplotlib
- While I didn't do it in this project. I really should have defined classes or namedtuples which represented the data I was scraping.
  It eventually became quite annoying when every object, whether it was a user profile, or a course, or an entry in a
  participants list was a dict instead of a class.