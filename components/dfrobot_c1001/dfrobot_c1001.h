#pragma once

#include "esphome/core/component.h"
#include "esphome/components/uart/uart.h"
#include "esphome/components/sensor/sensor.h"

// Include the original DFRobot library
#include "DFRobot_HumanDetection.h"

namespace esphome {
namespace dfrobot_c1001 {

/**
 * @brief Wrapper class for the DFRobot C1001 sensor library.
 *        Inherits from ESPHome's Component and UARTDevice.
 */
class DFRobotC1001Component : public Component, public uart::UARTDevice {
 public:
  // ---------------------------------------------------------
  // Setters for sensor pointers (called from sensor.py)
  // ---------------------------------------------------------
  void set_presence_sensor(sensor::Sensor *s) { presence_sensor_ = s; }
  void set_movement_sensor(sensor::Sensor *s) { movement_sensor_ = s; }
  void set_distance_sensor(sensor::Sensor *s) { distance_sensor_ = s; }
  void set_heart_rate_sensor(sensor::Sensor *s) { heart_rate_sensor_ = s; }
  void set_breathe_value_sensor(sensor::Sensor *s) { breathe_sensor_ = s; }

  // Optional: set a custom polling interval in ms
  void set_update_interval(uint32_t interval) { this->update_interval_ = interval; }

  // ---------------------------------------------------------
  // Standard ESPHome methods
  // ---------------------------------------------------------
  void setup() override;
  void loop() override;

 protected:
  // The actual DFRobot sensor driver
  DFRobot_HumanDetection *human_ = nullptr;

  // Sensor references
  sensor::Sensor *presence_sensor_{nullptr};
  sensor::Sensor *movement_sensor_{nullptr};
  sensor::Sensor *distance_sensor_{nullptr};
  sensor::Sensor *heart_rate_sensor_{nullptr};
  sensor::Sensor *breathe_sensor_{nullptr};

  // Polling interval
  uint32_t update_interval_{15000};  // default 15s
  uint32_t last_update_{0};

  // Private helper to read data from the sensor
  void read_sensors_();
};

}  // namespace dfrobot_c1001
}  // namespace esphome
