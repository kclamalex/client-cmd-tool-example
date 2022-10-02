class CPXInternalError(Exception):
    """
    Raise when Exception is raised in cpx command tool
    """


class CPXExternalError(Exception):
    """
    Raise when Exception is raised in cpx command tool
    """


class CPXValueError(ValueError):
    """
    Raise when ValueError is raised in cpx command tool
    """


class CPXNotImplementedError(NotImplementedError):
    """
    Raise when NotImplementedError is raised in cpx command tool
    """


class CPXHttpClientError(CPXInternalError):
    """
    Raise when HTTP client error is raised in cpx command tool
    """


class CPXHttpServerError(CPXExternalError):
    """
    Raise when HTTP server error is raised in cpx command tool
    """


class CPXUnknownError(CPXInternalError):
    """
    Raise when unknown error is raised in cpx command tool
    """
