#include <Python.h>
#include <wiringPi.h>
//This one is not exposed
extern void delayMicrosecondsHard (unsigned int howLong);

static PyObject * dcc_rpi_encoder_c_send_bit_array(PyObject *self, PyObject *args){
    const char *bit_array;
    const int count;
    const unsigned int bit_one_part_duration;
    const unsigned int bit_zero_part_duration;
    int i;

    if (!PyArg_ParseTuple(args, "siII", &bit_array, &count,
                          &bit_one_part_duration,
                          &bit_zero_part_duration))
        return NULL;

    for (i = 0; i < count; i++){
        while (*bit_array){
            if (*bit_array++ == '0'){
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
