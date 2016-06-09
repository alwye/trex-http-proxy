error = {
    'not_implemented': {
        'err_code': 'not_implemented',
        'err_description': 'Method is not implemented',
        'err_resolution': 'Check '
    }
}


# Get an error details by its code
def get_error_message(code):
    return error[code]
