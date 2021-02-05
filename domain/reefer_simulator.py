import csv
import sys
import json
import datetime
import random
import numpy as np
import pandas as pd
import os
import logging


'''
Simulate the metrics for a Reefer container according to the type of simulation.
Each simulation type is a different method.
The variables that changes are Co2, O2, power and temperature

'''

# Define constants

CO2_LEVEL = 7  # in percent - above 12 is bad
O2_LEVEL = 21  # in percent - below 12 it is bad
NITROGEN_LEVEL = 78  # in percent
POWER_LEVEL = 2.7  # in kW
HUMIDITY_LEVEL = 30  # in percent
MAX_RECORDS = 1000
PER_NB_WRONG_RECORDS = .17  # percentage of wrong records to produce
NB_WRONG_RECORDS = int(MAX_RECORDS * PER_NB_WRONG_RECORDS)
NB_WRONG_RECORD_SERIE = 3

DEFROST_LEVEL = 7   # Common timing periods were 6, 8, 12 and 24 hours.
METRIC_FREQUENCY = "5min"

SIGMA_BASE = 1
products = {'P01': {'d': 'covid-19', 'type': 1, 'T': -50.0, 'H': 40},
            'covid-19': {'d': 'covid-19', 'type': 1, 'T': -50.0, 'H': 40},
            'P02': {'d': 'covid-05', 'type': 2, 'T': 6.0, 'H': 60},
            'P03': {'d': 'ebola', 'type': 1, 'T': 4.0, 'H': 40},
            'P04': {'d': 'yellow-fever', 'type': 2.0, 'T': 6.0, 'H': 40},
            'P05': {'d': 'vid-20', 'type': 1, 'T': 5.0, 'H': 40}}


def _generateTimestamps(nb_records: int, start_time: datetime.datetime):
    '''
    Generate a timestamp column for a dataframe of results.

    Arguments:
        nb_records: Number of rows to generate
        start_time: Timestamp of first row, or None to use the current time.
            By convention, each subsequent row will be exactly METRIC_FREQUENCY minutes later..

    Returns a Pandas Series object, suitable for use as a column or index
    '''
    if start_time is None:
        start_time = datetime.datetime.today()
    return pd.date_range(start_time, periods=nb_records, freq=METRIC_FREQUENCY).strftime("%Y-%m-%d %H:%M:%S")


def _generateStationaryCols(nb_records: int, cid: str, product_id: str):
    '''
    Generate the columns of the simulator output that can be generated by
    stationary (stateless) processes.

    Note that the values of these columns may be replaced with values from
    a stateful generator in the data generation process.

    Arguments:
        nb_records: How many rows of data to generate
        cid: Container ID string
        content_type: integer key representing what's in the container, or
            None to have this function pick a random integer
        tgood: Target temperature

    Returns a Pandas dataframe with the indicated set of columns populated.
    '''
    logging.info("Generate " + str(nb_records) +
                 " records for " + products[product_id]['d'])
    cols = {}

    # Constant values
    cols["container_id"] = np.repeat(cid, nb_records)
    cols["product_id"] = np.repeat(product_id, nb_records)
    cols["temperature"] = np.random.normal(
        products[product_id]['T'], SIGMA_BASE, size=nb_records)
    cols["target_temperature"] = np.repeat(
        products[product_id]['T'], nb_records)
    cols["ambiant_temperature"] = np.random.normal(
        20, SIGMA_BASE, size=nb_records)
    cols["kilowatts"] = np.random.normal(
        POWER_LEVEL, SIGMA_BASE, size=nb_records)
    cols["time_door_open"] = np.repeat(0, nb_records)
    content_type = products[product_id]['type']
    cols["content_type"] = np.repeat(content_type, nb_records)
    cols["defrost_cycle"] = np.random.randint(
        3, DEFROST_LEVEL, size=nb_records)
    # Normally-distributed floating-point values
    cols["oxygen_level"] = np.random.normal(
        O2_LEVEL, SIGMA_BASE, size=nb_records)
    cols["nitrogen_level"] = np.random.normal(
        NITROGEN_LEVEL, SIGMA_BASE, size=nb_records)
    cols["humidity_level"] = np.random.normal(
        products[product_id]['H'], SIGMA_BASE, size=nb_records)
    cols["carbon_dioxide_level"] = np.random.normal(
        CO2_LEVEL, SIGMA_BASE, size=nb_records)
    cols["fan_1"] = np.repeat(True, nb_records)
    cols["fan_2"] = np.repeat(True, nb_records)
    cols["fan_3"] = np.repeat(True, nb_records)
    cols["latitude"] = np.repeat("37.8226902168957", nb_records)
    cols["longitude"] = np.repeat("-122.324895", nb_records)
    # Uniform values
    cols["maintenance_required"] = np.repeat(0, nb_records)
    return pd.DataFrame(data=cols)


def _generateFaultyValue(df: pd.DataFrame,
                         nb_wrong_records: int = int(
                             NB_WRONG_RECORDS * PER_NB_WRONG_RECORDS),
                         nb_times: int = NB_WRONG_RECORD_SERIE,
                         attribute: str = "kilowatts",
                         mean: float = 0, sigma: float = 3):
    """
    Generate nb_wrong_records records nb_times times in the data set on a specific column,
    named with the attribute value.

    Arguments:
    - dataframe containing the normal data
    - number of wrong records to create in the given data set. The wrong records will be sequential
    - number of time it needs to generate the wrong records.
    - normal distribution mean : this mean can be 2 or 3 times higher than the normal mean
    - normal distribution sigma: this could be 1 to 6 sigma
    """
    initial_index = 0
    for time in range(0, nb_times):
        start_index = random.randint(
            initial_index, df[attribute].size - nb_wrong_records)
        for i in range(start_index, start_index + nb_wrong_records):
            df.at[i, attribute] = np.random.normal(mean, sigma)
        initial_index = start_index


class ReeferSimulator:
    # Constants used elsewhere in the application
    SIMUL_POWEROFF = "poweroff"
    SIMUL_CO2 = "co2sensor"
    SIMUL_O2 = "o2sensor"
    SIMUL_TEMPERATURE = "temperature"
    NORMAL = "normal"
    TEMP_GROWTH = "tempgrowth"
    # try to match the name in the database too
    COLUMN_NAMES = ["container_id", "measurement_time", "product_id",
                    "temperature", "target_temperature", "ambiant_temperature",
                    "kilowatts", "time_door_open",
                    "content_type", "defrost_cycle",
                    "oxygen_level",
                    "nitrogen_level",
                    "humidity_level",
                    "carbon_dioxide_level",
                    "fan_1", "fan_2", "fan_3", "latitude", "longitude", "maintenance_required"]

    def generateNormalRecords(self, cid: str = "C01",
                              nb_records: int = MAX_RECORDS,
                              product_id: str = 'P02',
                              start_time: datetime.datetime = None
                              ):
        """
        Generate n records using clean telemetries

        Arguments:
            cid: Container ID
            nb_records: Number of records to generate
            product_id: product identified from the table above
            start_time: Timestamp of first row, or None to use the current time.
                By convention, each subsequent row will be exactly 15 minutes
                later.
        Returns a Pandas dataframe.
        """
        logging.info("Generating records for normal behavior")
        df = _generateStationaryCols(nb_records, cid, product_id)
        df["measurement_time"] = _generateTimestamps(nb_records, start_time)
        return df[ReeferSimulator.COLUMN_NAMES]

    def generateNormalTuples(self,
                               cid: str = "C01",
                               nb_records: int = MAX_RECORDS,
                               product_id: str = 'P02',
                               start_time: datetime.datetime = None):
        '''
        Generate an array of tuples with reefer container values

        Returns an array of Python tuples, where the order of fields in the tuples
        the same as that in ReeferSimulator.COLUMN_NAMES.
        '''
        df = self.generateNormalRecords(
            cid, nb_records, product_id, start_time)
        return list(df.to_records(index=False))
    
    def generatePowerOffRecords(self,
                                cid: str = "C01",
                                nb_records: int = MAX_RECORDS,
                                product_id: str = 'P02',
                                start_time: datetime.datetime = None):
        '''
        Generate n records for training and test set for the power off
        simulation.
        Power off will be off for n records in the total n times withing the total records.

        Arguments:
            cid: Container ID
            nb_records: Number of records to generate
            tgood: Mean temperature to generate when power is NOT off
            content_type: ID of the type of stuff in the container, or None
                to choose a random number
            start_time: Timestamp of first row, or None to use the current time.
                By convention, each subsequent row will be exactly 15 minutes
                later.
        Returns a Pandas dataframe.
        '''
        logging.info("Generating records for some poweroff")
        df = self.generateNormalRecords(
            cid, nb_records, product_id, start_time)
        _generateFaultyValue(df,
                             int(nb_records * PER_NB_WRONG_RECORDS),
                             NB_WRONG_RECORD_SERIE,
                             "kilowatts", POWER_LEVEL, 3 * SIGMA_BASE)
        for i in range(0, df['kilowatts'].size - 1):
            if (df.at[i, "kilowatts"] <= 0 and df.at[i + 1, "kilowatts"] <= 0):
                df.at[i, "maintenance_required"] = 1
                df.at[i, "fan_1"] = False
                df.at[i, "fan_2"] = False
                df.at[i, "fan_3"] = False
        return df[ReeferSimulator.COLUMN_NAMES]

    def generatePowerOffTuples(self,
                               cid: str = "C01",
                               nb_records: int = MAX_RECORDS,
                               product_id: str = 'P02',
                               start_time: datetime.datetime = None):
        '''
        Generate an array of tuples with reefer container values

        Returns an array of Python tuples, where the order of fields in the tuples
        the same as that in ReeferSimulator.COLUMN_NAMES.
        '''
        df = self.generatePowerOffRecords(
            cid, nb_records, product_id, start_time)
        return list(df.to_records(index=False))

    def generateCo2Records(self,
                           cid: str = "C01",
                           nb_records: int = MAX_RECORDS,
                           product_id: str = 'P02',
                           start_time: datetime.datetime = None):
        '''
        Generate a dataframe of training data for CO2 sensor malfunctions.

        Returns a Pandas dataframe with the schema given in
        ReeferSimulator.COLUMN_NAMES.
        '''
        logging.info("Generating records for co2 sensor issue")
        df = self.generateNormalRecords(
            cid, nb_records, product_id, start_time)
        _generateFaultyValue(df,
                             int(nb_records * PER_NB_WRONG_RECORDS),
                             NB_WRONG_RECORD_SERIE,
                             "carbon_dioxide_level",
                             1.5 * CO2_LEVEL, 3 * SIGMA_BASE)
        for i in range(0, df['carbon_dioxide_level'].size):
            currentCO2 = df.at[i, "carbon_dioxide_level"]
            df.at[i, "maintenance_required"] = 1 if (
                (currentCO2 > 12) or (currentCO2 < 0)) else 0
        return df[ReeferSimulator.COLUMN_NAMES]

    def generateCo2Tuples(self,
                          cid: str = "C01",
                          nb_records: int = MAX_RECORDS,
                          product_id: str = 'P02',
                          start_time: datetime.datetime = None):
        '''
        Generate a dataframe of training data for CO2 sensor malfunctions.

        Arguments:

        Returns an array of Python tuples, where the order of fields in the tuples
        the same as that in ReeferSimulator.COLUMN_ORDER.
        '''
        df = self.generateCo2Records(cid, nb_records, product_id, start_time)
        return list(df.to_records(index=False))

    def generateO2Records(self,
                          cid: str = "C01",
                          nb_records: int = MAX_RECORDS,
                          product_id: str = 'P02',
                          start_time: datetime.datetime = None):
        '''
        Generate a dataframe of training data for O2 sensor malfunctions.

        Returns a Pandas dataframe with the schema given in
        ReeferSimulator.COLUMN_NAMES.
        '''
        logging.info("Generating records for O2 sensor issue")
        df = self.generateNormalRecords(
            cid, nb_records, product_id, start_time)
        _generateFaultyValue(df,
                             int(nb_records * PER_NB_WRONG_RECORDS),
                             NB_WRONG_RECORD_SERIE,
                             "oxygen_level",
                             O2_LEVEL-10, 2*SIGMA_BASE)
        for i in range(0, df['oxygen_level'].size):
            currentO2 = df.at[i, "oxygen_level"]
            df.at[i, "maintenance_required"] = 1 if (currentO2 < 12) else 0
        return df[ReeferSimulator.COLUMN_NAMES]

    def generateO2Tuples(self,
                         cid: str = "C01",
                         nb_records: int = MAX_RECORDS,
                         product_id: str = 'P02',
                         start_time: datetime.datetime = None):
        df = self.generateO2Records(cid, nb_records, product_id, start_time)
        return list(df.to_records(index=False))

    def generateTemperatureRecords(self,
                                   cid: str = "C01",
                                   nb_records: int = MAX_RECORDS,
                                   product_id: str = 'P01',
                                   start_time: datetime.datetime = None):
        '''
        Generate a dataframe of training data for temperature sensor malfunctions.

        Returns a Pandas dataframe with the schema given in
        ReeferSimulator.COLUMN_NAMES.
        '''
        logging.info("Generating records for Temperature sensor issue")
        df = self.generateNormalRecords(
            cid, nb_records, product_id, start_time)
        _generateFaultyValue(df,
                             int(nb_records * PER_NB_WRONG_RECORDS),
                             NB_WRONG_RECORD_SERIE,
                             "temperature",
                             products[product_id]['T'] + 20, 3 * SIGMA_BASE)
        for i in range(0, df['temperature'].size):
            currentT = df.at[i, "temperature"]
            df.at[i, "maintenance_required"] = 1 if (
                np.abs(products[product_id]['T'] - currentT) > 20) else 0
        return df[ReeferSimulator.COLUMN_NAMES]

    def generateTemperatureTuples(self,
                                  cid: str = "C01",
                                  nb_records: int = MAX_RECORDS,
                                  product_id: str = 'P01',
                                  start_time: datetime.datetime = None):
        df = self.generateTemperatureRecords(
            cid, nb_records, product_id, start_time)
        return list(df.to_records(index=False))

    def generateTemperatureGrowthTuples(self,
                                  cid: str = "C01",
                                  nb_records: int = MAX_RECORDS,
                                  product_id: str = 'P01',
                                  start_time: datetime.datetime = None):
        df = self.generateTemperatureGrowthRecords(
            cid, nb_records, product_id, start_time)
        return list(df.to_records(index=False))

    def generateTemperatureGrowthRecords(self,
                                   cid: str = "C01",
                                   nb_records: int = MAX_RECORDS,
                                   product_id: str = 'P01',
                                   start_time: datetime.datetime = None):
        '''
        Generate a dataframe of training data for temperature sensor malfunctions.

        Returns a Pandas dataframe with the schema given in
        ReeferSimulator.COLUMN_NAMES.
        '''
        logging.info("Generating records for Temperature growth")
        df = self.generateNormalRecords(
            cid, nb_records, product_id, start_time)
        startAt=np.round(nb_records/3)
        for i in range(startAt, df['temperature'].size):
            df.at[i, "temperature"]+=2
        return df[ReeferSimulator.COLUMN_NAMES]

if __name__ == '__main__':
    simul = ReeferSimulator()
    df1 = simul.generatePowerOffRecords("C300", 100, "P01")
    df2 = simul.generateCo2Records("C300", 200, "P01")
    df3 = simul.generateTemperatureRecords("C300", 200, "P01")
    df = df1.append(df2).append(df3)
    for i in list(df.to_records()):
        logging.info(i)
