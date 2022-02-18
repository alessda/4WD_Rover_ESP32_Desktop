/*
 * Copyright (c) 2020 Francesco Pio Squillante

 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

#define ZERYNTH_PRINTF

#include "zerynth.h"

#define TicksPerMicros  (_system_frequency / 1000000)

void pseudoSleepForMicros(uint32_t micros){
    uint32_t startTicks = *vosTicks();
    
    while (*vosTicks() - startTicks < (TicksPerMicros * micros));
}

uint32_t pseudoICU(int pin, int mode, uint32_t timeout){
    uint32_t startTicks = *vosTicks();
    
    while (*vosTicks() - startTicks < (TicksPerMicros * timeout))
        if(!!vhalPinRead(pin) != !!mode)
            break;
    
    return (*vosTicks() - startTicks) / TicksPerMicros;
}

err_t HCRS04_readDistanceRaw(int32_t nArgs, PObject *self, PObject **args, PObject **res) {
    int32_t triggerPin, echoPin;
    
    if (parse_py_args("ii", nArgs, args, &triggerPin, &echoPin) != 2)
        return ERR_TYPE_EXC;
    
    vosSysLock();
    vhalPinWrite(triggerPin, 0);
    vhalPinWrite(triggerPin, 1);
    pseudoSleepForMicros(10);
    vhalPinWrite(triggerPin, 0);
    
    uint32_t start_ticks = *vosTicks();
    
    while(!vhalPinRead(echoPin));
    
    *res = PSMALLINT_NEW(pseudoICU(echoPin, 1, 35000));
    
    vosSysUnlock();
    
    return ERR_OK;
}