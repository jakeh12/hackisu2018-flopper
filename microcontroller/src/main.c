#include <stdbool.h>
#include <stdint.h>

#include "inc/tm4c123gh6pm.h"
#include "inc/hw_memmap.h"
#include "driverlib/rom.h"
#include "driverlib/timer.h"
#include "driverlib/sysctl.h"
#include "driverlib/gpio.h"

#define LED_RED GPIO_PIN_1
#define LED_BLUE GPIO_PIN_2
#define LED_GREEN GPIO_PIN_3

// 80 MHz / 4 kHz = 20000 (-1)
//#define TIMER1A_PRESCALER 20000-1 // will fire every 0.25 ms

// TODO: DELETE LATER, VISIBLE FLASH
#define TIMER1A_PRESCALER 20000000-1

volatile int i = 0;

void Timer1AHandler(void) {
  ROM_TimerIntClear(TIMER1_BASE, TIMER_A);
  i++; 
  if (i % 2 == 0)
  	ROM_GPIOPinWrite(GPIO_PORTF_BASE, LED_RED | LED_GREEN, LED_GREEN | ~LED_RED);
  else
    ROM_GPIOPinWrite(GPIO_PORTF_BASE, LED_RED | LED_GREEN, LED_RED | ~LED_GREEN);
}

void configureTimer1A() {
  ROM_SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER1);
  ROM_TimerConfigure(TIMER1_BASE, TIMER_CFG_PERIODIC);
  ROM_TimerLoadSet(TIMER1_BASE, TIMER_A, TIMER1A_PRESCALER); 
  ROM_IntEnable(INT_TIMER1A);
  ROM_TimerIntEnable(TIMER1_BASE, TIMER_TIMA_TIMEOUT);
  ROM_TimerEnable(TIMER1_BASE, TIMER_A);
}

int main() {
    ROM_IntMasterDisable(); 
    ROM_SysCtlClockSet(SYSCTL_SYSDIV_2_5 | SYSCTL_USE_PLL| SYSCTL_OSC_MAIN | SYSCTL_XTAL_16MHZ);
    ROM_SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOF);
    ROM_GPIOPinTypeGPIOOutput(GPIO_PORTF_BASE, LED_RED | LED_BLUE | LED_GREEN);
    configureTimer1A();
    ROM_IntMasterEnable();
    while(1);
}
