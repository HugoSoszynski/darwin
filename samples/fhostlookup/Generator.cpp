/// \file     Generator.cpp
/// \authors  jjourdin
/// \version  1.0
/// \date     07/09/18
/// \license  GPLv3
/// \brief    Copyright (c) 2018 Advens. All rights reserved.

#include <fstream>
#include <string>

#include "../../toolkit/lru_cache.hpp"
#include "base/Logger.hpp"
#include "Generator.hpp"
#include "HostLookupTask.hpp"
#include "tsl/hopscotch_map.h"
#include "tsl/hopscotch_set.h"
#include "../toolkit/rapidjson/document.h"
#include "../toolkit/rapidjson/istreamwrapper.h"
#include "AlertManager.hpp"


bool Generator::ConfigureAlerting(const std::string& tags) {
    DARWIN_LOGGER;

    DARWIN_LOG_DEBUG("Hostlookup:: ConfigureAlerting:: Configuring Alerting");
    DARWIN_ALERT_MANAGER_SET_FILTER_NAME(DARWIN_FILTER_NAME);
    DARWIN_ALERT_MANAGER_SET_RULE_NAME(DARWIN_ALERT_RULE_NAME + this->_feed_name);
    if (tags.empty()) {
        DARWIN_LOG_DEBUG("Hostlookup:: ConfigureAlerting:: No alert tags provided in the configuration. Using default.");
        DARWIN_ALERT_MANAGER_SET_TAGS(DARWIN_ALERT_TAGS);
    } else {
        DARWIN_ALERT_MANAGER_SET_TAGS(tags);
    }
    return true;
}

bool Generator::LoadConfig(const rapidjson::Document &configuration) {
    DARWIN_LOGGER;
    DARWIN_LOG_DEBUG("HostLookup:: Generator:: Loading classifier...");
    std::string db;
    std::string db_type;

    // Load DB Name
    if (!configuration.HasMember("database")) {
        DARWIN_LOG_CRITICAL("HostLookup:: Generator:: Missing parameter: 'database'");
        return false;
    }
    if (!configuration["database"].IsString()) {
        DARWIN_LOG_CRITICAL("HostLookup:: Generator:: 'database' needs to be a string");
        return false;
    }
    db = configuration["database"].GetString();

    // Load DB Type
    if (configuration.HasMember("db_type")) {
            if (!configuration["db_type"].IsString()) {
            DARWIN_LOG_CRITICAL("HostLookup:: Generator:: 'db_type' needs to be a string");
            return false;
        }
        db_type = configuration["db_type"].GetString();
    } else {
        db_type = "text";
    }

    // Load the DB according to the given type
    if (db_type == "json") {
        return this->LoadJsonFile(db, db_type::json);
    } else if (db_type == "rsyslog") {
        return this->LoadJsonFile(db, db_type::rsyslog);
    } else if (db_type == "text") {
        return this->LoadTextFile(db);
    } else {
        DARWIN_LOG_CRITICAL("HostLookup:: Generator:: Unknown 'db_type'");
    }

    return false;
}

bool Generator::LoadTextFile(const std::string& filename) {
    DARWIN_LOGGER;
    std::ifstream file(filename.c_str());
    std::string buf;

    // Load file content
    if (!file) {
        DARWIN_LOG_CRITICAL("HostLookup:: Generator:: Configure:: Cannot open host database");
        return false;
    }
    while (!darwin::files_utils::GetLineSafe(file, buf).eof()) {
        if(file.fail() or file.bad()){
            DARWIN_LOG_CRITICAL("HostLookup:: Generator:: Configure:: Error when reading host database");
            return false;
        }
        if (!buf.empty()){
            _database.insert({buf,{"", 100}});
        }
    }
    this->LoadFeedNameFromFile(filename);
    file.close();
    return true;
}

bool Generator::LoadJsonFile(const std::string& filename, const db_type type) {
    DARWIN_LOGGER;
    std::ifstream file(filename.c_str());
    rapidjson::Document database;
    bool ret = true;

    if (!file) {
        DARWIN_LOG_CRITICAL("HostLookup:: Generator:: Configure:: Cannot open host database");
        return false;
    }
    DARWIN_LOG_DEBUG("HostlookupGenerator:: Parsing database...");
    rapidjson::IStreamWrapper isw(file);
    database.ParseStream(isw);
    if (not database.IsObject()) {
        DARWIN_LOG_CRITICAL("HostlookupGenerator:: Database is not a JSON object");
        file.close();
        return false;
    }
    if (type == db_type::json) {
        ret = this->LoadJsonDatabase(database);
    } else if (type == db_type::rsyslog) {
        this->LoadFeedNameFromFile(filename);
        ret = this->LoadRsyslogDatabase(database);
    }
    file.close();
    return ret;
}

void Generator::LoadFeedNameFromFile(const std::string& filename) {
        this->_feed_name = darwin::files_utils::GetNameFromPath(filename);
        darwin::files_utils::ReplaceExtension(this->_feed_name, "");
}

bool Generator::LoadJsonDatabase(const rapidjson::Document& database) {
    DARWIN_LOGGER;
    if (not database.HasMember("feed_name") or not database["feed_name"].IsString()) {
        DARWIN_LOG_CRITICAL("HostlookupGenerator:: No proper feed name provided in the database");
        return false;
    }
    this->_feed_name = database["feed_name"].GetString();
    if (not database.HasMember("data") or not database["data"].IsArray()) {
        DARWIN_LOG_CRITICAL("HostlookupGenerator:: No or ill formated entries in the database");
        return false;
    }
    auto entries = database["data"].GetArray();
    if (entries.Size() == 0) {
        DARWIN_LOG_CRITICAL("HostlookupGenerator:: No entry in the database. Stopping.");
        return false;
    }
    for (auto& entry : entries) {
        this->LoadJsonEntry(entry);
    }
    if (this->_database.size() == 0) {
        DARWIN_LOG_CRITICAL("HostlookupGenerator:: No usable entry in the database. Stopping.");
        return false;
    }
    return true;
}

bool Generator::LoadJsonEntry(const rapidjson::Value& entry) {
    DARWIN_LOGGER;
    int score = 100;
    std::string sentry;
    if (not entry.IsObject()) {
        DARWIN_LOG_WARNING("HostlookupGenerator:: Database entry is not a JSON object. Ignoring.");
        return false;
    }
    if (not entry.HasMember("entry") or not entry["entry"].IsString()) {
        DARWIN_LOG_WARNING("HostlookupGenerator:: Entry is not a string. Ignoring.");
        return false;
    }
    if (entry.HasMember("score") and entry["score"].IsInt()) {
        score = entry["score"].GetInt();
        if (score < 0 or score > 100) {
            DARWIN_LOG_WARNING("HostlookupGenerator:: Found score not between 0 and 100 in database " + this->_feed_name + ", setting to 100");
            score = 100;
        }
    }
    this->_database[entry["entry"].GetString()] = std::pair<std::string, int>("", score);
    return true;
}

bool Generator::LoadRsyslogDatabase(const rapidjson::Document& database) {
    DARWIN_LOGGER;

    if (not database.HasMember("table") or not database["table"].IsArray()) {
        DARWIN_LOG_CRITICAL("HostlookupGenerator:: No table provided in the database");
        return false;
    }
    auto entries = database["table"].GetArray();
    for (auto& entry : entries) {
        this->LoadRsyslogEntry(entry);
    }
    if (this->_database.size() == 0) {
        DARWIN_LOG_CRITICAL("HostlookupGenerator:: No usable entry in the database. Stopping.");
        return false;
    }
    return true;
}

bool Generator::LoadRsyslogEntry(const rapidjson::Value& entry) {
    if (not entry.IsObject()) {
        return false;
    }
    if (not entry.HasMember("index") or not entry["index"].IsString()) {
        return false;
    }
    if (not entry.HasMember("value")) {
        return false;
    }

    if (entry["value"].IsString()) {
        this->_database[entry["index"].GetString()] = std::pair<std::string, int>(entry["value"].GetString(), 100);
    }
    else if (entry["value"].IsInt()) {
        this->_database[entry["index"].GetString()] = std::pair<std::string, int>("", entry["value"].GetInt());
    }
    else {
        return false;
    }

    return true;
}

darwin::session_ptr_t
Generator::CreateTask(boost::asio::local::stream_protocol::socket& socket,
                      darwin::Manager& manager) noexcept {
    return std::static_pointer_cast<darwin::Session>(
            std::make_shared<HostLookupTask>(socket, manager, _cache, _cache_mutex, _database, _feed_name));
}
