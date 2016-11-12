/*
 ** Copyright (c) 2016, Chris Stillson <stillson@gmail.com>
 ** All rights reserved.
 **
 ** Redistribution and use in source and binary forms, with or without
 ** modification, are permitted provided that the following conditions are met:
 **
 ** 1. Redistributions of source code must retain the above copyright notice,
 **    this list of conditions and the following disclaimer.
 ** 2. Redistributions in binary form must reproduce the above copyright notice,
 **    this list of conditions and the following disclaimer in the documentation
 **    and/or other materials provided with the distribution.
 **
 ** THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 ** AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 ** IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 ** ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
 ** LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 ** CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 ** SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 ** INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 ** CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 ** ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 ** POSSIBILITY OF SUCH DAMAGE.
 **/

/* CR objects */

#define PY_SSIZE_T_CLEAN
#include <stdint.h>
#include <errno.h>
#include <fcntl.h>

#include "Python.h"
#if OSVERSION < 1020000
#include "sys/capability.h"
#else
#include "sys/capsicum.h"
#endif
#include "sys/caprights.h"
#include "structmember.h"

#if PY_MAJOR_VERSION == 2
#define PYTHON2 1
#elif PY_MAJOR_VERSION == 3
#define PYTHON3 1
#else
#error requires python 2 or 3
#endif


#define AND &&
#define OR  ||

typedef struct {
    PyObject_HEAD
    PyObject            *pocket;
    cap_rights_t         cr_cap_rights;
} CRObject;

static PyTypeObject CR_Type;

#define CRObject_Check(v)      (Py_TYPE(v) == &CR_Type)

static CRObject *
newCRObject(PyObject *arg)
{
    CRObject *self;
    self = PyObject_New(CRObject, &CR_Type);
    if (self == NULL)
        return NULL;
    self->pocket        = NULL;
    return self;
}

/* CR methods */

static int
CR_init(CRObject *self, PyObject *args, PyObject *kwds)
{
    cap_rights_init(&self->cr_cap_rights);
    self->pocket = PyDict_New();

    return 0;
}

static void
CR_dealloc(CRObject *self)
{
    Py_XDECREF(self->pocket);
    PyObject_Del(self);
}


//part of capRights
static PyObject *
CR_set(CRObject *self, PyObject *args)
{
    int         rval = 0;
    int         n;
    PyObject   *item;
    PyObject   *new_caps;

    if (!PyArg_ParseTuple(args, "O!", &PyList_Type, &new_caps))
        return NULL;

    n = PyList_Size(new_caps);

    for (int i=0; i<n; i++)
    {
        item = PyList_GetItem(new_caps, i);
#if PYTHON2 == 1
        if (!PyInt_Check(item)) continue;
        cap_rights_set(&self->cr_cap_rights, PyInt_AsLong(item));
#else
        if (!PyLong_Check(item)) continue;
        cap_rights_set(&self->cr_cap_rights, PyLong_AsUnsignedLongLong(item));
#endif
    }

    return Py_BuildValue("i", rval);
}

static PyObject *
CR_clear(CRObject *self, PyObject *args)
{
    int         rval = 0;
    int         n;
    PyObject   *item;
    PyObject   *caps_list;

    if (!PyArg_ParseTuple(args, "O!", &PyList_Type, &caps_list))
        return NULL;

    n = PyList_Size(caps_list);

    for (int i=0; i<n; i++)
    {
        item = PyList_GetItem(caps_list, i);
#if PYTHON2 == 1
        if (!PyInt_Check(item)) continue;
        cap_rights_clear(&self->cr_cap_rights, PyInt_AsLong(item));
#else
        if (!PyLong_Check(item)) continue;
        cap_rights_clear(&self->cr_cap_rights, PyLong_AsUnsignedLong(item));
#endif
    }

    return Py_BuildValue("i", rval);
}

static PyObject *
CR_is_set(CRObject *self, PyObject *args)
{
    int                 rval = 0;
    unsigned long long  check_cap = 0;

    if (!PyArg_ParseTuple(args, "K", &check_cap))
        return NULL;

    if (cap_rights_is_set(&self->cr_cap_rights, check_cap))
        return Py_BuildValue("i", 1);
    return Py_BuildValue("i", 0);
}

static PyObject *
CR_is_valid(CRObject *self, PyObject *args)
{
    if (!PyArg_ParseTuple(args, ""))
        return NULL;

    if (cap_rights_is_valid(&self->cr_cap_rights))
        return Py_BuildValue("i", 1);
    return Py_BuildValue("i", 0);
}

static PyObject *
CR_merge(CRObject *self, PyObject *args)
{
    CRObject   *other_cr;

    if (!PyArg_ParseTuple(args, "O!", &CR_Type, &other_cr))
        return NULL;

    cap_rights_merge(&self->cr_cap_rights, &other_cr->cr_cap_rights);
    return Py_BuildValue("i", 0);
}

static PyObject *
CR_remove(CRObject *self, PyObject *args)
{
    CRObject    *other_cr;

    if (!PyArg_ParseTuple(args, "O!", &CR_Type, &other_cr))
        return NULL;

    cap_rights_remove(&self->cr_cap_rights, &other_cr->cr_cap_rights);

    return Py_BuildValue("i", 0);
}

static PyObject *
CR_contains(CRObject *self, PyObject *args)
{
    CRObject    *other_cr;

    if (!PyArg_ParseTuple(args, "O!", &CR_Type, &other_cr))
        return NULL;

    if (cap_rights_contains(&self->cr_cap_rights, &other_cr->cr_cap_rights))
        return Py_BuildValue("i", 1);
    return Py_BuildValue("i", 0);
}

static PyObject *
CR_limit(CRObject *self, PyObject *args)
{
    u_int           rval = 0;
    int             fd;
    CRObject       *cr_in;

    if (!PyArg_ParseTuple(args, "i", &fd))
        return NULL;

    if (cap_rights_limit(fd, &self->cr_cap_rights))
        rval = errno;

    return Py_BuildValue("i", rval);
}

static PyObject*
CR_get(CRObject *self, PyObject *args)
{
    u_int           rval = 0;
    int             fd;

    if (!PyArg_ParseTuple(args, "i", &fd))
        return NULL;

    if (cap_rights_get(fd, &self->cr_cap_rights))
    {
        rval = errno;
    }

    return Py_BuildValue("i", rval);
}

static struct PyMethodDef CR_methods[] = {
    {"set",      (PyCFunction)CR_set,      METH_VARARGS, PyDoc_STR("")},
    {"clear",    (PyCFunction)CR_clear,    METH_VARARGS, PyDoc_STR("")},
    {"is_set",   (PyCFunction)CR_is_set,   METH_VARARGS, PyDoc_STR("")},
    {"is_valid", (PyCFunction)CR_is_valid, METH_VARARGS, PyDoc_STR("")},
    {"merge",    (PyCFunction)CR_merge,    METH_VARARGS, PyDoc_STR("")},
    {"remove",   (PyCFunction)CR_remove,   METH_VARARGS, PyDoc_STR("")},
    {"contains", (PyCFunction)CR_contains, METH_VARARGS, PyDoc_STR("")},
    {"limit",    (PyCFunction)CR_limit,    METH_VARARGS, PyDoc_STR("")},
    {"get",      (PyCFunction)CR_get,      METH_VARARGS, PyDoc_STR("")},
    {NULL, NULL}  /* Sentinel */
};

static struct PyMemberDef CR_members[] = {
    {"_pocket",     T_OBJECT,  offsetof(CRObject, pocket),      READONLY,   "hidden goodie holder"},
    {0}  /* Sentinel */
};

static PyTypeObject CR_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "capsimodule.CR",       /*tp_name*/
    sizeof(CRObject),       /*tp_basicsize*/
    0,                      /*tp_itemsize*/
    /* methods */
    (destructor)CR_dealloc, /*tp_dealloc*/
    0,                      /*tp_print*/
    0,                      /*tp_getattr*/
    0,                      /*tp_setattr*/
    0,                      /*tp_compare*/
    0,                      /*tp_repr*/
    0,                      /*tp_as_number*/
    0,                      /*tp_as_sequence*/
    0,                      /*tp_as_mapping*/
    0,                      /*tp_hash*/
    0,                      /*tp_call*/
    0,                      /*tp_str*/
    0,                      /*tp_getattro*/
    0,                      /*tp_setattro*/
    0,                      /*tp_as_buffer*/
    Py_TPFLAGS_DEFAULT,     /*tp_flags*/
    PyDoc_STR("A cap rights object. Do not enter."),                 /*tp_doc*/
    0,                      /*tp_traverse*/
    0,                      /*tp_clear*/
    0,                      /*tp_richcompare*/
    0,                      /*tp_weaklistoffset*/
    0,                      /*tp_iter*/
    0,                      /*tp_iternext*/
    CR_methods,             /*tp_methods*/
    CR_members,             /*tp_members*/
    0,                      /*tp_getset*/
    0,                      /*tp_base*/
    0,                      /*tp_dict*/
    0,                      /*tp_descr_get*/
    0,                      /*tp_descr_set*/
    0,                      /*tp_dictoffset*/
    (initproc)CR_init,      /*tp_init*/
    0,                      /*tp_alloc*/
    (newfunc)newCRObject,   /*tp_new*/
    0,                      /*tp_free*/
    0,                      /*tp_is_gc*/
};
/* --------------------------------------------------------------------- */

// general functions
static PyObject *
capsi_cap_enter(PyObject *self, PyObject *args)
{
    int rval;

    if (!PyArg_ParseTuple(args, ""))
        return NULL;

    rval = cap_enter();
    if (rval != 0)
        rval = errno;

    return Py_BuildValue("i", rval);
}

static PyObject *
capsi_cap_sandboxed(PyObject *self, PyObject *args)
{
    if (!PyArg_ParseTuple(args, ""))
        return NULL;

    if (cap_sandboxed())
        return Py_BuildValue("i", 1);
    return Py_BuildValue("i", 0);
}

static PyObject *
capsi_cap_getmode(PyObject *self, PyObject *args)
{
    u_int rval;
    u_int error = 0;

    if (!PyArg_ParseTuple(args, ""))
        return NULL;

    if (cap_getmode(&rval))
        error = errno;

    return Py_BuildValue("(ii)", rval, error);
}

static PyObject*
capsi_cap_ioctls_limit(PyObject *self, PyObject *args)
{
    u_int           rval = 0;
    int             fd;
    PyObject       *cmd_list;
    PyObject       *item;
    unsigned long   cmds[256];
    size_t          ncmds=0;
    int             i,n;

    if (!PyArg_ParseTuple(args, "iO", &fd, &cmd_list))
        return NULL;

    n = PyList_Size(cmd_list);
    if (n < 0 OR n>255)
        return NULL;

    for (i=0; i<n; i++)
    {
        item = PyList_GetItem(cmd_list, i);
#if PYTHON2 == 1
        if (!PyInt_Check(item)) continue;
        cmds[ncmds++] = PyInt_AsLong(item);
#else
        if (!PyLong_Check(item)) continue;
        cmds[ncmds++] = PyLong_AsUnsignedLong(item);
#endif
    }

    if (cap_ioctls_limit(fd, cmds, ncmds))
        rval = errno;

    return Py_BuildValue("i", rval);
}


static PyObject*
capsi_cap_ioctls_get(PyObject *self, PyObject *args)
{
    u_int           rval = 0;
    int             fd;
    unsigned long   cmds[256];
    long            ncmds = 0;
    long            eff_ncmds;
    PyObject        *rlist;
    PyObject        *py_ncmds;

    bzero(cmds, 256 * sizeof(unsigned long));

    if (!PyArg_ParseTuple(args, "i", &fd))
        return NULL;

    if ((ncmds = cap_ioctls_get(fd, cmds, 256)) < 0)
    {
        rval = errno;
        return Py_BuildValue("i", rval);
    }

    if ( (rlist = PyList_New(0)) == NULL )
    {
        rval = errno;
        return Py_BuildValue("i", rval);
    }

    if (ncmds > 256)
        eff_ncmds = 256;
    else
        eff_ncmds = ncmds;

    for (int i = 0; i < eff_ncmds; i++)
#if PYTHON2 == 1
        PyList_Append(rlist, PyInt_FromLong((int)cmds[i]));

    return PyTuple_Pack(2, PyInt_FromLong(ncmds), rlist);
#else
        PyList_Append(rlist, PyLong_FromLong((int)cmds[i]));

    return PyTuple_Pack(2, PyLong_FromLong(ncmds), rlist);
#endif
}

static PyObject*
capsi_cap_fcntls_limit(PyObject *self, PyObject *args)
{
    u_int           rval = 0;
    int             fd;
    uint32_t        rights;

    if (!PyArg_ParseTuple(args, "ii", &fd, &rights))
        return NULL;

    if (cap_fcntls_limit(fd, rights))
        rval = errno;

    return Py_BuildValue("i", rval);
}

static PyObject*
capsi_cap_fcntls_get(PyObject *self, PyObject *args)
{
    u_int           rval = 0;
    u_int32_t       rights;
    int             fd;

    if (!PyArg_ParseTuple(args, "i", &fd))
        return NULL;

    if (cap_fcntls_get(fd, &rights))
        rval = errno;

    return Py_BuildValue("(ii)", rights, rval);
}

//int openat(int fd, const char *path, int flags, ...);
static PyObject *
capsi_openat(PyObject *self, PyObject *args)
{
    int fd, flags, rv;
    const char *path;

    if ( !PyArg_ParseTuple(args, "isi", &fd, &path, &flags) )
        return NULL;

    rv = openat(fd, path, flags);

    return Py_BuildValue("i", rv);
}

static PyObject *
capsi_opendir(PyObject *self, PyObject *args)
{
    int flags, rv;
    const char *path;

    if ( !PyArg_ParseTuple(args, "si", &path, &flags) )
        return NULL;

    rv = open(path, flags);

    return Py_BuildValue("i", rv);
}



/* List of functions defined in the module */

static PyMethodDef capsi_methods[] = {
{"enter",           capsi_cap_enter,            METH_VARARGS, ""},
{"sandboxed",       capsi_cap_sandboxed,        METH_VARARGS, ""},
{"getmode",         capsi_cap_getmode,          METH_VARARGS, ""},
{"ioctls_limit",    capsi_cap_ioctls_limit,     METH_VARARGS, ""},
{"ioctls_get",      capsi_cap_ioctls_get,       METH_VARARGS, ""},
{"fcntls_limit",    capsi_cap_fcntls_limit,     METH_VARARGS, ""},
{"fcntls_get",      capsi_cap_fcntls_get,       METH_VARARGS, ""},
{"openat",          capsi_openat,               METH_VARARGS, ""},
{"opendir",         capsi_opendir,              METH_VARARGS, ""},
{NULL, NULL}
};

PyDoc_STRVAR(module_doc,
"Capsicum for python. Spicy snake.");

#if PYTHON2 == 1
PyMODINIT_FUNC
init_pycapsicum(void)
{
    PyObject *m;

    if (PyType_Ready(&CR_Type) < 0)
        return;

    m = Py_InitModule3("_pycapsicum", capsi_methods, module_doc);
    if (m == NULL)
        return;

    Py_INCREF(&CR_Type);
    PyModule_AddObject(m, "CapRights_", (PyObject*)&CR_Type);
}

#else
static struct PyModuleDef capsi_module = {
   PyModuleDef_HEAD_INIT, "_pycapsicum", module_doc, -1, capsi_methods
};

PyMODINIT_FUNC
PyInit__pycapsicum(void)
{
    PyObject *m;

    if (PyType_Ready(&CR_Type) < 0)
        return NULL;

    m = PyModule_Create(&capsi_module);
    if (m == NULL)
        return NULL;

    Py_INCREF(&CR_Type);
    PyModule_AddObject(m, "CapRights_", (PyObject*)&CR_Type);

    return m;
}
#endif
