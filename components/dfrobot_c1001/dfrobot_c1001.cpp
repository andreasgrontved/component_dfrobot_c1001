#include "dfrobot_c1001.h"

namespace esphome {
namespace dfrobot_c1001 {

void DFRobotC1001Component::setup() {
  // Create the DFRobot library object, using our underlying ESPHome UART stream
  this->human_detection_ = new DFRobot_HumanDetection(this->parent_);

  // Initialize the sensor
  uint8_t ret = this->human_detection_->begin();
  if (ret == 0) {
    ESP_LOGE("dfrobot_c1001", "Failed to initialize DFRobot C1001 sensor!");
  } else {
    ESP_LOGI("dfrobot_c1001", "DFRobot C1001 sensor initialized successfully.");
  }

  // If you want to set the working mode, do it here:
  // this->human_detection_->configWorkMode(DFRobot_HumanDetection::eSleepMode);
}

void DFRobotC1001Component::loop() {
  // Periodically poll the sensor
  uint32_t now = millis();
  if (now - this->last_update_ >= this->update_interval_) {
    this->last_update_ = now;
    this->read_sensors_();
  }
}

void DFRobotC1001Component::read_sensors_() {
  // Example: read presence
  if (this->presence_sensor_ != nullptr) {
    float val = this->human_detection_->smHumanData(DFRobot_HumanDetection::eHumanPresence);
    this->presence_sensor_->publish_state(val);
  }

  // Movement
  if (this->movement_sensor_ != nullptr) {
    float val = this->human_detection_->smHumanData(DFRobot_HumanDetection::eHumanMovement);
    this->movement_sensor_->publish_state(val);
  }

  // Distance
  if (this->distance_sensor_ != nullptr) {
    float val = this->human_detection_->smHumanData(DFRobot_HumanDetection::eHumanDistance);
    this->distance_sensor_->publish_state(val);
  }

  // Heart Rate
  if (this->heart_rate_sensor_ != nullptr) {
    float val = this->human_detection_->getHeartRate();
    this->heart_rate_sensor_->publish_state(val);
  }

  // Breathe Value
  if (this->breathe_value_sensor_ != nullptr) {
    float val = this->human_detection_->getBreatheValue();
    this->breathe_value_sensor_->publish_state(val);
  }
}

}  // namespace dfrobot_c1001
}  // namespace esphome
