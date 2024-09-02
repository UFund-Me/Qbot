import logging
import sys
import traceback


def log_exception(level):
    exc_type, exc_value, exc_traceback = sys.exc_info()
    for i in traceback.extract_tb(exc_traceback):
        # line = (os.path.basename(i[0]), i[1], i[2])
        line = (i[0], i[1], i[2])
        logging.log(level, 'File "%s", line %d, in %s' % line)
        logging.log(level, "\t%s" % i[3])
