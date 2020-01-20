from collections import Counter
from matplotlib import pyplot as plt
import upsetplot
import json
import itertools
import re
import pandas
from collections import Counter

with open('fall2019classes.json', 'r') as json_file:
    classes = json.load(json_file)

course_participants = {}

for c in classes:
    course_participants[c['class_text']] = [p['user_id'] for p in c['participants']]


# Enchrich with class breakdown.
with open('users0-67025.json', 'r') as json_file:
    users = json.load(json_file)

users_id_dict = {}
for u in users:
    users_id_dict[u['id']] = u

def plot_upset():
    # At some point I should be moving into classes rather than dicts.

    participant_ids = itertools.chain.from_iterable(course_participants.values())
    participant_ids = sorted(list(set(participant_ids))) # sort for pandas assign
    graduation_years = []

    # All 461 users have an email address associated with their coursesite!!!
    for p_id in participant_ids:
        # print(users_id_dict[p_id])
        email = users_id_dict[p_id]['user_details']['Email address']
        # print(email)
        match = re.search(r'[a-zA-Z]{3}\d(\d{2})@lehigh.edu', email)
        if match:
            grad_year = int(match.group(1))
            # Get rid of really old emails things...
            if grad_year < 18:
                grad_year = None
        else:
            grad_year = None

        graduation_years.append(grad_year)

    # Plot the data
    df = upsetplot.from_contents(course_participants)
    # Add the grad_year column
    df = df.assign(graduation_year=graduation_years)
    print(df, type(df))

    us = upsetplot.UpSet(df, subset_size='count', show_counts='%d')
    # us.add_catplot(value='graduation_year', kind='boxen')
    us.plot()
    plt.title('Set Intersections in My Fall 2019 Schedule')
    plt.show()

def plot_grad_year():
    course_grad_years = {}
    for course, participants in course_participants.items():
        grad_years = []
        for p_id in participants:
            # print(users_id_dict[p_id])
            email = users_id_dict[p_id]['user_details']['Email address']
            # print(email)
            match = re.search(r'[a-zA-Z]{3}\d(\d{2})@lehigh.edu', email)
            if match:
                grad_year = '20' + match.group(1)
                # Get rid of really old emails things...
                if int(grad_year) < 2019:
                    grad_string = 'grad_student'
                elif int(grad_year) == 2019 or int(grad_year) == 2020:
                    grad_string = 'senior'
                elif int(grad_year) == 2021:
                    grad_string = 'junior'
                elif int(grad_year) == 2022:
                    grad_string = 'sophomore'
                elif int(grad_year) == 2023:
                    grad_string = 'freshman'
                else:
                    grad_string = 'error'
            else:
                grad_string = 'unknown'
            grad_years.append(grad_string)
        course_grad_years[course] = Counter(grad_years)

    print(course_grad_years)
    r = [0, 1, 2, 3, 4]

    print(course_grad_years['CSE-216'])
    print(sum(course_grad_years['CSE-216'].values()))
    # fresh_bar = []
    soph_bar = []
    jun_bar = []
    sen_bar = []
    grad_bar = []
    unkn_bar = []
    for course, counter in course_grad_years.items():
        total = sum(counter.values())
        # fresh_bar.append(counter['freshman'] / total)
        soph_bar.append(counter['sophomore'] / total * 100)
        jun_bar.append(counter['junior'] / total * 100)
        sen_bar.append(counter['senior'] / total * 100)
        grad_bar.append(counter['grad_student'] / total * 100)
        unkn_bar.append(counter['unknown'] / total * 100)

    plt.bar(r, soph_bar, label='sophomore')
    plt.bar(r, jun_bar, bottom=soph_bar, label='junior')
    plt.bar(r, sen_bar, bottom=[i+j for i,j in zip(soph_bar, jun_bar)], label='senior')
    plt.bar(r, grad_bar, bottom=[i+j+k for i,j,k in zip(soph_bar, jun_bar, sen_bar)], label='grad_student')
    plt.bar(r, unkn_bar, bottom=[i+j+k+l for i,j,k,l in zip(soph_bar, jun_bar, sen_bar, grad_bar)], label='unknown')
    plt.xticks(r, course_grad_years.keys())
    plt.legend()
    plt.ylabel('Percentage of Class Makeup')
    plt.xlabel('Class')
    plt.title('Percentage of Class Makeup by Grade')
    plt.show()





if __name__ == '__main__':
    plot_upset()
    # plot_grad_year()
