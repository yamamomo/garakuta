##################################
#
# package Yamamoto
#
# yamamoto
#
################################
use strict;

package Yamamoto;

use Exporter;
our @ISA = qw(Exporter);

our @EXPORT = qw (Text_To_Db 
                  Text_To_Html
                  Db_To_Text 
                  Db_To_Html
                  Seq_num
		  Nen_List
                 );

#use CGI;
#my $obj = new CGI;

sub Text_To_Db {
$_[0] =~ s/\x0D\x0A/<BR>/g;
$_[0] =~ s/\x0D/<BR>/g;
$_[0] =~ s/\x0A/<BR>/g;
return $_[0];
}

sub Text_To_Html {
use CGI;
my $obj = new CGI;
$_[0] = $obj->escapeHTML($_[0]);
$_[0] =~ s/\x0D\x0A/<BR>/g;
$_[0] =~ s/\x0D/<BR>/g;
$_[0] =~ s/\x0A/<BR>/g;
return $_[0];
}

sub Db_To_Text {
$_[0] =~ s/<BR>/\n/g;
return $_[0];
}

sub Db_To_Html {
use CGI;
my $obj = new CGI;
$_[0] =~ s/<BR>/\n/g;
$_[0] = $obj->escapeHTML($_[0]);
$_[0] =~ s/\n/<BR>/g;
return $_[0];
}

sub Seq_num {
my ($start,$end,$interval) = @_;

unless ($interval){$interval=1;}

my @seq_num;
my $i = 0;
for (${start}..${end}){
    unless ($i){
        push (@seq_num,sprintf ("%02d",$_));
        }
    $i++;
    if ($i==$interval){$i=0;}
    }
push (@seq_num,"");
return \@seq_num;
}

sub Nen_List {
    my $end_year = shift @_;
    my $start_year = '2010';
    my @year_list;

    for ($start_year .. $end_year) {
	push (@year_list,$_);
    }
    push (@year_list,"");
    return \@year_list;
}

1;
