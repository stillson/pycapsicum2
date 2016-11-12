#
# Copyright (c) 2016, Chris Stillson <stillson@gmail.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#


import _pycapsicum
import os

class CapsicumError(Exception):
    pass

def CAPRIGHT(idx, bit):
    return (1 << (57 + idx)) | bit

# computing these values in python is not ideal....
class Caps(object):
    CAP_READ        = CAPRIGHT(0, 0x0000000000000001)
    CAP_WRITE       = CAPRIGHT(0, 0x0000000000000002)
    CAP_SEEK_TELL   = CAPRIGHT(0, 0x0000000000000004)
    CAP_MMAP        = CAPRIGHT(0, 0x0000000000000010)
    CAP_CREATE      = CAPRIGHT(0, 0x0000000000000040)
    CAP_FEXECVE     = CAPRIGHT(0, 0x0000000000000080)
    CAP_FSYNC       = CAPRIGHT(0, 0x0000000000000100)
    CAP_FTRUNCATE   = CAPRIGHT(0, 0x0000000000000200)
    CAP_LOOKUP      = CAPRIGHT(0, 0x0000000000000400)
    CAP_FCHDIR      = CAPRIGHT(0, 0x0000000000000800)
    CAP_FCHFLAGS    = CAPRIGHT(0, 0x0000000000001000)
    CAP_FCHMOD      = CAPRIGHT(0, 0x0000000000002000)
    CAP_FCHOWN      = CAPRIGHT(0, 0x0000000000004000)
    CAP_FCNTL       = CAPRIGHT(0, 0x0000000000008000)
    CAP_FLOCK       = CAPRIGHT(0, 0x0000000000010000)
    CAP_FPATHCONF   = CAPRIGHT(0, 0x0000000000020000)
    CAP_FSCK        = CAPRIGHT(0, 0x0000000000040000)
    CAP_FSTAT       = CAPRIGHT(0, 0x0000000000080000)
    CAP_FSTATFS     = CAPRIGHT(0, 0x0000000000100000)
    CAP_FUTIMES     = CAPRIGHT(0, 0x0000000000200000)
    CAP_ACCEPT      = CAPRIGHT(0, 0x0000000020000000)
    CAP_BIND        = CAPRIGHT(0, 0x0000000040000000)
    CAP_CONNECT     = CAPRIGHT(0, 0x0000000080000000)
    CAP_GETPEERNAME = CAPRIGHT(0, 0x0000000100000000)
    CAP_GETSOCKNAME = CAPRIGHT(0, 0x0000000200000000)
    CAP_GETSOCKOPT  = CAPRIGHT(0, 0x0000000400000000)
    CAP_LISTEN      = CAPRIGHT(0, 0x0000000800000000)
    CAP_PEELOFF     = CAPRIGHT(0, 0x0000001000000000)
    CAP_SETSOCKOPT  = CAPRIGHT(0, 0x0000002000000000)
    CAP_SHUTDOWN    = CAPRIGHT(0, 0x0000004000000000)

    # not real caps
    CAP_ALL0        = CAPRIGHT(0, 0x0000007FFFFFFFFF)
    CAP_UNUSED0_40  = CAPRIGHT(0, 0x0000008000000000)
    CAP_UNUSED0_57  = CAPRIGHT(0, 0x0100000000000000)

    # INDEX 1
    CAP_MAC_GET         = CAPRIGHT(1, 0x0000000000000001)
    CAP_MAC_SET         = CAPRIGHT(1, 0x0000000000000002)
    CAP_SEM_GETVALUE    = CAPRIGHT(1, 0x0000000000000004)
    CAP_SEM_POST        = CAPRIGHT(1, 0x0000000000000008)
    CAP_SEM_WAIT        = CAPRIGHT(1, 0x0000000000000010)
    CAP_EVENT           = CAPRIGHT(1, 0x0000000000000020)
    CAP_KQUEUE_EVENT    = CAPRIGHT(1, 0x0000000000000040)
    CAP_IOCTL           = CAPRIGHT(1, 0x0000000000000080)
    CAP_TTYHOOK         = CAPRIGHT(1, 0x0000000000000100)
    CAP_PDGETPID        = CAPRIGHT(1, 0x0000000000000200)
    CAP_PDWAIT          = CAPRIGHT(1, 0x0000000000000400)
    CAP_PDKILL          = CAPRIGHT(1, 0x0000000000000800)
    CAP_EXTATTR_DELETE  = CAPRIGHT(1, 0x0000000000001000)
    CAP_EXTATTR_GET     = CAPRIGHT(1, 0x0000000000002000)
    CAP_EXTATTR_LIST    = CAPRIGHT(1, 0x0000000000004000)
    CAP_EXTATTR_SET     = CAPRIGHT(1, 0x0000000000008000)
    CAP_ACL_CHECK       = CAPRIGHT(1, 0x0000000000010000)
    CAP_ACL_DELETE      = CAPRIGHT(1, 0x0000000000020000)
    CAP_ACL_GET         = CAPRIGHT(1, 0x0000000000040000)
    CAP_ACL_SET         = CAPRIGHT(1, 0x0000000000080000)
    CAP_KQUEUE_CHANGE   = CAPRIGHT(1, 0x0000000000100000)

    # not real caps
    CAP_ALL1            = CAPRIGHT(1, 0x00000000001FFFFF)
    CAP_UNUSED1_22      = CAPRIGHT(1, 0x0000000000200000)
    CAP_UNUSED1_57      = CAPRIGHT(1, 0x0100000000000000)

# needs to be first
Caps.CAP_SEEK        = Caps.CAP_SEEK_TELL | 0x0000000000000008
Caps.CAP_MMAP_X      = (Caps.CAP_MMAP | Caps.CAP_SEEK | 0x0000000000000020)
# caps that are combinations
Caps.CAP_PREAD       = (Caps.CAP_SEEK | Caps.CAP_READ)
Caps.CAP_PWRITE      = (Caps.CAP_SEEK | Caps.CAP_WRITE)
Caps.CAP_MMAP_R      = (Caps.CAP_MMAP | Caps.CAP_SEEK | Caps.CAP_READ)
Caps.CAP_MMAP_W      = (Caps.CAP_MMAP | Caps.CAP_SEEK | Caps.CAP_WRITE)
Caps.CAP_MMAP_RW     = (Caps.CAP_MMAP_R | Caps.CAP_MMAP_W)
Caps.CAP_MMAP_RX     = (Caps.CAP_MMAP_R | Caps.CAP_MMAP_X)
Caps.CAP_MMAP_WX     = (Caps.CAP_MMAP_W | Caps.CAP_MMAP_X)
Caps.CAP_MMAP_RWX    = (Caps.CAP_MMAP_R | Caps.CAP_MMAP_W | Caps.CAP_MMAP_X)
Caps.CAP_CHFLAGSAT   = (Caps.CAP_FCHFLAGS | Caps.CAP_LOOKUP)
Caps.CAP_FCHMODAT    = (Caps.CAP_FCHMOD | Caps.CAP_LOOKUP)
Caps.CAP_FCHOWNAT    = (Caps.CAP_FCHOWN | Caps.CAP_LOOKUP)
Caps.CAP_FSTATAT     = (Caps.CAP_FSTAT | Caps.CAP_LOOKUP)
Caps.CAP_FUTIMESAT   = (Caps.CAP_FUTIMES | Caps.CAP_LOOKUP)
Caps.CAP_RECV        = Caps.CAP_READ
Caps.CAP_SEND        = Caps.CAP_WRITE
Caps.CAP_SOCK_CLIENT =\
    (Caps.CAP_CONNECT | Caps.CAP_GETPEERNAME | Caps.CAP_GETSOCKNAME | Caps.CAP_GETSOCKOPT |
     Caps.CAP_PEELOFF | Caps.CAP_RECV | Caps.CAP_SEND | Caps.CAP_SETSOCKOPT | Caps.CAP_SHUTDOWN)

Caps.CAP_SOCK_SERVER =\
    (Caps.CAP_ACCEPT | Caps.CAP_BIND | Caps.CAP_GETPEERNAME | Caps.CAP_GETSOCKNAME |
     Caps.CAP_GETSOCKOPT | Caps.CAP_LISTEN | Caps.CAP_PEELOFF | Caps.CAP_RECV | Caps.CAP_SEND |
     Caps.CAP_SETSOCKOPT | Caps.CAP_SHUTDOWN)
Caps.CAP_KQUEUE          = (Caps.CAP_KQUEUE_EVENT | Caps.CAP_KQUEUE_CHANGE)

# caps that are caps + a bit
Caps.CAP_LINKAT      = (Caps.CAP_LOOKUP | 0x0000000000400000)
Caps.CAP_MKDIRAT     = (Caps.CAP_LOOKUP | 0x0000000000800000)
Caps.CAP_MKFIFOAT    = (Caps.CAP_LOOKUP | 0x0000000001000000)
Caps.CAP_MKNODAT     = (Caps.CAP_LOOKUP | 0x0000000002000000)
Caps.CAP_RENAMEAT    = (Caps.CAP_LOOKUP | 0x0000000004000000)
Caps.CAP_SYMLINKAT   = (Caps.CAP_LOOKUP | 0x0000000008000000)
Caps.CAP_UNLINKAT    = (Caps.CAP_LOOKUP | 0x0000000010000000)
Caps.CAP_BINDAT      = (Caps.CAP_LOOKUP | 0x0000008000000000)
Caps.CAP_CONNECTAT   = (Caps.CAP_LOOKUP | 0x0000010000000000)


def cap_list_fix(caplist):
    capset = set(caplist)

    if 'CAP_RECV' in capset:
        capset = capset - {'CAP_RECV'}
        capset = capset.union({'CAP_READ'})

    if 'CAP_SEND' in capset:
        capset = capset - {'CAP_SEND'}
        capset = capset.union({'CAP_WRITE'})

    fixlist = [
    ['CAP_SEEK_TELL',    {'CAP_SEEK'}],
    ['CAP_MMAP_X',       {'CAP_MMAP', 'CAP_SEEK'}],
    ['CAP_PREAD',        {'CAP_SEEK', 'CAP_READ'}],
    ['CAP_PWRITE',       {'CAP_SEEK', 'CAP_WRITE'}],
    ['CAP_MMAP_RWX',     {'CAP_MMAP_R', 'CAP_MMAP_W', 'CAP_MMAP_X'}],
    ['CAP_MMAP_RW',      {'CAP_MMAP_R', 'CAP_MMAP_W'}],
    ['CAP_MMAP_RX',      {'CAP_MMAP_R', 'CAP_MMAP_X'}],
    ['CAP_MMAP_WX',      {'CAP_MMAP_W', 'CAP_MMAP_X'}],
    ['CAP_MMAP_R',       {'CAP_MMAP', 'CAP_SEEK', 'CAP_READ'}],
    ['CAP_MMAP_W',       {'CAP_MMAP', 'CAP_SEEK', ' CAP_WRITE'}],
    ['CAP_CHFLAGSAT',    {'CAP_FCHFLAGS', 'CAP_LOOKUP'}],
    ['CAP_FCHMODAT',     {'CAP_FCHMOD', 'CAP_LOOKUP'}],
    ['CAP_FCHOWNAT',     {'CAP_FCHOWN', 'CAP_LOOKUP'}],
    ['CAP_FSTATAT',      {'CAP_FSTAT', 'CAP_LOOKUP'}],
    ['CAP_FUTIMESAT',    {'CAP_FUTIMES', 'CAP_LOOKUP'}],
    ['CAP_SOCK_CLIENT',  {'CAP_CONNECT', 'CAP_GETPEERNAME', 'CAP_GETSOCKNAME', 'CAP_GETSOCKOPT', 'CAP_PEELOFF', 'CAP_READ', 'CAP_WRITE', 'CAP_SETSOCKOPT', 'CAP_SHUTDOWN'}],
    ['CAP_SOCK_SERVER',  {'CAP_ACCEPT', 'CAP_BIND', 'CAP_GETPEERNAME', 'CAP_GETSOCKNAME', 'CAP_GETSOCKOPT', 'CAP_LISTEN', 'CAP_PEELOFF', 'CAP_READ', 'CAP_WRITE', 'CAP_SETSOCKOPT', 'CAP_SHUTDOWN'}],
    ['CAP_KQUEUE',       {'CAP_KQUEUE_EVENT', 'CAP_KQUEUE_CHANGE'}],
    ['CAP_LINKAT',       {'CAP_LOOKUP'}],
    ['CAP_MKDIRAT',      {'CAP_LOOKUP'}],
    ['CAP_MKFIFOAT',     {'CAP_LOOKUP'}],
    ['CAP_MKNODAT',      {'CAP_LOOKUP'}],
    ['CAP_RENAMEAT',     {'CAP_LOOKUP'}],
    ['CAP_SYMLINKAT',    {'CAP_LOOKUP'}],
    ['CAP_UNLINKAT',     {'CAP_LOOKUP'}],
    ['CAP_BINDAT',       {'CAP_LOOKUP'}],
    ['CAP_CONNECTAT',    {'CAP_LOOKUP'}],]

    for cap, r_set in fixlist:
        if cap in capset:
            capset = capset - r_set

    return list(capset)


NAME_2_CAPS = {
'CAP_READ':              Caps.CAP_READ,
'CAP_WRITE':             Caps.CAP_WRITE,
'CAP_SEEK_TELL':         Caps.CAP_SEEK_TELL,
'CAP_MMAP':              Caps.CAP_MMAP,
'CAP_CREATE':            Caps.CAP_CREATE,
'CAP_FEXECVE':           Caps.CAP_FEXECVE,
'CAP_FSYNC':             Caps.CAP_FSYNC,
'CAP_FTRUNCATE':         Caps.CAP_FTRUNCATE,
'CAP_LOOKUP':            Caps.CAP_LOOKUP,
'CAP_FCHDIR':            Caps.CAP_FCHDIR,
'CAP_FCHFLAGS':          Caps.CAP_FCHFLAGS,
'CAP_FCHMOD':            Caps.CAP_FCHMOD,
'CAP_FCHOWN':            Caps.CAP_FCHOWN,
'CAP_FCNTL':             Caps.CAP_FCNTL,
'CAP_FLOCK':             Caps.CAP_FLOCK,
'CAP_FPATHCONF':         Caps.CAP_FPATHCONF,
'CAP_FSCK':              Caps.CAP_FSCK,
'CAP_FSTAT':             Caps.CAP_FSTAT,
'CAP_FSTATFS':           Caps.CAP_FSTATFS,
'CAP_FUTIMES':           Caps.CAP_FUTIMES,
'CAP_ACCEPT':            Caps.CAP_ACCEPT,
'CAP_BIND':              Caps.CAP_BIND,
'CAP_CONNECT':           Caps.CAP_CONNECT,
'CAP_GETPEERNAME':       Caps.CAP_GETPEERNAME,
'CAP_GETSOCKNAME':       Caps.CAP_GETSOCKNAME,
'CAP_GETSOCKOPT':        Caps.CAP_GETSOCKOPT,
'CAP_LISTEN':            Caps.CAP_LISTEN,
'CAP_PEELOFF':           Caps.CAP_PEELOFF,
'CAP_SETSOCKOPT':        Caps.CAP_SETSOCKOPT,
'CAP_SHUTDOWN':          Caps.CAP_SHUTDOWN,
'CAP_MAC_GET':           Caps.CAP_MAC_GET,
'CAP_MAC_SET':           Caps.CAP_MAC_SET,
'CAP_SEM_GETVALUE':      Caps.CAP_SEM_GETVALUE,
'CAP_SEM_POST':          Caps.CAP_SEM_POST,
'CAP_SEM_WAIT':          Caps.CAP_SEM_WAIT,
'CAP_EVENT':             Caps.CAP_EVENT,
'CAP_KQUEUE_EVENT':      Caps.CAP_KQUEUE_EVENT,
'CAP_IOCTL':             Caps.CAP_IOCTL,
'CAP_TTYHOOK':           Caps.CAP_TTYHOOK,
'CAP_PDGETPID':          Caps.CAP_PDGETPID,
'CAP_PDWAIT':            Caps.CAP_PDWAIT,
'CAP_PDKILL':            Caps.CAP_PDKILL,
'CAP_EXTATTR_DELETE':    Caps.CAP_EXTATTR_DELETE,
'CAP_EXTATTR_GET':       Caps.CAP_EXTATTR_GET,
'CAP_EXTATTR_LIST':      Caps.CAP_EXTATTR_LIST,
'CAP_EXTATTR_SET':       Caps.CAP_EXTATTR_SET,
'CAP_ACL_CHECK':         Caps.CAP_ACL_CHECK,
'CAP_ACL_DELETE':        Caps.CAP_ACL_DELETE,
'CAP_ACL_GET':           Caps.CAP_ACL_GET,
'CAP_ACL_SET':           Caps.CAP_ACL_SET,
'CAP_KQUEUE_CHANGE':     Caps.CAP_KQUEUE_CHANGE,
'CAP_PREAD':             Caps.CAP_PREAD,
'CAP_PWRITE':            Caps.CAP_PWRITE,
'CAP_MMAP_R':            Caps.CAP_MMAP_R,
'CAP_MMAP_W':            Caps.CAP_MMAP_W,
'CAP_MMAP_RW':           Caps.CAP_MMAP_RW,
'CAP_MMAP_RX':           Caps.CAP_MMAP_RX,
'CAP_MMAP_WX':           Caps.CAP_MMAP_WX,
'CAP_MMAP_RWX':          Caps.CAP_MMAP_RWX,
'CAP_CHFLAGSAT':         Caps.CAP_CHFLAGSAT,
'CAP_FCHMODAT':          Caps.CAP_FCHMODAT,
'CAP_FCHOWNAT':          Caps.CAP_FCHOWNAT,
'CAP_FSTATAT':           Caps.CAP_FSTATAT,
'CAP_FUTIMESAT':         Caps.CAP_FUTIMESAT,
'CAP_RECV':              Caps.CAP_RECV,
'CAP_SEND':              Caps.CAP_SEND,
'CAP_SOCK_CLIENT':       Caps.CAP_SOCK_CLIENT,
'CAP_SOCK_SERVER':       Caps.CAP_SOCK_SERVER,
'CAP_KQUEUE':            Caps.CAP_KQUEUE,
'CAP_SEEK':              Caps.CAP_SEEK,
'CAP_MMAP_X':            Caps.CAP_MMAP_X,
'CAP_LINKAT':            Caps.CAP_LINKAT,
'CAP_MKDIRAT':           Caps.CAP_MKDIRAT,
'CAP_MKFIFOAT':          Caps.CAP_MKFIFOAT,
'CAP_MKNODAT':           Caps.CAP_MKNODAT,
'CAP_RENAMEAT':          Caps.CAP_RENAMEAT,
'CAP_SYMLINKAT':         Caps.CAP_SYMLINKAT,
'CAP_UNLINKAT':          Caps.CAP_UNLINKAT,
'CAP_BINDAT':            Caps.CAP_BINDAT,
'CAP_CONNECTAT':         Caps.CAP_CONNECTAT,
}

CAPS_2_NAME = {
Caps.CAP_READ:           "CAP_READ",
Caps.CAP_WRITE:          "CAP_WRITE",
Caps.CAP_SEEK_TELL:      "CAP_SEEK_TELL",
Caps.CAP_SEEK:           "CAP_SEEK",
Caps.CAP_MMAP:           "CAP_MMAP",
Caps.CAP_MMAP_X:         "CAP_MMAP_X",
Caps.CAP_CREATE:         "CAP_CREATE",
Caps.CAP_FEXECVE:        "CAP_FEXECVE",
Caps.CAP_FSYNC:          "CAP_FSYNC",
Caps.CAP_FTRUNCATE:      "CAP_FTRUNCATE",
Caps.CAP_LOOKUP:         "CAP_LOOKUP",
Caps.CAP_FCHDIR:         "CAP_FCHDIR",
Caps.CAP_FCHFLAGS:       "CAP_FCHFLAGS",
Caps.CAP_FCHMOD:         "CAP_FCHMOD",
Caps.CAP_FCHOWN:         "CAP_FCHOWN",
Caps.CAP_FCNTL:          "CAP_FCNTL",
Caps.CAP_FLOCK:          "CAP_FLOCK",
Caps.CAP_FPATHCONF:      "CAP_FPATHCONF",
Caps.CAP_FSCK:           "CAP_FSCK",
Caps.CAP_FSTAT:          "CAP_FSTAT",
Caps.CAP_FSTATFS:        "CAP_FSTATFS",
Caps.CAP_FUTIMES:        "CAP_FUTIMES",
Caps.CAP_LINKAT:         "CAP_LINKAT",
Caps.CAP_MKDIRAT:        "CAP_MKDIRAT",
Caps.CAP_MKFIFOAT:       "CAP_MKFIFOAT",
Caps.CAP_MKNODAT:        "CAP_MKNODAT",
Caps.CAP_RENAMEAT:       "CAP_RENAMEAT",
Caps.CAP_SYMLINKAT:      "CAP_SYMLINKAT",
Caps.CAP_UNLINKAT:       "CAP_UNLINKAT",
Caps.CAP_ACCEPT:         "CAP_ACCEPT",
Caps.CAP_BIND:           "CAP_BIND",
Caps.CAP_CONNECT:        "CAP_CONNECT",
Caps.CAP_GETPEERNAME:    "CAP_GETPEERNAME",
Caps.CAP_GETSOCKNAME:    "CAP_GETSOCKNAME",
Caps.CAP_GETSOCKOPT:     "CAP_GETSOCKOPT",
Caps.CAP_LISTEN:         "CAP_LISTEN",
Caps.CAP_PEELOFF:        "CAP_PEELOFF",
Caps.CAP_SETSOCKOPT:     "CAP_SETSOCKOPT",
Caps.CAP_SHUTDOWN:       "CAP_SHUTDOWN",
Caps.CAP_BINDAT:         "CAP_BINDAT",
Caps.CAP_CONNECTAT:      "CAP_CONNECTAT",
Caps.CAP_MAC_GET:        "CAP_MAC_GET",
Caps.CAP_MAC_SET:        "CAP_MAC_SET",
Caps.CAP_SEM_GETVALUE:   "CAP_SEM_GETVALUE",
Caps.CAP_SEM_POST:       "CAP_SEM_POST",
Caps.CAP_SEM_WAIT:       "CAP_SEM_WAIT",
Caps.CAP_EVENT:          "CAP_EVENT",
Caps.CAP_KQUEUE_EVENT:   "CAP_KQUEUE_EVENT",
Caps.CAP_IOCTL:          "CAP_IOCTL",
Caps.CAP_TTYHOOK:        "CAP_TTYHOOK",
Caps.CAP_PDGETPID:       "CAP_PDGETPID",
Caps.CAP_PDWAIT:         "CAP_PDWAIT",
Caps.CAP_PDKILL:         "CAP_PDKILL",
Caps.CAP_EXTATTR_DELETE: "CAP_EXTATTR_DELETE",
Caps.CAP_EXTATTR_GET:    "CAP_EXTATTR_GET",
Caps.CAP_EXTATTR_LIST:   "CAP_EXTATTR_LIST",
Caps.CAP_EXTATTR_SET:    "CAP_EXTATTR_SET",
Caps.CAP_ACL_CHECK:      "CAP_ACL_CHECK",
Caps.CAP_ACL_DELETE:     "CAP_ACL_DELETE",
Caps.CAP_ACL_GET:        "CAP_ACL_GET",
Caps.CAP_ACL_SET:        "CAP_ACL_SET",
Caps.CAP_KQUEUE_CHANGE:  "CAP_KQUEUE_CHANGE",
}

class CapsName:
    CAP_READ =            "CAP_READ"
    CAP_WRITE =           "CAP_WRITE"
    CAP_SEEK_TELL =       "CAP_SEEK_TELL"
    CAP_SEEK =            "CAP_SEEK"
    CAP_MMAP =            "CAP_MMAP"
    CAP_MMAP_X =          "CAP_MMAP_X"
    CAP_CREATE =          "CAP_CREATE"
    CAP_FEXECVE =         "CAP_FEXECVE"
    CAP_FSYNC =           "CAP_FSYNC"
    CAP_FTRUNCATE =       "CAP_FTRUNCATE"
    CAP_LOOKUP =          "CAP_LOOKUP"
    CAP_FCHDIR =          "CAP_FCHDIR"
    CAP_FCHFLAGS =        "CAP_FCHFLAGS"
    CAP_FCHMOD =          "CAP_FCHMOD"
    CAP_FCHOWN =          "CAP_FCHOWN"
    CAP_FCNTL =           "CAP_FCNTL"
    CAP_FLOCK =           "CAP_FLOCK"
    CAP_FPATHCONF =       "CAP_FPATHCONF"
    CAP_FSCK =            "CAP_FSCK"
    CAP_FSTAT =           "CAP_FSTAT"
    CAP_FSTATFS =         "CAP_FSTATFS"
    CAP_FUTIMES =         "CAP_FUTIMES"
    CAP_LINKAT =          "CAP_LINKAT"
    CAP_MKDIRAT =         "CAP_MKDIRAT"
    CAP_MKFIFOAT =        "CAP_MKFIFOAT"
    CAP_MKNODAT =         "CAP_MKNODAT"
    CAP_RENAMEAT =        "CAP_RENAMEAT"
    CAP_SYMLINKAT =       "CAP_SYMLINKAT"
    CAP_UNLINKAT =        "CAP_UNLINKAT"
    CAP_ACCEPT =          "CAP_ACCEPT"
    CAP_BIND =            "CAP_BIND"
    CAP_CONNECT =         "CAP_CONNECT"
    CAP_GETPEERNAME =     "CAP_GETPEERNAME"
    CAP_GETSOCKNAME =     "CAP_GETSOCKNAME"
    CAP_GETSOCKOPT =      "CAP_GETSOCKOPT"
    CAP_LISTEN =          "CAP_LISTEN"
    CAP_PEELOFF =         "CAP_PEELOFF"
    CAP_SETSOCKOPT =      "CAP_SETSOCKOPT"
    CAP_SHUTDOWN =        "CAP_SHUTDOWN"
    CAP_BINDAT =          "CAP_BINDAT"
    CAP_CONNECTAT =       "CAP_CONNECTAT"
    CAP_MAC_GET =         "CAP_MAC_GET"
    CAP_MAC_SET =         "CAP_MAC_SET"
    CAP_SEM_GETVALUE =    "CAP_SEM_GETVALUE"
    CAP_SEM_POST =        "CAP_SEM_POST"
    CAP_SEM_WAIT =        "CAP_SEM_WAIT"
    CAP_EVENT =           "CAP_EVENT"
    CAP_KQUEUE_EVENT =    "CAP_KQUEUE_EVENT"
    CAP_IOCTL =           "CAP_IOCTL"
    CAP_TTYHOOK =         "CAP_TTYHOOK"
    CAP_PDGETPID =        "CAP_PDGETPID"
    CAP_PDWAIT =          "CAP_PDWAIT"
    CAP_PDKILL =          "CAP_PDKILL"
    CAP_EXTATTR_DELETE =  "CAP_EXTATTR_DELETE"
    CAP_EXTATTR_GET =     "CAP_EXTATTR_GET"
    CAP_EXTATTR_LIST =    "CAP_EXTATTR_LIST"
    CAP_EXTATTR_SET =     "CAP_EXTATTR_SET"
    CAP_ACL_CHECK =       "CAP_ACL_CHECK"
    CAP_ACL_DELETE =      "CAP_ACL_DELETE"
    CAP_ACL_GET =         "CAP_ACL_GET"
    CAP_ACL_SET =         "CAP_ACL_SET"
    CAP_KQUEUE_CHANGE =   "CAP_KQUEUE_CHANGE"


CAP_FCNTL_GETFL  = 1 <<  3 # F_GETFL = 3
CAP_FCNTL_SETFL  = 1 <<  4 # F_SETFL = 4
CAP_FCNTL_GETOWN = 1 <<  5 # F_GETOWN = 5
CAP_FCNTL_SETOWN = 1 <<  6 # F_SETOWN = 6
CAP_FCNTL_ALL    = CAP_FCNTL_GETFL | CAP_FCNTL_SETFL | CAP_FCNTL_GETOWN | CAP_FCNTL_SETOWN

OPEN_FLAGS = \
{
'r' : 0,
'w' : 1,
'rw': 2,
}

def _fd_check(fd):
    if isinstance(fd, int):
        return fd
    return fd.fileno()

def _rw_flags(flag):
    if isinstance(flag, int):
        return flag
    return(OPEN_FLAGS[flag])

def enter():
    if _pycapsicum.enter() != 0:
        raise CapsicumError

def sandboxed():
    return _pycapsicum.sandboxed() == 1

def getmode():
    rval, error = _pycapsicum.getmode()
    if error != 0:
        raise CapsicumError
    return rval

def ioctls_limit(fd, cmdlist):
    _pycapsicum.ioctls_limit(_fd_check(fd), cmdlist)

def ioctls_get(fd):
    return _pycapsicum.ioctls_get(_fd_check(fd))

def fcntls_limit(fd, rights):
    rval = _pycapsicum.fcntls_limit(_fd_check(fd), rights)
    if rval != 0:
        raise CapsicumError

def fcntls_get(fd):
    return _pycapsicum.fcntls_get(_fd_check(fd))


def openat(fd, path, flags):
    return os.fdopen(_pycapsicum.openat(fd, path, _rw_flags(flags)))

def opendir(path, flags):
    return _pycapsicum.opendir(path, _rw_flags(flags))


class CapRights(object):
    def __init__(self, caps=None):
        self.cr = _pycapsicum.CapRights_()
        if caps:
            self.set(caps)

    @property
    def caps(self):
        rval = []
        for a_name,a_cap in NAME_2_CAPS.items():
            if self.is_set([a_name]):
                rval.append(a_name)

        return cap_list_fix(rval)

    def _get_raw_caps(self,caplist):
        caplist = cap_list_fix(caplist)
        cap_set = set(caplist)
        return [NAME_2_CAPS[i] for i in cap_set]

    def set(self, caplist):
        raw_cap = self._get_raw_caps(caplist)
        self.cr.set(raw_cap)

    def clear(self, caplist):
        raw_cap = self._get_raw_caps(caplist)
        self.cr.clear(raw_cap)

    def is_valid(self):
        return self.cr.is_valid() == 1

    def is_set(self, caplist):
        caplist = cap_list_fix(caplist)
        raw_cap = self._get_raw_caps(caplist)
        for a_cap in raw_cap:
            rv = self.cr.is_set(a_cap)
            if rv == 0:
                return False
            if rv == 1:
                return True
            raise CapsicumError

    def merge(self, otherCR):
        self.cr.merge(otherCR.cr)

    def remove(self, otherCR):
        self.cr.remove(otherCR.cr)

    def contains(self, otherCR):
        if self.cr.contains(otherCR.cr) == 1:
            return True
        return False

    def limit(self, fd):
        if self.cr.limit(_fd_check(fd)) != 0:
            raise CapsicumError

    def get(self, fd):
        if self.cr.get(_fd_check(fd)) != 0:
            raise CapsicumError

