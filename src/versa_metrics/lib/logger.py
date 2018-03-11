# -*- coding: utf-8 -*-
"""
@author: bbaby000
"""
import logging
from logging.handlers import RotatingFileHandler

def setup_logger(name, file_name, debug=False):

   # create logger
    lgr = logging.getLogger(name)
    fh = RotatingFileHandler(file_name,
                                  maxBytes=1024*1024*10, #10MB
                                  backupCount=10)
    fh = logging.FileHandler(file_name)
    lgr.setLevel(logging.INFO)
    fh.setLevel(logging.INFO)
    if debug:
        lgr.setLevel(logging.DEBUG)
        fh.setLevel(logging.DEBUG)

   # create a formatter and set the formatter for the handler.
    frmt = \
        logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                          )
    fh.setFormatter(frmt)

   # add the Handler to the logger
    lgr.addHandler(fh)
    return lgr