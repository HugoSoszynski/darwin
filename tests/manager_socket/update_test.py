import logging
from time import sleep
from manager_socket.utils import requests, check_filter_files, PATH_CONF_FTEST, CONF_EMPTY, CONF_ONE, CONF_ONE_V2, CONF_THREE, CONF_THREE_V2, CONF_THREE_V2_ALT, CONF_TWO_V2, CONF_FOUR_V2, CONF_FTEST, CONF_FTEST_WRONG_CONF, REQ_MONITOR, REQ_UPDATE_EMPTY, REQ_UPDATE_ONE, REQ_UPDATE_TWO, REQ_UPDATE_THREE, REQ_UPDATE_NON_EXISTING, REQ_UPDATE_NO_FILTER, RESP_EMPTY, RESP_TEST_1, RESP_TEST_2, RESP_TEST_3, RESP_TEST_4, RESP_STATUS_OK, RESP_STATUS_KO, RESP_ERROR_FILTER_NOT_EXISTING
from tools.darwin_utils import darwin_configure, darwin_remove_configuration, darwin_start, darwin_stop
from tools.output import print_result


def run():
    tests = [
        no_filter_to_none,
        no_filter_to_one,
        no_filter_to_one_conf_v2,
        no_filter_to_many,
        no_filter_to_many_conf_v2,
        one_filter_to_none,
        one_filter_to_none_conf_v2,
        many_filters_to_none,
        many_filters_to_none_conf_v2,
        many_filters_to_one,
        many_filters_to_one_conf_v2,
        one_update_none,
        one_update_none_conf_v2,
        one_update_one,
        one_update_one_conf_v2,
        one_update_one_wrong_conf,
        one_update_one_wrong_conf_conf_v2,
        many_update_none,
        many_update_none_conf_v2,
        many_update_one,
        many_update_one_conf_v2,
        many_update_many,
        many_update_many_conf_v2,
        many_update_two_wrong_conf_conf_v2,
        many_update_two_wrong_conf,
        many_update_all,
        many_update_all_conf_v2,
        many_update_all_wrong_conf,
        many_update_all_wrong_conf_conf_v2,
        non_existing_filter,
        non_existing_filter_conf_v2,
        update_no_filter,
        many_update_diff_one_more_v2,
        many_update_diff_one_less_v2,
        many_update_diff_one_more_one_less_v2,
    ]

    for i in tests:
        print_result("Update: " + i.__name__, i)


def no_filter_to_none():
    ret = True

    darwin_configure(CONF_EMPTY)
    process = darwin_start()

    resp = requests(REQ_MONITOR)
    if RESP_EMPTY not in resp:
        logging.error("no_filter_to_none: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    resp = requests(REQ_UPDATE_EMPTY)
    if RESP_STATUS_OK not in resp:
        logging.error("no_filter_to_none: Update response error; got \"{}\"".format(resp))
        ret = False

    resp = requests(REQ_MONITOR)
    if RESP_EMPTY not in resp:
        logging.error("no_filter_to_none: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    darwin_stop(process)
    darwin_remove_configuration()
    return ret


def no_filter_to_one():

    ret = True

    darwin_configure(CONF_EMPTY)
    process = darwin_start()

    resp = requests(REQ_MONITOR)
    if RESP_EMPTY not in resp:
        logging.error("no_filter_to_one: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    darwin_configure(CONF_ONE)
    darwin_configure(CONF_FTEST, path=PATH_CONF_FTEST)
    resp = requests(REQ_UPDATE_ONE)
    if RESP_STATUS_OK not in resp:
        logging.error("no_filter_to_one: Update response error; got \"{}\"".format(resp))
        ret = False

    resp = requests(REQ_MONITOR)
    if RESP_TEST_1 not in resp:
        logging.error("no_filter_to_one: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    darwin_stop(process)
    darwin_remove_configuration()
    darwin_remove_configuration(path=PATH_CONF_FTEST)
    return ret

def no_filter_to_one_conf_v2():

    ret = True

    darwin_configure(CONF_EMPTY)
    process = darwin_start()

    resp = requests(REQ_MONITOR)
    if RESP_EMPTY not in resp:
        logging.error("no_filter_to_one: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    darwin_configure(CONF_ONE_V2)
    darwin_configure(CONF_FTEST, path=PATH_CONF_FTEST)
    resp = requests(REQ_UPDATE_ONE)
    if RESP_STATUS_OK not in resp:
        logging.error("no_filter_to_one: Update response error; got \"{}\"".format(resp))
        ret = False

    resp = requests(REQ_MONITOR)
    if RESP_TEST_1 not in resp:
        logging.error("no_filter_to_one: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    darwin_stop(process)
    darwin_remove_configuration()
    darwin_remove_configuration(path=PATH_CONF_FTEST)
    return ret


def no_filter_to_many():

    ret = True

    darwin_configure(CONF_EMPTY)
    process = darwin_start()

    resp = requests(REQ_MONITOR)
    if RESP_EMPTY not in resp:
        logging.error("no_filter_to_many: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    darwin_configure(CONF_THREE)
    darwin_configure(CONF_FTEST, path=PATH_CONF_FTEST)
    resp = requests(REQ_UPDATE_THREE)
    if RESP_STATUS_OK not in resp:
        logging.error("no_filter_to_many: Update response error; got \"{}\"".format(resp))
        ret = False

    resp = requests(REQ_MONITOR)
    if not all(x in resp for x in [RESP_TEST_1, RESP_TEST_2, RESP_TEST_3]):
        logging.error("no_filter_to_many: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    darwin_stop(process)
    darwin_remove_configuration()
    darwin_remove_configuration(path=PATH_CONF_FTEST)
    return ret

def no_filter_to_many_conf_v2():

    ret = True

    darwin_configure(CONF_EMPTY)
    process = darwin_start()

    resp = requests(REQ_MONITOR)
    if RESP_EMPTY not in resp:
        logging.error("no_filter_to_many: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    darwin_configure(CONF_THREE_V2)
    darwin_configure(CONF_FTEST, path=PATH_CONF_FTEST)
    resp = requests(REQ_UPDATE_THREE)
    if RESP_STATUS_OK not in resp:
        logging.error("no_filter_to_many: Update response error; got \"{}\"".format(resp))
        ret = False

    resp = requests(REQ_MONITOR)
    if not all(x in resp for x in [RESP_TEST_1, RESP_TEST_2, RESP_TEST_3]):
        logging.error("no_filter_to_many: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    darwin_stop(process)
    darwin_remove_configuration()
    darwin_remove_configuration(path=PATH_CONF_FTEST)
    return ret

def one_filter_to_none():

    ret = True

    darwin_configure(CONF_ONE)
    darwin_configure(CONF_FTEST, path=PATH_CONF_FTEST)
    process = darwin_start()

    resp = requests(REQ_MONITOR)
    if RESP_TEST_1 not in resp:
        logging.error("one_filter_to_none: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    darwin_configure(CONF_EMPTY)
    resp = requests(REQ_UPDATE_ONE)
    if RESP_STATUS_OK not in resp:
        logging.error("one_filter_to_none: Update response error; got \"{}\"".format(resp))
        ret = False

    resp = requests(REQ_MONITOR)
    if RESP_EMPTY not in resp:
        logging.error("one_filter_to_none: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    darwin_stop(process)
    darwin_remove_configuration()
    darwin_remove_configuration(path=PATH_CONF_FTEST)
    return ret

def one_filter_to_none_conf_v2():

    ret = True

    darwin_configure(CONF_ONE_V2)
    darwin_configure(CONF_FTEST, path=PATH_CONF_FTEST)
    process = darwin_start()

    resp = requests(REQ_MONITOR)
    if RESP_TEST_1 not in resp:
        logging.error("one_filter_to_none: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    darwin_configure(CONF_EMPTY)
    resp = requests(REQ_UPDATE_ONE)
    if RESP_STATUS_OK not in resp:
        logging.error("one_filter_to_none: Update response error; got \"{}\"".format(resp))
        ret = False

    resp = requests(REQ_MONITOR)
    if RESP_EMPTY not in resp:
        logging.error("one_filter_to_none: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    darwin_stop(process)
    darwin_remove_configuration()
    darwin_remove_configuration(path=PATH_CONF_FTEST)
    return ret

def many_filters_to_none():

    ret = True

    darwin_configure(CONF_THREE)
    darwin_configure(CONF_FTEST, path=PATH_CONF_FTEST)
    process = darwin_start()

    resp = requests(REQ_MONITOR)
    if not all(x in resp for x in [RESP_TEST_1, RESP_TEST_2, RESP_TEST_3]):
        logging.error("many_filters_to_none: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    darwin_configure(CONF_EMPTY)
    resp = requests(REQ_UPDATE_THREE)
    if RESP_STATUS_OK not in resp:
        logging.error("many_filters_to_none: Update response error; got \"{}\"".format(resp))
        ret = False

    resp = requests(REQ_MONITOR)
    if RESP_EMPTY not in resp:
        logging.error("many_filters_to_none: Mismatching second monitor response; got \"{}\"".format(resp))
        ret = False

    darwin_stop(process)
    darwin_remove_configuration()
    darwin_remove_configuration(path=PATH_CONF_FTEST)
    return ret

def many_filters_to_none_conf_v2():

    ret = True

    darwin_configure(CONF_THREE_V2)
    darwin_configure(CONF_FTEST, path=PATH_CONF_FTEST)
    process = darwin_start()

    resp = requests(REQ_MONITOR)
    if not all(x in resp for x in [RESP_TEST_1, RESP_TEST_2, RESP_TEST_3]):
        logging.error("many_filters_to_none: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    darwin_configure(CONF_EMPTY)
    resp = requests(REQ_UPDATE_THREE)
    if RESP_STATUS_OK not in resp:
        logging.error("many_filters_to_none: Update response error; got \"{}\"".format(resp))
        ret = False

    resp = requests(REQ_MONITOR)
    if RESP_EMPTY not in resp:
        logging.error("many_filters_to_none: Mismatching second monitor response; got \"{}\"".format(resp))
        ret = False

    darwin_stop(process)
    darwin_remove_configuration()
    darwin_remove_configuration(path=PATH_CONF_FTEST)
    return ret


def many_filters_to_one():

    ret = True

    darwin_configure(CONF_THREE)
    darwin_configure(CONF_FTEST, path=PATH_CONF_FTEST)
    process = darwin_start()

    resp = requests(REQ_MONITOR)
    if not all(x in resp for x in [RESP_TEST_1, RESP_TEST_2, RESP_TEST_3]):
        logging.error("many_filters_to_one: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    sleep(1) # Need this because of the starting delay
    darwin_configure(CONF_ONE)
    resp = requests(REQ_UPDATE_TWO)
    if RESP_STATUS_OK not in resp:
        logging.error("many_filters_to_one: Update response error; got \"{}\"".format(resp))
        ret = False

    sleep(1)
    resp = requests(REQ_MONITOR)
    if RESP_TEST_1 not in resp:
        logging.error("many_filters_to_one: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    darwin_stop(process)
    darwin_remove_configuration()
    darwin_remove_configuration(path=PATH_CONF_FTEST)
    return ret


def many_filters_to_one_conf_v2():

    ret = True

    darwin_configure(CONF_THREE_V2)
    darwin_configure(CONF_FTEST, path=PATH_CONF_FTEST)
    process = darwin_start()

    resp = requests(REQ_MONITOR)
    if not all(x in resp for x in [RESP_TEST_1, RESP_TEST_2, RESP_TEST_3]):
        logging.error("many_filters_to_one: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    sleep(1) # Need this because of the starting delay
    darwin_configure(CONF_ONE_V2)
    resp = requests(REQ_UPDATE_TWO)
    if RESP_STATUS_OK not in resp:
        logging.error("many_filters_to_one: Update response error; got \"{}\"".format(resp))
        ret = False

    sleep(1)
    resp = requests(REQ_MONITOR)
    if RESP_TEST_1 not in resp:
        logging.error("many_filters_to_one: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    darwin_stop(process)
    darwin_remove_configuration()
    darwin_remove_configuration(path=PATH_CONF_FTEST)
    return ret


def one_update_none():

    ret = True

    darwin_configure(CONF_ONE)
    darwin_configure(CONF_FTEST, path=PATH_CONF_FTEST)
    process = darwin_start()

    resp = requests(REQ_MONITOR)
    if RESP_TEST_1 not in resp:
        logging.error("one_update_none: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    sleep(1) # Need this because of the starting delay
    resp = requests(REQ_UPDATE_EMPTY)
    if RESP_STATUS_OK not in resp:
        logging.error("one_update_none: Update response error; got \"{}\"".format(resp))
        ret = False

    sleep(1) # Need this because of the starting delay
    resp = requests(REQ_MONITOR)
    if RESP_TEST_1 not in resp:
        logging.error("one_update_none: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    darwin_stop(process)
    darwin_remove_configuration()
    darwin_remove_configuration(path=PATH_CONF_FTEST)
    return ret


def one_update_none_conf_v2():

    ret = True

    darwin_configure(CONF_ONE_V2)
    darwin_configure(CONF_FTEST, path=PATH_CONF_FTEST)
    process = darwin_start()

    resp = requests(REQ_MONITOR)
    if RESP_TEST_1 not in resp:
        logging.error("one_update_none: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    sleep(1) # Need this because of the starting delay
    resp = requests(REQ_UPDATE_EMPTY)
    if RESP_STATUS_OK not in resp:
        logging.error("one_update_none: Update response error; got \"{}\"".format(resp))
        ret = False

    sleep(1) # Need this because of the starting delay
    resp = requests(REQ_MONITOR)
    if RESP_TEST_1 not in resp:
        logging.error("one_update_none: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    darwin_stop(process)
    darwin_remove_configuration()
    darwin_remove_configuration(path=PATH_CONF_FTEST)
    return ret


def one_update_one():

    ret = True

    darwin_configure(CONF_ONE)
    darwin_configure(CONF_FTEST, path=PATH_CONF_FTEST)
    process = darwin_start()

    resp = requests(REQ_MONITOR)
    if RESP_TEST_1 not in resp:
        logging.error("one_update_one: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    sleep(2) # Need this because of the starting delay
    resp = requests(REQ_UPDATE_ONE)
    if RESP_STATUS_OK not in resp:
        logging.error("one_update_one: Update response error; got \"{}\"".format(resp))
        ret = False

    sleep(1) # Need this because of the starting delay
    resp = requests(REQ_MONITOR)
    if RESP_TEST_1 not in resp:
        logging.error("one_update_one: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    darwin_stop(process)
    darwin_remove_configuration()
    darwin_remove_configuration(path=PATH_CONF_FTEST)
    return ret


def one_update_one_conf_v2():

    ret = True

    darwin_configure(CONF_ONE_V2)
    darwin_configure(CONF_FTEST, path=PATH_CONF_FTEST)
    process = darwin_start()

    resp = requests(REQ_MONITOR)
    if RESP_TEST_1 not in resp:
        logging.error("one_update_one: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    sleep(2) # Need this because of the starting delay
    resp = requests(REQ_UPDATE_ONE)
    if RESP_STATUS_OK not in resp:
        logging.error("one_update_one: Update response error; got \"{}\"".format(resp))
        ret = False

    sleep(1) # Need this because of the starting delay
    resp = requests(REQ_MONITOR)
    if RESP_TEST_1 not in resp:
        logging.error("one_update_one: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    darwin_stop(process)
    darwin_remove_configuration()
    darwin_remove_configuration(path=PATH_CONF_FTEST)
    return ret


def one_update_one_wrong_conf():

    ret = True

    darwin_configure(CONF_ONE)
    darwin_configure(CONF_FTEST, path=PATH_CONF_FTEST)
    process = darwin_start()

    resp = requests(REQ_MONITOR)
    if RESP_TEST_1 not in resp:
        logging.error("one_update_one_wrong_conf: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    sleep(2) # Need this because of the starting delay
    darwin_configure(CONF_FTEST_WRONG_CONF, path=PATH_CONF_FTEST)
    resp = requests(REQ_UPDATE_ONE)
    if RESP_STATUS_KO not in resp:
        logging.error("one_update_one_wrong_conf: Update response error; got \"{}\"".format(resp))
        ret = False

    resp = requests(REQ_MONITOR)
    if RESP_TEST_1 not in resp:
        logging.error("one_update_one_wrong_conf: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    if not check_filter_files("test_1", ".1"):
        logging.error("Error: filter files check failed")
        ret = False

    darwin_stop(process)
    darwin_remove_configuration()
    darwin_remove_configuration(path=PATH_CONF_FTEST)
    return ret


def one_update_one_wrong_conf_conf_v2():

    ret = True

    darwin_configure(CONF_ONE_V2)
    darwin_configure(CONF_FTEST, path=PATH_CONF_FTEST)
    process = darwin_start()

    resp = requests(REQ_MONITOR)
    if RESP_TEST_1 not in resp:
        logging.error("one_update_one_wrong_conf: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    sleep(2) # Need this because of the starting delay
    darwin_configure(CONF_FTEST_WRONG_CONF, path=PATH_CONF_FTEST)
    resp = requests(REQ_UPDATE_ONE)
    if RESP_STATUS_KO not in resp:
        logging.error("one_update_one_wrong_conf: Update response error; got \"{}\"".format(resp))
        ret = False

    resp = requests(REQ_MONITOR)
    if RESP_TEST_1 not in resp:
        logging.error("one_update_one_wrong_conf: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    if not check_filter_files("test_1", ".1"):
        logging.error("Error: filter files check failed")
        ret = False

    darwin_stop(process)
    darwin_remove_configuration()
    darwin_remove_configuration(path=PATH_CONF_FTEST)
    return ret


def many_update_none():

    ret = True

    darwin_configure(CONF_THREE)
    darwin_configure(CONF_FTEST, path=PATH_CONF_FTEST)
    process = darwin_start()

    resp = requests(REQ_MONITOR)
    if not all(x in resp for x in [RESP_TEST_1, RESP_TEST_2, RESP_TEST_3]):
        logging.error("many_update_none: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    sleep(1) # Need this because of the starting delay
    resp = requests(REQ_UPDATE_EMPTY)
    if RESP_STATUS_OK not in resp:
        logging.error("many_update_none: Update response error; got \"{}\"".format(resp))
        ret = False

    resp = requests(REQ_MONITOR)
    if not all(x in resp for x in [RESP_TEST_1, RESP_TEST_2, RESP_TEST_3]):
        logging.error("many_update_none: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    darwin_stop(process)
    darwin_remove_configuration()
    darwin_remove_configuration(path=PATH_CONF_FTEST)
    return ret


def many_update_none_conf_v2():

    ret = True

    darwin_configure(CONF_THREE_V2)
    darwin_configure(CONF_FTEST, path=PATH_CONF_FTEST)
    process = darwin_start()

    resp = requests(REQ_MONITOR)
    if not all(x in resp for x in [RESP_TEST_1, RESP_TEST_2, RESP_TEST_3]):
        logging.error("many_update_none: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    sleep(1) # Need this because of the starting delay
    resp = requests(REQ_UPDATE_EMPTY)
    if RESP_STATUS_OK not in resp:
        logging.error("many_update_none: Update response error; got \"{}\"".format(resp))
        ret = False

    resp = requests(REQ_MONITOR)
    if not all(x in resp for x in [RESP_TEST_1, RESP_TEST_2, RESP_TEST_3]):
        logging.error("many_update_none: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    darwin_stop(process)
    darwin_remove_configuration()
    darwin_remove_configuration(path=PATH_CONF_FTEST)
    return ret


def many_update_one():

    ret = True

    darwin_configure(CONF_THREE)
    darwin_configure(CONF_FTEST, path=PATH_CONF_FTEST)
    process = darwin_start()

    resp = requests(REQ_MONITOR)
    if not all(x in resp for x in [RESP_TEST_1, RESP_TEST_2, RESP_TEST_3]):
        logging.error("many_update_one: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    sleep(1) # Need this because of the starting delay
    resp = requests(REQ_UPDATE_ONE)
    if RESP_STATUS_OK not in resp:
        logging.error("many_update_one: Update response error; got \"{}\"".format(resp))
        ret = False

    resp = requests(REQ_MONITOR)
    if not all(x in resp for x in [RESP_TEST_1, RESP_TEST_2, RESP_TEST_3]):
        logging.error("many_update_one: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    darwin_stop(process)
    darwin_remove_configuration()
    darwin_remove_configuration(path=PATH_CONF_FTEST)
    return ret


def many_update_one_conf_v2():

    ret = True

    darwin_configure(CONF_THREE_V2)
    darwin_configure(CONF_FTEST, path=PATH_CONF_FTEST)
    process = darwin_start()

    resp = requests(REQ_MONITOR)
    if not all(x in resp for x in [RESP_TEST_1, RESP_TEST_2, RESP_TEST_3]):
        logging.error("many_update_one: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    sleep(1) # Need this because of the starting delay
    resp = requests(REQ_UPDATE_ONE)
    if RESP_STATUS_OK not in resp:
        logging.error("many_update_one: Update response error; got \"{}\"".format(resp))
        ret = False

    resp = requests(REQ_MONITOR)
    if not all(x in resp for x in [RESP_TEST_1, RESP_TEST_2, RESP_TEST_3]):
        logging.error("many_update_one: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    darwin_stop(process)
    darwin_remove_configuration()
    darwin_remove_configuration(path=PATH_CONF_FTEST)
    return ret


def many_update_many():
    ret = True

    darwin_configure(CONF_THREE)
    darwin_configure(CONF_FTEST, path=PATH_CONF_FTEST)
    process = darwin_start()

    resp = requests(REQ_MONITOR)
    if not all(x in resp for x in [RESP_TEST_1, RESP_TEST_2, RESP_TEST_3]):
        logging.error("many_update_many: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    sleep(1) # Need this because of the starting delay
    resp = requests(REQ_UPDATE_TWO)
    if RESP_STATUS_OK not in resp:
        logging.error("many_update_many: Update response error; got \"{}\"".format(resp))
        ret = False

    resp = requests(REQ_MONITOR)
    if not all(x in resp for x in [RESP_TEST_1, RESP_TEST_2, RESP_TEST_3]):
        logging.error("many_update_many: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    darwin_stop(process)
    darwin_remove_configuration()
    darwin_remove_configuration(path=PATH_CONF_FTEST)
    return ret


def many_update_many_conf_v2():
    ret = True

    darwin_configure(CONF_THREE_V2)
    darwin_configure(CONF_FTEST, path=PATH_CONF_FTEST)
    process = darwin_start()

    resp = requests(REQ_MONITOR)
    if not all(x in resp for x in [RESP_TEST_1, RESP_TEST_2, RESP_TEST_3]):
        logging.error("many_update_many: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    sleep(1) # Need this because of the starting delay
    resp = requests(REQ_UPDATE_TWO)
    if RESP_STATUS_OK not in resp:
        logging.error("many_update_many: Update response error; got \"{}\"".format(resp))
        ret = False

    resp = requests(REQ_MONITOR)
    if not all(x in resp for x in [RESP_TEST_1, RESP_TEST_2, RESP_TEST_3]):
        logging.error("many_update_many: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    darwin_stop(process)
    darwin_remove_configuration()
    darwin_remove_configuration(path=PATH_CONF_FTEST)
    return ret


def many_update_two_wrong_conf():

    ret = True

    darwin_configure(CONF_THREE)
    darwin_configure(CONF_FTEST, path=PATH_CONF_FTEST)
    process = darwin_start()

    resp = requests(REQ_MONITOR)
    if not all(x in resp for x in [RESP_TEST_1, RESP_TEST_2, RESP_TEST_3]):
        logging.error("one_update_one_wrong_conf: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    sleep(2) # Need this because of the starting delay
    darwin_configure(CONF_FTEST_WRONG_CONF, path=PATH_CONF_FTEST)
    resp = requests(REQ_UPDATE_TWO)
    if RESP_STATUS_KO not in resp:
        logging.error("one_update_one_wrong_conf: Update response error; got \"{}\"".format(resp))
        ret = False

    resp = requests(REQ_MONITOR)
    if not all(x in resp for x in [RESP_TEST_1, RESP_TEST_2, RESP_TEST_3]):
        logging.error("one_update_one_wrong_conf: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    if not check_filter_files("test_2", ".1"):
        logging.error("Error: filter files check failed")
        ret = False

    if not check_filter_files("test_3", ".1"):
        logging.error("Error: filter files check failed")
        ret = False

    darwin_stop(process)
    darwin_remove_configuration()
    darwin_remove_configuration(path=PATH_CONF_FTEST)
    return ret


def many_update_two_wrong_conf_conf_v2():

    ret = True

    darwin_configure(CONF_THREE_V2)
    darwin_configure(CONF_FTEST, path=PATH_CONF_FTEST)
    process = darwin_start()

    resp = requests(REQ_MONITOR)
    if not all(x in resp for x in [RESP_TEST_1, RESP_TEST_2, RESP_TEST_3]):
        logging.error("one_update_one_wrong_conf: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    sleep(2) # Need this because of the starting delay
    darwin_configure(CONF_FTEST_WRONG_CONF, path=PATH_CONF_FTEST)
    resp = requests(REQ_UPDATE_TWO)
    if RESP_STATUS_KO not in resp:
        logging.error("one_update_one_wrong_conf: Update response error; got \"{}\"".format(resp))
        ret = False

    resp = requests(REQ_MONITOR)
    if not all(x in resp for x in [RESP_TEST_1, RESP_TEST_2, RESP_TEST_3]):
        logging.error("one_update_one_wrong_conf: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    if not check_filter_files("test_2", ".1"):
        logging.error("Error: filter files check failed")
        ret = False

    if not check_filter_files("test_3", ".1"):
        logging.error("Error: filter files check failed")
        ret = False

    darwin_stop(process)
    darwin_remove_configuration()
    darwin_remove_configuration(path=PATH_CONF_FTEST)
    return ret


def many_update_all_wrong_conf():

    ret = True

    darwin_configure(CONF_THREE)
    darwin_configure(CONF_FTEST, path=PATH_CONF_FTEST)
    process = darwin_start()

    resp = requests(REQ_MONITOR)
    if not all(x in resp for x in [RESP_TEST_1, RESP_TEST_2, RESP_TEST_3]):
        logging.error("one_update_one_wrong_conf: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    sleep(2) # Need this because of the starting delay
    darwin_configure(CONF_FTEST_WRONG_CONF, path=PATH_CONF_FTEST)
    resp = requests(REQ_UPDATE_THREE)
    if RESP_STATUS_KO not in resp:
        logging.error("one_update_one_wrong_conf: Update response error; got \"{}\"".format(resp))
        ret = False

    resp = requests(REQ_MONITOR)
    if not all(x in resp for x in [RESP_TEST_1, RESP_TEST_2, RESP_TEST_3]):
        logging.error("one_update_one_wrong_conf: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    if not check_filter_files("test_1", ".1"):
        logging.error("Error: filter files check failed")
        ret = False

    if not check_filter_files("test_2", ".1"):
        logging.error("Error: filter files check failed")
        ret = False

    if not check_filter_files("test_3", ".1"):
        logging.error("Error: filter files check failed")
        ret = False

    darwin_stop(process)
    darwin_remove_configuration()
    darwin_remove_configuration(path=PATH_CONF_FTEST)
    return ret


def many_update_all_wrong_conf_conf_v2():

    ret = True

    darwin_configure(CONF_THREE_V2)
    darwin_configure(CONF_FTEST, path=PATH_CONF_FTEST)
    process = darwin_start()

    resp = requests(REQ_MONITOR)
    if not all(x in resp for x in [RESP_TEST_1, RESP_TEST_2, RESP_TEST_3]):
        logging.error("one_update_one_wrong_conf: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    sleep(2) # Need this because of the starting delay
    darwin_configure(CONF_FTEST_WRONG_CONF, path=PATH_CONF_FTEST)
    resp = requests(REQ_UPDATE_THREE)
    if RESP_STATUS_KO not in resp:
        logging.error("one_update_one_wrong_conf: Update response error; got \"{}\"".format(resp))
        ret = False

    resp = requests(REQ_MONITOR)
    if not all(x in resp for x in [RESP_TEST_1, RESP_TEST_2, RESP_TEST_3]):
        logging.error("one_update_one_wrong_conf: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    if not check_filter_files("test_1", ".1"):
        logging.error("Error: filter files check failed")
        ret = False

    if not check_filter_files("test_2", ".1"):
        logging.error("Error: filter files check failed")
        ret = False

    if not check_filter_files("test_3", ".1"):
        logging.error("Error: filter files check failed")
        ret = False

    darwin_stop(process)
    darwin_remove_configuration()
    darwin_remove_configuration(path=PATH_CONF_FTEST)
    return ret


def many_update_all():

    ret = True

    darwin_configure(CONF_THREE)
    darwin_configure(CONF_FTEST, path=PATH_CONF_FTEST)
    process = darwin_start()

    resp = requests(REQ_MONITOR)
    if not all(x in resp for x in [RESP_TEST_1, RESP_TEST_2, RESP_TEST_3]):
        logging.error("many_update_all: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    sleep(1) # Need this because of the starting delay
    resp = requests(REQ_UPDATE_THREE)
    if RESP_STATUS_OK not in resp:
        logging.error("many_update_all: Update response error; got \"{}\"".format(resp))
        ret = False

    resp = requests(REQ_MONITOR)
    if not all(x in resp for x in [RESP_TEST_1, RESP_TEST_2, RESP_TEST_3]):
        logging.error("many_update_all: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    darwin_stop(process)
    darwin_remove_configuration()
    darwin_remove_configuration(path=PATH_CONF_FTEST)
    return ret


def many_update_all_conf_v2():

    ret = True

    darwin_configure(CONF_THREE_V2)
    darwin_configure(CONF_FTEST, path=PATH_CONF_FTEST)
    process = darwin_start()

    resp = requests(REQ_MONITOR)
    if not all(x in resp for x in [RESP_TEST_1, RESP_TEST_2, RESP_TEST_3]):
        logging.error("many_update_all: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    sleep(1) # Need this because of the starting delay
    resp = requests(REQ_UPDATE_THREE)
    if RESP_STATUS_OK not in resp:
        logging.error("many_update_all: Update response error; got \"{}\"".format(resp))
        ret = False

    resp = requests(REQ_MONITOR)
    if not all(x in resp for x in [RESP_TEST_1, RESP_TEST_2, RESP_TEST_3]):
        logging.error("many_update_all: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    darwin_stop(process)
    darwin_remove_configuration()
    darwin_remove_configuration(path=PATH_CONF_FTEST)
    return ret


def non_existing_filter():

    ret = True

    darwin_configure(CONF_THREE)
    darwin_configure(CONF_FTEST, path=PATH_CONF_FTEST)
    process = darwin_start()

    resp = requests(REQ_MONITOR)
    if not all(x in resp for x in [RESP_TEST_1, RESP_TEST_2, RESP_TEST_3]):
        logging.error("non_existing_filter: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    sleep(1) # Need this because of the starting delay
    resp = requests(REQ_UPDATE_NON_EXISTING)
    if RESP_ERROR_FILTER_NOT_EXISTING not in resp:
        logging.error("non_existing_filter: Update response error; got \"{}\"".format(resp))
        ret = False

    resp = requests(REQ_MONITOR)
    if not all(x in resp for x in [RESP_TEST_1, RESP_TEST_2, RESP_TEST_3]):
        logging.error("non_existing_filter: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    darwin_stop(process)
    darwin_remove_configuration()
    darwin_remove_configuration(path=PATH_CONF_FTEST)
    return ret


def non_existing_filter_conf_v2():

    ret = True

    darwin_configure(CONF_THREE_V2)
    darwin_configure(CONF_FTEST, path=PATH_CONF_FTEST)
    process = darwin_start()

    resp = requests(REQ_MONITOR)
    if not all(x in resp for x in [RESP_TEST_1, RESP_TEST_2, RESP_TEST_3]):
        logging.error("non_existing_filter: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    sleep(1) # Need this because of the starting delay
    resp = requests(REQ_UPDATE_NON_EXISTING)
    if RESP_ERROR_FILTER_NOT_EXISTING not in resp:
        logging.error("non_existing_filter: Update response error; got \"{}\"".format(resp))
        ret = False

    resp = requests(REQ_MONITOR)
    if not all(x in resp for x in [RESP_TEST_1, RESP_TEST_2, RESP_TEST_3]):
        logging.error("non_existing_filter: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    darwin_stop(process)
    darwin_remove_configuration()
    darwin_remove_configuration(path=PATH_CONF_FTEST)
    return ret


def update_no_filter():

    ret = True

    darwin_configure(CONF_ONE)
    darwin_configure(CONF_FTEST, path=PATH_CONF_FTEST)
    process = darwin_start()

    resp = requests(REQ_MONITOR)
    if RESP_TEST_1 not in resp:
        logging.error("update_no_filter: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    sleep(1) # Need this because of the starting delay
    resp = requests(REQ_UPDATE_NO_FILTER)
    if RESP_STATUS_OK not in resp:
        logging.error("update_no_filter: Update response error; got \"{}\"".format(resp))
        ret = False

    resp = requests(REQ_MONITOR)
    if RESP_TEST_1 not in resp:
        logging.error("update_no_filter: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    darwin_stop(process)
    darwin_remove_configuration()
    darwin_remove_configuration(path=PATH_CONF_FTEST)
    return ret


def many_update_diff_one_more_v2():

    ret = True

    darwin_configure(CONF_THREE_V2)
    darwin_configure(CONF_FTEST, path=PATH_CONF_FTEST)
    process = darwin_start()

    resp = requests(REQ_MONITOR)
    if not all(x in resp for x in [RESP_TEST_1, RESP_TEST_2, RESP_TEST_3]):
        logging.error("many_update_diff_one_more_v2: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    sleep(1) # Need this because of the starting delay
    darwin_configure(CONF_FOUR_V2)
    resp = requests(REQ_UPDATE_EMPTY)
    if RESP_STATUS_OK not in resp:
        logging.error("many_update_diff_one_more_v2: Update response error; got \"{}\"".format(resp))
        ret = False

    resp = requests(REQ_MONITOR)
    if not all(x in resp for x in [RESP_TEST_1, RESP_TEST_2, RESP_TEST_3, RESP_TEST_4]):
        logging.error("many_update_diff_one_more_v2: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    darwin_stop(process)
    darwin_remove_configuration()
    darwin_remove_configuration(path=PATH_CONF_FTEST)
    return ret


def many_update_diff_one_less_v2():

    ret = True

    darwin_configure(CONF_THREE_V2)
    darwin_configure(CONF_FTEST, path=PATH_CONF_FTEST)
    process = darwin_start()

    resp = requests(REQ_MONITOR)
    if not all(x in resp for x in [RESP_TEST_1, RESP_TEST_2, RESP_TEST_3]):
        logging.error("many_update_diff_one_less_v2: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    sleep(1) # Need this because of the starting delay
    darwin_configure(CONF_TWO_V2)
    resp = requests(REQ_UPDATE_EMPTY)
    if RESP_STATUS_OK not in resp:
        logging.error("many_update_diff_one_less_v2: Update response error; got \"{}\"".format(resp))
        ret = False

    resp = requests(REQ_MONITOR)
    if not all(x in resp for x in [RESP_TEST_1, RESP_TEST_2]):
        logging.error("many_update_diff_one_less_v2: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    if RESP_TEST_3 in resp:
        logging.error('many_update_diff_one_less_v2: Too much filters in monitoring response; got "{}"'.format(resp))
        ret = False

    darwin_stop(process)
    darwin_remove_configuration()
    darwin_remove_configuration(path=PATH_CONF_FTEST)
    return ret


def many_update_diff_one_more_one_less_v2():

    ret = True

    darwin_configure(CONF_THREE_V2)
    darwin_configure(CONF_FTEST, path=PATH_CONF_FTEST)
    process = darwin_start()

    resp = requests(REQ_MONITOR)
    if not all(x in resp for x in [RESP_TEST_1, RESP_TEST_2, RESP_TEST_3]):
        logging.error("many_update_diff_one_more_one_less_v2: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    sleep(1) # Need this because of the starting delay
    darwin_configure(CONF_THREE_V2_ALT)
    resp = requests(REQ_UPDATE_EMPTY)
    if RESP_STATUS_OK not in resp:
        logging.error("many_update_diff_one_more_one_less_v2: Update response error; got \"{}\"".format(resp))
        ret = False

    resp = requests(REQ_MONITOR)
    if not all(x in resp for x in [RESP_TEST_1, RESP_TEST_2, RESP_TEST_4]):
        logging.error("many_update_diff_one_more_one_less_v2: Mismatching monitor response; got \"{}\"".format(resp))
        ret = False

    if RESP_TEST_3 in resp:
        logging.error('many_update_diff_one_more_one_less_v2: Wrong filter in monitor response; got "{}"'.format(resp))
        ret = False

    darwin_stop(process)
    darwin_remove_configuration()
    darwin_remove_configuration(path=PATH_CONF_FTEST)
    return ret
