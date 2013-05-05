########################################
#
# package Calendar_Hyoji
#
# 2013/4 yamamoto
#
########################################

use strict;

package Calendar_Hyoji;

use Exporter;
our @ISA = qw(Exporter);

our @EXPORT = qw ( 
	Copyright
	$calendar_title
                 );

								 
our $calendar_title = "HOME CALENDAR";
								 

sub Copyright{
	my ($year,$copywrite) = @_;
	my $kikan;
	my $create_year = 2013;
	if ($year == $create_year){
		$kikan = $create_year;
	}else{
		$kikan = "${create_year}-${year}";
	}
	my $kekka = <<EOM;
<div class = "copyright">Copyright(c)${kikan} ${copywrite} All Right Reserved</div>
EOM
}


1;
