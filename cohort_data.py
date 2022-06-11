"""Functions to parse a file containing student data."""

def all_houses(data):
    """Return a set of all house names in the given file.

    For example:
      >>> unique_houses('cohort_data.txt')
      {"Dumbledore's Army", 'Gryffindor', ..., 'Slytherin'}

    Arguments:
      - filename (str): the path to a data file

    Return:
      - set[str]: a set of strings
    """
  

    houses = set()

    data = open('cohort_data.txt')

    for line in data:
      house = line.rstrip().split('|')[2]
      if house:
        houses.add(house)

    return houses


def students_by_cohort(data, cohort='All'):
    """Return a list of students' full names by cohort.

    Names are sorted in alphabetical order. If a cohort isn't
    given, return a list of all students. For example:
      >>> students_by_cohort('cohort_data.txt')
      ['Adrian Pucey', 'Alicia Spinnet', ..., 'Zacharias Smith']

      >>> students_by_cohort('cohort_data.txt', cohort='Fall 2015')
      ['Angelina Johnson', 'Cho Chang', ..., 'Terence Higgs', 'Theodore Nott']

      >>> students_by_cohort('cohort_data.txt', cohort='Winter 2016')
      ['Adrian Pucey', 'Andrew Kirke', ..., 'Roger Davies', 'Susan Bones']

      >>> students_by_cohort('cohort_data.txt', cohort='Spring 2016')
      ['Cormac McLaggen', 'Demelza Robins', ..., 'Zacharias Smith']

      >>> students_by_cohort('cohort_data.txt', cohort='Summer 2016')
      ['Alicia Spinnet', 'Dean Thomas', ..., 'Terry Boot', 'Vincent Crabbe']

    Arguments:
      - filename (str): the path to a data file
      - cohort (str): optional, the name of a cohort

    Return:
      - list[list]: a list of lists
    """

    students = []

    data = open('cohort_data.txt')

    for line in data:
      fname, lname, _, _, cohort_name = line.rstrip().split('|')
      if cohort_name not in ('I', 'G') and cohort in ('All', cohort_name):
        students.append(f'{fname} {lname}')
    

    return sorted(students)


def all_names_by_house(data):
    """Return a list that contains rosters for all houses, ghosts, instructors.

    Rosters appear in this order:
    - Dumbledore's Army
    - Gryffindor
    - Hufflepuff
    - Ravenclaw
    - Slytherin
    - Ghosts
    - Instructors

    Each roster is a list of names sorted in alphabetical order.

    For example:
      >>> rosters = hogwarts_by_house('cohort_data.txt')
      >>> len(rosters)
      7

      >>> rosters[0]
      ['Alicia Spinnet', ..., 'Theodore Nott']
      >>> rosters[-1]
      ['Filius Flitwick', ..., 'Severus Snape']

    Arguments:
      - filename (str): the path to a data file

    Return:
      - list[list]: a list of lists
    """

    dumbledores_army = []
    gryffindor = []
    hufflepuff = []
    ravenclaw = []
    slytherin = []
    ghosts = []
    instructors = []

    data = open('cohort_data.txt')

    for line in data:
      fname, lname, house, _, cohort_name = line.rstrip().split('|')

      cname = f'{fname} {lname}'

      if house:
        if house == "Dumbledore's Army":
          dumbledores_army.append(cname)
      
        elif house == "Gryffindor":
          gryffindor.append(cname)

        elif house == "Hufflepuff":
          hufflepuff.append(cname)

        elif house == "Ravenclaw":
          ravenclaw.append(cname)

        elif house == "Slytherin":
          slytherin.append(cname)
      else:
        if cohort_name == "G":
          ghosts.append(cname)
        elif cohort_name == "I":
          instructors.append(cname)


    return [sorted(dumbledores_army),
            sorted(gryffindor),
            sorted(hufflepuff),
            sorted(ravenclaw),
            sorted(slytherin),
            sorted(ghosts),
            sorted(instructors), ]


def all_data(data):
    """Return all the data in a file.

    Each line in the file is a tuple of (full_name, house, advisor, cohort)

    Iterate over the data to create a big list of tuples that individually
    hold all the data for each person. (full_name, house, advisor, cohort)

    For example:
      >>> all_student_data('cohort_data.txt')
      [('Harry Potter', 'Gryffindor', 'McGonagall', 'Fall 2015'), ..., ]

    Arguments:
      - filename (str): the path to a data file

    Return:
      - list[tuple]: a list of tuples
    """

    all_data = []

    data = open('cohort_data.txt')

    for line in data:
      fname, lname, house, head, cohort_name = line.rstrip().split('|')
      all_data.append((f'{fname} {lname}', house, head, cohort_name))

    return all_data


def get_cohort_for(data, name):
    """Given someone's name, return the cohort they belong to.

    Return None if the person doesn't exist. For example:
      >>> get_cohort_for('cohort_data.txt', 'Harry Potter')
      'Fall 2015'

      >>> get_cohort_for('cohort_data.txt', 'Hannah Abbott')
      'Winter 2016'

      >>> get_cohort_for('cohort_data.txt', 'Someone else')
      None

    Arguments:
      - filename (str): the path to a data file
      - name (str): a person's full name

    Return:
      - str: the person's cohort or None
    """

    for cname, _, _, cohort_name in all_data(data):
      if cname == name:
        return cohort_name


def find_duped_last_names(data):
    """Return a set of duplicated last names that exist in the data.

    For example:
      >>> find_name_duplicates('cohort_data.txt')
      {'Creevey', 'Weasley', 'Patil'}

    Arguments:
      - filename (str): the path to a data file

    Return:
      - set[str]: a set of strings
    """

    dupes = set()
    seen = set()

    for cname, _, _, _, in all_data(data):
      last = cname.split(' ')[-1]

      if last in seen:
        dupes.add(last)

      seen.add(last)

    return dupes


def get_housemates_for(data, name):
    """Return a set of housemates for the given student.

    Given a student's name, return a list of their housemates. Housemates are
    students who belong to the same house and were in the same cohort as the
    given student.

    For example:
    >>> get_housemates_for('cohort_data.txt', 'Hermione Granger')
    {'Angelina Johnson', ..., 'Seamus Finnigan'}
    """

    housemate = set()

    target = None

    for person in all_data(data):
      cname, house, head, cohort_name = person

      if cname == name:
        target = person
        break
    if target:
      target_name, target_house, _, target_cohort = target

      for cname, house, _, cohort_name in all_data(data):
        if((house, cohort_name) == (target_house, target_cohort) and 
          cname != name):
          housemate.add(cname)

    return housemate

##############################################################################
# END OF MAIN EXERCISE.  Yay!  You did it! You Rock!
#

if __name__ == '__main__':
    import doctest

    result = doctest.testfile('doctests.py',
                              report=False,
                              optionflags=(
                                  doctest.REPORT_ONLY_FIRST_FAILURE
                              ))
    doctest.master.summarize(1)
    if result.failed == 0:
        print('ALL TESTS PASSED')
