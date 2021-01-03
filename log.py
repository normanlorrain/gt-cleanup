import sys
from logging import (
    INFO,
    DEBUG,
    FileHandler,
    Formatter,
    StreamHandler,
    getLogger,
    debug,
    info,
    warning,
    error,
)

LONGFORMAT = "%(levelname)8s: %(asctime)s %(filename)10s: %(lineno)4d:\t%(message)s"
SHORTFORMAT = "%(levelname)-8s: %(message)s"

# Root logger gets everything.  Handlers defined below will filter it out...

getLogger("").setLevel(DEBUG)


def init(filename):
    filehandler = FileHandler(filename, mode="a", encoding="utf-8")
    filehandler.setLevel(INFO)
    filehandler.setFormatter(Formatter(LONGFORMAT))
    getLogger("").addHandler(filehandler)
    info("logging initialized")


# define a Handler which writes to sys.stderr
console = StreamHandler()
console.setLevel(DEBUG)
console.setFormatter(Formatter(SHORTFORMAT))
# add the handler to the root logger
getLogger("").addHandler(console)
