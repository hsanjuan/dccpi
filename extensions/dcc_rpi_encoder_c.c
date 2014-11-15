/*
    dcc_rpi_encoder_c.c - Uses wiringPI delayMicrosecondsHard() to
    generate a DCC protocol signal.

    Copyright (C) 2014  Hector Sanjuan

    This file is part of "dccpi".

    "dccpi" is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    "dccpi" is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
*/

#include <Python.h>
#include <wiringPi.h>
//This one is not exposed
extern void delayMicrosecondsHard (unsigned int howLong);

static PyObject * dcc_rpi_encoder_c_send_bit_array(PyObject *self, PyObject *args){
    char const *bit_array;
    char const *bit_array_pos;
    const int count;
    const unsigned int bit_one_part_duration;
    const unsigned int bit_zero_part_duration;
    int i;

    if (!PyArg_ParseTuple(args, "siII", &bit_array, &count,
                          &bit_one_part_duration,
                          &bit_zero_part_duration))
        return NULL;

    for (i = 0; i < count; i++){
        bit_array_pos = bit_array;
        while (*bit_array_pos){ //string will be null terminated
            if (*bit_array_pos++ == '0'){
                //Encode 0 with 100us for each part
                digitalWrite(0, LOW);
                delayMicrosecondsHard(bit_zero_part_duration);
                digitalWrite(0, HIGH);
                delayMicrosecondsHard(bit_zero_part_duration);
            }
            else {
                //Encode 1 with 58us for each part
                digitalWrite(0, LOW);
                delayMicrosecondsHard(bit_one_part_duration);
                digitalWrite(0, HIGH);
                delayMicrosecondsHard(bit_one_part_duration);
            }
        }
    }

    Py_RETURN_NONE;
}

static PyMethodDef DCCRPiEncoderMethods[] = {
    {"send_bit_array", dcc_rpi_encoder_c_send_bit_array, METH_VARARGS,
     "Send some bits to the tracks"},
    {NULL, NULL, 0, NULL} /* Sentinel - whatever that means */
};

PyMODINIT_FUNC initdcc_rpi_encoder_c(void){
    wiringPiSetup();
    pinMode(0, OUTPUT);
    Py_InitModule("dcc_rpi_encoder_c", DCCRPiEncoderMethods);
}
