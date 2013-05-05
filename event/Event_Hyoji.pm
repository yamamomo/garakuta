########################################
#
# package Event_Hyoji
#
# 2013/4 yamamoto
#
########################################

use strict;

package Event_Hyoji;

use Exporter;
our @ISA = qw(Exporter);

our @EXPORT = qw ( 
	Event_Success
	Event_Error
	Event_Errors
	$event_title
                 );

our $event_title = "home event";

sub Event_Success{
	my $message = shift;
	my $kekka = <<EOM;
<div class="alert alert-success">
<p>$message</p>
</div>
EOM
}

sub Event_Error {
	my $error = shift;
	my $kekka = <<EOM;
<div class="alert alert-error">
<p>$error</p>
</div>
EOM
}

sub Event_Errors {
	my @errors = @_;
	my $contents;

	foreach (@errors){
		$contents .= "<p>$_</p>";
	}
	my $kekka = <<EOM;
<div class="alert alert-error">
$contents
</div>
EOM
}

1;
