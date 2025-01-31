# dfrobot_c1001/dfrobot_c1001.py

"""
ESPHome domain-based integration for the DFRobot C1001 (SEN0623) Radar Sensor
"""

# 1. Declare the domain name so ESPHome maps 'dfrobot_c1001:' in YAML to this file
DOMAIN = "dfrobot_c1001"

import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor, uart
from esphome.const import (
    CONF_ID,
    UNIT_EMPTY,
    ICON_EMPTY,
)

CODEOWNERS = ["@your_github_username"]
DEPENDENCIES = ["uart"]   # We need UART for sensor communication
AUTO_LOAD = ["sensor"]    # So we can create sensor entities

# 2. Create a namespace that matches your C++ code namespace: esphome::dfrobot_c1001
dfrobot_ns = cg.esphome_ns.namespace("dfrobot_c1001")
DFRobotC1001Component = dfrobot_ns.class_(
    "DFRobotC1001Component",  # C++ class name
    cg.Component,             # Inherits from esphome::Component
    uart.UARTDevice           # Inherits from esphome::uart::UARTDevice
)

# 3. Config keys in YAML
CONF_PRESENCE_SENSOR = "presence_sensor"
CONF_MOVEMENT_SENSOR = "movement_sensor"
CONF_DISTANCE_SENSOR = "distance_sensor"
CONF_HEART_RATE_SENSOR = "heart_rate_sensor"
CONF_BREATHE_VALUE_SENSOR = "breathe_value_sensor"

# 4. Top-level CONFIG_SCHEMA for 'dfrobot_c1001:'
CONFIG_SCHEMA = (
    cv.Schema({
        cv.GenerateID(): cv.declare_id(DFRobotC1001Component),
        # Optional sensors the user can enable
        cv.Optional(CONF_PRESENCE_SENSOR): sensor.sensor_schema(
            unit_of_measurement=UNIT_EMPTY,
            icon=ICON_EMPTY
        ),
        cv.Optional(CONF_MOVEMENT_SENSOR): sensor.sensor_schema(
            unit_of_measurement=UNIT_EMPTY,
            icon=ICON_EMPTY
        ),
        cv.Optional(CONF_DISTANCE_SENSOR): sensor.sensor_schema(
            unit_of_measurement=UNIT_EMPTY,
            icon="mdi:ruler"
        ),
        cv.Optional(CONF_HEART_RATE_SENSOR): sensor.sensor_schema(
            unit_of_measurement="bpm",
            icon="mdi:heart-pulse"
        ),
        cv.Optional(CONF_BREATHE_VALUE_SENSOR): sensor.sensor_schema(
            unit_of_measurement=UNIT_EMPTY,
            icon="mdi:lungs"
        ),
    })
    # Extend the UART schema so user can specify tx_pin, rx_pin, baud_rate, etc.
    .extend(uart.UART_DEVICE_SCHEMA)
)

# 5. 'to_code' builds the actual C++ object from the user's YAML config
async def to_code(config):
    # Create the main C++ instance
    var = cg.new_Pvariable(config[CONF_ID])

    # Example: set a default 15s update interval
    cg.add(var.set_update_interval(15000))

    # Register as a standard ESPHome component & a UART device
    await cg.register_component(var, config)
    await uart.register_uart_device(var, config)

    # For each optional sensor in the config, create & attach it
    if CONF_PRESENCE_SENSOR in config:
        sens = await sensor.new_sensor(config[CONF_PRESENCE_SENSOR])
        cg.add(var.set_presence_sensor(sens))

    if CONF_MOVEMENT_SENSOR in config:
        sens = await sensor.new_sensor(config[CONF_MOVEMENT_SENSOR])
        cg.add(var.set_movement_sensor(sens))

    if CONF_DISTANCE_SENSOR in config:
        sens = await sensor.new_sensor(config[CONF_DISTANCE_SENSOR])
        cg.add(var.set_distance_sensor(sens))

    if CONF_HEART_RATE_SENSOR in config:
        sens = await sensor.new_sensor(config[CONF_HEART_RATE_SENSOR])
        cg.add(var.set_heart_rate_sensor(sens))

    if CONF_BREATHE_VALUE_SENSOR in config:
        sens = await sensor.new_sensor(config[CONF_BREATHE_VALUE_SENSOR])
        cg.add(var.set_breathe_value_sensor(sens))
