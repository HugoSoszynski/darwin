import pprint
import manager_socket.monitor_test as monitor_test
import manager_socket.update_test as update_test
from tools.output import print_results

def run():
    print('Management Socket Results:')

    monitor_test.run()
    update_test.run()

    print()
    print()