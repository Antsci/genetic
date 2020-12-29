
from time import time
import sqlite3
from tabulate import tabulate
# constant zoo
MUTATION_RATE = 2
NUM_SCHEDULES_TO_RETAIN = 3
TOURNAMENT_SIZE = 3
DATABASE = "schedule_data.db"

class random_number_generator():
    '''Random number generation object, using LCG method.'''
    def __init__(self):
        self.seed = int(time())#Sets the seed to the integer number of seconds since epoch, January 1, 1970, 00:00:00.

    def random_int(self) -> int:
        '''Returns random number, when next() called around it as method of object instance.'''
        #This function is a generator which means it maintains its state between calls.
        #Therefore each time it computes the seed based based on the previous one.
        while True:
            self.seed = (48271*self.seed) % ((2 ** 31) - 1)#These coefficents are taken from the C++11 implementation of minstd_rand.
            yield self.seed

    def random_choice(self, deck):
        '''Returns random selection from given iterable. '''
        return deck[next(self.random_int()) % len(deck)]#Casts the random output into the given modulos 


def sorter(scheds: list) -> list:
    '''Recursive implementation of merge sort.'''
    if len(scheds) > 1:
        mid_point = len(scheds) // 2
        left_half = scheds[:mid_point]
        right_half = scheds[mid_point:]
        sorter(left_half)
        sorter(right_half)
        i, j, k = 0, 0, 0
        while (i < len(left_half)) and (j < len(right_half)):
            if left_half[i].get_fitness() < right_half[j].get_fitness():
                scheds[k] = left_half[i]
                i += 1
            else:
                scheds[k] = right_half[j]
                j += 1
            k += 1
        while i < len(left_half):
            scheds[k] = left_half[i]
            i += 1
            k += 1
        while j < len(right_half):
            scheds[k] = right_half[j]
            j += 1
            k += 1
    return scheds


my_random = random_number_generator()


class data:
    '''Imports data about school from DATABASE, e.g. teachers, time periods, rooms, classes etc.'''
    def create_connection(self, db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except sqlite3.Error as e:
            print(e)
        return conn

    def __init__(self):

        conn = self.create_connection(DATABASE)
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
  

class population:
    '''The competing schedules.'''

    def __init__(self, empty = False):
        if not empty:#Unless declared on instantiation, fill the population container with new schedules.
            self.pops = [schedule(i) for i in range(10)]
        else:
            self.pops = []

class schedule:
    '''A full, usually a week's, timetable initiated with fully random characteristics.'''
    def __init__(self, self_id = 'test'):
        '''Randomly generates a full schedule, with random variables(teacher, room, time) for each class like y9 maths or y12 physics.'''
        self.classes = []
        self.id = self_id
        school_data = data()#Imports the data about the school, teachers, rooms, time-slots, etc.
        for i in school_data.departments:#Generates a class for each year for each subject.
            for j in range(7, 14):
                slots = [my_random.random_choice(school_data.timeslots) for _ in range(3)]#Randomly picks three unique timeslots.
                while len(set(slots)) != len(slots):
                    slots = [my_random.random_choice(school_data.timeslots) for _ in range(3)]
                self.classes.append(teaching_class(my_random.random_choice(school_data.teachers), slots, my_random.random_choice(school_data.rooms), i, "year "+str(j)+" "+i[1]))
                #Generates a class with a randomly selected room, teacher and timeslot.

    def get_fitness(self) -> float:
        '''Returns a calculation of the schedule instance's fitness.'''
        conflicts = 0
        for k in self.classes:#Iterate through the class-list, comparing each class with every other class.
            for l in self.classes:
                if (len(set(k.times).intersection(set(l.times))) != 0 ) and ((k.room == l.room) or (k.teacher == l.teacher)):
                    #If they share a time-slot and either a room or a teacher.
                    if k.name != l.name:
                        conflicts += 1
            if k.room[1] != k.subject[2]:#If the room is suitable for the subject.
                conflicts += 1
            if k.subject[0] not in k.teacher[1:3]:#If the subject is not a speciality of the teacher.
                conflicts += 1
        return 1 / conflicts if conflicts != 0 else 1
        #conflicts are opposite to fitness so its fitness is the reciprocal of the conflicts

    def get_classes_printable(self) -> list:
       return [i.__dict__ for i in self.classes]
       #__dict__ is an innate meta-attribute of all python objects, it is a dictionary holding all the object's other attributes as key:value pairs.


        
class teaching_class:
    '''With who, when, on what and where the class is.'''
    def __init__(self, teacher, times, room, subject, name):
        self.teacher = teacher
        self.times = times
        self.room = room
        self.subject = subject
        self.name = name

    def get_class_printable(self):
        return self.__dict__


def evolution(pop: population) -> population :
    evolution_pop = population(True)#Creates empty population.
    while len(evolution_pop.pops) < 10: #Whilst the population is less than 10.
        parent1 = tournament_selection(pop)#Pick two schedules using tournament selection.
        parent2 = tournament_selection(pop)
        evolution_pop.pops.append(crossover(parent1, parent2))#cross these two schedules over to produce a child schedule
    evolution_pop.pops = sorter(evolution_pop.pops)#sort the population by fitness
    for i in range(len(evolution_pop.pops) - NUM_SCHEDULES_TO_RETAIN, len(evolution_pop.pops)):#mutate the least fit schedules 
        evolution_pop.pops[i] = mutate(evolution_pop.pops[i])
    return evolution_pop


def crossover(schedule1: schedule, schedule2: schedule) -> schedule:
    '''Assigns characteristics from the two parent schedules, at 50/50, to the child schedule.'''
    child = schedule()#instantiates the child schedule
    child.classes = [schedule1.classes[i] if (next(my_random.random_int()) % 2 == 0) else schedule2.classes[i] for i in range(len(schedule1.classes))]
    #A list comprehension that generates a random integer, if said integer is even then the child uses parent1's values for that class, else it uses parent2's values.
    return child #Returns the child schedule with the new class list as determined by the previous line.


def mutate(input_schedule: schedule) -> schedule:
    '''Generates a new schedule with random characteristics and assigns them to the mutant at a rate defined by the mutation rate.'''
    random_schedule = schedule()#instantiates a new schedule with random characteristics.
    for i in range(len(input_schedule.classes)):#Iterates through the random schedule's classes. 
        a = my_random.random_choice(range(10))#Randomly picks a number 0-9.
        if a < MUTATION_RATE:#If said number is below this then replace the input schedule's class at this indice with a random one.
            input_schedule.classes[i] = random_schedule.classes[i]
    return input_schedule


def tournament_selection(tournament_attendees: population) -> list:
    '''Selects K, in this case 3, random schedules from the inputted schedules and ranks them by fitness and returns them.'''
    tournament_competitors = population(True)#instantiates an empty population container.
    tournament_competitors.pops = [my_random.random_choice(tournament_attendees.pops) for _ in range(TOURNAMENT_SIZE)]#Randomly selects schedules from the general populace.
    return sorter(tournament_competitors.pops)[0]#Return the fittest of the selected schedules.


def table_display(population):
    '''Formats the data into a pretty-print table for outputing.''' 
    table = [[i.id, i.get_classes_printable()[0]] for i in population.pops]
    print(tabulate(table, headers=["table id", "classes"]))

def main():
    competing_population = population()
    #sched_fitness = [i.get_fitness() for  i in competing_population.pops]
    # while 1 not in sched_fitness:
    #     table_display(competing_population)
    #     competing_population = evolution(competing_population)
    for _ in range(10):
        #table_display(competing_population)
        table_display(competing_population)
        competing_population = evolution(competing_population)


#testing
a = population()
# table_display(a)
#print([i.get_fitness() for i in a.pops])
#print([i.get_fitness() for i in sorter(a.pops)])
 #print(a.get_classes_printable())
#print(mutate(a).get_classes_printable())
#print(a.get_fitness())
main()