error = {
    'not_implemented': {
        'err_code': 'not_implemented',
        'err_description': 'Method is not implemented',
        'err_resolution': 'Check '
    }
}


def get_error_message(code):
    return error[code]
