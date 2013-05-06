#!/usr/bin/perl

#####################################
#
# calendar.cgi
#
# 2013/4  yamamoto
# 
######################################

use strict;
use lib "../event";
use CGI;
use Date::Calc qw(Days_in_Month Day_of_Week Today Add_Delta_YMD);
use Nihon_No_Yasumi;
use Data_From_Events;
use Calendar_Hyoji;

use vars qw($obj $dow @week);
$obj = new CGI;

my $param_year = $obj->param('year');
my $param_month = $obj->param('month');

my ($t_year,$t_month,$t_day) = Today();

@week = ('','月','火','水','木','金','土','日');

my $year = $param_year || $t_year;
my $month = $param_month || $t_month;

my $days_month = Days_in_Month($year,$month);
my $holiday = &Nihon_No_Kyujitsu($year);
my ($prev_year,$prev_month,undef) = Add_Delta_YMD($year,$month,1,0,-1,0);
my ($next_year,$next_month,undef) = Add_Delta_YMD($year,$month,1,0,1,0);

my $HTML_header = <<EOM;
Content-Type: text/html;

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html lang="ja">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
	<title>event calendar</title>
	<link href='http://fonts.googleapis.com/css?family=Neucha' rel='stylesheet' type='text/css'>
	<link rel="stylesheet" href="css/metro-bootstrap.css" type="text/css"  charset="EUC-JP">
	<link rel="stylesheet" href="css/calendar.css" type="text/css"  charset="UTF-8">
</head>
<body>
EOM

######## HTML start ######
print $HTML_header;
print <<EOM;
<div class="container">
EOM
print $obj->h2("${calendar_title}");

###  form
print <<EOM;
  <div class="sapn4">
    <form class="form-horizontal" action="calendar.cgi" method="post">
      <div class="control-group">
        <select class="span2" name = "year">
EOM

## 年
for (2010..($year + 3)){
	if ($_ == $year){
		print "<option selected>$_</option>";
	}else{
		print "<option>$_</option>";
	}
}

print <<EOM;
    </select>
    <span>年</span>
    <select class="span1" name = "month">
EOM

# 月
for (1..12){
	if ($_ == $month) {
		print "<option selected>$_</option>";
	}else{
		print "<option>$_</option>";
	}
}

print <<EOM;
    </select>
    <span>月</span>
    <input type="submit" class="btn btn-primary" value="Submit">
    </div>
  </form>
  </div>
	<div class="span8"></div>
EOM

# next prev link
print <<EOM;
<div class="row">
	<div class="span4">
		<ul class="pager">
			<li class="previous">
				<a href="calendar.cgi?year=${prev_year}&month=${prev_month}">&larr; Prev</a>
			</li>
			<span>${year}年${month}月</span>
			<li class="next">
				<a href="calendar.cgi?year=${next_year}&month=${next_month}">Next &rarr;</a>
			</li>
		</ul>
	</div>
	<div class="span8"></div>
</div>
EOM

## table
print <<EOM;
<table class="table table-bordered">
  <thead>
    <tr>
     <th id = "nichi">日</th>
     <th id = "youbi">曜日</th>
     <th id = "jikan">時間</th>
     <th>内容</th>
    </tr>
  </thead>
<tbody>
EOM

for (1..$days_month){
	# 日ごとの処理
	$dow = Day_of_Week($year,$month,$_);
	my $holiday_name;
	my $youbi_class;
	my $todays_class;
	my $naiyo_contents;
	my $jikan_contents;
	my ($kyo_event,$event_jikan) = Kyo_No_Event($year,$month,$_);
	$naiyo_contents .= $kyo_event;
	$jikan_contents .= $event_jikan;

	# 今日の処理
	if ($t_year == $year && $t_month == $month && $t_day == $_){
		$todays_class = "alert alert-success";
		my ($keizoku_event,$keizoku_jikan) = Keizoku_Event($t_year,$t_month,$t_day);
		$naiyo_contents .= $keizoku_event;
		$jikan_contents .= $keizoku_jikan;
	}
	# 祝日、土曜、日曜の処理
	if (defined $holiday->[$month][$_]){
		$holiday_name = $holiday->[$month][$_];
		$youbi_class = "badge badge-important";
		$naiyo_contents .= &add_holiday($holiday_name);
	}elsif ($dow == 7){
		$youbi_class = "badge badge-important";
	}elsif ($dow == 6){
		$youbi_class = "badge badge-info";
	}

	print "<tr>";
	#日付欄
print <<EOM;
<td class = nichi>
<a href="../event/new_events.cgi?year=${year}&month=${month}&day=$_">$_</a>
</td>
EOM
	#曜日欄
print <<EOM;
<td><span class = "${youbi_class}">$week[$dow]</span></td>
EOM

	#時間欄
print <<EOM;
<td>$jikan_contents</td>
EOM
	#内容欄
print <<EOM;
<td class = "$todays_class">
<div>$naiyo_contents</div>
</td>
EOM
	print "</tr>\n";
}

print <<EOM;
</tbody>
</table>
EOM

print Copyright($t_year,"yamamoto kouichi");

print <<EOM;
</div>
EOM
print $obj->end_html;

### sub ルーチン
sub add_holiday {
	my $holiday_name = shift;
my $kekka = <<EOM;
<div class = "holiday">${holiday_name}</div>\n
EOM
}

