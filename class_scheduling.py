
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

    def random_choice(self, deck):
        return deck[next(self.random_int()) % len(deck)]


def sorter(move):
    ''' merge sorter'''
    if len(move) > 1:
        mid_point = len(move) // 2
        left_half = move[:mid_point]
        right_half = move[mid_point:]
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
    return move


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
        self.timeslots = [[(u[0] + ' ' + str((i % 12))+":00").replace(" 0:00", " 12:00") for i in range(8, u[1])] for u in days]


   

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
                self.classes.append(teaching_class(p.random_choice(school_data.teachers), p.random_choice(school_data.timeslots), p.random_choice(school_data.rooms), i, "year "+j+" "+i))

    def get_fitness(self):
        '''returns a calculation of the schedule instance's fitness'''
        conflicts = 0
        for i in self.classes:
            for j in self.classes:
                if (i.time == j.time) and ((i.room == j.room) or (i.teacher == j.teacher)):
                    if i.name != j.name:
                        conflicts += 1
        
        return 1/conflicts
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
    def __init__(self, teacher, time, room, subject, name):
        self.teacher = teacher
        self.time = time
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
    ''' child randomly inherits each characteristic from parents @50/50'''
    child = schedule()
    child.classes = [schedule1.classes[i] if (next(p.random_int(
    )) % 2 == 0) else schedule2.classes[i] for i in range(len(schedule1.classes))]
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
