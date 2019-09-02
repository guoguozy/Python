# Problem Set 4: Simulating the Spread of Disease and Bacteria Population Dynamics
# Name: Guo Ziyu
# Collaborators (Discussion): None
# Time: thirty minutes

import math
import numpy as np
import pylab as pl
import random

##########################
# End helper code
##########################


class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleBacteria
    and ResistantBacteria classes to indicate that a bacteria cell does not
    reproduce. You should use NoChildException as is; you do not need to
    modify it or add any code.
    """


def make_one_curve_plot(x_coords, y_coords, x_label, y_label, title):
    """
    Makes a plot of the x coordinates and the y coordinates with the labels
    and title provided.

    Args:
        x_coords (list of floats): x coordinates to graph
        y_coords (list of floats): y coordinates to graph
        x_label (str): label for the x-axis
        y_label (str): label for the y-axis
        title (str): title for the graph
    """
    pl.figure()
    pl.plot(x_coords, y_coords)
    pl.xlabel(x_label)
    pl.ylabel(y_label)
    pl.title(title)
    pl.show()


def make_two_curve_plot(x_coords, y_coords1, y_coords2, y_name1, y_name2,
                        x_label, y_label, title):
    """
    Makes a plot with two curves on it, based on the x coordinates with each of
    the set of y coordinates provided.

    Args:
        x_coords (list of floats): the x coordinates to graph
        y_coords1 (list of floats): the first set of y coordinates to graph
        y_coords2 (list of floats): the second set of y-coordinates to graph
        y_name1 (str): name describing the first y-coordinates line
        y_name2 (str): name describing the second y-coordinates line
        x_label (str): label for the x-axis
        y_label (str): label for the y-axis
        title (str): the title of the graph
    """
    pl.figure()
    pl.plot(x_coords, y_coords1, label=y_name1)
    pl.plot(x_coords, y_coords2, label=y_name2)
    pl.legend()
    pl.xlabel(x_label)
    pl.ylabel(y_label)
    pl.title(title)
    pl.show()


##########################
# PROBLEM 1
##########################


class SimpleBacteria(object):
    """A simple bacteria cell with no antibiotic resistance"""

    def __init__(self, birth_prob, death_prob):
        """
        Args:
            birth_prob (float in [0, 1]): Maximum possible reproduction
                probability
            death_prob (float in [0, 1]): Maximum death probability
        """
        self.birth_prob = birth_prob
        self.death_prob = death_prob

    def is_killed(self):
        """
        Stochastically determines whether this bacteria cell is killed in
        the patient's body at a time step, i.e. the bacteria cell dies with
        some probability equal to the death probability each time step.

        Returns:
            bool: True with probability self.death_prob, False otherwise.
        """
        return True if random.random() <= self.death_prob else False
        # 随机生成数来与self.death_prob比较

    def reproduce(self, pop_density):
        """
        Stochastically determines whether this bacteria cell reproduces at a
        time step. Called by the update() method in the Patient and
        TreatedPatient classes.

        The bacteria cell reproduces with probability
        self.birth_prob * (1 - pop_density).

        If this bacteria cell reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleBacteria (which has the same
        birth_prob and death_prob values as its parent).

        Args:
            pop_density (float): The population density, defined as the
                current bacteria population divided by the maximum population

        Returns:
            SimpleBacteria: A new instance representing the offspring of
                this bacteria cell (if the bacteria reproduces). The child
                should have the same birth_prob and death_prob values as
                this bacteria.

        Raises:
            NoChildException if this bacteria cell does not reproduce.
        """
        if random.random() <= self.birth_prob * (1 - pop_density):
            # 返回一个细菌类
            return SimpleBacteria(self.birth_prob, self.death_prob)
        else:  # 返回一个异常
            raise NoChildException


class Patient(object):
    """
    Representation of a simplified patient. The patient does not take any
    antibiotics and his/her bacteria populations have no antibiotic resistance.
    """

    def __init__(self, bacteria, max_pop):
        """
        Args:
            bacteria (list of SimpleBacteria): The bacteria in the population
            max_pop (int): Maximum possible bacteria population size for
                this patient
        """
        self.bacteria = bacteria
        self.max_pop = max_pop

    def get_total_pop(self):
        """
        Gets the size of the current total bacteria population.

        Returns:
            int: The total bacteria population
        """
        return len(self.bacteria)

    def update(self):
        """
        Update the state of the bacteria population in this patient for a
        single time step. update() should execute the following steps in
        this order:

        1. Determine whether each bacteria cell dies (according to the
           is_killed method) and create a new list of surviving bacteria cells.

        2. Calculate the current population density by dividing the surviving
           bacteria population by the maximum population. This population
           density value is used for the following steps until the next call
           to update()

        3. Based on the population density, determine whether each surviving
           bacteria cell should reproduce and add offspring bacteria cells to
           a list of bacteria in this patient. New offspring do not reproduce.

        4. Reassign the patient's bacteria list to be the list of surviving
           bacteria and new offspring bacteria

        Returns:
            int: The total bacteria population at the end of the update
        """
        bacteria_size = len(self.bacteria)  # 细菌个数
        not_kill_list = []  # 未死细菌
        new_bacteria = []  # 新细菌
        pop_density = 0
        for i in range(bacteria_size):
            if (not self.bacteria[i].is_killed()):
                not_kill_list.append(self.bacteria[i])  # 没死的加入

        pop_density = len(not_kill_list) / self.max_pop  # 更新现存量/最大生存数量
        for not_kill in not_kill_list:
            try:  # 分裂
                temp = not_kill.reproduce(pop_density)
                new_bacteria.append(temp)  # 加入新生组
            except NoChildException:
                continue
        self.bacteria = not_kill_list + new_bacteria
        return len(self.bacteria)


##########################
# PROBLEM 2
##########################


def calc_pop_avg(populations, n):
    """
    Finds the average bacteria population size across trials at time step n

    Args:
        populations (list of lists or 2D array): populations[i][j] is the
            number of bacteria in trial i at time step j

    Returns:F
        float: The average bacteria population size at time step n
    """
    total_sum = 0
    for i in range(len(populations)):
        total_sum += populations[i][n]
    return total_sum / len(populations)


def simulation_without_antibiotic(num_bacteria, max_pop, birth_prob,
                                  death_prob, num_trials):
    """
    Run the simulation and plot the graph for problem 2. No antibiotics
    are used, and bacteria do not have any antibiotic resistance.

    For each of num_trials trials:
        * instantiate a list of SimpleBacteria
        * instantiate a Patient using the list of SimpleBacteria
        * simulate changes to the bacteria population for 300 timesteps,
          recording the bacteria population after each time step. Note
          that the first time step should contain the starting number of
          bacteria in the patient

    Then, plot the average bacteria population size (y-axis) as a function of
    elapsed time steps (x-axis) You might find the make_one_curve_plot
    function useful.

    Args:
        num_bacteria (int): number of SimpleBacteria to create for patient
        max_pop (int): maximum bacteria population for patient
        birth_prob (float in [0, 1]): maximum reproduction
            probability
        death_prob (float in [0, 1]): maximum death probability
        num_trials (int): number of simulation runs to execute

    Returns:
        populations (list of lists or 2D array): populations[i][j] is the
            number of bacteria in trial i at time step j
    """
    populations = []
    for i in range(num_trials):
        bacteria_list = [
            SimpleBacteria(birth_prob, death_prob)
            for size in range(num_bacteria)
        ]  # 细菌列表
        patient = Patient(bacteria_list, max_pop)
        population = [num_bacteria]  # 各实验step的数目
        for j in range(300):  # 300次
            population.append(patient.update())
        populations.append(population)

    # 构造x,y变量 画图
    y = []
    for j in range(len(populations[0])):  # 求平均值
        y.append(calc_pop_avg(populations, j))
    x = np.arange(0.0, 301.0, 1.0)
    make_one_curve_plot(x, y, 'timestep', 'Average', 'Without Antibiotic')
    return populations


# When you are ready to run the simulation, uncomment the next line
populations = simulation_without_antibiotic(100, 1000, 0.1, 0.025, 50)

##########################
# PROBLEM 3
##########################


def calc_pop_std(populations, t):
    """
    Finds the standard deviation of populations across different trials
    at time step t by:
        * calculating the average population at time step t
        * compute average squared distance of the data points from the average
          and take its square root

    You may not use third-party functions that calculate standard deviation,
    such as numpy.std. Other built-in or third-party functions that do not
    calculate standard deviation may be used.

    Args:
        populations (list of lists or 2D array): populations[i][j] is the
            number of bacteria present in trial i at time step j
        t (int): time step

    Returns:
        float: the standard deviation of populations across different trials at
             a specific time step
    """
    average = calc_pop_avg(populations, t)  # 获取该次step的平均数目
    total_num = 0.0
    for i in range(len(populations)):
        total_num += (populations[i][t] - average)**2
    return ((total_num / len(populations))**0.5)


def calc_95_ci(populations, t):
    """
    Finds a 95% confidence interval around the average bacteria population
    at time t by:
        * computing the mean and standard deviation of the sample
        * using the standard deviation of the sample to estimate the
          standard error of the mean (SEM)
        * using the SEM to construct confidence intervals around the
          sample mean

    Args:
        populations (list of lists or 2D array): populations[i][j] is the
            number of bacteria present in trial i at time step j
        t (int): time step

    Returns:
        mean (float): the sample mean
        width (float): 1.96 * SEM

        I.e., you should return a tuple containing (mean, width)
    """
    mean = calc_pop_avg(populations, t)  # 平均值
    std = calc_pop_std(populations, t)  # 标准差
    width = 1.96 * (std / len(populations)**0.5)
    return mean, width


##########################
# PROBLEM 4
##########################


class ResistantBacteria(SimpleBacteria):
    """A bacteria cell that can have antibiotic resistance."""

    def __init__(self, birth_prob, death_prob, resistant, mut_prob):
        """
        Args:
            birth_prob (float in [0, 1]): reproduction probability
            death_prob (float in [0, 1]): death probability
            resistant (bool): whether this bacteria has antibiotic resistance
            mut_prob (float): mutation probability for this
                bacteria cell. This is the maximum probability of the
                offspring acquiring antibiotic resistance
        """
        SimpleBacteria.__init__(self, birth_prob, death_prob)
        self.resistant = resistant
        self.mut_prob = mut_prob

    def get_resistant(self):
        """Returns whether the bacteria has antibiotic resistance"""
        return self.resistant

    def is_killed(self):
        """Stochastically determines whether this bacteria cell is killed in
        the patient's body at a given time step.

        Checks whether the bacteria has antibiotic resistance. If resistant,
        the bacteria dies with the regular death probability. If not resistant,
        the bacteria dies with the regular death probability / 4.

        Returns:
            bool: True if the bacteria dies with the appropriate probability
                and False otherwise.
        """
        if self.resistant:  # 抗性 正常死亡
            return True if random.random() <= self.death_prob else False
        else:  # 降低到1/4死亡率
            return True if random.random() <= (self.death_prob / 4) else False

    def reproduce(self, pop_density):
        """
        Stochastically determines whether this bacteria cell reproduces at a
        time step. Called by the update() method in the TreatedPatient class.

        A surviving bacteria cell will reproduce with probability:
        self.birth_prob * (1 - pop_density).

        If the bacteria cell reproduces, then reproduce() creates and returns
        an instance of the offspring ResistantBacteria, which will have the
        same birth_prob, death_prob, and mut_prob values as its parent.

        If the bacteria has antibiotic resistance, the offspring will also be
        resistant. If the bacteria does not have antibiotic resistance, its
        offspring have a probability of self.mut_prob * (1-pop_density) of
        developing that resistance trait. That is, bacteria in less densely
        populated environments have a greater chance of mutating to have
        antibiotic resistance.

        Args:
            pop_density (float): the population density

        Returns:
            ResistantBacteria: an instance representing the offspring of
            this bacteria cell (if the bacteria reproduces). The child should
            have the same birth_prob, death_prob values and mut_prob
            as this bacteria. Otherwise, raises a NoChildException if this
            bacteria cell does not reproduce.
        """
        if random.random() <= self.birth_prob * (1 - pop_density):
            # 判断能否分裂
            if self.resistant:
                # 返回有抗性的子体
                return ResistantBacteria(self.birth_prob, self.death_prob,
                                         True, self.mut_prob)
            else:
                # 判断是否变异
                if random.random() <= self.mut_prob * (1 - pop_density):
                    # 变异，返回有抗性子体
                    return ResistantBacteria(self.birth_prob, self.death_prob,
                                             True, self.mut_prob)
                else:
                    return ResistantBacteria(self.birth_prob, self.death_prob,
                                             False, self.mut_prob)
        else:
            raise NoChildException


class TreatedPatient(Patient):
    """
    Representation of a treated patient. The patient is able to take an
    antibiotic and his/her bacteria population can acquire antibiotic
    resistance. The patient cannot go off an antibiotic once on it.
    """

    def __init__(self, bacteria, max_pop):
        """
        Args:
            bacteria: The list representing the bacteria population (a list of
                      bacteria instances)
            max_pop: The maximum bacteria population for this patient (int)

        This function should initialize self.on_antibiotic, which represents
        whether a patient has been given an antibiotic. Initially, the
        patient has not been given an antibiotic.

        Don't forget to call Patient's __init__ method at the start of this
        method.
        """
        Patient.__init__(self, bacteria, max_pop)
        self.antibiotic = False

    def set_on_antibiotic(self):
        """
        Administer an antibiotic to this patient. The antibiotic acts on the
        bacteria population for all subsequent time steps.
        """
        self.antibiotic = True

    def get_resist_pop(self):
        """
        Get the population size of bacteria cells with antibiotic resistance

        Returns:
            int: the number of bacteria with antibiotic resistance
        """
        resistance_num = 0
        for bacteria in self.bacteria:
            if bacteria.get_resistant():
                resistance_num += 1
        return resistance_num

    def update(self):
        """
        Update the state of the bacteria population in this patient for a
        single time step. update() should execute these actions in order:

        1. Determine whether each bacteria cell dies (according to the
           is_killed method) and create a new list of surviving bacteria cells.

        2. If the patient is on antibiotics, the surviving bacteria cells from
           (1) only survive further if they are resistant. If the patient is
           not on the antibiotic, keep all surviving bacteria cells from (1)

        3. Calculate the current population density. This value is used until
           the next call to update(). Use the same calculation as in Patient

        4. Based on this value of population density, determine whether each
           surviving bacteria cell should reproduce and add offspring bacteria
           cells to the list of bacteria in this patient.

        5. Reassign the patient's bacteria list to be the list of survived
           bacteria and new offspring bacteria

        Returns:
            int: The total bacteria population at the end of the update
        """
        bacteria_size = len(self.bacteria)  # 当前细菌数目
        not_kill_list = []  # 幸存组
        new_bacteria = []  # 新生组
        pop_density = 0  # 现存占数量上限的
        for i in range(bacteria_size):
            not_kill = True  # 用来判断死没死
            if self.bacteria[i].is_killed():  # 先判断会不会自然消亡
                not_kill = False
            else:  # 判断有没有加抗生素
                if self.antibiotic:
                    if not self.bacteria[i].get_resistant():  # 没抗性直接死
                        not_kill = False
            if not_kill:  # 没死可以分裂
                not_kill_list.append(self.bacteria[i])  # 加入幸存组

        pop_density = len(not_kill_list) / self.max_pop  # 更新比例
        for not_kill in not_kill_list:
            try:  # 尝试分裂
                temp = not_kill.reproduce(pop_density)
                new_bacteria.append(temp)  # 加入幸存组
            except NoChildException:
                continue
        self.bacteria = not_kill_list + new_bacteria
        return len(self.bacteria)


##########################
# PROBLEM 5
##########################


def simulation_with_antibiotic(num_bacteria, max_pop, birth_prob, death_prob,
                               resistant, mut_prob, num_trials):
    """
    Runs simulations and plots graphs for problem 4.

    For each of num_trials trials:
        * instantiate a list of ResistantBacteria
        * instantiate a patient
        * run a simulation for 150 timesteps, add the antibiotic, and run the
          simulation for an additional 250 timesteps, recording the total
          bacteria population and the resistance bacteria population after
          each time step

    Plot the average bacteria population size for both the total bacteria
    population and the antibiotic-resistant bacteria population (y-axis) as a
    function of elapsed time steps (x-axis) on the same plot. You might find
    the helper function make_two_curve_plot helpful

    Args:
        num_bacteria (int): number of ResistantBacteria to create for
            the patient
        max_pop (int): maximum bacteria population for patient
        birth_prob (float int [0-1]): reproduction probability
        death_prob (float in [0, 1]): probability of a bacteria cell dying
        resistant (bool): whether the bacteria initially have
            antibiotic resistance
        mut_prob (float in [0, 1]): mutation probability for the
            ResistantBacteria cells
        num_trials (int): number of simulation runs to execute

    Returns: a tuple of two lists of lists, or two 2D arrays
        populations (list of lists or 2D array): the total number of bacteria
            at each time step for each trial; total_population[i][j] is the
            total population for trial i at time step j
        resistant_pop (list of lists or 2D array): the total number of
            resistant bacteria at each time step for each trial;
            resistant_pop[i][j] is the number of resistant bacteria for
            trial i at time step j
    """
    populations = []  # 用于返回总细菌数列表
    resistant_pops = []  # 用于返回抗性细菌数列表
    for i in range(num_trials):
        bacteria_list = [
            ResistantBacteria(birth_prob, death_prob, False, mut_prob)
            for size in range(num_bacteria)
        ]  # 构造一个细菌列表
        patient = TreatedPatient(bacteria_list, max_pop)  # 实例化病人
        population = [num_bacteria]  # 单次试验各步骤细菌存活数目
        resistant_pop = [0]  # 单次试验各步骤抗性细菌存活数目
        for j in range(350):
            if j == 150:  # 150次之后服用抗生素
                patient.set_on_antibiotic()
            population.append(patient.update())  # 更新后存活数目
            resistant_pop.append(patient.get_resist_pop())  # 更新后抗性细菌存活数目
        populations.append(population)
        resistant_pops.append(resistant_pop)

    # 构造x，y轴变量列表
    y1 = []
    for j in range(len(populations[0])):  # 计算每个步骤的细菌存活平均数量
        y1.append(calc_pop_avg(populations, j))
    y2 = []
    for j in range(len(resistant_pops[0])):  # 计算每个步骤抗性细菌存活平均数量
        y2.append(calc_pop_avg(resistant_pops, j))
    x = np.arange(0.0, 351.0, 1.0)
    # print(len(x), ' ', len(y1))
    # 画表
    make_two_curve_plot(x, y1, y2, 'Total', 'Resistant', 'timestep', 'Average',
                        'With Antibiotic')
    return populations, resistant_pops


# When you are ready to run the simulations, uncomment the next lines one
# at a time
total_pop, resistant_pop = simulation_with_antibiotic(
    num_bacteria=100, max_pop=1000, birth_prob=0.3, death_prob=0.2, resistant=False, mut_prob=0.8, num_trials=50)
# print(total_pop, resistant_pop)
total_pop, resistant_pop = simulation_with_antibiotic(
    num_bacteria=100, max_pop=1000, birth_prob=0.17, death_prob=0.2, resistant=False, mut_prob=0.8, num_trials=50)
