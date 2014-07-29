#!/bin/bash

java -jar selenium-server-standalone-2.42.2.jar -maxSession 10 -timeout 30 -newSessionWaitTimeout 25000 -role hub &> selenium_server.log &
