#!/usr/bin/perl

###############################
# index events                #
#                             #
# 2013/4 yamamoto             #
#                             #
###############################

### モジュール読み込み
use strict;
use CGI;
use DBI;
use DBD::Pg;
use Yamamoto;
use Event_Util;
use Event_Hyoji;

###
use vars qw($obj);
$obj = new CGI;

#
my $search_word = $obj->param('search_word');
if ($search_word) {
	$search_word = "%${search_word}%";
}

my $HTML_header = <<EOM;
Content-Type: text/html;

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html lang="ja">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
	<title>index events</title>
	<link rel="stylesheet" href="../calendar/css/metro-bootstrap.css" type="text/css"  charset="EUC-JP">
	<link rel="stylesheet" href="css/index.css" type="text/css"  charset="UTF-8">
 </head>
 <body>
EOM

######## DB 接続処理
# データソース
my $dbi = "DBI:Pg:dbname=${dbname}";
#my $user = $db_user;

# 接続
my $dbh = DBI->connect($dbi ,$db_user); 
my $sth;

if ($search_word){
	$sth = $dbh->prepare(
		"SELECT id,title,status,category,start_time,end_time,create_by,update_by
		FROM ${table_name}
		WHERE title LIKE ? or content LIKE ?
		order by id"
		);

	# SQL文の実行
	$sth->execute($search_word,$search_word);

}else{
	$sth = $dbh->prepare(
		"SELECT id,title,status,category,start_time,end_time,create_by,update_by,content
		FROM ${table_name}
		order by id"
		);

	# SQL文の実行
	$sth->execute();
}

######## HTML start ######
print $HTML_header;
print <<EOM;
<div class="container">
EOM

print $obj->h3("${event_title} 一覧");

### search form
print <<EOM;
<form class="form-search" action="index_events.cgi" method="post">
<input type="text" class="input-medium search-query" name="search_word">
<button type="submit" class="btn-small btn-info"><i class="icon-search icon-white"></i>Search</button>
</form>
EOM

### リンク
print <<EOM;
<a href="new_events.cgi">[新規作成]</a>
<a href="../calendar/calendar.cgi">[CALENDARへ]</a>
EOM

########## table 開始#############
print "<table>";

print <<EOM;
<thead>
<tr>
<th>id</th>
<th>title</th>
<th>status</th>
<th>category</th>
<th>start</th>
<th>end</th>
<th>作成者</th>
<th>更新者</th>
</tr>
</thead>
EOM

# データの取得と出力
while(my @row = $sth->fetchrow_array) {
my $query_link = "show_events.cgi?id=${row[0]}";

    ### 出力表示処理
    my $title = Db_To_Html($row[1]);
    my $status = Db_To_Html($row[2]);
    my $category = Db_To_Html($row[3]);
    my $start_time = $row[4];
    my $end_time = $row[5];
    my $create_by = Db_To_Html($row[6]);
    my $update_by = Db_To_Html($row[7]);

print <<EOM;
<tr>
<td>$row[0]</td>
<td><a href="$query_link">$title</a></td>
<td>$status</td>
<td>$category</td>
<td>$start_time</td>
<td>$end_time</td>
<td>$create_by</td>
<td>$update_by</td>
</tr>
EOM
}

print "</table>";
######### table 終わり ##########

### 新規作成リンク
print <<EOM;
<a href="new_events.cgi">[新規作成]</a>
EOM


## 処理した行数
my $gyo = $sth->rows;
print "<p> ${gyo} rows </P>";

# DB切断
$sth->finish;
$dbh->disconnect;



print "</div>";
print $obj->end_html;
######## HTML end ####### 
