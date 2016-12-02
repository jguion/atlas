
#Helper methods
def get_node_color(status):
    if status >= 100:
        return 'rgb(131, 217, 116)'
    elif status >= 50:
        return 'rgb(255, 201, 70)'
    else:
        return 'rgb(241, 138, 114)'
