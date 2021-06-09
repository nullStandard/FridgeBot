#include "cam_pins.h"
#include "BluetoothSerial.h"
#include "esp_camera.h"

BluetoothSerial SerialBT;

void setup() 
{
  Serial.begin(115200);
  initBT();
  camPinsFile::loadCamera();
}

void initBT()
{
  if(!SerialBT.begin("FridgeCam"))
  {
    Serial.println("An error occurred initializing Bluetooth");
    ESP.restart();
  }
  else
  {
    Serial.println("Bluetooth initialized");
  }

  SerialBT.register_callback(btCallback);
  Serial.println("The device started, now you can pair it with bluetooth");
}

void btCallback(esp_spp_cb_event_t event, esp_spp_cb_param_t *param)
{
  if(event == ESP_SPP_SRV_OPEN_EVT)
  {
    Serial.println("Client Connected!");
  }
  else if(event == ESP_SPP_DATA_IND_EVT)
  {
    Serial.printf("Data callback was invoked: \"%s\" from Raspberry!", 
                   String(*param->data_ind.data));
    capture();
  }
}

void capture()
{
  camera_fb_t *fb = NULL;
  esp_err_t res = ESP_OK;
  fb = esp_camera_fb_get();
  if (!fb)
    {
      Serial.println("Camera capture failed");
      esp_camera_fb_return(fb);
      return;
    }
    else
    {
      Serial.println("Captured!");
      if(fb->format != PIXFORMAT_JPEG)
      {
        Serial.println("Not JPEG, aborting!");
        return;
      }

      SerialBT.write(fb->buf, fb->len);
      SerialBT.flush();
      esp_camera_fb_return(fb);
    }
}

void loop() { }
