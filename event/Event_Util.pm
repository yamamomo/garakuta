########################################
#
# package Event_Util
#
# 2013/4 yamamoto
#
########################################

use strict;

package Event_Util;

use Exporter;
our @ISA = qw(Exporter);

our @EXPORT = qw ( 
      $dbname
		  $db_user
		  $table_name
      Event_Status_Array
		  Event_Category_Array
		  Event_Date_Check
      Time_Decompo
                 );

use Date::Calc qw ( check_date );

our $dbname = "calendar";
our $db_user = "pgsql";
our $table_name = "events";

sub Event_Status_Array {
	["open","update","close",""]
}

sub Event_Category_Array {
	["周知","計画作業","障害","申告","メモ",""]
}

sub Event_Date_Check {

my ($year,$month,$day,$hour,$min) = @_;
my $message;
my $ymd = "${year}-${month}-${day}";
my $hhmm;
my $date_time;
my $class;

#年月日のチェック
unless (($year)and($month)and($day)){
    #いずれかが空欄の時
    unless (($year)or($month)or($day)){
        $message = "年月日が指定されてません";
        $class = "caution";
        $ymd ="";
    }elsif (!(($year)or($month))){
        $message ="年月が指定されてません";
        $class = "warnning";
    }elsif (!($year)){
        if (!($day)){
            $message ="年日が指定されてません";
            $class = "warnning";
        }else {
            $message ="年が指定されてません";
            $class = "warnning";
        }
    }elsif (!($month)){
        if (!($day)){
            $message ="月日が指定されてません";
            $class = "warnning";
       }else {
            $message ="月が指定されてません";
            $class = "warnning";
        }
    }else {
        $message ="日が指定されてません";
        $class = "warnning";
    }
}else{
    #すべて設定されている時の処理
    if (!check_date($year,$month,$day)){
        $message ="存在しない日付です";
        $class = "warnning";
    }else{
        #正規の日付
        $message = "";
        $class = "";
    }
}

#時間のチェック
if (($hour)and($min)){
    $hhmm = "${hour}:${min}";
}elsif (!$hour){
    $hhmm = "";
}else {
    $hhmm = "${hour}:00";
}

unless ($ymd or $hhmm){
    $date_time = "";
}else {
    $date_time = "${ymd} $hhmm";
}

return $date_time,$message,$class;

}

# timestamp型 を年月日時分秒に分解する
sub Time_Decompo {
    my @nengetu;
    my @jikan;

    my @day_time = split (/\s+/,$_[0]);
    @nengetu = split (/-/,$day_time[0]);
    @jikan = split (/:/,$day_time[1]);

    return $nengetu[0],$nengetu[1],$nengetu[2],$jikan[0],$jikan[1];
}


1;
