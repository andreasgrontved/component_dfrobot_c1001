# dfrobot_c1001/sensor.py

DOMAIN = "dfrobot_c1001"

import esphome.config_validation as cv
from esphome import codegen as cg
from esphome.components import sensor, uart
from esphome.const import CONF_ID, CONF_BAUD_RATE, UNIT_EMPTY, ICON_EMPTY

# ------------------------------------------------------------------
# 1) DECLARE OUR NAMESPACE AND CLASS
# ------------------------------------------------------------------
# This matches the C++ namespace: esphome::dfrobot_c1001
CODEOWNERS = ["@your_github_username"]
DEPENDENCIES = ["uart"]   # We use the UART bus
AUTO_LOAD = ["sensor"]    # So sensor entities can be created

dfrobot_ns = cg.esphome_ns.namespace("dfrobot_c1001")
# Our main class in C++ is DFRobotC1001Component
DFRobotC1001Component = dfrobot_ns.class_("DFRobotC1001Component", cg.Component, uart.UARTDevice)

# ------------------------------------------------------------------
# 2) DEFINE CONFIG KEYS
# ------------------------------------------------------------------
CONF_PRESENCE_SENSOR = "presence_sensor"
CONF_MOVEMENT_SENSOR = "movement_sensor"
CONF_DISTANCE_SENSOR = "distance_sensor"
CONF_HEART_RATE_SENSOR = "heart_rate_sensor"
CONF_BREATHE_VALUE_SENSOR = "breathe_value_sensor"

# The schema below dictates how the user can configure in YAML.
CONFIG_SCHEMA = (
    cv.Schema({
        cv.GenerateID(): cv.declare_id(DFRobotC1001Component),
        # In addition to standard UART settings, we let them specify sensors:
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
    # Extend the UART device schema so user can specify tx_pin, rx_pin, baud_rate, etc.:
    .extend(uart.UART_DEVICE_SCHEMA)
)

# ------------------------------------------------------------------
# 3) "to_code" FUNCTION
#     This is called by ESPHome to generate the backing C++ code
#     from the user’s YAML config.
# ------------------------------------------------------------------
def to_code(config):
    # Create the main component object
    var = cg.new_Pvariable(config[CONF_ID])
    cg.add(var.set_update_interval(15000))  # Default 15s update rate (optional)

    # Register it as a Component and a UART device
    cg.register_component(var, config)
    uart.register_uart_device(var, config)

    # If the user specified a "presence_sensor" in YAML,
    # create a Sensor object and tell the C++ code about it.
    if CONF_PRESENCE_SENSOR in config:
        sens = yield sensor.new_sensor(config[CONF_PRESENCE_SENSOR])
        cg.add(var.set_presence_sensor(sens))

    if CONF_MOVEMENT_SENSOR in config:
        sens = yield sensor.new_sensor(config[CONF_MOVEMENT_SENSOR])
        cg.add(var.set_movement_sensor(sens))

    if CONF_DISTANCE_SENSOR in config:
        sens = yield sensor.new_sensor(config[CONF_DISTANCE_SENSOR])
        cg.add(var.set_distance_sensor(sens))

    if CONF_HEART_RATE_SENSOR in config:
        sens = yield sensor.new_sensor(config[CONF_HEART_RATE_SENSOR])
        cg.add(var.set_heart_rate_sensor(sens))

    if CONF_BREATHE_VALUE_SENSOR in config:
        sens = yield sensor.new_sensor(config[CONF_BREATHE_VALUE_SENSOR])
        cg.add(var.set_breathe_value_sensor(sens))
