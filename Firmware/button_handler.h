void setupButtons()
{
    pinMode(BTN1_PIN, INPUT_PULLUP);
    pinMode(BTN2_PIN, INPUT_PULLUP);
    pinMode(BTN3_PIN, INPUT_PULLUP);
    pinMode(BTN4_PIN, INPUT_PULLUP);
    pinMode(BTN5_PIN, INPUT_PULLUP);
    pinMode(BTN6_PIN, INPUT_PULLUP);
}

uint8_t getButtonState(int btn)
{
    if (btn == BTN_1)
    {
        digitalRead(BTN1_PIN);
    }
    else if (btn == BTN_2)
    {
        digitalRead(BTN2_PIN);
    }
    else if (btn == BTN_3)
    {
        digitalRead(BTN3_PIN);
    }

    else if (btn == BTN_4)
    {
        digitalRead(BTN4_PIN);
    }

    else if (btn == BTN_5)
    {
        digitalRead(BTN5_PIN);
    }

    else if (btn == BTN_6)
    {
        digitalRead(BTN6_PIN);
    }
}