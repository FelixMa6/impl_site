#! /bin/env perl 
# $Id$
# vim: set ft=perl sw=4 ts=8 tw=78:
#*****************************************************************************
#
#             (c) Copyright 1987 - 2013,  VIA Technologies, Inc.       
#                           ALL RIGHTS RESERVED                            
#                                                                    
#                                                                    
#  This design and all of its related documentation constitutes valuable and
#  confidential property of VIA Technologies, Inc.  No part of it may be
#  reproduced in any form or by any means   used to make any transformation
#  /adaptation / redistribution without the prior written permission from the
#  copyright holders. 
#
#-----------------------------------------------------------------------------
#
# DESCRIPTION:
#
# FEATURES:
#
# TODO
#
# AUTHORS:
#    Felix Ma
#
#   
#-----------------------------------------------------------------------------
#                            REVISION HISTORY
#   $Log$
#****************************************************************************/
#
#
use warnings;

use Getopt::Std;
getopts('i:');

$input = shift @ARGV;

print $input;

#open(EO,"< combine.txt") or die "Cannot open $file!\n";
open(EO,"< $input") or die "Cannot open $file!\n";
while(<EO>){
    push @src, $_;
}

$start = 0;
foreach(@src){
    if(/Felix: The file is (\w+\.\w+)/){
        $file = $1;
        @out = ();
        $start = 1;
    }
    elsif($start){
        $start = 0;
    }
    else{
        push @out, $_;
        open OUT, "> ./$file";
        print OUT @out;
        close OUT;
    }
}
