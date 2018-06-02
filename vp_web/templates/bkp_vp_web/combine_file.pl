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

$dir = ".";

opendir DIR, $dir or die "Cannot open $dir !\n";
@dir = readdir DIR;
#print @dir; 

$num = 0;
foreach(@dir){
    if(/swp|swo/){ }
    elsif(/html/){ 
        $num++;

        $file = "$dir/$_";
	    push @out, "Felix: The file is $_, num is $num \n\n"; 

        open(EO,"< $file") or die "Cannot open $file!\n";
	    while(<EO>){
	        push @out, $_;
	    }
	    close(EO);

    }
}

open OUT, "> ./combine";
print OUT @out;
close OUT;