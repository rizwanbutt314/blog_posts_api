def format_query_param_error(error):
    arg_name = list(error.data['message'].keys())[0]
    return {'error': error.data['message'][arg_name]}


def sort_list_of_objects(data, sort_by, direction='asc'):
    if direction == 'asc':
        sorted_data = sorted(data, key=lambda i: i[sort_by])
    else:
        sorted_data = sorted(data, key=lambda i: i[sort_by], reverse=True)

    return sorted_data
