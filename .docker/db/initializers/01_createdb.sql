-- 最初にデータベースを作成するSQL
create database db_development;
create database db_test;
grant all privileges on database db_development to deploy;
grant all privileges on database db_test to deploy;
