#!/usr/bin/perl

###############################
# events  show                #
#                             #
# 2013/4 yamamoto             #
#                             #
###############################

### モジュール読み込み
use strict;
use DBI;
use DBD::Pg;
use CGI;
use Date::Calc qw(Today_and_Now);
use Yamamoto;
use Event_Util;
use Event_Hyoji;


###
use vars qw($obj);
$obj = new CGI;
my ($t_year,$t_month,$t_day,$t_hour,$t_min,undef) = Today_and_Now();

my $param_year = $obj->param('year');
my $param_month = $obj->param('month');
my $id = $obj->param('id');

my $year = $param_year || $t_year;
my $month = $param_month || $t_month;
$month = sprintf("%02d",$month);


my $HTML_header = <<EOM;
Content-Type: text/html;

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html lang="ja">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
	<title>show event</title>
	<script language="JavaScript" type="text/javascript" src="javascripts/events.js"></script>
	<link rel="stylesheet" href="../calendar/css/metro-bootstrap.css" type="text/css"  charset="EUC-JP">
	<link rel="stylesheet" href="css/basic.css" type="text/css"  charset="EUC-JP">
 </head>
 <body>
EOM

######## DB 接続処理
my $dbi = "DBI:Pg:dbname=$dbname";
my $dbh = DBI->connect($dbi ,$db_user);

my $sth = $dbh->prepare(
	"SELECT id,title,content,status,category,start_time,end_time,
	 create_by,create_at,update_by,update_at
	 FROM ${table_name}
	 WHERE id = ?"
);

# SQL文の実行
$sth->execute($id);



######## HTML start ######
print $HTML_header;

print <<EOM;
<div class="container">
EOM
print $obj->h3("${event_title} 詳細");

## index へリンク

print <<EOM;
<a href="index_events.cgi">[INDEXへ]</a>
<a href="../calendar/calendar.cgi?year=${year}&month=${month}">[CALENDARへ]</a>
EOM

### データの取得と出力

while(my @row = $sth->fetchrow_array) {
	my $title = Db_To_Html($row[1]);
	my $content = Db_To_Html($row[2]);
	my $status = Db_To_Html($row[3]);
	my $category = Db_To_Html($row[4]);
	my $create_by = Db_To_Html($row[7]);
	my $create_at = $row[8];
	my $update_by = Db_To_Html($row[9]);
	my $update_at = $row[10];

########## table 開始#############
print "<table>";

print <<EOM;
<tr>
<th>*タイトル</th>
<td class="span8">$title</td>
</tr>
EOM

print <<EOM;
<tr>
<th>ステータス</th>
<td>$status</td>
</tr>
EOM

print <<EOM;
<tr>
<th>カテゴリー</th>
<td>$category</td>
</tr>
EOM

# STASRT
print <<EOM;
<tr>
<th>START</th>
<td>$row[5]</td>
</tr>
EOM

# END
print <<EOM;
<tr>
<th>END</th>
<td>$row[6]</td>
</tr>
EOM



print <<EOM;
<tr>
<th>*内容</th>
<td>$content</td>
</tr>
EOM

print <<EOM;
<tr>
<th>更新者</th>
<td>${update_by}</td>
</tr>
EOM


print <<EOM;
</table>
EOM
######### table 終わり ##########

### 編集画面へのリンク
print <<EOM;   
<a href="edit_events.cgi?id=${id}">[編集]</a>
EOM

# footer
print <<EOM;
<div class = "footer">
<div>created by ${create_by} at ${create_at}</div>
<div>Last update at ${update_at}</div>
</div>
EOM

##### delete button
## form 開始

print <<EOM;
<form action="delete_events.cgi" method="post" class ="span6 well form-inline" name="form1" onSubmit="return del_kakunin()">
<div>削除する場合は...passwordが...</div>
<input type="hidden" name="id" value="$id">
<input type="password" name="del_pass" class="input-small" placeholder="Password">
<button type="submit" class="btn-danger">DELETE</button>
</form>
EOM

print "</div>";
print $obj->end_html;
######## HTML end ####### 
}

# DB切断
$sth->finish;
$dbh->disconnect;
