import urllib.request
import re

distributions = ["ALC-AS","BIO-AS",'ETM-AS','GLC-AS','HST-AS','PHS-AS','SCD-AS','SSC-AS','SDS-AS','SMR-AS']
distribution_names = ['Arts, Literature, and Culture', 'Biological Sciences', 'Ethics and the Mind', 'Global Citizenship', 'Historical Analysis', 'Physical Sciences', "Social Difference", 'Social Sciences', 'Statistics and Data Science', 'Symbolic and Mathematical Reasoning']

#excluding = set(['PHS-AS','SMR-AS'])
excluding = set()
html_start = "https://classes.cornell.edu/search/roster/FA20?q=&days-type=any&crseAttrs-type=any&breadthDistr-type=any&breadthDistr%5B%5D="
html_end = "&pi="


course_dict = dict() #a dictionary that maps a specific class(for example 'MATH2230') to to the distributions it satisfies
reduced = dict() # a dictionary that maps a pair of distribution requirements two the classes that satisfy both requirements

def get_html(url):
    fp = urllib.request.urlopen(url)
    mybytes = fp.read()

    mystr = mybytes.decode("utf8")
    fp.close()
    return mystr

def get_courses_page(distribution):
    return get_html(html_start+distribution+html_end)

def atd(dictionary,key,element): # add to dict #
    if key not in dictionary:
        dictionary[key] = set()
    dictionary[key].add(element)


def process_courses(distribution):  #returns a list of all classes fulfilling a specific distribution requirement
                                    #AND updates the course dict

    course_list = re.findall(r'ddescr-[a-zA-Z]+\d+',get_courses_page(distribution)) #searches the class roster for all classes
                                                                                    # that satisfy the particular distribution
    for index in range(len(course_list)):
        course_list[index] = course_list[index][7:]
        atd(course_dict,course_list[index],distribution)
    return set(course_list)

def cycle_all_distributions():
    all_sets = []
    for dist in distributions:

        if dist in excluding:
            print("Skipping " + dist)
            all_sets.append(set())
            continue
        print("Processing " + dist)
        all_sets.append(process_courses(dist))

def find_all_doubles(): #returns a dictionary of all classes that fulfill two+ distribution requirements
    double_dict = dict()
    if len(course_dict) == 0:
        cycle_all_distributions()
    for course in course_dict:
        if len(course_dict[course]) > 1:
            double_dict[course] = course_dict[course]
    return double_dict


def do_the_thing():     #tries to combine classes that fulfill two+ distributions
                        # so as to minimize the number of classes needed for graduation
    pass
    #ok so the main goal is to ELIMINATE DOUBLES WITH OVERLAP. I think it  would be best to do this in the way that I did sudoku.
    #ok so there are a lot of possible courses, however for our purposes the distinctions between INDIVIDUAL COURSES DONT MATTER
    #all that matters is what distribution requirements a course fulfills. In this way we can simplify the list of doubles down from a
    #dictionary with hundreds (probably) of entries down to a much more manageable number. I am going to make a new function for this called
    #'reduce_to_distribution'
    #now that I have that method coded I need a way of combining the categories to fulfill the requirements
    #I think what I am going to do is this: I will make the tuple into a set. I will then successively perform
    #a UNION function that combines that with another. If there is overlap IT MOVES ON.
    double_dict = find_all_doubles()

    pass

def reduce_to_distributions(doubles):   #this method will create a dictionary where the keys are a tuple of distribution requirements
                                        #e.g. ('ALC-AS', 'SCD-AS') and the values are the list of all class id's that satisfy those double
                                        #requirements
    types_of_doubles = dict()
    for course in doubles:
        list_form = list(doubles[course])
        list_form.sort()
        atd(types_of_doubles,tuple(list_form),course)
    return types_of_doubles

def space_print(iterable):
    for x in iterable:
        print(x)
def combine(reduced_distributions, visited,current_combination, min_remaining, min_combination):
    #this will certainly not be the most efficient way of doing this, but I frankly don't care

    courses_remaining = len(set(distributions).difference(visited).difference(excluding))
    #remember that there will be a problem in the future here. This method will not update the min_combinations if it finds
    #another set of courses that will satisfy the same number of requirements. I should update this in the future but I just want it
    #to be working for now
    if courses_remaining<min_remaining:
        min_remaining = courses_remaining
        min_combination = current_combination
    if courses_remaining == len(set(distributions).difference(excluding))%2:
        return visited,current_combination, courses_remaining, current_combination

    for pair in reduced_distributions:
        new_visited= set(pair).union(visited)

        if not len(new_visited) == len(pair) + len(visited):
            continue
        new_combination = current_combination.union((pair,))
        return combine(reduced_distributions,new_visited,new_combination,min_remaining, min_combination)
    return visited,current_combination, min_remaining, min_combination
def write_HTML_file():
    open()
def printOptions():
    global reduced
    if len(reduced) ==0:
        reduced = reduce_to_distributions(find_all_doubles())
    combined = combine(reduced,set(),set(),len(set(distributions).difference(excluding)),set())
    if not combined[2] ==0:
        visited = set()
        for pair in combined[3]:
            visited = visited.union(pair)

        print("You would still have to complete distribution requirements for " + set(distributions).difference(excluding).difference(visited).__str__() + " after signing up for the courses below")
    for pair in combined[3]:
        print("\t" +pair[0] + " AND " + pair[1])
        for course in reduced[pair]:
            print("\t\t" + course[:-4] + " " + course[-4: ])
def runTheProgram():
    global excluding

    val = input("Please input the distributions you have already completed. (example input: 'BIO-AS ETM-AS PHS-AS') Information can be found on https://as.cornell.edu/fall2020-degree-requirements\nInput:")
    val = val.split(" ")
    excluding = set(val)
    #semester = input("Please input the current semester. (e.g. Fall 2020 would be FA20) There is currently no data for anything after Fall 2020")
    printOptions()
#cycle_all_distributions()
runTheProgram()