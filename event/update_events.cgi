#!/usr/bin/perl

###############################
# update event                #
#                             #
# 2013/4 yamamoto             #
#                             #
###############################

### モジュール読み込み
use strict;
use CGI;
use DBI;
use DBD::Pg;
use Date::Calc qw(Today_and_Now);
use Yamamoto;
use Event_Util;
use Event_Hyoji;

###
use vars qw($obj);
$obj = new CGI;

my ($t_year,$t_month,$t_day,$t_hour,$t_min,$t_sec) = Today_and_Now();

##### 受信データ処理
my $id = $obj->param('id');
my $title = $obj->param('title');
my $content = $obj->param('content');
my $status = $obj->param('status');
my $category = $obj->param('category');
my $start_year = $obj->param('start_year');
my $start_month = $obj->param('start_month');
my $start_day = $obj->param('start_day');
my $start_jikan = $obj->param('start_jikan');
my $start_min = $obj->param('start_min');
my $end_year = $obj->param('end_year');
my $end_month = $obj->param('end_month');
my $end_day = $obj->param('end_day');
my $end_jikan = $obj->param('end_jikan');
my $end_min = $obj->param('end_min');
my $update_by = $obj->param('update_by');

$content = Text_To_Db($content);
$title = Text_To_Db($title);
$update_by = Text_To_Db($update_by);
my $update_at = "${t_year}-${t_month}-${t_day} ${t_hour}:${t_min}:${t_sec}";

## データチェック
my ($start_time,undef,undef) = Event_Date_Check($start_year,$start_month,$start_day,$start_jikan,$start_min);
my ($end_time,undef,undef) = Event_Date_Check($end_year,$end_month,$end_day,$end_jikan,$end_min);

undef($start_time) unless $start_time;
undef($end_time) unless $end_time;

undef ($title) unless $title;
undef ($content) unless $content;


## HTML のヘッダー
my $HTML_header = <<EOM;
Content-Type: text/html;

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html lang="ja">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
	<title>update event</title>
	<link rel="stylesheet" href="../calendar/css/metro-bootstrap.css" type="text/css" charset="EUC-JP">
	<link rel="stylesheet" href="css/basic.css" type="text/css" charset="UTF-8">
 </head>
 <body>
EOM

######## DB 接続処理
# データソース
my $dbi = "DBI:Pg:dbname=$dbname";

# 接続
my $dbh = DBI->connect($dbi ,$db_user); 

my $sth = $dbh->prepare(
           "UPDATE ${table_name} set title = ?,content = ?,status = ?,
	    category = ?,update_by = ?,update_at = ?,start_time = ?,
	    end_time = ?
           WHERE id = ?"
);

# SQL文の実行
$sth->execute($title,$content,$status,$category,$update_by,$update_at,$start_time,$end_time,$id);

# エラーキャッチ
my $err = $dbh->errstr;

# DB切断
$sth->finish;
if ($dbh){
$dbh->disconnect;
}

######## HTML start ######
print $HTML_header;
print <<EOM;
<div id = "container">
EOM

print $obj->h3('T-WAN EVENT');

if ($err){
	print Event_Error($err);
}else{
	print Event_Success("UPDATEしました");
}

##tile
print <<EOM;
<div class="">
  <div class="span4">
    <ul class="thumbnails">
      <li class="span3 tile tile-double tile-teal">
        <a href="index_events.cgi"><h2 class="tile-text">${event_title} INDEX</h2></a>
      </li>
    </ul>
  </div>
  <div class="span4">
    <ul class="thumbnails">
      <li class="span3 tile tile-double tile-orange">
        <a href="../calendar/calendar.cgi?year=${start_year}&month=${start_month}" ><h1 class="tile-text">calendar</h1></a>
      </li>
  </ul>
</div>
<div>
  <div class="span4">
    <ul class="thumbnails">
      <li class="span3 tile tile-double">
        <a href="show_events.cgi?id=${id}"><h2 class="tile-text">T-WAN EVENT SHOW</h2></a>
      </li>
    </ul>
  </div>
</div>
EOM

print "</div>";
print $obj->end_html;
######## HTML end ####### 
