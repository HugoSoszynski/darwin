/// \file     Generator.cpp
/// \authors  Hugo Soszynski
/// \version  1.0
/// \date     25/11/19
/// \license  GPLv3
/// \brief    Copyright (c) 2019 Advens. All rights reserved.

#include <fstream>
#include <random>
#include <string>

#include "../../toolkit/lru_cache.hpp"
#include "base/Logger.hpp"
#include "Generator.hpp"
#include "SofaTask.hpp"
#include "AlertManager.hpp"

bool Generator::ConfigureAlerting(const std::string& tags) {
    DARWIN_LOGGER;

    DARWIN_LOG_DEBUG("Sofa:: ConfigureAlerting:: Configuring Alerting");
    DARWIN_ALERT_MANAGER_SET_FILTER_NAME(DARWIN_FILTER_NAME);
    DARWIN_ALERT_MANAGER_SET_RULE_NAME(DARWIN_ALERT_RULE_NAME);
    if (tags.empty()) {
        DARWIN_LOG_DEBUG("Sofa:: ConfigureAlerting:: No alert tags provided in the configuration. Using default.");
        DARWIN_ALERT_MANAGER_SET_TAGS(DARWIN_ALERT_TAGS);
    } else {
        DARWIN_ALERT_MANAGER_SET_TAGS(tags);
    }
    return true;
}

bool Generator::LoadConfig(const rapidjson::Document &configuration) {
    DARWIN_LOGGER;
    DARWIN_LOG_DEBUG("SofaTask:: Generator:: Loading configuration file...");

    if (!configuration.HasMember("python_env_path")) {
        DARWIN_LOG_CRITICAL("SofaTask:: Generator:: Missing parameter: 'python_env_path'");
        return false;
    }

    if (!configuration["python_env_path"].IsString()) {
        DARWIN_LOG_CRITICAL("SofaTask:: Generator:: 'python_env_path' needs to be a string");
        return false;
    }

    std::string python_env_path_str = configuration["python_env_path"].GetString();

    if (!configuration.HasMember("module")) {
        DARWIN_LOG_CRITICAL("SofaTask:: Generator:: Missing parameter: 'module'");
        return false;
    }

    if (!configuration["module"].IsString()) {
        DARWIN_LOG_CRITICAL("SofaTask:: Generator:: 'module' needs to be a string");
        return false;
    }

    std::string module_str = configuration["module"].GetString();

    if (!configuration.HasMember("function")) {
        DARWIN_LOG_CRITICAL("SofaTask:: Generator:: Missing parameter: 'function'");
        return false;
    }

    if (!configuration["function"].IsString()) {
        DARWIN_LOG_CRITICAL("SofaTask:: Generator:: 'function' needs to be a string");
        return false;
    }

    std::string function_str = configuration["function"].GetString();

    bool is_custom_path = configuration.HasMember("custom_python_path");

    if (!is_custom_path) {
        return LoadPythonCode(python_env_path_str, module_str, function_str);
    }

    if (!configuration["custom_python_path"].IsString()) {
        DARWIN_LOG_CRITICAL("SofaTask:: Generator:: 'custom_python_path' needs to be a string");
        return false;
    }

    std::string custom_python_path_str = configuration["custom_python_path"].GetString();

    return LoadPythonCode(python_env_path_str, module_str, function_str, &custom_python_path_str);
}

bool Generator::LoadPythonCode(const std::string& python_env_path_str, const std::string& module_str,
                               const std::string& function_str, const std::string* custom_python_path_str) {
    DARWIN_LOGGER;

    if (!darwin::pythonutils::InitPythonProgram(python_env_path_str, &_program_name, custom_python_path_str)) {
        DARWIN_LOG_CRITICAL("SofaTask:: Generator:: Could not initialize generator: "
                            "Python program initialization went wrong");
        return false;
    }

    if (!darwin::pythonutils::ImportPythonModule(module_str, &_py_module)) {
        DARWIN_LOG_CRITICAL("SofaTask:: Generator:: Could not initialize generator: "
                            "Python module import went wrong");
        return false;
    }

    if (!darwin::pythonutils::GetPythonFunction(_py_module, function_str, &_py_function)) {
        DARWIN_LOG_CRITICAL("SofaTask:: Generator:: Could not initialize generator: "
                            "Something went wrong while getting Python function");
        return false;
    }

    return true;
}

darwin::session_ptr_t
Generator::CreateTask(boost::asio::local::stream_protocol::socket& socket,
                      darwin::Manager& manager) noexcept {
    std::string input_csv = "/var/tmp/" + RandomString() + ".csv";
    std::string output_csv = "/var/tmp/" + RandomString() + ".csv";
    std::string output_json = "/var/tmp/" + RandomString() + ".json";
    return std::static_pointer_cast<darwin::Session>(
            std::make_shared<SofaTask>(socket, manager, _cache,
                                            _cache_mutex, _py_function,
                                            input_csv, output_csv, output_json));
}

std::string Generator::RandomString() {
    std::string str("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz");
    std::random_device rd;
    std::mt19937 generator(rd());
    std::shuffle(str.begin(), str.end(), generator);
    return str.substr(0, 32);
}


Generator::~Generator() {
    darwin::pythonutils::ExitPythonProgram(&_program_name);
}