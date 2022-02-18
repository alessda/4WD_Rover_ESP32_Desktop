# Copyright (c) 2020 Francesco Pio Squillante
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

class hcsr04:
    
    @c_native("HCRS04_readDistanceRaw", ["csrc/hcsr04.c"], [])
    def _getDistanceRaw(trig, echo):
        pass
    
    def getDistanceRaw(self):
        return hcsr04._getDistanceRaw(self.trigger, self.echo)
    
    def getDistanceCM(self):
        return self.getDistanceRaw() / 58
    
    def getDistanceINCH(self):
        return self.getDistanceRaw() / 148
    
    def __init__(self, trigger, echo):
        self.trigger = trigger
        self.echo = echo
        
        pinMode(self.trigger, OUTPUT)
        pinMode(self.echo, INPUT)