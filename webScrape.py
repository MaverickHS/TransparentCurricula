import requests
from bs4 import BeautifulSoup

url = "https://www.cs.fsu.edu/academics/graduate-programs/courses/"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Find all course blocks.
course_blocks = soup.find_all("p")

for block in course_blocks:
    course_name = block.find("b")
    if course_name:
        course_name = course_name.text.strip()
    else:
        continue  # ignore blocks without a course name

    if '–' in block.text:
        continue  # ignore blocks with course keys (CAP, CDA, etc.)

    prerequisite = block.find("em")
    if prerequisite:
        prerequisite = prerequisite.text.strip().split(":")[-1].strip()
    else:
        prerequisite = None

    # Course description is the rest of the text in the <p> tag after removing course_name and prerequisite.
    course_description = block.text.strip()
    if course_name:
        course_description = course_description.replace(course_name, "")
    if prerequisite:
        course_description = course_description.replace("Prerequisite: " + prerequisite, "")

    print("Course Name: _{}_".format(course_name))
    print("Prerequisite: {}".format(prerequisite))
    print("Course Description: {}\n".format(course_description))
