################################
#
# package Data_From_Events
#
# yamamoto
#
###############################
package Data_From_Events;

use Exporter;

our @ISA = qw(Exporter);
our @EXPORT = qw (
		  Kyo_No_Event
		  Keizoku_Event
                 );

use strict;
use Event_Util;
use DBD::Pg;

my $event_url = "../event/show_events.cgi";

sub Kyo_No_Event {
    use CGI;
    my $obj = new CGI;
    my ($year,$month,$day) = @_;
    my $kyo_s = "${year}-${month}-${day}";
    my $kyo_e = "${kyo_s} 23:59";
    my $kyo_contents;
    my $kyo_jikan;


    # データソース
    my $dbi = "DBI:Pg:dbname=${dbname}";
    # ユーザ名
    my $user = $db_user;

    # 接続
    my $dbh = DBI->connect($dbi ,$user);

    ###SQL文
    # 今日で始まり、今日で終わる
     my $sth = $dbh->prepare(
	     "SELECT id,title,status,category,start_time,end_time
	      FROM $table_name
	      WHERE (start_time >= ? and start_time <= ?)and(end_time >= ? and end_time <= ?)
	      ORDER BY start_time"
     );

    # 今日で始まり、今日で終わらない
     my $sth1 = $dbh->prepare(
	     "SELECT id,title,status,category,start_time,end_time
	      FROM $table_name
	      WHERE (start_time >= ? and start_time <= ?)and((end_time > ?) or (end_time IS NULL))
	      ORDER BY start_time"
     );

    # 以前に始まり、今日で終わる
     my $sth2 = $dbh->prepare(
	     "SELECT id,title,status,category,start_time,end_time
	      FROM $table_name
	      WHERE (end_time >= ? and end_time <= ?)and(start_time < ?)
	      ORDER BY end_time"
     );

     #SQL 実行
     $sth->execute($kyo_s,$kyo_e,$kyo_s,$kyo_e);
     $sth1->execute($kyo_s,$kyo_e,$kyo_e);
     $sth2->execute($kyo_s,$kyo_e,$kyo_s);

     #データ処理
     while(my @row = $sth->fetchrow_array) {
	     my $title = $obj->escapeHTML($row[1]);
	     my $status = $obj->escapeHTML($row[2]);
	     my $category = $obj->escapeHTML($row[3]);
	     my $start_time = _Jikan_Dake($row[4]);
	     my $end_time = _Jikan_Dake($row[5]);
	     $kyo_contents .= _add_content($row[0],$title,$status,$category);
	     $kyo_jikan .= "<div>${start_time}～${end_time}</div>";
     }

     while(my @row = $sth1->fetchrow_array) {
	     my $title = $obj->escapeHTML($row[1]);
	     my $status = $obj->escapeHTML($row[2]);
	     my $category = $obj->escapeHTML($row[3]);
	     my $start_time = _Jikan_Dake($row[4]);
	     $kyo_contents .= _add_content($row[0],$title,$status,$category);
	     $kyo_jikan .= "<div>${start_time}～</div>";
     }

     while(my @row = $sth2->fetchrow_array) {
	     my $title = $obj->escapeHTML($row[1]);
	     my $status = $obj->escapeHTML($row[2]);
	     my $category = $obj->escapeHTML($row[3]);
	     my $end_time = _Jikan_Dake($row[5]);
	     $kyo_contents .= _add_content($row[0],$title,$status,$category);
	     $kyo_jikan .= <<EOM;
<div class ="left">～${end_time}</div>
EOM
     }

     # DB切断
     $sth->finish;
     $sth1->finish;
     $sth2->finish;
     if ($dbh){
         $dbh->disconnect;
     }
     return  $kyo_contents,$kyo_jikan;
}


sub Keizoku_Event {
    use CGI;
    my $obj = new CGI;
    my ($year,$month,$day) = @_;
    my $kyo_s = "${year}-${month}-${day}";
    my $kyo_e = "${kyo_s} 23:59";
    my $kyo_contents;
    my $kyo_jikan;


    # データソース
    my $dbi = "DBI:Pg:dbname=${dbname}";
    # ユーザ名
    my $user = $db_user;

    # 接続
    my $dbh = DBI->connect($dbi ,$user);

    ###SQL文
    # 継続中
     my $sth = $dbh->prepare(
	     "SELECT id,title,status,category,start_time,end_time
	      FROM $table_name
	      WHERE (start_time < ?)and((end_time > ?) or (end_time IS NULL))and NOT(status = ?)
	      ORDER BY start_time"
     );

     #SQL 実行
     $sth->execute($kyo_s,$kyo_e,"close");

     #データ処理
     while(my @row = $sth->fetchrow_array) {
	     my $title = $obj->escapeHTML($row[1]);
	     my $status = $obj->escapeHTML($row[2]);
	     my $category = $obj->escapeHTML($row[3]);
	     $kyo_contents .= _add_content($row[0],$title,$status,$category);
	     $kyo_jikan .= "<div>継続中</div>";
     }

     # DB切断
     $sth->finish;
     if ($dbh){
         $dbh->disconnect;
     }
     return  $kyo_contents,$kyo_jikan;
}
     

sub _add_content {
	my ($id,$title,$status,$category) = @_; 
	my $link = _Link($id);
	my $class = _add_class($category);
	my $kekka =<<EOM;
<div class="event_${status}">[${status}]<span class = "${class}">■${category}■</span>&nbsp;${title}${link}</div>
EOM
}

sub _Jikan_Dake {
    my @jikan;

    my @day_time = split (/\s+/,$_[0]);
    @jikan = split (/:/,$day_time[1]);

    return "$jikan[0]:$jikan[1]";
}

sub _Link {
	my $id = shift;
	my $link = <<EOM;
<a href="${event_url}?id=${id}">[LINK]</a>
EOM
}

sub _add_class {
	my $category = shift;
	my $class;
	if (($category eq "障害")||($category eq "申告")){
		$class = "trouble";
	}elsif ($category eq "計画作業"){
		$class = "plan";
	}elsif ($category eq "周知"){
		$class = "shuchi";
	}elsif ($category eq "メモ"){
		$class = "memo"
	}
	return $class;
}


1;
