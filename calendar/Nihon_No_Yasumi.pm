#!/usr/bin/perl
use strict;

package Nihon_No_Yasumi;

use Exporter;
our @ISA = qw(Exporter);

our @EXPORT = qw (Yasumi Nihon_No_Kyujitsu Nihon_No_Saijitsu );

use Date::Calc qw(Nth_Weekday_of_Month_Year
                  Day_of_Week
                  Add_Delta_Days
                  check_date
                 );

#######################################################
# 与えられた年、月、日から該当日が休日にあたるか      #
# どうかを0,1で返すサブルーチン                       #
# *日曜日は法律的に休日と規定されてない               #
#######################################################

sub Yasumi {
        my($year,$month,$day)=@_;
        unless (check_date($year,$month,$day)){
                return -1;
                exit;
        }
        my ($kyujitsu) = &Nihon_No_Kyujitsu($year);
        if (defined $kyujitsu->[$month][$day]){
                return 1;
        }else{
                return 0;
        }
}# sub Yasumi終わり

#####################################################
# 国民の祝日に関する法律 第3条第1項から第3項の休日  #
# を2次元配列入れて配列のリファレンスを返す         #
# サブルーチン                                      #
#####################################################

sub Nihon_No_Kyujitsu {

my $year = shift;
my @kyujitsu;
my($saijitsu) = &Nihon_No_Saijitsu($year);

for my $month (1..12){
    for my $day (1..31){
        ##########################################
        # 国民の祝日に関する法律 第3条第1項      #
        # 「国民の祝日」は、休日とする。         #
        #                                        #
        ##########################################
        if (defined $saijitsu->[$month][$day]){
            $kyujitsu[$month][$day]=$saijitsu->[$month][$day];
            (my $day_of_week)=Day_of_Week($year,$month,$day);
    my(undef,$d_month,$d_day)=Add_Delta_Days($year,$month,$day,1);
    my(undef,$t_month,$t_day)=Add_Delta_Days($year,$month,$day,2);
        ######################################################
        # 国民の祝日に関する法律 第3条第2項                  #
        # 振替休日の規定                                     #
        # 2006 までは月曜固定                                #
        # 2007 からは祝日直後の平日                          #
        ######################################################
            if ($day_of_week == 7){
                 if ($year < 2007){
                    unless(defined $saijitsu->[$d_month][$d_day]){
                     $kyujitsu[$d_month][$d_day]="振替休日";
                        }
        }else{
              my $f = 1;
              while ($f < 7){
      my(undef,$f_month,$f_day)=Add_Delta_Days($year,$month,$day,$f);
      if (!defined $saijitsu->[$f_month][$f_day]){
              $kyujitsu[$f_month][$f_day]="振替休日";
              last;
      }
      $f++;
              }#while終わり

        }#振替休日判定終わり

        ######################################################
        # 国民の祝日に関する法律 第3条第3項                  #
        # その前日及び翌日が「国民の祝日」である日           #
        # （「国民の祝日」でない日に限る。）は、休日とする。 #
        # 1985/12/27 施行                                    #
        ######################################################
            }elsif (!(defined $saijitsu->[$d_month][$d_day])and
                    (defined $saijitsu->[$t_month][$t_day])and
                    ($year > 1985)and($day_of_week == 6)){
              $kyujitsu[$d_month][$d_day]="国民の休日";
            }#国民の休日判定終わり
            }#祝日だった場合終わり
        }#$day終わり
    }#$month終わり
return \@kyujitsu;
}#subルーチン終わり

#########################################
# 国民の祝日に関する法律 第2条          #
#   該当年の祝日を2次元配列に入れる     #
#   サブルーチン                        #
#########################################
sub Nihon_No_Saijitsu {

        my $year = shift;
my @shuku;
my @period;
my @saijitsu;
open (SD,"shukujitsu.dat");
while (<SD>){
    chomp;
    unless (/^#/){
    @shuku = split (/\s+/);
    if ($shuku[0] =~ /-/){
        @period = split (/-/,$shuku[0]);
        if ($year >= $period[0] and $year <= $period[1]){
            ## 春分の日
            if ($shuku[2] eq "SHUNBUN"){
                $shuku[2] = &shunbun($year);
            ## 秋分の日
            }elsif ($shuku[2] eq "SYUBUN"){
                $shuku[2] = &syubun($year);
            ## Happy Monday
            }elsif ($shuku[2] =~ /^HM/){
                $shuku[2] =~ (s/HM//);
                $shuku[2] = &Happy_Monday($year,$shuku[1],$shuku[2]);
                    }
                     $saijitsu[$shuku[1]][$shuku[2]]="$shuku[3]";
       }
   #### 該当年限りの祝日の処理
   }else {
           if ($year == $shuku[0]){
                   $saijitsu[$shuku[1]][$shuku[2]]="$shuku[3]";
           }
   }
   }## unless終わり
}## while 終わり
return \@saijitsu;
}#サブルーチン終わり



#### 春分の日を決めるサブルーチン
sub shunbun {
   (my $year)=@_;
   my $shunbun =int(20.8431+0.242194*($year-1980)-int(($year-1980)/4));
   }

#### 秋分の日を決めるサブルーチン
sub syubun {
   (my $year)=@_;
   my $syubun = int(23.2488+0.242194*($year-1980)-int(($year-1980)/4));
   }

#### Happy Monday の日付を特定するサブルーチン
sub Happy_Monday {
        (my $year,my $month,my $week)=@_;
        (my $h_year,my $h_month,my $h_day)=Nth_Weekday_of_Month_Year($year,$month,"1",$week);
        return $h_day;
}

1;

