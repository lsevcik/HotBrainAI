def raise_exception_if(status):
    if status.Success == 0:
        err_msg = ''.join([chr(i) for i in status.ErrorMsg]).rstrip('\x00')
        raise Exception('Code {0}. Message:{1}'.format(status.Error, err_msg))
