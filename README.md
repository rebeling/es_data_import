es_data_import
==============

prepare dataset for bulk import to elasticsearch


Simple script to read in data, modify and write it to a file.
You can use this file to bulk import to elasticsearch.

data source
-----------
http://www.imdb.com/interfaces

> The Plain Text Data Files > actresses.list.gz


bulk import via curl
--------------------

    curl -s -XPOST localhost:9200/actresses/_bulk --data-binary @actresses.json;
