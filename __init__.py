from management import HandlerManager

mgr = HandlerManager()

def display_results(field_names, results):
    print field_names
    for result in results:
        print result

while True:
    user_input = raw_input('#>')
    field_names, results = mgr.exec_command(user_input)
    if results is not None:
        display_results(field_names, results)
