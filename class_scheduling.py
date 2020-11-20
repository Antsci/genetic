
import time
import sqlite3
# constant zoo
mutation_rate = 2
num_schedules_to_retain = 3
tournament_size = 4
database = "schedule_data.db"

class my_random():
    '''random number generation object, using LCG method'''
    seed = int(time.time())

    def __init__(self):
        pass

    def random_int(self):
        '''returns random number, when next() called around it as method of object instance'''
        while True:
            self.seed = (48271*self.seed) % ((2 ** 31) - 1)
            yield self.seed

    def random_choice(self, deck):
        '''returns random selection from given iterable '''
        return deck[next(self.random_int()) % len(deck)]


def sorter(fitnesses):
    '''recursive implementation of merge sort'''
    if len(fitnesses) > 1:
        mid_point = len(fitnesses) // 2
        left_half = fitnesses[:mid_point]
        right_half = fitnesses[mid_point:]
        sorter(left_half)
        sorter(right_half)
        i, j, k = 0, 0, 0
        while (i < len(left_half)) and (j < len(right_half)):
            if left_half[i].get_fitness() < right_half[j].get_fitness():
                fitnesses[k] = left_half[i]
                i += 1
            else:
                fitnesses[k] = right_half[j]
                j += 1
            k += 1
        while i < len(left_half):
            fitnesses[k] = left_half[i]
            i += 1
            k += 1
        while j < len(right_half):
            fitnesses[k] = right_half[j]
            j += 1
            k += 1
    return fitnesses


p = my_random()


class data:
    ''' 
    imports data about school from database
    e.g. teachers, time periods, rooms, classes etc 
    '''
    def create_connection(self, db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except sqlite3.Error as e:
            print(e)
        return conn

    def __init__(self):

        conn = self.create_connection(database)
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM Departments")
            self.departments = cur.fetchall()
            cur.execute("SELECT * FROM Room_Types")
            self.room_types = cur.fetchall()
            cur.execute("SELECT * FROM Rooms")
            self.rooms = cur.fetchall()
            cur.execute("SELECT * FROM Teachers")
            self.teachers = cur.fetchall()
        days = [["Mon", 16], ["Tue", 16],["Wed", 16], ["Thu", 16], ["Fri", 13]]
        d_timeslots = [[(u[0] + ' ' + str((i % 12))+":00").replace(" 0:00", " 12:00") for i in range(8, u[1])] for u in days]
        self.timeslots = [y for x in d_timeslots for y in x]

school_data = data()
print(school_data.rooms)
print(school_data.departments)
print(school_data.teachers)

   

class population:
    '''The competing schedules '''

    def __init__(self):
        self.pop = []


class schedule:
    ''' when, where and with who the class is'''

    def __init__(self):
        '''randomly generates a full schedule, with random variables(teacher, room, time) for each class like y9 set 4 maths or y12 physics'''
        self.classes = []
        school_data = data()
        for i in school_data.departments:
            for j in range(7, 14):
                self.classes.append(teaching_class(p.random_choice(school_data.teachers),[p.random_choice(school_data.timeslots) for _ in range(3)], p.random_choice(school_data.rooms), i, "year "+j+" "+i[1]))

    def get_fitness(self):
        '''returns a calculation of the schedule instance's fitness'''
        conflicts = 0
        for i in self.classes:
            for j in self.classes:
                if (len(set(i.times).intersection(set(j.times))) != 0 ) and ((i.room == j.room) or (i.teacher == j.teacher)):
                    if i.name != j.name:
                        conflicts += 1
            if len(i.time) > len(set(i.time)):
                conflicts += 1
            if i.room[1] != i.subjec[2]:
                conflicts += 1
            if i.subject[0] not in i.teacher[1:3]:
                conflicts += 1
        return 1/conflicts

        
class teaching_class:
    def __init__(self, teacher, times, room, subject, name):
        self.teacher = teacher
        self.times = times
        self.room = room
        self.subject = subject
        self.name = name


def evolve(self, pop):
    ''' wrapper func'''


def select_for_crossing(self, incoming_population):
    population_to_be_crossed = population()
    population_to_be_crossed.pop.append(
        incoming_population.pop[:num_schedules_to_retain])


def select_for_mutation(self, population):
    sorted_pop = population()
    sorted_pop.pop = sorter(population.pop)
    to_be_mutated = sorted_pop.pop[num_schedules_to_retain:]
    return to_be_mutated


def crossover(self, schedule1, schedule2):
    ''' child randomly inherits each characteristic from parents @ 50/50'''
    child = schedule()
    child.classes = [schedule1.classes[i] if (next(p.random_int()) % 2 == 0) else schedule2.classes[i] for i in range(len(schedule1.classes))]
    return child


def muatate(self, schedule):
    random_schedule = schedule.start()
    for i in enumerate(schedule.classes):
        if p.random_choice(range(10)) < mutation_rate:
            schedule.classes[i[0]] = random_schedule.classes[i[0]]
    return schedule


def tournament_selection(self, population):
    ''' Selects K, in this case 3, random schedules from the inputted schedules and ranks them by fitness and returns them'''
    tournament_attendees = population()
    tournament_attendees.pop = [p.random_choice(
        population.pop) for _ in range(tournament_size)]
    return sorter(tournament_attendees.pop)


""" class table_display:
    ''' ''' """
