#!/bin/bash

java -jar selenium-server-standalone-2.42.2.jar -role node  -browser browserName=safari,platform=MAC,maxInstances=5 -browser browserName=firefox,platform=MAC,maxInstances=5 -browser browserName=chrome,platform=MAC,maxInstances=5 -Dwebdriver.chrome.driver=./chromedriver
