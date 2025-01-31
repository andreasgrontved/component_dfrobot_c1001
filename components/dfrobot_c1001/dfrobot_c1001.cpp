#include "dfrobot_c1001.h"

namespace esphome {
namespace dfrobot_c1001 {

void DFRobotC1001Component::setup() {
  // Construct the DFRobot driver with the underlying UART Stream
  this->human_ = new DFRobot_HumanDetection(this->parent_);

  // Initialize
  uint8_t ret = this->human_->begin();
  if (ret == 0) {
    ESP_LOGE("dfrobot_c1001", "Failed to initialize DFRobot C1001!");
  } else {
    ESP_LOGI("dfrobot_c1001", "DFRobot C1001 sensor initialized.");
  }
}

void DFRobotC1001Component::loop() {
  uint32_t now = millis();
  if (now - this->last_update_ >= this->update_interval_) {
    this->last_update_ = now;
    this->read_sensors_();
  }
}

void DFRobotC1001Component::read_sensors_() {
  // Example: presence
  if (this->presence_sensor_ != nullptr) {
    float presence = this->human_->smHumanData(DFRobot_HumanDetection::eHumanPresence);
    this->presence_sensor_->publish_state(presence);
  }

  // movement
  if (this->movement_sensor_ != nullptr) {
    float movement = this->human_->smHumanData(DFRobot_HumanDetection::eHumanMovement);
    this->movement_sensor_->publish_state(movement);
  }

  // distance
  if (this->distance_sensor_ != nullptr) {
    float distance = this->human_->smHumanData(DFRobot_HumanDetection::eHumanDistance);
    this->distance_sensor_->publish_state(distance);
  }

  // heart rate
  if (this->heart_rate_sensor_ != nullptr) {
    float hr = this->human_->getHeartRate();
    this->heart_rate_sensor_->publish_state(hr);
  }

  // breathe
  if (this->breathe_sensor_ != nullptr) {
    float breathe = this->human_->getBreatheValue();
    this->breathe_sensor_->publish_state(breathe);
  }
}

}  // namespace dfrobot_c1001
}  // namespace esphome
