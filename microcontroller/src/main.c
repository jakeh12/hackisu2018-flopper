#include <stdbool.h>
#include <stdint.h>

#include "inc/tm4c123gh6pm.h"
#include "inc/hw_memmap.h"
#include "driverlib/rom.h"
#include "driverlib/timer.h"
#include "driverlib/sysctl.h"
#include "driverlib/gpio.h"
#include "driverlib/uart.h"
#include "driverlib/pin_map.h"

// 80 MHz / 4 kHz = 20000 (-1)
#define TIMER1A_PRESCALER 4000 // will fire every 0.1 ms
#define NUM_OF_FLOPPYS 10
#define MAX_NUM_OF_STEPS 140

const int freq_count_lookup[60] = {
1,
1,
1,
1,
1,
1,
1,
1,
1,
1,
1,
1,
1,
1,
1,
1,
1,
1,
1,
1,
1,
182,
172,
162,
153,
144,
136,
129,
121,
115,
108,
102,
96,
91,
86,
81,
76,
72,
68,
64,
61,
57,
54,
51,
48,
45,
43,
40,
38,
36,
34,
32,
30,
29,
27,
26,
24,
23,
1,
1
};

volatile int counter = 0;

volatile int stepCounters[NUM_OF_FLOPPYS];
volatile int frequencyDividers[NUM_OF_FLOPPYS];
volatile int frequencyOn[NUM_OF_FLOPPYS];

volatile int floppy_initialized = 0;

void pinToggle(int port, int pin) {
      ROM_GPIOPinWrite(port, pin, ROM_GPIOPinRead(port, pin) ^ pin);
}

void toggleDir(int outputNumber) {
  switch(outputNumber) {
  case 0:
      pinToggle(GPIO_PORTA_BASE, GPIO_PIN_2);
      break;
    case 1:
      pinToggle(GPIO_PORTA_BASE, GPIO_PIN_3);
      break;
    case 2:
      pinToggle(GPIO_PORTA_BASE, GPIO_PIN_4);
      break;
    case 3:
      pinToggle(GPIO_PORTB_BASE, GPIO_PIN_6);
      break;
    case 4:
      pinToggle(GPIO_PORTB_BASE, GPIO_PIN_7);
      break;
    case 5:
      pinToggle(GPIO_PORTE_BASE, GPIO_PIN_0);
      break;
    case 6:
      pinToggle(GPIO_PORTB_BASE, GPIO_PIN_2);
      break;
    case 7:
      pinToggle(GPIO_PORTA_BASE, GPIO_PIN_7);
      break;
    case 8:
      pinToggle(GPIO_PORTD_BASE, GPIO_PIN_6);
      break;
    case 9:
      pinToggle(GPIO_PORTC_BASE, GPIO_PIN_7);
      break;
    default:
      	break;

  }
}

void initialize_arrays(void) {
	int i;
	for (i = 0; i < NUM_OF_FLOPPYS; i++) {
		frequencyDividers[i] = 45;
		frequencyOn[i] = 1;
		stepCounters[i] = 0;
        toggleDir(i);	
  }
}

void checkDir(int outputNumber) {
  if (stepCounters[outputNumber] > MAX_NUM_OF_STEPS) {
    toggleDir(outputNumber);
    stepCounters[outputNumber] = 0;
  }
}

void toggleOutput(int outputNumber) {
  switch(outputNumber) {
    case 0:
      pinToggle(GPIO_PORTC_BASE, GPIO_PIN_6);
      break;
    case 1:
      pinToggle(GPIO_PORTC_BASE, GPIO_PIN_5);
      break;
    case 2:
      pinToggle(GPIO_PORTC_BASE, GPIO_PIN_4);
      break;
    case 3:
      pinToggle(GPIO_PORTB_BASE, GPIO_PIN_3);
      break;
    case 4:
      pinToggle(GPIO_PORTF_BASE, GPIO_PIN_3);
      break;
    case 5:
      pinToggle(GPIO_PORTF_BASE, GPIO_PIN_2);
      break;
    case 6:
      pinToggle(GPIO_PORTF_BASE, GPIO_PIN_1);
      break;
    case 7:
      pinToggle(GPIO_PORTE_BASE, GPIO_PIN_3);
      break;
    case 8:
      pinToggle(GPIO_PORTE_BASE, GPIO_PIN_2);
      break;
    case 9:
      pinToggle(GPIO_PORTE_BASE, GPIO_PIN_1);
      break;
    default:
      	break;
  }
}

void Timer1AHandler(void) {
  ROM_TimerIntClear(TIMER1_BASE, TIMER_A);
  
  int i;
  for (i = 0; i < NUM_OF_FLOPPYS; i++) {
    if (counter % frequencyDividers[i] == 0 && frequencyOn[i]) {
      toggleOutput(i);
      if (floppy_initialized) {
      checkDir(i);
      }
      stepCounters[i]++;
    }
  }
  counter++;
  if (floppy_initialized == 0 && counter > 16000) {
    floppy_initialized = 1;
    int i;
         for (i = 0; i < NUM_OF_FLOPPYS; i++) {
                 frequencyDividers[i] = 1;
                 frequencyOn[i] = 0;
                 stepCounters[i] = 0;
                 toggleDir(i);
         }
  } 
}

void UART0Handler(void) {
    uint32_t ui32Status;
    ui32Status = ROM_UARTIntStatus(UART0_BASE, true);
    ROM_UARTIntClear(UART0_BASE, ui32Status);

    int byte_counter = 0;
    char byte_array[2];
    while(ROM_UARTCharsAvail(UART0_BASE))
    {
      byte_array[byte_counter] = ROM_UARTCharGetNonBlocking(UART0_BASE);
      byte_counter++;
      if (byte_counter == 2)
        break; 
    }
      int note = (int)byte_array[0];
      int turn_on = (int)((byte_array[1] >> 7) & 0x01);
      int floppy = (int)(byte_array[1] & 0x7F);
      
      frequencyDividers[floppy] = freq_count_lookup[note];
      frequencyOn[floppy] = turn_on;

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
    
    ROM_SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOA);
    ROM_GPIOPinTypeGPIOOutput(GPIO_PORTA_BASE, GPIO_PIN_2 | GPIO_PIN_3 | GPIO_PIN_4 |  GPIO_PIN_7);
    
    ROM_SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOB);
    ROM_GPIOPinTypeGPIOOutput(GPIO_PORTB_BASE, GPIO_PIN_2 | GPIO_PIN_3 | GPIO_PIN_6 | GPIO_PIN_7);
    
    ROM_SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOC);
    ROM_GPIOPinTypeGPIOOutput(GPIO_PORTC_BASE, GPIO_PIN_4 | GPIO_PIN_5 | GPIO_PIN_6 | GPIO_PIN_7);
    
    ROM_SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOD);
    ROM_GPIOPinTypeGPIOOutput(GPIO_PORTD_BASE, GPIO_PIN_6);
    
    ROM_SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOE);
    ROM_GPIOPinTypeGPIOOutput(GPIO_PORTE_BASE, GPIO_PIN_0 | GPIO_PIN_1 | GPIO_PIN_2 | GPIO_PIN_3);
    
    ROM_SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOF);
    ROM_GPIOPinTypeGPIOOutput(GPIO_PORTF_BASE, GPIO_PIN_1 | GPIO_PIN_2 | GPIO_PIN_3);
    
    ROM_SysCtlPeripheralEnable(SYSCTL_PERIPH_UART0);

    ROM_GPIOPinConfigure(GPIO_PA0_U0RX);
    ROM_GPIOPinConfigure(GPIO_PA1_U0TX);
    ROM_GPIOPinTypeUART(GPIO_PORTA_BASE, GPIO_PIN_0 | GPIO_PIN_1);

    //
    // Configure the UART for 115,200, 8-N-1 operation.
    //
    ROM_UARTConfigSetExpClk(UART0_BASE, ROM_SysCtlClockGet(), 115200,
                            (UART_CONFIG_WLEN_8 | UART_CONFIG_STOP_ONE |
                             UART_CONFIG_PAR_NONE));
    
    initialize_arrays();
    
    configureTimer1A();
    
    
    ROM_IntEnable(INT_UART0);
    ROM_UARTIntEnable(UART0_BASE, UART_INT_RX | UART_INT_RT);
    
    ROM_IntMasterEnable();

    while(1){}
}
