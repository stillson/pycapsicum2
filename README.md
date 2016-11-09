==========
pycapsicum
==========

Pycapsicum is a python interface to Capsicum (sandboxing for FreeBSD). It
is works on Freebsd10, but not Freebsd9 (an earlier version supports 9)

I would reccomend you understand capsicum in C before using this module,
because it's not a simple system to understand.

API
---

::

Quick Demo:


    import pycapsicum as p

    # get a fileno for /tmp
    t = p.opendir('/tmp',0)

    #enter capability mode
    p.enter()

    # create a new CapRights object
    a = p.CapRights()

    # use openat to open a file in tmp
    x = p.openat(t,'foo',0)

    # x is a python file object
    x.readlines()

    # get the capabilities on x
    a.get(x)

    # print the capabilites out
    print a.caps

    # make a new CapRights, set to CAP_READ
    b = p.CapRights(['CAP_READ'])

    # set those capabilites to x
    b.limit(x)

    # get the capabilities from x
    a.get(x)

    # print them out. will be ['CAP_READ']
    print a.caps


For details on the specific functions see the man pages for the man pages.

``enter()``::

    Enter sandboxed mode.

``sandboxed``()::

    Returns True if in sandboxed mode, False otherwise.

``getmode()``::

    Like sandboxed(), but causes an exception on error.

``ioctls_limit(fd, cmdlist)``::

    Sets ioctl limits on FD. See the manpage for cap_ioctls_limit for
    more details.

    fd can be a integer, python file, or python socket. Or, and object
    a fileno() method

``ioctls_get(fd)``::

    Gets ioctl limits on FD. See the manpage for cap_ioctls_get for
    more details.

    fd can be a integer, python file, or python socket. Or, and object
    a fileno() method


``fcntls_limit(fd, rights)``::

    Sets fcntls limits on FD. See the manpage for cap_fcntls_limit for
    more details.

    Possible values for right are pycapsicum.CAP_FCNTL_GETFL,
    pycapsicum.CAP_FCNTL_SETFL, pycapsicum.CAP_FCNTL_GETOWN,
    pycapsicum.CAP_FCNTL_SETOWN, pycapsicum.CAP_FCNTL_ALL, or any set
    of flags '|'ed together

    fd can be a integer, python file, or python socket. Or, and object
    a fileno() method


``fcntls_get(fd)``::

    Gets fcntls limits on FD. See the manpage for cap_fcntls_get for
    more details.

    fd can be a integer, python file, or python socket. Or, and object
    a fileno() method


``openat(fd, path, flags)``::

    Not strictly cap related, openat() allows you to open a file if you
    have the fd (int only) of and opened directory.

``opendir(path, flags)``:

    opendir() allows you to get the FD for a directory (since standard
    python doesn't allow you to call open() on a directory)


 The CapRights() object:

``class CapRights(object)``::

    An Object that encapsulates a cap_rights_t. Represents a set of
    capabilites

``__init__(self, caps=None)``::

    Can be called with optional list of capabilites to initialize with

``caps``::

    A list of human readable capabilities set in the CapRights

``set(self, caplist)``:

    set a list of capabilities on the object

``clear(self, caplist)``:

    clear a list of capabilities from the object

``is_set(self, caplist)``:

    return true if the list of capabilities are set

``is_valid(self)``:

    return true if the set of capabilites are valid

``merge(self, otherCR)``:

    Merge the capabilities set in otherCR into this CapRights

``remove(self, otherCR)``:

    remove the capabilities set in otherCR from this CapRights

``contains(self, otherCR)``:

    True if this CapRights has all the capabilities in otherCR

``limit(self, fd)``:

    Set the capabilities in this CapRights onto fd (which can be an
    int, file object, socket object, or any object with a fileno()
    method.

``get(self, fd)``:

    Get the capabilities into this CapRights from fd (which can be an
    int, file object, socket object, or any object with a fileno()
    method.


