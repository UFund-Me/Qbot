if [ $# != 1 ]; then
        echo "需要指定表名"
        exit -1
fi
table2struct --tag_gorm --db_host localhost --db_port 3306 --db_user root --db_pwd roooooot --db_name test $1
