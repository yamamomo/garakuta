#!/usr/bin/perl

###############################
#  delete event               #
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
use Digest::MD5 qw(md5 md5_hex);

###
use vars qw($obj $err @err_messages);
$obj = new CGI;

my $mirror_pass = "7d9e9796d95826fdc2120b98244823d5";

##### 受信データ処理
my $id = $obj->param('id');
my $del_pass = $obj->param('del_pass');

$del_pass = md5_hex($del_pass);

unless ($del_pass eq $mirror_pass){
	push(@err_messages,"password が違います\n");
}


## HTML のヘッダー
my $HTML_header = <<EOM;
Content-Type: text/html;

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html lang="ja">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
	<title>delete event</title>
	<link rel="stylesheet" href="../calendar/css/metro-bootstrap.css" type="text/css" charset="EUC-JP">
	<link rel="stylesheet" href="css/basic.css" type="text/css" charset="UTF-8">
 </head>
 <body>
EOM

&delete_event unless @err_messages;

sub delete_event {
  ######## DB 接続処理
  # データソース
  my $dbi = "DBI:Pg:dbname=$dbname";

  # 接続
  my $dbh = DBI->connect($dbi ,$db_user); 

  my $sth = $dbh->prepare(
           "DELETE FROM ${table_name} WHERE id = ?"
  );

  # SQL文の実行
  $sth->execute($id);

  # エラーキャッチ
  $err = $dbh->errstr;

  # DB切断
  $sth->finish;
  if ($dbh){
    $dbh->disconnect;
  }
}

######## HTML start ######
print $HTML_header;
print <<EOM;
<div class="container">
EOM

print $obj->h3('T-WAN EVENT');

if ($err){
	print Event_Error($err);
}elsif (@err_messages){
	print Event_Errors(@err_messages);
}else{
	print Event_Success("DELETEしました");
}

##tile
print <<EOM;
<div class="row">
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
        <a href="../calendar/calendar.cgi" ><h1 class="tile-text">calendar</h1></a>
      </li>
  </ul>
</div>
EOM

print "</div>";
print $obj->end_html;
######## HTML end ####### 
