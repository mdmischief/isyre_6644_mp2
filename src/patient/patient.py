from math import ceil
import numpy as np


class Patient:

    def __init__(
        self,
        id: int,
        name: str = None,
        infectious_probability: float = 0.02,
        # mask_protection_factor_generators=[0.0, 0.01],
        # social_distance_protection_factor_generators=[0.0, 0.01],
        # handwash_distance_protection_factor_generators=[0.0, 0.01],
        mask_protection_factor_generators=[0.25, 0.75],
        social_distance_protection_factor_generators=[0.25, 0.35],
        handwash_distance_protection_factor_generators=[0.25, 0.35],
        incubation_period_generators=[0.4, 1.0, 5],
        infectious_period_generators=[0.4, 1.0, 5],
        vaccination_protection_factor_generators=[0.1, 0.5]
    ):
        """Patient for use in Flu Pandemic simulation.

        Args:
            id (int): ID of this instantiation.
            name (str, optional): Name of this instantiation. Defaults to None.
            infectious_probability (float, optional): Probability of infection. Defaults to 0.02.
            mask_protection_factor_generators (list, optional): Bounds for RV generation. Defaults to [0.25, 0.75].
            social_distance_protection_factor_generators (list, optional): Bounds for RV generation. Defaults to [0.25, 0.35].
            handwash_distance_protection_factor_generators (list, optional): Bounds for RV generation. Defaults to [0.25, 0.35].
            incubation_period_generators (list, optional): Bounds and scaling factor C for RV generation. Defaults to [0.4, 1.0, 5].
            infectious_period_generators (list, optional): Bounds and scaling factor C for RV generation. Defaults to [0.4, 1.0, 5].
            vaccination_protection_factor_generators (list, optional): Bounds for RV generation - assumption of two doses required stacking 0.2..1.0 effectivity. Defaults to [0.1, 0.5].
        """
        self.id = id
        self.name = name
        self.infectious_probability = infectious_probability
        self.mask_protection_factor_generators = mask_protection_factor_generators
        self.social_distance_protection_factor_generators = social_distance_protection_factor_generators
        self.handwash_distance_protection_factor_generators = handwash_distance_protection_factor_generators
        self.incubation_period_generators = incubation_period_generators
        self.infectious_period_generators = infectious_period_generators
        self.vaccination_protection_factor_generators = vaccination_protection_factor_generators

        # Track protection factors: [mask, social_distance, handwashing]
        _ml, _mu = mask_protection_factor_generators
        _sl, _su = social_distance_protection_factor_generators
        _hl, _hu = handwash_distance_protection_factor_generators
        self.protection_factors = 1+np.random.uniform(_ml, _mu) * 1+np.random.uniform(_sl, _su) * 1+np.random.uniform(_hl, _hu)

        # Generate a duration for incubation - defaults give a 2..5 day period
        _lower, _upper, c = self.incubation_period_generators
        self.incubation_period = ceil(np.random.uniform(_lower, _upper)*c)

        # Generate a duration for being infectious - defaults give a 2..5 day period
        _lower, _upper, c = self.infectious_period_generators
        self.infectious_period = ceil(np.random.uniform(_lower, _upper)*c)

        # Track vaccination protection factor
        self.vaccination_protection_factor = 1

        # Track which PT caused the infection
        self.infected_by = None

        # Track when they were infected
        self.infected_on = None

        # self.infected_on + self.incubation_period
        self.infectious_on = None

        self.infectious_start = -1
        self.infectious_end = 2**31

        # Track vaccination timehack
        self.vaccinated_on = np.zeros(0)

    # def __str__(self):
    #     return f'Patient ID {self.id} named {self.name} has infectious probability {self.infectious_probability}'

    def __repr__(self):
        return f'Patient(id={self.id}, name={self.name}, infectious_probability={self.infectious_probability}, mask_protection_factor_generators={self.mask_protection_factor_generators}, social_distance_protection_factor_generators={self.social_distance_protection_factor_generators}, handwash_distance_protection_factor_generators={self.handwash_distance_protection_factor_generators}, incubation_period_generators={self.incubation_period_generators}, infectious_period_generators={self.infectious_period_generators}, vaccination_protection_factor_generators={self.vaccination_protection_factor_generators})'

    # def infection_status(self):
    def __str__(self):
        return f'Patient ID {self.id} named {self.name} infected by {self.infected_by} on {self.infected_on} and will be infectious from {self.infectious_start} until {self.infectious_end}.'

    def vaccinate(
        self,
        simulation_timehack: int
    ):
        """Vaccinate the Patient.

        Args:
            simulation_timehack (int): Timehack for tracking when vaccination occurred.
        """
        _lower, _upper = self.vaccination_protection_factor_generators
        protection_factor = np.random.uniform(_lower, _upper)

        self.vaccination_protection_factor += protection_factor

        self.vaccinated_on = np.append(self.vaccinated_on, simulation_timehack)

    def encounter(
        self,
        peer,
        simulation_timehack: int
    ):
        """Simulate the interation between two Patients.

        Args:
            peer (Patient): Peer of type Patient.
            simulation_timehack (int): Timehack for tracking when encounter occurred.
        """
        # If Peer is self do nothing
        # If Peer is not infectious do nothing
        # print(f'Self check {self.id == peer.id} Infected_By {peer.infected_by is None} clock {not (self.infectious_start <= simulation_timehack <= self.infectious_end)}')

        if self.id == peer.id:
            return

        if peer.infected_by is None:
            return

        if not (peer.infectious_start <= simulation_timehack <= peer.infectious_end):
            return

        if self.infected_on is not None and self.infected_by < simulation_timehack:
            return

        # Generate the probability of infection based on the Peer/Subject attributes
        rand = np.random.uniform(0, 1) * self.protection_factors * self.vaccination_protection_factor

        if rand <= self.infectious_probability:
            self.infected_by = peer.id
            self.infected_on = simulation_timehack
            self.infectious_start = self.infected_on + self.incubation_period
            self.infectious_end = self.infectious_start + self.infectious_period

    def patient_zero(self):
        self.infected_by = self.id
        self.infected_on = 0
        self.infectious_start = self.infected_on + self.incubation_period
        self.infectious_end = self.infectious_start + self.infectious_period
