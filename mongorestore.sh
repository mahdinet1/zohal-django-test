#!/bin/sh

mongorestore --username admin --password admin --gzip --archive=/import/transactions.agz --nsInclude='*'
