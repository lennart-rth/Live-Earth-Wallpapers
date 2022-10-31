#!/bin/bash
#
# Developed by Fred Weinhaus 10/7/2008 .......... revised 11/6/2014
#
# ------------------------------------------------------------------------------
# 
# Licensing:
# 
# Copyright © Fred Weinhaus
# 
# My scripts are available free of charge for non-commercial use, ONLY.
# 
# For use of my scripts in commercial (for-profit) environments or 
# non-free applications, please contact me (Fred Weinhaus) for 
# licensing arrangements. My email address is fmw at alink dot net.
# 
# If you: 1) redistribute, 2) incorporate any of these scripts into other 
# free applications or 3) reprogram them in another scripting language, 
# then you must contact me for permission, especially if the result might 
# be used in a commercial or for-profit environment.
# 
# My scripts are also subject, in a subordinate manner, to the ImageMagick 
# license, which can be found at: http://www.imagemagick.org/script/license.php
# 
# ------------------------------------------------------------------------------
# 
####
#
# USAGE: autolevel [-c colormode] [-m midrange] infile outfile
# USAGE: autolevel [-h or -help]
#
# OPTIONS:
#
# -c      colormode       colorspace/channel to use to compute 
#                         min, max, gamma statistics; choices are: 
#                         gray, intensity, luminance, lightness, brightness, 
#                         average, magnitude, rgb; default=luminance
# -m      midrange        midrange value for autogamma part of script;
#                         0<float<1; default=0.5
#
###
#
# NAME: AUTOLEVEL 
# 
# PURPOSE: To modify an image to automatically stretch the dynamic range  
# between full black and white and automatically apply a gamma correction.
# 
# DESCRIPTION: AUTOLEVEL modifies an image to automatically stretch the
# dynamic range between full black and white and automatically apply a 
# gamma correction. The minimum, maximum and gamma values may be computed  
# from various graylevel representations of the image or individually 
# channel-by-channel. The script then passes these values to the IM 
# function -level.
# 
# OPTIONS: 
# 
# -c colormode ... COLORMODE is the colorspace/channel to use to compute
# the minimum, maximum and gamma values. The choices are: gray, intensity, 
# luminance, lightness, brightness, average, magnitude and rgb. Values  
# of gray and intensity are equivalent. The default is luminance.
# 
# Gray or Intensity uses statistics from -colorspace Gray.
# Luminance uses statistics from -colorspace Rec709Luma.
# Lightness uses statistics from the lightness channel of -colorspace HSL.
# Brightness uses statistics from the brightness channel of -colorspace HSB.
# Average uses statistics from the first channel of -colorspace OHTA.
# Magnitude uses aggregate statistics from all the channels.
# RGB uses statistics independently from each channel of -colorspace sRGB/RGB.
# See definitions at: 
# http://www.imagemagick.org/script/command-line-options.php#colorspace
# 
# Note: generally there are only slight differences between the various 
# non-rgb colormode results. Colormode=rgb can cause color balance shifts.
# 
# -m midrange ... MIDRANGE is the midrange value for the autogamma technique, 
# which uses the formula: Gamma = log(mean)/log(mid-dynamic-range). Values 
# are in the range 0<float<1. The default=0.5
# 
# CAVEAT: No guarantee that this script will work on all platforms, 
# nor that trapping of inconsistent parameters is complete and 
# foolproof. Use At Your Own Risk. 
# 
######
#

# set default values
colormode="luminance"
midrange=0.5			# mid dynamic range (between 0 and 1)


# set directory for temporary files
dir="."    # suggestions are dir="." or dir="/tmp"

# set up functions to report Usage and Usage with Description
PROGNAME=`type $0 | awk '{print $3}'`  # search for executable on path
PROGDIR=`dirname $PROGNAME`            # extract directory of program
PROGNAME=`basename $PROGNAME`          # base name of program
usage1() 
	{
	echo >&2 ""
	echo >&2 "$PROGNAME:" "$@"
	sed >&2 -e '1,/^####/d;  /^###/g;  /^#/!q;  s/^#//;  s/^ //;  4,$p' "$PROGDIR/$PROGNAME"
	}
usage2() 
	{
	echo >&2 ""
	echo >&2 "$PROGNAME:" "$@"
	sed >&2 -e '1,/^####/d;  /^######/g;  /^#/!q;  s/^#*//;  s/^ //;  4,$p' "$PROGDIR/$PROGNAME"
	}


# function to report error messages
errMsg()
	{
	echo ""
	echo $1
	echo ""
	usage1
	exit 1
	}


# function to test for minus at start of value of second part of option 1 or 2
checkMinus()
	{
	test=`echo "$1" | grep -c '^-.*$'`   # returns 1 if match; 0 otherwise
    [ $test -eq 1 ] && errMsg "$errorMsg"
	}

# test for correct number of arguments and get values
if [ $# -eq 0 ]
	then
	# help information
   echo ""
   usage2
   exit 0
elif [ $# -gt 6 ]
	then
	errMsg "--- TOO MANY ARGUMENTS WERE PROVIDED ---"
else
	while [ $# -gt 0 ]
		do
			# get parameter values
			case "$1" in
		  -h|-help)    # help information
					   echo ""
					   usage2
					   exit 0
					   ;;
				-c)    # get  colormode
					   shift  # to get the next parameter
					   # test if parameter starts with minus sign 
					   errorMsg="--- INVALID COLORMODE SPECIFICATION ---"
					   checkMinus "$1"
					   colormode=`echo "$1" | tr '[A-Z]' '[a-z]'`
					   case "$colormode" in 
					   		gray) ;;
					   		intensity) ;;
					   		luminance|luminosity) colormode="luminance" ;;
					   		lightness) ;;
					   		brightness) ;;
					   		average) ;;
					   		magnitude|global) colormode="magnitude" ;;
					   		rgb|separate) colormode="rgb" ;;
					   		*) errMsg "--- COLORMODE=$colormode IS AN INVALID VALUE ---" 
					   	esac
					   ;;
				-m)    # get midrange
					   shift  # to get the next parameter - radius,sigma
					   # test if parameter starts with minus sign 
					   errorMsg="--- INVALID MIDRANGE SPECIFICATION ---"
					   checkMinus "$1"
					   midrange=`expr "$1" : '\([.0-9]*\)'`
					   [ "$midrange" = "" ] && errMsg "--- MIDRANGE=$midrange MUST BE A NON-NEGATIVE FLOAT ---"
					   midrangetestA=`echo "$midrange <= 0" | bc`
					   midrangetestB=`echo "$midrange >= 1" | bc`
					   [ $midrangetestA -eq 1 -o $midrangetestB -eq 1 ] && errMsg "--- MIDRANGE=$midrange MUST BE AN FLOAT GREATER THAN 0 AND SMALLER THAN 1 ---"
					   ;;
				 -)    # STDIN and end of arguments
					   break
					   ;;
				-*)    # any other - argument
					   errMsg "--- UNKNOWN OPTION ---"
					   ;;
		     	 *)    # end of arguments
					   break
					   ;;
			esac
			shift   # next option
	done
	#
	# get infile and outfile
	infile="$1"
	outfile="$2"
fi

# test that infile provided
[ "$infile" = "" ] && errMsg "NO INPUT FILE SPECIFIED"

# test that outfile provided
[ "$outfile" = "" ] && errMsg "NO OUTPUT FILE SPECIFIED"


# setup temporary images
tmpA1="$dir/autolevel_1_$$.mpc"
tmpA2="$dir/autolevel_1_$$.cache"
tmpI1="$dir/autolevel_2_$$.mpc"
tmpI2="$dir/autolevel_2_$$.cache"
tmpR1="$dir/autolevel_R_$$.mpc"
tmpR2="$dir/autolevel_R_$$.cache"
tmpG1="$dir/autolevel_G_$$.mpc"
tmpG2="$dir/autolevel_G_$$.cache"
tmpB1="$dir/autolevel_B_$$.mpc"
tmpB2="$dir/autolevel_B_$$.cache"
trap "rm -f $tmpA1 $tmpA2 $tmpI1 $tmpI2 $tmpR1 $tmpR2 $tmpG1 $tmpG2 $tmpB1 $tmpB2;" 0
trap "rm -f $tmpA1 $tmpA2 $tmpI1 $tmpI2 $tmpR1 $tmpR2 $tmpG1 $tmpG2 $tmpB1 $tmpB2; exit 1" 1 2 3 15
trap "rm -f $tmpA1 $tmpA2 $tmpI1 $tmpI2 $tmpR1 $tmpR2 $tmpG1 $tmpG2 $tmpB1 $tmpB2; exit 1" ERR


# read input and convert to appropriate colorspace/channel
if convert -quiet "$infile" +repage "$tmpA1"
	then
	: ' do nothing '
else
	errMsg "--- FILE $infile DOES NOT EXIST OR IS NOT AN ORDINARY FILE, NOT READABLE OR HAS ZERO SIZE ---"
fi

# get im version
im_version=`convert -list configure | \
	sed '/^LIB_VERSION_NUMBER */!d; s//,/;  s/,/,0/g;  s/,0*\([0-9][0-9]\)/\1/g' | head -n 1`

# colorspace RGB and sRGB swapped between 6.7.5.5 and 6.7.6.7 
# though probably not resolved until the latter
# then -colorspace gray changed to linear between 6.7.6.7 and 6.7.8.2 
# then -separate converted to linear gray channels between 6.7.6.7 and 6.7.8.2,
# though probably not resolved until the latter
# so -colorspace HSL/HSB -separate and -colorspace gray became linear
# but we need to use -set colorspace RGB before using them at appropriate times
# so that results stay as in original script
# The following was determined from various version tests using autolevel.
# with IM 6.7.4.10, 6.7.6.10, 6.7.8.6
if [ "$im_version" -lt "06070606" -o "$im_version" -gt "06070707" ]; then
	cspace="RGB"
else
	cspace="sRGB"
fi
if [ "$im_version" -lt "06070607" -o "$im_version" -gt "06070707" ]; then
	setcspace="-set colorspace RGB"
else
	setcspace=""
fi
# no need for setcspace for grayscale or channels after 6.8.5.4
if [ "$im_version" -gt "06080504" ]; then
	setcspace=""
	cspace="sRGB"
fi

#convert image to RGB and separate channels according to colormode
if [ "$colormode" = "intensity" -o "$colormode" = "gray" ]; then
	convert $tmpA1 $setcspace -colorspace Gray $tmpI1
elif [ "$colormode" = "luminance" -a "$im_version" -ge "07000000" ]; then
	convert $tmpA1 $setcspace -grayscale Rec709Luma $tmpI1
elif [ "$colormode" = "luminance" -a "$im_version" -lt "07000000" ]; then
	convert $tmpA1 $setcspace -colorspace Rec709Luma $tmpI1
elif [ "$colormode" = "lightness" ]; then
	convert $tmpA1 $setcspace -colorspace HSL -channel B -separate $tmpI1
elif [ "$colormode" = "brightness" ]; then
	convert $tmpA1 $setcspace -colorspace HSB -channel B -separate $tmpI1
elif [ "$colormode" = "average" ]; then
	convert $tmpA1 $setcspace -colorspace OHTA -channel R -separate $tmpI1
elif [ "$colormode" = "magnitude" ]; then
	convert $tmpA1 $tmpI1
elif [ "$colormode" = "rgb" ]; then
	convert $tmpA1 $setcspace -channel R -separate $tmpR1
	convert $tmpA1 $setcspace -channel G -separate $tmpG1
	convert $tmpA1 $setcspace -channel B -separate $tmpB1
fi


getChannelStats()
	{
	img="$1"
	# statistics computed as percent (of dynamic range) values
	if [ "$im_version" -ge "06030901" ]
		then 
		min=`convert $img -format "%[min]" info:`
		max=`convert $img -format "%[max]" info:`
		mean=`convert $img -format "%[mean]" info:`
		min=`convert xc: -format "%[fx:100*$min/quantumrange]" info:`
		max=`convert xc: -format "%[fx:100*$max/quantumrange]" info:`
		mean=`convert xc: -format "%[fx:100*$mean/quantumrange]" info:`
	else
		data=`convert $img -verbose info:`
		min=`echo "$data" | sed -n 's/^.*[Mm]in:.*[(]\([0-9.]*\).*$/\1/p ' | head -1`
		max=`echo "$data" | sed -n 's/^.*[Mm]ax:.*[(]\([0-9.]*\).*$/\1/p ' | head -1`
		mean=`echo "$data" | sed -n 's/^.*[Mm]ean:.*[(]\([0-9.]*\).*$/\1/p ' | head -1`
		min=`convert xc: -format "%[fx:100*$min]" info:`
		max=`convert xc: -format "%[fx:100*$max]" info:`
		mean=`convert xc: -format "%[fx:100*$mean]" info:`
	fi
	# gamma is the ratio of logs of the mean and midvalue of the dynamic range
	# where we normalize both to the range between 0 and 1
	# ref: http://rsb.info.nih.gov/ij/plugins/auto-gamma.html
	# However, I have inverted his formula for use with values 
	# in range 0 to 1, which works much better my way
	gammaval=`convert xc: -format "%[fx:log($mean/100)/log($midrange)]" info:`
	}


# process image
echo ""
if [ "$colormode" != "rgb" ]; then
	getChannelStats "$tmpI1"
	echo "min=$min%; max=$max%; gamma=$gammaval"
	convert $tmpA1 -level ${min}%,${max}%,$gammaval "$outfile"
else
	getChannelStats "$tmpR1"
	echo "RED: min=$min%; max=$max%; gamma=$gammaval"
	convert $tmpR1 -level ${min}%,${max}%,$gammaval $tmpR1

	getChannelStats "$tmpG1"
	echo "GREEN: min=$min%; max=$max%; gamma=$gammaval"
	convert $tmpG1 -level ${min}%,${max}%,$gammaval $tmpG1

	getChannelStats "$tmpB1"
	echo "BLUE: min=$min%; max=$max%; gamma=$gammaval"
	convert $tmpB1 -level ${min}%,${max}%,$gammaval $tmpB1

	convert $tmpR1 $tmpG1 $tmpB1 -combine -colorspace $cspace "$outfile"
fi
echo ""
exit 0

	



