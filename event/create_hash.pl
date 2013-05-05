#!/usr/bin/perl

###########################
#
# create_hash.pl
#
# yamamoto
#
############################

use strict;
use Digest::MD5 qw(md5 md5_hex);

print md5_hex($ARGV[0]),"\n";
