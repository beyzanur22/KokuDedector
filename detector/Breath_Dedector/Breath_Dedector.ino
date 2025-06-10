void setup() {
  Serial.begin(9600); // Bilgisayar ile haberleşmeyi başlat
}

void loop() {
  int sensorValue = analogRead(A0); // A0 pininden analog veri oku
  Serial.println(sensorValue);      // Seri port üzerinden gönder
  delay(100); // Her 100 ms'de bir veri gönder
}