#include <Python.h>
#include <stdio.h>
#include "utils.h"

/*
 * modulename.functionname -> modulename_functionname
 */

/*
 * implementation of blocks.get_blocks()
 */
static PyObject * blocks_get_blocks(PyObject * self, PyObject * args)
{

  PyObject * retval;

  /*
   * using independent function
   */
  unsigned char * b = get_blocks();

  /*
   * Conversion of C object to Python object
   */
  retval = (PyObject *) Py_BuildValue("[BBBBB]", b[0], b[1], b[2], b[3], b[4]);

  free(b);

  return retval;

}

/*
 * List of python module elements
 */
PyMethodDef blocksMethods[] = {
  {"get_blocks", blocks_get_blocks, METH_VARARGS, "blocks methods"},
  { NULL, NULL, 0, NULL },
};

/*
 * module definition
 */
static struct PyModuleDef blocksmodule = {
   PyModuleDef_HEAD_INIT,
   "blocks",     /* name of module */
   NULL,         /* module documentation, may be NULL */
   -1,           /* size of per-interpreter state of the module,
                    or -1 if the module keeps state in global variables. */
   blocksMethods /* */
};

/*
 * Init Function
 */
PyMODINIT_FUNC PyInit_blocks(void)
{
    return PyModule_Create(&blocksmodule);
}
