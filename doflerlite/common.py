from hashlib import md5
import logging
import json
from dofler.db import Session, User


_loglevels = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warn': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL,
}
_log_to_console = False
_log_to_file = False
log = logging.getLogger('DoFler')


def log_to_console(self, level='info'):
    '''
    Enables Console logging if not already enabled. 

    :param level: The log level that is desired for the console.
                  Valid values are: debug, info, warn, error, critical
                  Default value is info.
    :type level: str 
    :return: None
    '''  
    if not _log_to_console:
        stderr = logging.StreamHandler()
        console_format = logging.Formatter('%(levelname)s %(message)s')
        stderr.setFormatter(console_format)
        log.setLevel(_loglevels[config.get('Logging', 'level')])
        log.addHandler(stderr)
        _log_to_console = True


def log_to_file(self, filename, level='debug'):
    '''
    Enables logging output to a file if not already enabled. 

    :param filename: absolute path & filename for the logfile.
    :param level: The log level that is desired for the console.
                  Valid values are: debug, info, warn, error, critical
                  Default value is info.

    :type filename: str 
    :type level: str 

    :return: None
    '''
    if not _log_to_file:
        hdlr = logging.FileHandler(filename)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        log.setLevel(_loglevels[config.get('Logging', 'level')])
        log.addHandler(hdlr)
        _log_to_fule = True


def ignore_exception(IgnoreException=Exception,DefaultVal=None):
    ''' Decorator for ignoring exception from a function
    e.g.   @ignore_exception(DivideByZero)
    e.g.2. ignore_exception(DivideByZero)(Divide)(2/0)
    From: sharjeel
    Source: stackoverflow.com
    '''
    def dec(function):
        def _dec(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except IgnoreException:
                return DefaultVal
        return _dec
    return dec
sint = ignore_exception(ValueError)(int)


def md5hash(*items):
    '''md5hash list, of, items
    A simple convenience function to return a hex md5hash of all of the
    items given.

    :param *items: list of items to hash. 
    :type *items: list
    :return: str 
    '''
    m = md5()
    for item in items:
        m.update(str(item))
    return m.hexdigest()


def jsonify(data):
    '''
    A simple shortcut for dumping json dictionaries.  This can come in handy
    if we need to make some global settings for how to return json data.

    :param data: Python dictionary dataset. 
    :type data: dict
    :return: str
    '''
    return json.dumps(data)


def auth(request, db):
    '''
    Authentication Check.  Returns True or False based on if the account 
    cookie is set.

    :prarm request: The request object for the given page. 
    :prarm db: The SQLAlchemy session object from the page. 

    :type request: request object
    :type db: Session object

    :return: bool    
    '''
    if request.remote_addr in ['127.0.0.1', 'localhost']:
        return True
    else:
        secret = db.query(Setting).filter_by(name='cookie_key').one()
        name = request.get_cookie('sensor', secret=secret.value)
        try:
            sensor = db.query(User).filter_by(name=name).one()
            return True
        except:
            return False


def auth_login(request, db):
    '''
    Base Login Function.  This function is what will handle all of the
    authentication for the API and the UI.  While both behave differently as 
    they are different interfaces into the data, they both handle authentication
    the same way.

    :prarm request: The request object for the given page. 
    :prarm db: The SQLAlchemy session object from the page. 

    :type request: request object
    :type db: Session object

    :return: bool
    '''
    loggedin = False
    if not auth(request, db):
        secret = db.query(Setting).filter_by(name='cookie_key').one()
        username = request.forms.get('username')
        password = request.forms.get('password')
        try:
            user = db.query(User).filter_by(name=name).one()
        except:
            pass
        else:
            if user.check(password):
                loggedin = True
    return loggedin