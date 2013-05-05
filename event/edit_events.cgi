#!/usr/bin/perl

###############################
#  edit event                 #
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
my $year_end = $t_year + 2;


my $HTML_header = <<EOM;
Content-Type: text/html;

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html lang="ja">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
	<title>edit event</title>
	<script language="JavaScript" type="text/javascript" src="javascripts/jquery-1.8.0.js"></script>
	<script language="JavaScript" type="text/javascript" src="javascripts/jquery.validate.js"></script>
	<script language="JavaScript" type="text/javascript" src="javascripts/events.js"></script>
	<link rel="stylesheet" href="../calendar/css/metro-bootstrap.css" type="text/css"  charset="EUC-JP">
	<link rel="stylesheet" href="css/basic.css" type="text/css"  charset="UTF-8">
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
<div id = "container">
EOM
print $obj->h3("${event_title} 編集");

## index へリンク

print <<EOM;
<a href="index_events.cgi">[INDEXへ]</a>
<a href="../calendar/calendar.cgi?year=${year}&month=${month}">[CALENDARへ]</a>
EOM

### form 開始
print <<EOM;
<form action="update_events.cgi" method="post" name="form1" id="form1">
EOM

### データの取得と出力

while(my @row = $sth->fetchrow_array) {

	my $title = Db_To_Text($row[1]);
	my $content = Db_To_Text($row[2]);
	my $status = Db_To_Text($row[3]);
	my $category = Db_To_Text($row[4]);
	my $update_by = Db_To_Text($row[9]);
	my ($start_year,$start_month,$start_day,$start_jikan,$start_min) = Time_Decompo($row[5]);
	my ($end_year,$end_month,$end_day,$end_jikan,$end_min) = Time_Decompo($row[6]);
	    

########## table 開始#############
print "<table>";

print <<EOM;
<tr>
<th>*タイトル</th>
<td>
EOM

print $obj->textfield(
		    -name=>'title',
		    -default=>"$title",
		    #-size=>64,
		    -class=>"span6",
		);

print <<EOM;
</td>
</tr>
EOM

print <<EOM;
<tr>
<th>ステータス</th>
<td>
EOM

print $obj->scrolling_list(
		    -name=>'status',
		    -default=>"$status",
                    -values=>Event_Status_Array(),
		    -size=>1,
		);

print <<EOM;
</td>
</tr>
EOM

print <<EOM;
<tr>
<th>カテゴリー</th>
<td>
EOM

print $obj->scrolling_list(
                    -name=>'category',
                    -default=>"$category",
		    -values=>Event_Category_Array(),
                    -size=>1,
                );

print <<EOM;
</td>
</tr>
EOM

# STASRT
print <<EOM;
<tr>
<th>START</th>
<td>
EOM

#
print $obj->scrolling_list(
-name=>'start_year',
-values=>Nen_List("$year_end"),
-default=>"$start_year",
-onChange=>"setEmptyStart(this)",
-class=>"span1",
-size=>1,
);

print "<span>年</span>";

#
print $obj->scrolling_list(
-name=>'start_month',
-values=>Seq_num(1,12),
-default=>"$start_month",
-class=>"span1",
-size=>1,
);

print "<span2>月</span>";

#
print $obj->scrolling_list(
-name=>'start_day',
-values=>Seq_num(1,31),
-default=>"$start_day",
-class=>"span1",
-size=>1,
);

print "<span>日</span>";

#
print $obj->scrolling_list(
-name=>'start_jikan',
-values=>Seq_num(0,23),
-default=>"$start_jikan",
-class=>"span1",
-size=>1,
);

print "<span>時</span>";

#
print $obj->scrolling_list(
-name=>'start_min',
-values=>Seq_num(0,59,5),
-default=>"$start_min",
-class=>"span1",
-size=>1,
);

print "<span>分</span>";

print <<EOM;
</td>
</tr>
EOM

# END
print <<EOM;
<tr>
<th>END</th>
<td>
EOM

#
print $obj->scrolling_list(
-name=>'end_year',
-values=>Nen_List("${year_end}"),
-default=>"$end_year",
-class=>"span1",
-onChange=>"setEmptyEnd(this)",
-size=>1,
);

print "<span>年</span>";

#
print $obj->scrolling_list(
-name=>'end_month',
-values=>Seq_num(1,12),
-default=>"$end_month",
-class=>"span1",
-size=>1,
);

print "<span2>月</span>";

#
print $obj->scrolling_list(
-name=>'end_day',
-values=>Seq_num(1,31),
-default=>"$end_day",
-class=>"span1",
-size=>1,
);

print "<span>日</span>";

#
print $obj->scrolling_list(
-name=>'end_jikan',
-values=>Seq_num(0,23),
-default=>"$end_jikan",
-class=>"span1",
-size=>1,
);

print "<span>時</span>";

#
print $obj->scrolling_list(
-name=>'end_min',
-values=>Seq_num(0,59,5),
-default=>"$end_min",
-class=>"span1",
-size=>1,
);

print "<span>分</span>";

print <<EOM;
</td>
</tr>
EOM



print <<EOM;
<tr>
<th>*内容</th>
<td>
EOM

print $obj->textarea(
                    -name=>'content',
                    -default=>"$content",
                    -rows=>15,
		    -class=>"span6",
                );

print <<EOM;
</td>
</tr>
EOM

print <<EOM;
<tr>
<th>更新者</th>
<td>
EOM

print $obj->textfield(
                    -name=>'update_by',
                    -default=>"$update_by",
                    -size=>24,
                );

print <<EOM;
</td>
</tr>
EOM

print <<EOM;
<tr>
<td colspan="2">
<br>
<button type="submit" class="btn-primary">UPDATE</button>
<button type="reset" class="btn">Reset</button>
</td><tr>
</table>
EOM
######### table 終わり ##########

## id hidden
print <<EOM;
<input type="hidden" name="id" value="$id">
EOM

print <<EOM;
</form>
EOM
### form 終わり

print "</div>";
print $obj->end_html;
######## HTML end ####### 
}

# DB切断
$sth->finish;
$dbh->disconnect;
