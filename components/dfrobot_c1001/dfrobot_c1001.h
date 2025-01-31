#pragma once

#include "esphome/core/component.h"
#include "esphome/components/uart/uart.h"
#include "esphome/components/sensor/sensor.h"

// Include the DFRobot library header
#include "DFRobot_HumanDetection.h"

namespace esphome {
namespace dfrobot_c1001 {

/**
 * @brief A C++ class that wraps the DFRobot_HumanDetection library
 *        and exposes sensor readings in ESPHome.
 *
 *        Inherits from:
 *        - esphome::Component (for setup, loop, etc.)
 *        - esphome::uart::UARTDevice (for serial comms)
 */
class DFRobotC1001Component : public Component, public uart::UARTDevice {
 public:
  DFRobotC1001Component() = default;

  // You can override if you want a custom poll rate from YAML, or you can leave it fixed.
  void set_update_interval(uint32_t update_interval) { this->update_interval_ = update_interval; }

  // Called by ESPHome once at startup
  void setup() override;

  // Called repeatedly. We'll poll periodically, so no continuous blocking.
  void loop() override;

  // ------------------------------------------------------------------
  // 1) Setters for sensor objects
  //    (called from the Python code in sensor.py)
  // ------------------------------------------------------------------
  void set_presence_sensor(sensor::Sensor *presence_sensor) { presence_sensor_ = presence_sensor; }
  void set_movement_sensor(sensor::Sensor *movement_sensor) { movement_sensor_ = movement_sensor; }
  void set_distance_sensor(sensor::Sensor *distance_sensor) { distance_sensor_ = distance_sensor; }
  void set_heart_rate_sensor(sensor::Sensor *heart_rate_sensor) { heart_rate_sensor_ = heart_rate_sensor; }
  void set_breathe_value_sensor(sensor::Sensor *breathe_sensor) { breathe_value_sensor_ = breathe_sensor; }

 protected:
  // We hold pointers to the sensors. If they're not configured, these pointers remain nullptr.
  sensor::Sensor *presence_sensor_{nullptr};
  sensor::Sensor *movement_sensor_{nullptr};
  sensor::Sensor *distance_sensor_{nullptr};
  sensor::Sensor *heart_rate_sensor_{nullptr};
  sensor::Sensor *breathe_value_sensor_{nullptr};

  // The underlying driver
  DFRobot_HumanDetection *human_detection_{nullptr};

  // Internal timer
  uint32_t update_interval_{15000};  // default 15s
  uint32_t last_update_{0};

  // ------------------------------------------------------------------
  // 2) Method to poll the sensor library
  // ------------------------------------------------------------------
  void read_sensors_();

};

}  // namespace dfrobot_c1001
}  // namespace esphome
