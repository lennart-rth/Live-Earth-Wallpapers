#!/bin/bash
#
# Developed by Fred Weinhaus 8/29/2012 .......... revised 6/10/2018
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
# USAGE: autotone [-b] [-g] [-w] [-G] [-n] [-s] [-p] [-R resize] [-P percent] 
# [-M midrange] [-N noise] [-S sharp] [-F feedback] [-WN whitenorm] 
# [-GN graynorm] infile outfile
#
# USAGE: autotone [-h or -help]
#
# OPTIONS:
#
# -b                      disable auto brightness/contrast
# -g                      disable auto gray balance
# -w                      disable auto white balance
# -G                      disable auto gamma correction
# -n                      disable auto noise removal
# -s                      disable auto sharpening
# -p                      enable progress monitoring
# -R      resize          limit the output size to this value; integer>0; 
#                         will resize if the larger dimension of the image 
#                         exceeds this value
# -P      percent         percent threshold for detecting gray/white 
#                         for auto gray and auto white balance; 0<float<100;
#                         default=1
# -M      midrange        midrange value for auto gamma correction;
#                         0<float<1; default=0.425
# -N      noise           noise removal factor; integer>0; default is 
#                         automatically computed; range is about 1 to 4
# -S      sharp           sharpening amount; float>=0; default is 
#                         automatically computed; range is about 1 to 4
# -F      feedback        sharpening feedback (gain); float>=1; default=1
# -WN     whitenorm       white balance normalization method; choices are: 
#                         none (n), ave (a), max (m); default=none
# -GN     graynorm        gray balance normalization method; choices are: 
#                         none (n), ave (a), max (m); default=none
#
###
#
# NAME: AUTOTONE 
# 
# PURPOSE: To automatically tone balance an image.
# 
# DESCRIPTION: AUTOTONE attempts to automatically tone balance and image. This 
# includes auto brightness/contrast adjustment, auto gray balance, auto white 
# balance, auto gamma correction, auto noise removal and auto sharpening.
# 
# OPTIONS: 
# 
# -b ... disable auto brightness/contrast
# 
# -g ... disable auto gray balance
# 
# -w ... disable auto white balance
# 
# -G ... disable auto gamma correction
# 
# -n ... disable auto noise removal
# 
# -s ... disable auto sharpening
# 
# -p ... enable progress monitoring
# 
# -R resize ... RESIZE is the limit on the output image size. Values are 
# integer>0. This will only resize if the larger dimension of the image 
# exceeds this value. The default is no limit (i.e. no resize).
# 
# -P percent ... PERCENT is the percent threshold for detecting gray/white 
# in the image for auto gray and auto white balance. Values are 0<floats<100.
# The default=1.
# 
# -M midrange ... MIDRANGE value for auto gamma correction. Values are 
# 0<floats<1. The default=0.425.
# 
# -N (noise) repeats ... NOISE REPEATS removal factor. Values are integers>0.  
# The default is automatically computed. The nominal range is about 1 to 4 
# depending upon image size. Larger values are used for larger images.
# 
# -S sharp ... SHARP is the sharpening amount. Values are floats>=0. The 
# default is automatically computed. The nominal range is about 1 to 4. 
# Larger values are used for larger images.
#
# -F feedback ... FEEDBACK is the sharpening feedback (gain). Values are 
# floats>=1. The default=1.
#  
# -WN whitenorm ... WHITENORM is the white balance r,g,b ratio normalization 
# method. The choices are: none (n), ave (a), max (m). The default=none
# 
# -GN graynorm ... GRAYNORM is the gray balance r,g,b ratio normalization  
# method. The choices are: none (n), ave (a), max (m). The default=none
# 
# NOTE: The white balance and gray balance techniques now have optional r,g,b
# ratio normalizations that help prevent brightness increases and 
# over-saturation at white from these parts of the script. Furthermore, to
# avoid possible excess color shifts as well as mitigate over-saturation of
# white, one may reduce the percent argument to about 0.1. All of the above
# as well as the midrange argument are subject to personal tastes and tuning.
# The defaults have been left in the old mode for backward compatibility. 
# I thank Dr. Guenter Grau for the suggestion to normalize the r,g,b ratios 
# in the white balance and gray balance parts of the code. My current 
# recommendation is to use whitenorm=ave, graynorm=ave and percent=0.1.
# 
# CAVEAT: No guarantee that this script will work on all platforms, 
# nor that trapping of inconsistent parameters is complete and 
# foolproof. Use At Your Own Risk. 
# 
######
#

# on/off parameters and resize input
resize=""  			#resizes input if larger than this; pixel dimension or "" for no resize
bright="yes"		#auto brighten; yes/no
gray="yes"			#auto gray balance; yes/no
white="yes"			#auto white balance; yes/no
gamma="yes"			#auto gamma; yes/no
noise="yes"			#auto noise removal; yes/no
sharpen="yes"		#auto sharpen; yes/no
progress="false"	#echo progress comments

# tuning parameters
percent=1			# percent near white from combined S and B channels of HSB to use for whitebalance
gammamid=0.425		# midrange for -gamma processing
skythresh=80		# percent threshold to isolate sky for gamma processing from combination of S and B channels of HSB
skyheight=25		# percent of height at top of image considered as sky
maskthresh=0.125	# threshold on sky mask to continue processing for sky; process only if larger than threshold; avoids compensation for too little sky
repeats=""			# denoise -enhance repeats; "" means autocompute the repeats; repeats>0
gain=0.75			# sharpening gain/attenuation factor; >1 is gain; <1 is attenuate; applied towards the automatic amount
feedback=1			# unsharp feedback/gain
whitenorm="none"	# white balance rgb ratio normalization; none, ave, max.
graynorm="none"		# gray balance rgb ratio normalization; none, ave, max.

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
elif [ $# -gt 25 ]
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
				-b)    # disable auto brightness/contrast
					   bright="no"
					   ;;
				-g)    # disable auto gray balance
					   gray="no"
					   ;;
				-w)    # disable auto white balance
					   white="no"
					   ;;
				-G)    # disable auto gamma correction
					   gamma="no"
					   ;;
				-n)    # disable auto noise removal
					   noise="no"
					   ;;
				-s)    # disable auto sharpening
					   sharpen="no"
					   ;;
				-p)    # enable progress monitoring
					   progress="true"
					   ;;
				-R)    # get resize
					   shift  # to get the next parameter 
					   # test if parameter starts with minus sign 
					   errorMsg="--- INVALID RESIZE SPECIFICATION ---"
					   checkMinus "$1"
					   resize=`expr "$1" : '\([0-9]*\)'`
					   [ "$resize" = "" ] && errMsg "--- RESIZE=$resize MUST BE A NON-NEGATIVE INTEGER ---"
					   testA=`echo "$resize <= 0" | bc`
					   [ $testA -eq 1 ] && errMsg "--- RESIZE=$resize MUST BE AN INTEGER GREATER THAN 0 ---"
					   ;;
				-P)    # get percent
					   shift  # to get the next parameter
					   # test if parameter starts with minus sign 
					   errorMsg="--- INVALID PERCENT SPECIFICATION ---"
					   checkMinus "$1"
					   percent=`expr "$1" : '\([.0-9]*\)'`
					   [ "$percent" = "" ] && errMsg "--- PERCENT=$percent MUST BE A NON-NEGATIVE FLOAT ---"
					   testA=`echo "$percent <= 0" | bc`
					   testB=`echo "$percent >= 100" | bc`
					   [ $testA -eq 1 -o $testB -eq 1 ] && errMsg "--- PERCENT=$percent MUST BE A FLOAT GREATER THAN 0 AND SMALLER THAN 100 ---"
					   ;;
				-M)    # get midrange
					   shift  # to get the next parameter
					   # test if parameter starts with minus sign 
					   errorMsg="--- INVALID MIDRANGE SPECIFICATION ---"
					   checkMinus "$1"
					   gammamid=`expr "$1" : '\([.0-9]*\)'`
					   [ "$gammamid" = "" ] && errMsg "--- MIDRANGE=$gammamid MUST BE A NON-NEGATIVE FLOAT ---"
					   testA=`echo "$gammamid <= 0" | bc`
					   testB=`echo "$gammamid >= 1" | bc`
					   [ $testA -eq 1 -o $testB -eq 1 ] && errMsg "--- MIDRANGE=$gammamid MUST BE A FLOAT GREATER THAN 0 AND SMALLER THAN 1 ---"
					   ;;
				-N)    # get noise repeats
					   shift  # to get the next parameter
					   # test if parameter starts with minus sign 
					   errorMsg="--- INVALID NOISE REPEATS SPECIFICATION ---"
					   checkMinus "$1"
					   repeats=`expr "$1" : '\([0-9]*\)'`
					   [ "$repeats" = "" ] && errMsg "--- NOISE REPEATS=$repeats MUST BE A NON-NEGATIVE INTEGER ---"
					   testA=`echo "$repeats <= 0" | bc`
					   [ $testA -eq 1 ] && errMsg "--- NOISE REPEATs=$repeats MUST BE AN INTEGER GREATER THAN 0 ---"
					   ;;
				-S)    # get sharp
					   shift  # to get the next parameter
					   # test if parameter starts with minus sign 
					   errorMsg="--- INVALID SHARP SPECIFICATION ---"
					   checkMinus "$1"
					   sharp=`expr "$1" : '\([.0-9]*\)'`
					   [ "$sharp" = "" ] && errMsg "--- SHARP=$sharp MUST BE A NON-NEGATIVE FLOAT ---"
					   ;;
				-F)    # get feedback
					   shift  # to get the next parameter
					   # test if parameter starts with minus sign 
					   errorMsg="--- INVALID FEEDBACK SPECIFICATION ---"
					   checkMinus "$1"
					   feedback=`expr "$1" : '\([.0-9]*\)'`
					   [ "$feedback" = "" ] && errMsg "--- FEEDBACK=$feedback MUST BE A NON-NEGATIVE FLOAT ---"
					   test=`echo "$feedback < 1" | bc`
					   [ $test -eq 1 ] && errMsg "--- FEEDBACK=$feedback MUST BE A FLOAT GREATER THAN OR EQUAL TO 1 ---"
					   ;;
			   -WN)    # get  whitenorm
					   shift  # to get the next parameter
					   # test if parameter starts with minus sign 
					   errorMsg="--- INVALID WHITENORM SPECIFICATION ---"
					   checkMinus "$1"
					   whitenorm=`echo "$1" | tr '[A-Z]' '[a-z]'`
					   case "$whitenorm" in 
					   		none|n) whitenorm="none";;
					   		ave|a) whitenorm="ave";;
					   		max|m) whitenorm="max";;
					   		*) errMsg "--- WHITENORM=$whitenorm IS AN INVALID VALUE ---" 
					   	esac
					   ;;
			   -GN)    # get  graynorm
					   shift  # to get the next parameter
					   # test if parameter starts with minus sign 
					   errorMsg="--- INVALID GRAYNORM SPECIFICATION ---"
					   checkMinus "$1"
					   graynorm=`echo "$1" | tr '[A-Z]' '[a-z]'`
					   case "$graynorm" in 
					   		none|n) graynorm="none";;
					   		ave|a) graynorm="ave";;
					   		max|m) graynorm="max";;
					   		*) errMsg "--- GRAYNORM=$graynorm IS AN INVALID VALUE ---" 
					   	esac
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



# set directory for temporary files
tmpdir="$dir"

dir="$tmpdir/AUTOTONE.$$"

mkdir "$dir" || errMsg "--- FAILED TO CREATE TEMPORARY FILE DIRECTORY ---"
trap "rm -rf $dir;" 0
trap "rm -rf $dir; exit 1" 1 2 3 15
trap "rm -rf $dir; exit 1" ERR

# Process Resize
if [ "$resize" != "" ]; then
	resizing="-resize $resize>"
else
	resizing=""
fi

# read input image into temporary memory mapped (mpc) format image
convert -quiet "$infile" +repage $resizing $dir/tmpI.mpc ||
	errMsg  "--- FILE $infile DOES NOT EXIST OR IS NOT AN ORDINARY FILE, NOT READABLE OR HAS ZERO SIZE  ---"

# get max dimension
dim=`convert $dir/tmpI.mpc -format "%[fx:max(w,h)]" info:`
#echo "$dim"

# set up to reduce image size if larger than 1000 pixels for certain processes to speed them up
if [ $dim -gt 1000 ]; then
	reducing="-resize 25%"
else
	reducing=""
fi

# get im version
im_version=`convert -list configure | \
sed '/^LIB_VERSION_NUMBER */!d;  s//,/;  s/,/,0/g;  s/,0*\([0-9][0-9]\)/\1/g' | head -n 1`

# colorspace RGB and sRGB swapped between 6.7.5.5 and 6.7.6.7 
# though probably not resolved until the latter
# then -colorspace gray changed to linear between 6.7.6.7 and 6.7.8.2 
# then -separate converted to linear gray channels between 6.7.6.7 and 6.7.8.2,
# though probably not resolved until the latter
# so -colorspace HSL/HSB -separate and -colorspace gray became linear
# but we need to use -set colorspace RGB before using them at appropriate times
# so that results stay as in original script
# The following was determined from various version tests 
# with IM 6.7.4.10, 6.7.6.10, 6.7.8.6
if [ "$im_version" -lt "06070607" -o "$im_version" -gt "06070707" ]; then
	setcspace="-set colorspace RGB"
else
	setcspace=""
fi
if [ "$im_version" -lt "06070607" ]; then
	cspace="RGB"
else
	cspace="sRGB"
fi
# no need for setcspace for grayscale or channels after 6.8.5.4
if [ "$im_version" -gt "06080504" ]; then
	setcspace=""
	cspace="sRGB"
fi


getMinMax()
	{
	img="$1"
	if [ "$im_version" -ge "06030901" ]
		then 
		min=`convert $img -format "%[min]" info:`
		max=`convert $img -format "%[max]" info:`
		min=`convert xc: -format "%[fx:100*$min/quantumrange]" info:`
		max=`convert xc: -format "%[fx:100*$max/quantumrange]" info:`
	else
		data=`convert $img -verbose info:`
		min=`echo "$data" | sed -n 's/^.*[Mm]in:.*[(]\([0-9.]*\).*$/\1/p ' | head -1`
		max=`echo "$data" | sed -n 's/^.*[Mm]ax:.*[(]\([0-9.]*\).*$/\1/p ' | head -1`
		min=`convert xc: -format "%[fx:100*$min)]" info:`
		max=`convert xc: -format "%[fx:100*$max)]" info:`
	fi
	}

# function to get mean of image
getMean()
	{
	img="$1"
	if [ "$im_version" -ge "06030901" ]
		then 
		mean=`convert $img -format "%[mean]" info:`
		mean=`convert xc: -format "%[fx:$mean/quantumrange]" info:`
	else
		data=`convert $img -verbose info:`
		mean=`echo "$data" | sed -n 's/^.*[Mm]ean:.*[(]\([0-9.]*\).*$/\1/p ' | head -1`
		mean=`convert xc: -format "%[fx:$mean]" info:`
	fi
	}

# function to get color ratios for white balancing
getRatio()
	{
	getMean "$1"
	ref="$2"
	# get ave in range 0-100
	# note both mean and mask_mean are in range 0-100
	# note average of just near_gray values mean of masked image divided by
	# the fraction of white pixels (from mask)
	# which is the mean in range 0 to 1 divided by 100
	ave=`convert xc: -format "%[fx:$mean/$maskmean]" info:`
	[ "$ave" = "0" -o "$ave" = "0.0" ] && ave=100
	ratio=`convert xc: -format "%[fx:$ref/$ave]" info:`
	}


# set up -recolor or -color-matrix for color balancing
if [ "$im_version" -lt "06060100" ]; then
	process="-recolor"
else
	process="-color-matrix"
fi


# Process Brightness
if [ "$bright" = "yes" ]; then
	$progress && echo "brighten"
	if [ "$im_version" -lt "06050501" ]; then
		getMinMax $dir/tmpI.mpc
		convert $dir/tmpI.mpc -level $min%,$max% $dir/tmpI.mpc
	else 
		convert $dir/tmpI.mpc -auto-level $dir/tmpI.mpc
	fi
fi


# Process graybalance
if [ "$gray" = "yes" ]; then
	$progress && echo "graybalance"

	# separate channels
	convert $dir/tmpI.mpc $setcspace $reducing -channel RGB -separate $dir/tmpRGB.mpc
	
	# get ratios for graybalance
	# get mask of top percent closest to gray
	# approximation using negated saturation and solarized brightness multiplied
	convert $dir/tmpI.mpc $setcspace $reducing \
		\( -clone 0 -colorspace HSB -channel G -negate -separate +channel \) \
		\( -clone 0 -colorspace HSB -channel B -separate +channel -solarize 50% -level 0x50% \) \
		\( -clone 1 -clone 2 -compose multiply -composite \) \
		\( -clone 3 -contrast-stretch 0,${percent}% -fill black +opaque white \) \
		-delete 0-3 $dir/tmpM.mpc

	
	# get mean of mask
	getMean $dir/tmpM.mpc
	maskmean=$mean
	#echo "maskmean=$maskmean"
	
	# use mask image to isolate user supplied percent of pixels closest to white
	# then get ave graylevel for each channel of mask selected pixels
		
	convert $dir/tmpRGB.mpc[0] $dir/tmpM.mpc -compose multiply -composite $dir/tmpT.mpc
	getRatio "$dir/tmpT.mpc[0]" "0.5"
	redave=$ave
	redratio=$ratio
	#echo "R: ave=$ave; redratio=$ratio"
	
	convert $dir/tmpRGB.mpc[1] $dir/tmpM.mpc -compose multiply -composite $dir/tmpT.mpc
	getRatio "$dir/tmpT.mpc[1]" "0.5"
	greenave=$ave
	greenratio=$ratio
	#echo "G: ave=$ave; greenratio=$ratio;"
	
	convert $dir/tmpRGB.mpc[2] $dir/tmpM.mpc -compose multiply -composite $dir/tmpT.mpc
	getRatio "$dir/tmpT.mpc[2]" "0.5"
	blueave=$ave
	blueratio=$ratio
	#echo "B: ave=$ave; blueratio=$ratio;"

	# normalize r,g,b ratios by maximum ratio, so no added increase in brightness
	if [ "$graynorm" != "none" ]; then
		if [ "$graynorm" = "ave" ]; then
			gnormfact=`convert xc: -format "%[fx: ($blueratio+$greenratio+$redratio)/3]" info:`
		elif [ "$graynorm" = "max" ]; then
			gnormfact=`convert xc: -format "%[fx: max(max($blueratio,$greenratio),$redratio)]" info:`
		fi
		redratio=`convert xc: -format "%[fx: $redratio/$gnormfact]" info:`
		greenratio=`convert xc: -format "%[fx: $greenratio/$gnormfact]" info:`
		blueratio=`convert xc: -format "%[fx: $blueratio/$gnormfact]" info:`
		#echo "R: ave=$redave; ratio=$redratio"
		#echo "G: ave=$greenave; ratio=$greenratio;"
		#echo "B: ave=$blueave; ratio=$blueratio;"
	fi
		
	#unused test
	#rmse=`convert xc: -format "%[fx:sqrt( (0.5-$redave)^2 + (0.5-$greenave)^2 + (0.5-$blueave)^2 )/3]" info:`
	#test1=`convert xc: -format "%[fx:$rmse>0?1:0]" info:`
	#echo "rmse=$rmse; test1=$test1"
	test1=1
	
	if [ $test1 -eq 1 ]; then 
		convert $dir/tmpI.mpc $process "$redratio 0 0 0 $greenratio 0 0 0 $blueratio" $dir/tmpI.mpc
	fi
fi

# Process whitebalance
if [ "$white" = "yes" ]; then
	$progress && echo "whitebalance"

	# separate channels
	convert $dir/tmpI.mpc $setcspace $reducing -channel RGB -separate $dir/tmpRGB.mpc
	
	# get ratios for whitebalance
	# get mask of top percent closest to white
	# approximation using negated saturation and brightness channels multiplied
	convert $dir/tmpI.mpc $setcspace $reducing \
		-colorspace HSB -channel G -negate -channel GB -separate +channel \
		-compose multiply -composite \
		-contrast-stretch 0,${percent}% -fill black +opaque white \
		$dir/tmpM.mpc
	
	# get mean of mask
	getMean $dir/tmpM.mpc
	maskmean=$mean
	#echo "maskmean=$maskmean"
	
	# use mask image to isolate user supplied percent of pixels closest to white
	# then get ave graylevel for each channel of mask selected pixels
		
	convert $dir/tmpRGB.mpc[0] $dir/tmpM.mpc -compose multiply -composite $dir/tmpT.mpc
	getRatio "$dir/tmpT.mpc[0]" "1"
	redave=$ave
	redratio=$ratio
	#echo "R: ave=$ave; redratio=$ratio"
	
	convert $dir/tmpRGB.mpc[1] $dir/tmpM.mpc -compose multiply -composite $dir/tmpT.mpc
	getRatio "$dir/tmpT.mpc[1]" "1"
	greenave=$ave
	greenratio=$ratio
	#echo "G: ave=$ave; greenratio=$ratio;"
	
	convert $dir/tmpRGB.mpc[2] $dir/tmpM.mpc -compose multiply -composite $dir/tmpT.mpc
	getRatio "$dir/tmpT.mpc[2]" "1"
	blueave=$ave
	blueratio=$ratio
	#echo "B: ave=$ave; blueratio=$ratio;"

	# normalize r,g,b ratios by maximum ratio, so no added increase in brightness
	if [ "$whitenorm" != "none" ]; then
		if [ "$whitenorm" = "ave" ]; then
			wnormfact=`convert xc: -format "%[fx: ($blueratio+$greenratio+$redratio)/3]" info:`
		elif [ "$whitenorm" = "max" ]; then
			wnormfact=`convert xc: -format "%[fx: max(max($blueratio,$greenratio),$redratio)]" info:`
		fi
		redratio=`convert xc: -format "%[fx: $redratio/$wnormfact]" info:`
		greenratio=`convert xc: -format "%[fx: $greenratio/$wnormfact]" info:`
		blueratio=`convert xc: -format "%[fx: $blueratio/$wnormfact]" info:`
		#echo "R: ave=$redave; ratio=$redratio"
		#echo "G: ave=$greenave; ratio=$greenratio;"
		#echo "B: ave=$blueave; ratio=$blueratio;"
	fi
	
	#unused test
	#rmse=`convert xc: -format "%[fx:sqrt( (1-$redave)^2 + (1-$greenave)^2 + (1-$blueave)^2 )/3]" info:`
	#test1=`convert xc: -format "%[fx:$rmse>0?1:0]" info:`
	#echo "rmse=$rmse; test1=$test1"
	test1=1
	
	if [ $test1 -eq 1 ]; then 
		convert $dir/tmpI.mpc $process "$redratio 0 0 0 $greenratio 0 0 0 $blueratio" $dir/tmpI.mpc
	fi
fi


# Process Gamma
if [ "$gamma" != "no" ]; then
	$progress && echo "gamma"
	# get gammaval for -gamma processing
	# gamma is the ratio of logs of the mean and mid value of the dynamic range
	# where we normalize both to the range between 0 and 1
	# ref: http://rsb.info.nih.gov/ij/plugins/auto-gamma.html
	# However, I have inverted his formula for use with values 
	# in range 0 to 1, which works much better my way
	
	# reduce image and get mean
	convert $dir/tmpI.mpc $setcspace $reducing $dir/tmpT.mpc
	getMean "$dir/tmpT.mpc"
	gmean=$mean
	#echo "gmean=$gmean;"

	if [ "$im_version" -ge "07000000" ]; then
		identifying="magick identify"
	else
		identifying="identify"
	fi

	# test for mask processing of upper portion of negated saturation * brightness 
	# to remove too much white from affecting the gamma processing

	# process only if gmean>gammamid; ie. overly bright image mean
	test1=`convert xc: -format "%[fx:$gmean>$gammamid?1:0]" info:`
	#echo "test1=$test1;"
	if [ $test1 -eq 1 ]; then
		# get mask from saturation and brightness channels
		convert $dir/tmpT.mpc -colorspace HSB -channel G -negate -channel GB -separate +channel \
			-compose multiply -composite -threshold $skythresh% $dir/tmpM.mpc

		# get mean of mask
		getMean "$dir/tmpM.mpc"
		maskmean=$mean
		
		# Process only if maskmean is larger than some threshold -- ie don't process if too little sky
		test2=`convert xc: -format "%[fx:$maskmean>$maskthresh?1:0 ]" info:`
		#echo "maskmean=$maskmean; test2=$test2"
		if [ $test2 -eq 1 ]; then
			# get dimensions
			ww=`$identifying -ping -format "%w" $dir/tmpM.mpc`
			hh=`$identifying -ping -format "%h" $dir/tmpM.mpc`
			hhh=`convert xc: -format "%[fx:round($skyheight*$hh)]" info:`
			convert \( -size ${ww}x${hh} xc:black \) \( -size ${ww}x${hhh} xc:white \) \
				-compose over -composite $dir/tmpM.mpc -compose multiply -composite -negate $dir/tmpM.mpc

			# get mean of mask
			getMean "$dir/tmpM.mpc"
			maskmean=$mean
			# compute new mean of masked image
			newmean=`convert $dir/tmpT.mpc $dir/tmpM.mpc -compose multiply -composite -format "%[fx:mean]" info:`
			gmean=`convert xc: -format "%[fx:$newmean/$maskmean]" info:`
		fi
	fi

	gammaval=`convert xc: -format "%[fx:log($gmean)/log($gammamid)]" info:`
	convert "$dir/tmpI.mpc" -gamma $gammaval "$dir/tmpI.mpc"
	#echo "gmean=$gmean; gammaval=$gammaval;"
fi


# Process Denoise
if [ "$noise" = "yes" ]; then
	$progress && echo "denoise"
	if [ "$repeats" = "" ]; then
		repeats=`convert xc: -format "%[fx:max(1,floor($dim/1000))]" info:`
	fi
	denoise=""
	for ((i=0;i<repeats;i++)) do
		denoise="$denoise -enhance"
	done
	convert $dir/tmpI.mpc $denoise $dir/tmpI.mpc
	#echo "denoise=$denoise"
fi


# Process Sharpening
if [ "$sharpen" = "yes" ]; then
	$progress && echo "sharpen"
	if [ "$sharp" = "" ]; then
		# get sharpening amount
		sharp=`convert $dir/tmpI.mpc -format "%[fx:max(0.5,$gain*$dim/1000)]" info:`
	fi
	#echo "sharp=$sharp"
	convert $dir/tmpI.mpc -unsharp 0x${sharp}+${feedback} $dir/tmpI.mpc
fi


# Save to Output
convert $dir/tmpI.mpc "$outfile"

exit 0



