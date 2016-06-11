error = {
    'not_implemented': {
        'err_code': 'not_implemented',
        'err_description': 'Method is not implemented',
        'err_resolution': 'Check your request.'
    },
    'not_json': {
        'err_code': 'not_json',
        'err_description': 'Request contains data in other than JSON format.',
        'err_resolution': 'Check your request, or contact the developer.'
    },
    'no_request_data': {
        'err_code': 'no_request_data',
        'err_description': 'Request data is empty.',
        'err_resolution': 'Check your request, or contact the developer.'
    },
    'trex_not_start': {
        'err_code': 'trex_not_start',
        'err_description': 'TRex could not start to generate traffic.',
        'err_resolution': 'Check with developer team.'
    },
}


# Get an error details by its code
def get_error_message(code):
    return error[code]
