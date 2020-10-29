
import time
import sqlite3
# constant zoo
mutation_rate = 2
num_schedules_to_retain = 3
tournament_size = 4
database = r"D:\projects\genetic\data\schedule_data.db"

class my_random():
    '''generator function for LCG method of random number generation'''
    seed = int(time.time())

    def __init__(self):
        pass

    def random_int(self):
        while True:
            self.seed = (48271*self.seed) % ((2 ** 31) - 1)
            yield self.seed

    def random_choice(self, deck, randomness):
        return deck[randomness % len(deck)]


def sorter(moves):
    # merge sort
    if len(moves) > 1:
        mid_point = len(moves) // 2
        left_half = moves[:mid_point]
        right_half = moves[mid_point:]
        sorter(left_half)
        sorter(right_half)
        i, j, k = 0, 0, 0
        while (i < len(left_half)) and (j < len(right_half)):
            if left_half[i].get_fitness() < right_half[j].get_fitness():
                moves[k] = left_half[i]
                i += 1
            else:
                moves[k] = right_half[j]
                j += 1
            k += 1
        while i < len(left_half):
            moves[k] = left_half[i]
            i += 1
            k += 1
        while j < len(right_half):
            moves[k] = right_half[j]
            j += 1
            k += 1
    return moves


p = my_random()


class data:
    ''' 
    imports data about school from database
    e.g. teachers, time periods, rooms, classes etc 
    hard coded atm
    '''
    def create_connection(self, db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except sqlite3.Error as e:
            print(e)
        return conn

    def __init__(self):
        # temporary hardcoded data
        # self.departments = ["Maths", "Physics", "Chemistry", "Computing"]
        # self.times = ["M-F 0825-0925", "M-F 0930-1030",
        #               "M-F 1035-1135", "M-F 1140-1240", "M-T 1345-1445"]
        # self.teachers['''list comp to make teacher objects''']
        conn = self.create_connection(database)
        with conn:
            

class population:
    '''The competing schedules '''

    def __init__(self):
        self.pop = []


class schedule:
    ''' when, where and with who the class is'''

    def __init__(self):
        self.classes = []

    def start(self):
        '''randomly generates a fully schedule, with random variables(teacher, room, time) for each class like y9 set 4 maths or y12 physics'''
        my_data = data()
        for i in my_data.departments:
            for j in range(7, 14):
                self.classes.append(teaching_class(p.random_choice(my_data.teachers, next(p.random_int())), p.random_choice(
                    my_data.times, next(p.random_int())), p.random_choice(my_data.rooms, next(p.random_int())), "year " + str(j) + i))

    def get_fitness(self):
        '''returns a calculation of the schedule instance's fitness'''
        # 1/conflicts


class room:
    def __init__(self, size, room_type):
        self.size = size
        self.room_type = room_type


class Subject:
    def __init__(self, name, qualified_teachers, maximum_students):
        self.name = name
        self.qualified_teachers = qualified_teachers
        self.maximum_students = maximum_students


class teaching_class:
    def __init__(self, teacher, time, room, subject):
        self.teacher = teacher
        self.time = time
        self.room = room
        self.subject = subject


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
    ''' child randomly inherits each characteristic from parents @50/50'''
    child = schedule()
    child.classes = [schedule1.classes[i] if (next(p.random_int(
    )) % 2 == 0) else schedule2.classes[i] for i in range(len(schedule1.classes))]
    return child


def muatate(self, schedule):
    random_schedule = schedule.start()
    for i in enumerate(schedule.classes):
        if p.random_choice(range(10), next(p.random_int()) < mutation_rate):
            schedule.classes[i[0]] = random_schedule.classes[i[0]]
    return schedule


def tournament_selection(self, population):
    ''' Selects K, in this case 3, random schedules from the inputted schedules and ranks them by fitness and returns them'''
    tournament_attendees = population()
    tournament_attendees.pop = [p.random_choice(
        population.pop, next(p.random_int())) for _ in range(tournament_size)]
    return sorter(tournament_attendees.pop)


class table_display:
    ''' '''
