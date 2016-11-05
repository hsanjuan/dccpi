/*
    dcc_rpi_encoder_c.c - Uses wiringPI delayMicrosecondsHard() to
    generate a DCC protocol signal.

    Copyright (C) 2016  Hector Sanjuan

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
    along with "dccpi".  If not, see <http://www.gnu.org/licenses/>.
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
    const unsigned int packet_separation;
    int i;

    if (!PyArg_ParseTuple(args, "siIII", &bit_array, &count,
                          &bit_one_part_duration,
                          &bit_zero_part_duration,
                          &packet_separation))
        return NULL;

    for (i = 0; i < count; i++){
        bit_array_pos = bit_array;
        while (*bit_array_pos){ //string will be null terminated
            if (*bit_array_pos == '0'){
                //Encode 0 with 100us for each part
                digitalWrite(0, LOW);
                delayMicrosecondsHard(bit_zero_part_duration);
                digitalWrite(0, HIGH);
                delayMicrosecondsHard(bit_zero_part_duration);
            }
            else if (*bit_array_pos == '1'){
                //Encode 1 with 58us for each part
                digitalWrite(0, LOW);
                delayMicrosecondsHard(bit_one_part_duration);
                digitalWrite(0, HIGH);
                delayMicrosecondsHard(bit_one_part_duration);
            } else {
                // Interpret this case as packet end char.
                // Standard says we should wait 5ms at least
                // and 30ms max between packets.
                digitalWrite(0, LOW);
                delay(packet_separation); //ms
                digitalWrite(0, HIGH);
            }
            bit_array_pos++;
        }
    }

    Py_RETURN_NONE;
}

static PyObject * dcc_rpi_encoder_c_brake(PyObject *self, PyObject *args){
    const int brake;
    if (!PyArg_ParseTuple(args, "I", &brake))
        return NULL;

    if (brake == 0)
        digitalWrite(2, LOW);
    else
        digitalWrite(2, HIGH);

    Py_RETURN_NONE;
}

static PyMethodDef DCCRPiEncoderMethods[] = {
    {"send_bit_array", dcc_rpi_encoder_c_send_bit_array, METH_VARARGS,
     "Send some bits to the tracks"},
    {"brake", dcc_rpi_encoder_c_brake, METH_VARARGS,
     "Enable or disable a brake signal"},
    {NULL, NULL, 0, NULL} /* Sentinel - whatever that means */
};


#if PY_MAJOR_VERSION >= 3
  static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "dcc_rpi_encoder_c",  /* m_name */
    NULL,                 /* m_doc */
    -1,                   /* m_size */
    DCCRPiEncoderMethods, /* m_methods */
    NULL,                 /* m_reload */
    NULL,                 /* m_traverse */
    NULL,                 /* m_clear */
    NULL,                 /* m_free */
  };
#endif

static PyObject * moduleinit(void){
    PyObject *m;

    wiringPiSetup();
    pinMode(0, OUTPUT);
    pinMode(2, OUTPUT);
    digitalWrite(2, HIGH); //Brake

#if PY_MAJOR_VERSION >= 3
    m = PyModule_Create(&moduledef);
#else
    m = Py_InitModule("dcc_rpi_encoder_c", DCCRPiEncoderMethods);
#endif

    if (m == NULL)
        return NULL;

    return m;
}

#if PY_MAJOR_VERSION < 3
    PyMODINIT_FUNC initdcc_rpi_encoder_c(void){
        moduleinit();
    }
#else
    PyMODINIT_FUNC PyInit_dcc_rpi_encoder_c(void){
        return moduleinit();
    }
#endif
