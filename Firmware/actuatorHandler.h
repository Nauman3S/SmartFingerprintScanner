// Motor A

// Setting PWM properties
const int freq = 30000;
const int pwmChannel = 0;
const int resolution = 8;
int dutyCycle = 200;

void setupActuator()
{
    // sets the pins as outputs:
    pinMode(motor1Pin1, OUTPUT);
    pinMode(motor1Pin2, OUTPUT);
    pinMode(enable1Pin, OUTPUT);

    // configure LED PWM functionalitites
    ledcSetup(pwmChannel, freq, resolution);

    // attach the channel to the GPIO to be controlled
    ledcAttachPin(enable1Pin, pwmChannel);
}

void moveActator(int dir, int speed)
{
     if (speed <= 255)
    {
        ledcWrite(pwmChannel, speed);
        Serial.print("Duty cycle: ");
        Serial.println(dutyCycle);
    }
    if (dir == FORWARD)
    {
        Serial.println("Moving Forward");
        digitalWrite(motor1Pin1, LOW);
        digitalWrite(motor1Pin2, HIGH);
    }

    if (dir == STOP)
    {
        // Stop the DC motor
        Serial.println("Motor stopped");
        digitalWrite(motor1Pin1, LOW);
        digitalWrite(motor1Pin2, LOW);
    }
    if (dir == BACKWARD)
    {
        // Move DC motor backwards at maximum speed
        Serial.println("Moving Backwards");
        digitalWrite(motor1Pin1, HIGH);
        digitalWrite(motor1Pin2, LOW);
    }

   
}
