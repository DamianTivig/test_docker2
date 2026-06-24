#!/usr/bin/env python3
import os
import stat

files = {
"SVF_PATCH.csh": {
"executable": True,
"content": r"""#!/bin/csh
 
echo Pause for 60 seconds; 
sleep 60
 
source ./LOAD_CFG_<AREA>.cfg
set C_USERLIST_TR=SVF_DCA2_611
set PATCH_DIR_DUPLICATE_DCA2="$RDF_HOME/patches/DUPLICATE_DCA2"
echo ===============================================================================================
echo `date`:  SVF patches - START
echo ===============================================================================================
 
set dir=$PATCH_DIR_DUPLICATE_DCA2
set c=0
#make sure $dir exits 
if ( -d ${dir} ) then
    set c=`ls -a ${dir} | wc | awk '{print $1}'`
  ##IS dir is empty
    if ( "${c}" == 2 ) then
		echo "Empty directory - "${dir}
    else 	#dir has files 	then do the following
		echo "Dir has files - "${dir}
		cd $RDF_HOME/patches
		./runPatch "nt#r2g2nsB" $SP_SERVER ./DUPLICATE_DCA2/SVF_DUPLICATE_DCA2.sql $C_USERLIST_TR 
		./errorCheck.csh $RDF_HOME/patches/DUPLICATE_DCA2/log/*SVF_DUPLICATE_DCA2*.log 
    endif
else
      echo " Not a directory"
endif
echo ===============================================================================================
echo `date`:  SVF patches -  DONE
echo ===============================================================================================
 
echo "SVF PATCHES DONE - check the logs for all the patches ${TIMESTAMP} " | mail -s "SVF PATCHES DONE" $MY_EMAIL
 
echo Pause for 60 seconds; 
sleep 60
"""
},
"RDF_NA_611.XML": {
"executable": False,
"content": r"""<?xml version="1.0" encoding="UTF-8"?>
<Workflow xmlns="http://navtech.com" 
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
    xmlns:log4j="http://jakarta.apache.org/log4j/" 
    xsi:schemaLocation="http://navtech.com RDFConfigSchema.xsd"
>
<!-- Quick start for new users: look for prefix YOUR_ and replace the names with your settings -->
 
 
<!-- !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! -->
<!-- !!!!!! NOTE: The config file has to be in the same directory as rdfConfigSchema.xsd !!!!!!
                    (Or, alternatively, adjust the reference location) --> 
<!-- !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! -->
 
 
<!-- Process Groups: ===============================================================
loadrdfCore:   		Creates the CoreSchema and loads Core(XMOB) rdf Data from the Loader Files, Validates the data and creates views. [executed by default]
loadAdmin:		Creates the Schema needed by Admin and Loads the tables [Not Executed by default]
loadSDO:	 	Creates the Schema needed by SDO and Loads the tables [Not Executed by default]
loadTraffic:		Creates the Schema needed by Traffic and loads the traffic data
loadVoice:		Creates the Schema needed by Voice and loads the Voice Data
createrdfSchemaOnly:	Creates the rdf base,SDO,Admin Schemas
 
Example to load Core rdf database, run the following:
rdf_installer.bat etc/xml/userconfig.xml loadrdfCore
 
Example to load complete rdf Database, run the following:
rdf_installer.bat etc/xml/userconfig.xml loadrdfCore loadAdmin loadSDO loadVoice loadTraffic
 
Example to load Chinese or World Markets rdf Database, run the following:
rdf_installer.bat etc/xml/userconfig.xml loadrdfCore loadAdmin loadSDO
 
Example to create rdf Schema Only
rdf_installer.bat etc/xml/userconfig.xml createrdfSchemaOnly
 
-->
 
  <!-- Settings for shared/globally managed ressources -->
<GlobalConfiguration>
 
    <Property Name="echo" Value="on"/>
<Property Name="timing" Value="on"/>
<Property Name="ParallelFactor" Value="4"/>
 
 
    <!-- Destination of Loader Files -->
<!-- SQLLoader options -->
<!-- YOUR LOADER FILE PATH SHOULD BE SET TO loaderfiles -->
<Property Name="LoaderFilePath" Value="LOADER_FILES"/>
<!-- Database connection parameters. Partially shared by SQL and JDBC connections -->
<Property Name="DBUser" Value="RDF_NA_610"/>
<Property Name="DBPassword" Value="nt#r2g2nsB"/>
<Property Name="JDBCURL" Value="jdbc:oracle:thin:RDF_NA_610/atadmin@//iadb101v.ia.ro.int.automotive-wan.com:1521/sgdf_1_P_PDB.ia.ro.int.automotive-wan.com" />
<Property Name="SID" Value="lizard1"/>
 
<!-- Configuration for sqlplus processes -->
<SQLConnection Name="default"
                   User="${DBUser}"
                   Password="${DBPassword}"
                   Instance="${SID}"
                   Url="${JDBCURL}"
    />
 
    <Transport Name="default" type="JDBCTransportType" Code="JDBC" Default="true">
<Class>com.navtech.maptools.transport.jdbc.JDBCTransport</Class>
<JDBCDriver>oracle.jdbc.driver.OracleDriver</JDBCDriver>
<ConnectionString>${JDBCURL}</ConnectionString>
<DatabaseUser>${DBUser}</DatabaseUser>
<DatabasePassword>${DBPassword}</DatabasePassword>
</Transport>
</GlobalConfiguration>
 
  <!-- Log4j configuration ======================================================  -->
<log4j:configuration xmlns:log4j="http://jakarta.apache.org/log4j/">
<!-- This Appender writes all output to stdout -->
<appender name="STDOUT" class="org.apache.log4j.ConsoleAppender">
<layout class="org.apache.log4j.PatternLayout">
<!-- Conversion patter for debugging/development -->
<!-- <param name="ConversionPattern" value="%d %-5p [%t] %C{1}.%M (%F:%L) - %m%n" /> -->
<!--  Conversion pattern for production - doesn't print line numbers,
              file names and other expensive stuff -->
<param name="ConversionPattern" value="[%r] - %-5p-> %m%n"/>
</layout>
</appender>
<!-- This Appender writes all output to the Log File -->
<appender name="LogFile" class="org.apache.log4j.FileAppender">
<param name="File" value="RDF_NA_610.LOG"/>
<param name="Append" value="true"/>
<!-- Conversion patter for debugging/development -->
<!-- <param name="ConversionPattern" value="%d %-5p [%t] %C{1}.%M (%F:%L) - %m%n" /> -->
<layout class="org.apache.log4j.PatternLayout">
<!-- Conversion patter for production -->
<param name="ConversionPattern" value="%d %-5p - %m%n"/>
</layout>
</appender>
 
    <!-- This appender will send a mail if a FATAL error occured -->
<!-- Requires mail.jar and activation.jar or j2ee available from http://java.sun.com -->        
<!--
<appender name="Mail" class="org.apache.log4j.net.SMTPAppender">
<param name="Threshold" value="FATAL" />
<param name="SMTPHost" value="YOUR_SMTP_SERVER" />
<param name="To" value="YOUR_MAIL@ADDRESS" />
<param name="From" value="YOUR_VALID_MAIL_USER@YOUR_SMTP_SERVER" />
<param name="Subject" value="rdf Fatal Error" />
<param name="BufferSize" value="4096" />
<layout class="org.apache.log4j.HTMLLayout">
</layout>
</appender>
    -->
<!-- Write all log events in the category com.navtech to the file appender
      and to mail (on fatal error). Change the priority from "info" to "debug"
      if you want to see all messages. Change additivity flag to "true" if you want
      output to console (inherited from root). Remove appender-ref to disable mail notification.
    -->
<category name="com.navtech">
<priority value="info"/>
<Param name="Additivity" value="false" />
<appender-ref ref="LogFile"/>
<!-- <appender-ref ref="Mail"/> -->
</category>
 
    <!-- Write Messages from WorkflowController to Console and to inherited
    appenders from com.navtech appenders. Comment out this category if you want output go to 
    log file only or change the priority to "warn" for reduced output on the console -->
<category name="com.navtech.util.framework.WorkflowController">
<priority value="info"/>
</category>
<!-- Write all log events in the root category
      which have a priority higher than info to the stdout appender -->
<root>
<priority value="warn"/>
<appender-ref ref="STDOUT"/>
</root>
</log4j:configuration>
</Workflow>
"""
},
"R2S_NA_611.CFG": {
"executable": False,
"content": r""";#################################################################################
;R2S generic 
;#################################################################################
 
;-------------------------------------------------------------------------------
; R2S_RDF_AREA = <The area covered by the RDF schema>
; Insert only one of the supported areas: NA EU AUNZ MEA CHN INDIA SA KOR
; Example: R2S_RDF_AREA = AUNZ
;
; Supported areas:
; NA - United States, Canada, Mexico
; EU - Europe
; AUNZ - Australia and New Zealand
; MEA - Middle East and Africa
; CHN - China and Hong Kong/Macau (product via NAV2)
; INDIA - India
; SA - Central and South America
; KOR - South Korea
R2S_RDF_AREA = NA
;-------------------------------------------------------------------------------
;-------------------------------------------------------------------------------
; R2S_RUN_RDF_CHECK = <yes/no>
; Set to yes if you want to run RDF CHECK
R2S_RUN_RDF_CHECK=yes
;-------------------------------------------------------------------------------
 
;-------------------------------------------------------------------------------
; R2S_RUN_PART1 = <yes/no>
; Set to yes if you want to run R2S part 1 (preselection step) 
R2S_RUN_PART1=yes
;-------------------------------------------------------------------------------
 
;-------------------------------------------------------------------------------
; R2S_RUN_PART2 = <yes/no>
; Set to yes if you want to run R2S part 2 (SVF population) 
R2S_RUN_PART2=yes
;-------------------------------------------------------------------------------
 
;-------------------------------------------------------------------------------
; R2S_RDF_OLD_DB_USER=<RDF db user>
; Username to be used for RDF-CHECK comparison
;-------------------------------------------------------------------------------
R2S_RDF_OLD_DB_USER = RDF_NA_510
 
;-------------------------------------------------------------------------------
; R2S_RDF_OLD_DB_PASSWORD=<RDF db password>
; Password for the above user (RDF-CHECK)
;-------------------------------------------------------------------------------
R2S_RDF_OLD_DB_PASSWORD = nt#r2g2nsB
 
;-------------------------------------------------------------------------------
; R2S_RDF_OLD_DB_SERVICE=<DB service>
; DB service for the above user (RDF-CHECK)
;-------------------------------------------------------------------------------
R2S_RDF_OLD_DB_SERVICE = lizard1
 
;-------------------------------------------------------------------------------
; R2S_LOG_DIR=<log dir where to store the log files>
; Represents the relative path to current directory
R2S_LOG_DIR=log
;-------------------------------------------------------------------------------
 
;-------------------------------------------------------------------------------
; R2S_SCRIPTS=<path to R2S sources>
; Represents absolute path to R2S sources
; R2S_SCRIPTS = /vobs/gdfConvert/svf/RDF2SVF
R2S_SCRIPTS =/PROJ/db4/db/RDF/NA/2026Q1_SeSp/2025R4_RDF_North_America_251H0/611/Scripts/compiler/gdfConvert/svf/RDF2SVF
 
;-------------------------------------------------------------------------------
 
;-------------------------------------------------------------------------------
; R2S_COMMON_SCRIPTS=<path to common scripts>
; Represents absolute path to common scripts
; R2S_COMMON_SCRIPTS=/vobs/gdfConvert/scripts
R2S_COMMON_SCRIPTS=/PROJ/db4/db/RDF/NA/2026Q1_SeSp/2025R4_RDF_North_America_251H0/611/Scripts/compiler/gdfConvert/scripts
;-------------------------------------------------------------------------------
 
;-------------------------------------------------------------------------------
; R2S_DATAMODEL_SCRIPTS=<path to common scripts>
; Represents absolute path to common scripts
; R2S_DATAMODEL_SCRIPTS=/vobs/gdfConvert/svf/data_model
R2S_DATAMODEL_SCRIPTS=/PROJ/db4/db/RDF/NA/2026Q1_SeSp/2025R4_RDF_North_America_251H0/611/Scripts/compiler/gdfConvert/svf/data_model
;-------------------------------------------------------------------------------
 
;-------------------------------------------------------------------------------
; R2S_RDF_DB_USER=<RDF db user>
R2S_RDF_DB_USER = RDF_NA_611
;-------------------------------------------------------------------------------
 
;-------------------------------------------------------------------------------
; R2S_RDF_DB_PASSWORD=<RDF db password>
R2S_RDF_DB_PASSWORD = nt#r2g2nsB
;-------------------------------------------------------------------------------
 
;-------------------------------------------------------------------------------
; R2S_RDF_DB_SERVICE=<DB service>
R2S_RDF_DB_SERVICE = lizard1
;-------------------------------------------------------------------------------
 
;-------------------------------------------------------------------------------
; R2S_STOP_ON_ERRORS = <yes/no>
; Set to yes if you want to stop R2S on first error occured
; Not recommended to be set to yes.
R2S_STOP_ON_ERRORS = no
;-------------------------------------------------------------------------------
 
;#################################################################################
;R2S Part 1
;#################################################################################
;
;-------------------------------------------------------------------------------
; R2SP1_DROP_TMP_TABLES=<yes/no>
; It is for debugging purposes. Recommanded to be left to yes for official productions
R2SP1_DROP_TMP_TABLES = no
 
;-------------------------------------------------------------------------------
; R2S_LOAD_BUA = <yes/no>
; Set to yes if you want to load the builtup areas for USA into RDF_NA_xxx
R2S_BUA_LOAD = no
;-------------------------------------------------------------------------------
 
;-------------------------------------------------------------------------------
; R2S_BUA_PATH = <path to shape files of USA builtup areas>
; Represents absolute path to shape files of the USA builtup areas
R2S_BUA_PATH =
 
R2S_BUA_FILE =
 
;-------------------------------------------------------------------------------
;
;#################################################################################
;R2S Part 2
;#################################################################################
;-------------------------------------------------------------------------------
; R2SP2_DB_ADMIN_USER=<RDF admin db user>
R2SP2_DB_ADMIN_USER=atadmin
;-------------------------------------------------------------------------------
 
;-------------------------------------------------------------------------------
; R2SP2_DB_ADMIN_PASSW=<RDF admin db password>
R2SP2_DB_ADMIN_PASSW=At1dm3nS
;-------------------------------------------------------------------------------
 
;-------------------------------------------------------------------------------
; R2SP2_PARALLEL=<number of threads for running R2S part 2 in parallel>
R2SP2_PARALLEL=3
;-------------------------------------------------------------------------------
 
;-------------------------------------------------------------------------------
; R2SP2_DROP_TMP_TABLES=<yes/no>
; It is for debugging purposes. Recommanded to be left to yes for official productions
R2SP2_DROP_TMP_TABLES = no   
;-------------------------------------------------------------------------------
 
;-------------------------------------------------------------------------------
; R2SP2_STOP_IF_SVF_USERS_EXIST=<yes/no>
; It is for debugging purposes. If set to yes, it will stop R2S in case SVF users already exists
R2SP2_STOP_IF_SVF_USERS_EXIST = no 
;-------------------------------------------------------------------------------
 
;-------------------------------------------------------------------------------
; R2SP2_TO_RUN=<list of regions for which to run R2S part 2>
; Each region should be defined below in the REGIONS DEFINITIONS sections
R2SP2_TO_RUN= DCA1 DCA2 DCA3 DCA4 DCA5 DCA6 DCA7 DCA8 DCA9 DCA10 DCA11 DCA12 DCA13 DCA14 MEX DCA15
#R2SP2_TO_RUN= DCA2 DCA3 DCA4 DCA5 DCA8 DCA9 DCA11 DCA13 DCA14 MEX 
#R2SP2_TO_RUN= DCA1 DCA6 DCA7 DCA10 DCA12 DCA15
;-------------------------------------------------------------------------------
 
;-------------------------------------------------------------------------------
; <REGION_CODE> = <SVF_USER_NAME> <SVF_PASSWORD> <REGION_ID> <LONG_HOUL>
; All region codes from R2SP2_TO_RUN should be defined in this section.
DCA1=SVF_DCA1_611 nt#r2g2nsB 921 0 lizard1
DCA6=SVF_DCA6_611 nt#r2g2nsB 926 0 lizard1
DCA7=SVF_DCA7_611 nt#r2g2nsB 927 0 lizard1
DCA10=SVF_DCA10_611 nt#r2g2nsB 930 0 lizard1
DCA12=SVF_DCA12_611 nt#r2g2nsB 932 0 lizard1
DCA15=SVF_DCA15_611 nt#r2g2nsB 935 0 lizard1
DCA2=SVF_DCA2_611 nt#r2g2nsB 922 0 lizard1
DCA3=SVF_DCA3_611 nt#r2g2nsB 923 0 lizard1
DCA4=SVF_DCA4_611 nt#r2g2nsB 924 0 lizard1
DCA5=SVF_DCA5_611 nt#r2g2nsB 925 0 lizard1
DCA8=SVF_DCA8_611 nt#r2g2nsB 928 0 lizard1
DCA9=SVF_DCA9_611 nt#r2g2nsB 929 0 lizard1
DCA11=SVF_DCA11_611 nt#r2g2nsB 931 0 lizard1
DCA13=SVF_DCA13_611 nt#r2g2nsB 933 0 lizard1
DCA14=SVF_DCA14_611 nt#r2g2nsB 934 0 lizard1
MEX=SVF_MEX_611 nt#r2g2nsB 484 0 lizard1
 
 
;-------------------------------------------------------------------------------
 
;-------------------------------------------------------------------------------
; REGION CODES FOR ALL SUPPORTED AREAS (to be used in R2SP2_TO_RUN):
; The mapping between REGION_ID and REGION_CODE can be found in RDF2SVF/cfg/regions-definitions.csv
; Note: leave the section commented
 
; Region codes for NA   : DCA1 DCA2 DCA3 DCA4 DCA5 DCA6 DCA7 DCA8 DCA9 DCA10 DCA11 DCA12 DCA13 DCA14 MEX
; Region codes for AUNZ : AU NZ
; Region codes for EU   : ACHM ACH ALM AL BAM BA BGM BG BLRM BLR BNLM BNL CSM CS CZM CZ DNKM DNK ELLM ELL FALLM FALL FINM FIN G1 G2M G3M G4 G4M G5M G6 G7M G8M GALLM GALL GRM GR HRM HR HUM HU I1 I2M I3M I4 I5M IM I MDM MD MKM MK NORM NOR PLM PL ROM RO RUM RU SCM SC SIM SI SKM SK SPM SP SWEM SWE TRM TR UKM UK UKRM UKR
; Region codes for MEA  : AE AR BH JO KU OM QA LB BW LS SZ ZA NAM MA RE
; Region codes for CHN  : CHN
; Region codes for SA   : BRA ARG VEN CHL
; Region codes for KOR  : KOR
;-------------------------------------------------------------------------------
 
 
;------------------------------------------------------------------
; Metadata for updating SVF_METADATA at run time
;------------------------------------------------------------------
 
;-------------------------------------------------------------------------------
; R2S_META_SVF_SPEC_VER=<SVF version specification>
R2S_META_SVF_SPEC_VER=3.20
;-------------------------------------------------------------------------------
 
;-------------------------------------------------------------------------------
; R2S_META_RELEASE_VER=<The label version of R2S used>
R2S_META_RELEASE_VER=R2S_1.17.2_RC2
;-------------------------------------------------------------------------------
 
;-------------------------------------------------------------------------------
; R2S_META_RELEASE_DATE=<The release date of the R2S label used. Date format: DDMMYY>
R2S_META_RELEASE_DATE=100226
;-------------------------------------------------------------------------------
 
;-------------------------------------------------------------------------------
; R2S_META_COMPATIBILITY=<RDF Data set compatibility>
R2S_META_COMPATIBILITY=2025R4
;-------------------------------------------------------------------------------
"""
},
"log_checker.pl": {
"executable": True,
"content": r"""#!/usr/bin/perl -w
 
=comment
06.05.2013 Andrei Carp
 
To do:
add more bad/good errrors to the bellow arrays
sort values in arrays to see them better
make sure that good types of error don't hide real bad errors
 
=cut
# use strict;
use warnings;
use Cwd;
use Cwd 'abs_path';
use File::Basename;
# use lib dirname(abs_path($0)).'/../perl/Tools/ExtraPERLModules/linux';
use lib dirname(abs_path($0)); use List::MoreUtils qw(uniq);
 
my @bad_types = ("^ORA-","SP2-","error","NoClassDefFoundError","Command not found","segmentation fault","Can not open","Can not initialize","assertion failed","contains 0 POI categories",
"sorry","cannot access","cannot access","not found in translation file","segment has no name","Fail to initialize","Retrieved 0 POI","No such file or directory","can't find or read input file",
"Stale NFS file handle","no match","text file busy","cannot create");
 
my @good_types = ("_error_","ErrorNum","no error","no  error","No error(s)","ErrorHandling","ORA-03292: Table to be","Checking Error Log","automatically placed in the error file","check_error",
"-fno-exceptions","arm_nr_exception_","exception segment","exception info","exceptions","_tmcp_chain_exception","XGetErrorDatabaseText","XGetErrorText","show errors","VALUE_ERROR",
"Will check log files for errors","Checking for new Errors","Checking for PEL and GPX errors","Checking tfumerge.master log file for errors","- Will check log files for errors");
 
# my @good_types1 = ("files for errors.","warning");
# my @good_types = ("error",",ERROR,","No error(s)","Check for errors","warning");
my $print_equal = "=" x 100;
my $print_line = "-" x 100;
 
# display the number of arguments provided
# my $numArgs = @ARGV;
my $numArgs = $#ARGV + 1;
print "\nThanks, you gave me $numArgs command-line arguments.\n\n";
# display the arguments
foreach my $arg (@ARGV) {
    print $arg, "\n";
}
print "\n\n";
# if no argument provided scan the current folder for .log files
my $cwd = getcwd();
my $log;
if ($numArgs  == 0) {
    opendir LOGS, $cwd or die "Directory error: $!\n";
    my @files = grep /\.log$/, readdir LOGS;
    closedir LOGS;
    for $log (@files) {
        porcess_file ($log); # process each .log file
    }
} elsif ($numArgs >= 1) {
    for $log (@ARGV) {
        porcess_file ($log); # process each .log file
    }
    # porcess_file ($ARGV[0]);
} else {
    print "\tusage:\t$0 <logfile(s)>\n\teg:\t$0 /path/to/logfile.log OR $0 /path/to/logfiles/*.log\n\n";
    exit;
}
 
 
sub porcess_file {
    my $logfile = $_[0];
    my $type;
    my $line;
    my @bad_errors = ();
    my @good_errors = ();
    my @bad_errors_u = ();
    my @good_errors_u = ();
    my $result;
 
    open(LOGFILE,$logfile) or die("Could not open log file: $!\n");
        foreach $line (<LOGFILE>) {
            foreach $type (@bad_types) {
                if ($line =~ /$type/) { 
                    # print "[$type]\t$logfile\n$line\n\n";
                    push(@bad_errors, $line);
                }
            }
            foreach $type (@good_types) {
                if ($line =~ /$type/) { 
                    # print "[$type]\t$logfile\n$line\n\n";
                    push(@good_errors, $line);
                }
            }
        }
    close(LOGFILE) or die $!;
    $result = $#bad_errors-$#good_errors;
    if ($result > 0) {
        print "[NOK]\t$logfile\n";
        print "\t(".($#bad_errors+1)." - ".($#good_errors+1)." = ".$result.")\n";
                 @bad_errors_u = uniq(@bad_errors);
        @good_errors_u = uniq(@good_errors);
        if ($#bad_errors+1 >= 1) {
        print_header ("BAD ERRORS");
        print join("", @bad_errors_u);
        }
        if ($#good_errors+1 >= 1) {
        print_header ("GOOD ERRORS");
        print join("", @good_errors_u);
        }
    print "$print_equal\n";
    } else {
        print "[ OK]\t$logfile\n";
    }
}
     sub print_header {
    my($headear) = @_;
    my $h_lenght = length($headear);
    my $h_start = ((100-$h_lenght)/2);
    print "$print_line\n";
    if ($h_start % 2 == 1) {
    # $number is odd
        print " " x $h_start,$headear," " x $h_start,"\n";
    } else {
    # $number is even
    print " " x (int($h_start + 0.5)-1),$headear," " x ($h_start+1),"\n";
    }
    print "$print_line\n";
}
 
 
__END__
"""
},
"LOAD_NA_611.CSH": {
"executable": True,
"content": r"""#!/bin/csh
 
echo $0 \[$$\]
 
if ( $?STY ) then
	echo "Screen: $STY"
endif
if ( $?CLEARCASE_ROOT ) then
	echo "View: $CLEARCASE_ROOT"
	set spec_view = `echo $CLEARCASE_ROOT | cut -d'/' -f3`
	echo ===================================================================================
	echo "Using a dynamic codebase..."
	cleartool setview -exec 'ct catcs' ${spec_view}
	echo ===================================================================================
endif
 
echo `uname -a`
echo `cat /etc/redhat-release`
echo $USER $HOST
 
set TIMESTAMP=`date +%Y%b%d_%Hh%Mm%Ss`
 
######## ADAPT the cfg file 
set SOURCE_CFG=LOAD_CFG_NA.cfg
source ./$SOURCE_CFG
echo RDF home directory is: $RDF_HOME
echo SCRIPTS home directory is: $SCRIPTS_HOME
 
#===================================================================================================
set LOGS_DIR=log
 
 
if ( -d $LOGS_DIR) then
	mv -v $LOGS_DIR $LOGS_DIR\_${TIMESTAMP}
	mkdir -p $LOGS_DIR
else
	mkdir -p $LOGS_DIR
endif
 
cat $SOURCE_CFG > $LOGS_DIR/${TIMESTAMP}_${SOURCE_CFG}
#########################################
##### CREATE STATIC COMPILER		START SECTION ######
 
source ./$SOURCE_CFG
 
if ($COPY_R2S_COMPILER == "1") then
echo -----------------------------------------------------------------------------------------------
echo `date`: Starting STEP copy R2S COMPILER ...
echo -----------------------------------------------------------------------------------------------
 
git clone ssh://$UID@buic-scm-ias.automotive-wan.com:29418/MAPS/R2S/compiler -b $BRANCH_NAME --single-branch && scp -p -P 29418 $UID@buic-scm-ias.automotive-wan.com:hooks/commit-msg compiler/.git/hooks/
 
mkdir -p $SCRIPTS_HOME/ut
cd $SCRIPTS_HOME/ut
git clone ssh://$UID@buic-scm-ias.automotive-wan.com:29418/MAPS/UTSQL/compiler -b $BRANCH_NAME_UT --single-branch && scp -p -P 29418 $UID@buic-scm-ias.automotive-wan.com:hooks/commit-msg compiler/.git/hooks/
 
mv $SCRIPTS_HOME/ut/compiler/gdfConvert/util $SCRIPTS_HOME/compiler/gdfConvert/
cd $SCRIPTS_HOME
rm -r -f ut
tree -L 2 -d compiler/
 
echo -----------------------------------------------------------------------------------------------
echo `date`: Starting STEP copy R2S COMPILER done
echo -----------------------------------------------------------------------------------------------
endif
 
##### CREATE STATIC COMPILER		END SECTION ##################
 
################################################################################################
 
######### BACKUP LOG DIRECTORY    START SECTION#############################
 
 
source ./$SOURCE_CFG
 
if ($COPY_DATA == "1") then
echo ===============================================================================================
echo `date`: Part I -- Prepare all files for Load
echo ===============================================================================================
echo -----------------------------------------------------------------------------------
echo  `date`: Folder structure and scripts
echo -----------------------------------------------------------------------------------
 
cd $RDF_HOME
mkdir -p load
cd load
cp -v $ARCHIVE_CORE_DATA/*.* .
cp -v $ARCHIVE_SLOPE_DATA/*.* .
cd $SCRIPTS_HOME				
echo -----------------------------------------------------------------------------------
echo  `date`: Folder structure and scripts done
echo -----------------------------------------------------------------------------------
endif
 
##### COPY DATA		END SECTION ######
 
############################################################################################
 
##### EXTRACT TO LOAD	(UNTAR UNZIP)	START SECTION ######
 
source ./$SOURCE_CFG
 
if ($EXTRACT_2_LOAD == "1") then
echo -----------------------------------------------------------------------------------
echo  `date`: Start extract to load
echo -----------------------------------------------------------------------------------
 
perl $SCRIPTS_HOME/extract_2_load.pl $SCRIPTS_HOME/../../load |& tee $SCRIPTS_HOME/$LOGS_DIR/extract_2_load.log
./errorCheck.csh $SCRIPTS_HOME/$LOGS_DIR/extract_2_load.log
 
echo -----------------------------------------------------------------------------------
echo  `date`: Extract to load finished
echo -----------------------------------------------------------------------------------
cd $SCRIPTS_HOME
 
echo "Subject: $RDF_AREA $DSUFIX EXTRACT TO LOAD finished..." | sendmail $MY_EMAIL
 
echo Pause 1 minute...
sleep 60
endif
 
##### EXTRACT TO LOAD		END SECTION ######
 
####################################################################################################
 
source ./$SOURCE_CFG
 
if ($GREP_MD5 == "1") then
echo -----------------------------------------------------------------------------------
echo  `date`: grep md5 files
echo -----------------------------------------------------------------------------------
 
cd $RDF_HOME/load
find . -name 'MD5result.log' -exec grep -iE 'NOK|ORA-|SP2-|ERROR' {} \; > md5error.log
 
set error=`wc -l < md5error.log`
echo count is $error
 
if($error != 0) then 
	echo "ERROR: Errors found" 
	exit 1
else
	echo "Successfully: No errors found"
endif
 
echo -----------------------------------------------------------------------------------
echo  `date`: grep md5 files finished
echo -----------------------------------------------------------------------------------
cd $SCRIPTS_HOME
endif
 
############################################################################################
 
source ./$SOURCE_CFG
 
if ($REN_RDF_CUS_SOFT == "1") then
echo -----------------------------------------------------------------------------------
echo  `date`: rename rdf_customer_software file
echo -----------------------------------------------------------------------------------
 
cd $RDF_HOME/load
# check if rdfdeploy already exists
if ( -d rdfdeploy ) then
	rm -rf rdfdeploy
	echo Old rdfdeploy folder was found and removed for new one ...
else
	echo Renaming rdf_customer_software to rdfdeploy started ...
endif
find . -depth -type d -name '*rdf_customer_software' -exec mv {} rdfdeploy \;
 
echo -----------------------------------------------------------------------------------
echo  `date`: rename rdf_customer_software file finished
echo -----------------------------------------------------------------------------------
cd $SCRIPTS_HOME
endif
 
############################################################################################
 
source ./$SOURCE_CFG
 
if ($CP_MV_ALLFILES == "1") then
echo -----------------------------------------------------------------------------------
echo  `date`: copy allfiles to loaderfiles
echo -----------------------------------------------------------------------------------
 
###rdfcore distance_markers adm midpoint ng point_address sc sdo traffic vng voice vul wkt
 
cd $RDF_HOME/load
 
mkdir -p $RDF_TOOL/RDF/LOADER_FILES/CORE/
mkdir -p $RDF_TOOL/RDF/LOADER_FILES/ADAS/
### mkdir -p $RDF_TOOL/RDF/LOADER_FILES/WKT/
### mkdir -p $RDF_TOOL/RDF/LOADER_FILES/SDO/
 
cp -r *CORE*/CORE/*.* $RDF_TOOL/RDF/LOADER_FILES/CORE/
cp -r *ADAS*/ADAS/*.* $RDF_TOOL/RDF/LOADER_FILES/ADAS/
### cp -r *WKT*/WKT/*.* $RDF_TOOL/RDF/LOADER_FILES/WKT/
### cp -r *SDO*/SDO/*.* $RDF_TOOL/RDF/LOADER_FILES/SDO/
 
echo -----------------------------------------------------------------------------------
echo  `date`: copy allfiles to loaderfiles finished
echo -----------------------------------------------------------------------------------
 
echo -----------------------------------------------------------------------------------
echo  `date`: move allfiles to allfiles
echo -----------------------------------------------------------------------------------
 
cd $RDF_HOME/load
mkdir -p allfiles
 
foreach i (`ls $RDF_HOME/load | grep -vw "allfiles" | grep -vw "rdfdeploy" | grep -vw "."`)
foreach i (`ls $RDF_HOME/load | grep -vw "allfiles" | grep -vw "rdfdeploy" | grep -vE '^\.{1,2}'`)
mv -v $RDF_HOME/load/$i $RDF_HOME/load/allfiles/
end
 
echo -----------------------------------------------------------------------------------
echo  `date`: move allfiles to allfiles finished
echo -----------------------------------------------------------------------------------
echo "Subject: $RDF_AREA $DSUFIX Prepare RDF & Load finished..." | sendmail $MY_EMAIL
cd $SCRIPTS_HOME
endif
 
############################################################################################
 
##### CLEAN USERS		START SECTION ######
 
source ./$SOURCE_CFG
 
if ($CLEAN_USERS == "1") then
echo -----------------------------------------------------------------------------------
echo  `date`: Clean previous users ...
echo -----------------------------------------------------------------------------------
 
cd $SCRIPTS_HOME
sqlplus atadmin/At1dm3nS@lizard1 @drop_users.sql >& drop_users.log
./errorCheck.csh $SCRIPTS_HOME/drop_users.log
 
echo -----------------------------------------------------------------------------------
echo  `date`: Clean previous users finished
echo -----------------------------------------------------------------------------------
cd $SCRIPTS_HOME
echo Pause 1 minute...
sleep 60
endif
 
##### CLEAN USERS		END SECTION ######
 
##############################################################
 
##### RDF		START SECTION ######
 
cd $SCRIPTS_HOME
source ./$SOURCE_CFG
 
if ($START_RDF == "1") then
echo ===============================================================================================
echo `date`: START_RDF
echo ===============================================================================================
 
echo -----------------------------------------------------------------------------------
echo  Create user $RDF_USER
echo -----------------------------------------------------------------------------------
 
cd $SCRIPTS_HOME
$RDF_COMPILER/gdfConvert/scripts/create_oracle_user.csh atadmin At1dm3nS $RDF_USER $PASSWORD $SERVER |& tee $SCRIPTS_HOME/$LOGS_DIR/create_user_$RDF_USER.log
./errorCheck.csh $SCRIPTS_HOME/$LOGS_DIR/create_user_$RDF_USER.log
 
echo -----------------------------------------------------------------------------------
echo Create user $RDF_USER done
echo -----------------------------------------------------------------------------------
cd $SCRIPTS_HOME
echo "Subject: `date` $RDF_AREA $DSUFIX RDF_USER done..." | sendmail $MY_EMAIL
 
echo -----------------------------------------------------------------------------------
echo Create 775 rights
echo -----------------------------------------------------------------------------------
 
chmod 775 $SCRIPTS_HOME/$CFG_XML
chmod 775 $RDF_TOOL/RDF/rdf_installer.*
chmod -R 775 $RDF_TOOL/RDF/LOADER_FILES
chmod -R 775 $RDF_HOME/load
 
echo -----------------------------------------------------------------------------------
echo Create 775 rights done !
echo -----------------------------------------------------------------------------------
 
echo -----------------------------------------------------------------------------------
echo  `date`: LOAD started
echo -----------------------------------------------------------------------------------
 
cp -vf $SCRIPTS_HOME/$CFG_XML $RDF_TOOL/RDF/BIN/etc/xml/$CFG_XML
 
cd $RDF_TOOL/RDF
##### mv -fv ${RDF_USER}.LOG ${RDF_NA}_$$.LOG	
 
										  
./rdf_installer.sh $RDF_BIN/etc/xml/$CFG_XML loadrdfCore |& tee $SCRIPTS_HOME/$LOGS_DIR/$RDF_USER.loadrdfCore.log
 
cd $SCRIPTS_HOME
 
source ./$SOURCE_CFG
 
########## CHECK IF THE ADAS DIRECTORY EXISTS #########################
set dir=$ADAS_DIR
set c=0
# make sure $dir exits 
if ( -d ${dir} ) then
    set c=`ls -a ${dir} | wc | awk '{print $1}'`
   # IS dir is empty
    if ( "${c}" == 2 ) then
		echo "Empty directory - "${dir}
    else 	#dir has files
		echo "Dir has files - "${dir}
		############ IF THE ADAS DIRECTORY EXISTS DO THE FOLLOWING ########
		cd $RDF_TOOL/RDF
		./rdf_installer.sh $RDF_BIN/etc/xml/$CFG_XML loadADAS   |& tee $SCRIPTS_HOME/$LOGS_DIR/$RDF_USER.loadADAS.log
    endif
else
      echo "Error: Not a directory"
endif
##################### END OF ADAS CHECK #########################
 
cd $SCRIPTS_HOME
source ./$SOURCE_CFG
 
cd $RDF_TOOL/RDF
./rdf_installer.sh $RDF_BIN/etc/xml/$CFG_XML PostImportStats   |& tee $SCRIPTS_HOME/$LOGS_DIR/$RDF_USER.PostImportStats.log
 
echo -----------------------------------------------------------------------------------------------
echo ===============================================================================================
echo `date`: CHECK WORKFLOW
echo ===============================================================================================
 
cd $SCRIPTS_HOME
source ./$SOURCE_CFG
echo "Subject: $RDF_AREA $DSUFIX `date` CHECK WORKFLOW..." | sendmail $MY_EMAIL
egrep 'Workflow success.|Workflow FAILED. ' $SCRIPTS_HOME/$LOGS_DIR/*.{load,Post}*.log
 
echo ===============================================================================================
echo `date`: CHECK WORKFLOW FROM ABOVE
echo ===============================================================================================
 
echo ===============================================================================================
echo  `date`: LOAD finished
echo ===============================================================================================
 
echo "Subject: $RDF_AREA $DSUFIX Load finished..." | sendmail $MY_EMAIL
cd $SCRIPTS_HOME
endif
 
##### 	RDF  	END SECTION ######
 
##################################################################################################################
 
#####   R2S		START SECTION ######
 
source ./$SOURCE_CFG
 
if ($START_R2S == "1") then
echo ===============================================================================================
echo `date`: START_R2S
echo ===============================================================================================
echo -----------------------------------------------------------------------------------------------
echo  `date`: R2S started
echo ===============================================================================================
 
cd $SCRIPTS_HOME/$LOGS_DIR
$RDF_COMPILER/gdfConvert/svf/RDF2SVF/bin/r2s.pl $R2S_CFG |& tee $SCRIPTS_HOME/$LOGS_DIR/$RDF_USER.log
$SCRIPTS_HOME/errorCheck.csh $SCRIPTS_HOME/$LOGS_DIR/$RDF_USER.log
 
echo ===============================================================================================
echo  `date`: R2S finished
echo ===============================================================================================
echo "Subject: $RDF_AREA $DSUFIX  R2S finished..." | sendmail $MY_EMAIL
cd $SCRIPTS_HOME
endif
 
##### R2S	END SECTION ######
 
###############################################################################################
 
##### P A T C H E S		START SECTION ######
 
cd $SCRIPTS_HOME
 
source ./$SOURCE_CFG
 
if ($RUN_PATCH == "1") then
echo -----------------------------------------------------------------------------------------------
echo `date`:  Run SVF PATCHES SECTION
echo -----------------------------------------------------------------------------------------------
 
eval $SVF_PATCH_LINE
 
echo -----------------------------------------------------------------------------------------------
echo `date`: Run SVF PATCHES SECTION DONE
echo -----------------------------------------------------------------------------------------------
cd $SCRIPTS_HOME
echo "Subject: $RDF_AREA $DSUFIX SVF PATCHES finished..." | sendmail $MY_EMAIL
endif
 
#### P A T C H E S		END SECTION ######
 
#### RDF_ABAKUS		START SECTION ######
 
source ./$SOURCE_CFG
 
if ($RDF_ABAKUS == "1") then
echo -----------------------------------------------------------------------------------
echo  `date`: Start Abakus on RDF user
echo -----------------------------------------------------------------------------------
 
cd $SCRIPTS_TEST/RDF
AbakusRDF.csh $OSUFIX R0 Y $DSUFIX R1 Y $ABAKUS_PROD results
cd $SCRIPTS_HOME
 
echo -----------------------------------------------------------------------------------
echo  `date`: Abakus on RDF user finished
echo -----------------------------------------------------------------------------------
cd $SCRIPTS_HOME
echo "Subject:RDF_ABAKUS finished..." | sendmail $MY_EMAIL
endif
 
#### RDF_ABAKUS		END SECTION ######
##########################################################################################
#### SVF_ABAKUS		START SECTION ######
 
source ./$SOURCE_CFG
 
if ($SVF_ABAKUS == "1") then
echo -----------------------------------------------------------------------------------
echo  `date`: Start Abakus on SVF users
echo -----------------------------------------------------------------------------------
 
cd $SCRIPTS_TEST/SVF
AbakusSVF.csh $OSUFIX S0 Y $DSUFIX S1 Y $ABAKUS_PROD results
echo -----------------------------------------------------------------------------------
echo  `date`: Abakus on SVF  users finished
echo -----------------------------------------------------------------------------------
 
# echo -----------------------------------------------------------------------------------
# echo  `date`: Start Abakus on SVF MRE users
# echo -----------------------------------------------------------------------------------
 
# cd $SCRIPTS_TEST/SVF_MRE
# AbakusSVF_MRE.csh 710 S0 Y 740 S1 Y eu2017r3 results
 
# echo -----------------------------------------------------------------------------------
# echo  `date`: Abakus on SVF MRE users finished
# echo -----------------------------------------------------------------------------------
cd $SCRIPTS_HOME			
echo "Subject: $RDF_AREA $DSUFIX SVF_ABAKUS finished..." | sendmail $MY_EMAIL
endif
 
#### SVF_ABAKUS		END SECTION ######
###########################################################################################
####  UTSQL		START SECTION ######
 
source ./$SOURCE_CFG
 
if ($START_UTSQL == "1") then
echo -----------------------------------------------------------------------------------
echo  `date`: Start UTSQL
echo -----------------------------------------------------------------------------------
echo -----------------------------------------------------------------------------------
echo UT
echo -----------------------------------------------------------------------------------																						
 
 
cd $SCRIPTS_TEST/UT
runUT $DSUFIX >& runUT_$$.log
 
 
echo -----------------------------------------------------------------------------------
echo UT END
echo -----------------------------------------------------------------------------------
echo  `date`: UTSQL finished
echo -----------------------------------------------------------------------------------
cd $SCRIPTS_HOME
echo "Subject: $RDF_AREA $DSUFIX  UTSQL finished..." | sendmail $MY_EMAIL
endif
 
####  UTSQL		END SECTION ######
#####################################################################################################
####  CALCULATE_SPACE		START SECTION ######
 
source ./$SOURCE_CFG
 
if ($CALCULATE_SPACE == "1") then
echo -----------------------------------------------------------------------------------
echo  `date`: Start calculate space on SVF user
echo -----------------------------------------------------------------------------------
 
cd $SCRIPTS_TEST/SIZE
sqlplus $SP_USER/$SP_PASS@$SP_SERVER @space_calculate.sql $DSUFIX >& space_calculate_${TIMESTAMP}.log
cd $SCRIPTS_HOME
 
echo -----------------------------------------------------------------------------------
echo  `date`: Calculate space on SVF user finished
echo -----------------------------------------------------------------------------------
cd $SCRIPTS_HOME
echo "Subject: $RDF_AREA $DSUFIX CALCULATE_SPACE finished..." | sendmail $MY_EMAIL
endif
####  CALCULATE_SPACE	END SECTION ######
echo "Subject: $RDF_AREA $DSUFIX Tests on R2S & Load finished..." | sendmail $MY_EMAIL
"""
},
"LOAD_CFG_NA.cfg": {
"executable": True,
"content": r"""#!/bin/csh
echo Loading configuration file
##########################################################################
set R2S_VIEW=sesp_na_611
set MY_EMAIL=sergiu-razvan.spatar@aumovio.com
set DSUFIX=611
set OSUFIX=510
set RDF_HOME=/PROJ/db4/db/RDF/NA/2026Q1_SeSp/2025R4_RDF_North_America_251H0/
set SCRIPTS_HOME="$RDF_HOME/$DSUFIX/Scripts"
set SCRIPTS_TEST="$RDF_HOME/$DSUFIX/Tests"
set ARCHIVE_CORE_DATA=/PROJ/db6/DOWNLOAD_Archive/NAVTEQ/Americas/North_America/2025R4_RDF_North_America
set ARCHIVE_SLOPE_DATA=/PROJ/db6/DOWNLOAD_Archive/NAVTEQ/Americas/North_America/2025R4_RDF_North_America_CurveHeightSlope_plugin
set PATCH_DIR="$RDF_HOME/patches"
set ADAS_DIR="$RDF_HOME/load/rdfdeploy/RDF/LOADER_FILES/ADAS"						
set SERVER=dragon1
set PASSWORD=nt\#r2g2nsB										   
set RDF_TOOL="$RDF_HOME/load/rdfdeploy"
set RDF_BIN="$RDF_TOOL/RDF/BIN"
set RDF_COMPILER="$SCRIPTS_HOME/compiler"
###############################################################################################################
#### Adapt the following variables 
set SP_SERVER=dragon1
set SP_USER=atadmin
set SP_PASS=At1dm3nS
set SVF_PATCH_LINE="source $SCRIPTS_HOME/SVF_PATCH.csh"											   
###############################################################################################################
##### Your UID and Branch name of last R2S Compiler version 
set BRANCH_NAME=R2S_1.17.2_RC2
set BRANCH_NAME_UT=UTSQL_2.6_RC3
set UID=uie74356
###############################################################################################################
###### main_area eu is for weu & eeu   and main_area mea is for mea
set MAIN_AREA=na
set RDF_AREA=NA
		### CN = COUNTRY NUMBER
		### PLEASE BE SURE THAT YOU HAVE THE CORRECT COUNTRY NUMBER THAT IS ASSOCIATED TO THE AREA
		### WEU= 20 EEU =30 MEA=99 AUNZ=99 NA=19 
set RDF_CN=19
set RDF_USER="RDF_${RDF_AREA}_${DSUFIX}"
set CFG_XML="RDF_${RDF_AREA}_${DSUFIX}.XML"
set R2S_CFG="$SCRIPTS_HOME/R2S_${RDF_AREA}_${DSUFIX}.CFG"
###############################################################################################################
#####
set COPY_R2S_COMPILER=1
set COPY_DATA=1
set EXTRACT_2_LOAD=1
set REN_RDF_CUS_SOFT=1
set CP_MV_ALLFILES=1
set GREP_MD5=1
set CLEAN_USERS=0
set START_RDF=1
set START_R2S=1
set RUN_PATCH=1
set RDF_ABAKUS=1
set SVF_ABAKUS=1
set START_UTSQL=1
set CALCULATE_SPACE=1
set ABAKUS_PROD=na2026q1
#################### PATCH --> SVF USER LIST - PATCH
###########################
"""
},
"extract_2_load.pl": {
"executable": True,
"content": r"""#!/usr/bin/perl -w
 
####################################################################################################
#  Script     : extract_2_load.pl
#  Author     : Andrei Carp
#  Date       : 07/19/2015
#  Last Edited: 08/20/2015, uidn3623
#  Description: extract recursively tar and gz archives
####################################################################################################
 
# perl extract_2_load.pl /PROJ/db4/db/DEVELOPMENT/ANCA/extract/test | & tee extract.log
 
use strict;
use Cwd;
use File::Copy;
use Data::Dumper;
use File::Find;
# no warnings 'File::Find';
use File::Basename;
 
my $delete_archives=0; #delete or not archives after untar
 
my $num_args = $#ARGV + 1;
if ($num_args != 1) {
	print "\nUsage: $0 [directory]\n";
	exit;
}
 
my $g_start_time = time();
my $echo_minus = '-' x 83;
my $echo_equal = '=' x 83;
 
my $directory = $ARGV[0];
my @array_files=();
 
#---------------------------------------------------------------------------------------------------
print "\n";
print "$echo_equal\n";
&check_tool("tar");
&check_tool("gzip");
print "$echo_equal\n";
 
find(\&do_something_with_file, $directory);
@array_files = map { $_->[0] } sort { $a->[1] <=> $b->[1] } map { [ $_, !/\.tar$/ ] } @array_files;
 
while(my $archive = shift(@array_files)) {
&do_extract ($archive);
	# 
	# open my $fh, '>>', 'extract_filelist.log' or die "Cannot open output file: $!";
	# print Dumper(\@array_files);
	# close $fh;
}
 
print "\n";
print "$echo_equal\n";
my $g_end_time     = time();
my $g_elapsed_time = sprintf( "%d", $g_end_time - $g_start_time );
print "START TIME         : ". localtime($g_start_time) . "\n";
print "END TIME           : ". localtime($g_end_time) . "\n";
print "TOTAL ELAPSED TIME : ". &secondsToReadableTime($g_elapsed_time) . "\n";
print "$echo_equal\n";
print "\n";
 
#---------------------------------------------------------------------------------------------------
sub do_something_with_file {
	# $File::Find::dir  = /some/path/
	# $_                = foo.ext
	# $File::Find::name = /some/path/foo.ext
	# $File::Find::fullname
	my $file = $_;
 
	return unless (-f $file);  
	return unless ($file =~ /\.tar$/) or ($file =~ /\.gz$/);
	# print($file." [".$File::Find::name."]\n");
	push @array_files, $File::Find::name;
}
 
sub do_extract {
	my $i_file = $_[0];
	my($filename, $dirs, $suffix) = fileparse($i_file, qr/\.[^.]*/);
	chdir $dirs or die "Can't chdir into path: $dirs";
	print "[DEBUG EXTRACT]\tChecking file $i_file\n"; 
	for ($suffix) {
		if (/tar/) {
			mkdir $filename, 0775 or die "Warning: Cannot make ".$filename." directory: $!\n" if(!-d $filename);
			chdir $filename or die "Can't chdir into path: $filename";
			print "[INFO]\tExtracting .tar archive: $filename$suffix\n";
			if ($delete_archives) {
				system "tar -xvf $i_file && rm $i_file";
			} else {
				system "tar -xvf $i_file";
			}
			find(\&do_something_with_md5, $dirs.$filename);
			# print "[INFO]\tRescan after .tar [$dirs$filename]\n"; 
			find(\&do_something_with_file, $dirs.$filename);
		} elsif (/gz/) {
			print "[INFO]\tExtracting .gz archive: $filename$suffix\n";
			system "gzip -dfv $i_file";
			# print "[INFO]\tRescan after .gz [$dirs$filename]\n"; 
			find(\&do_something_with_file, $dirs.$filename);
		}
		else { 
			print "[WARN]\tFind unexpected file extension, please check: $filename$suffix\n";
		}
	}
}
 
sub check_tool {
	my $i_toolname = $_[0];
	my $tool_path = '';
	for my $path ( split /:/, $ENV{PATH} ) {
		if ( -f "$path/$i_toolname" && -x _ ) {
			print "$i_toolname found in $path\n";
			$tool_path = "$path/$i_toolname";
			last;
		}
	}
	die "No $i_toolname command available\n" unless ( $tool_path );
}
 
sub do_something_with_md5 {
	# $File::Find::dir  = /some/path/
	# $_                = foo.ext
	# $File::Find::name = /some/path/foo.ext
	# $File::Find::fullname
 
	my $file = $_;
	my $t_md5log = "MD5result.log";
	my $t_counter = 0;
 
	return unless (-f $file);  
	return unless ($file =~ /MD5loaderfiles.txt$/) or ($file =~ /md5software.txt$/);
	# print($file." [".$File::Find::name."]\n");
&prepare_md5($File::Find::name);
	print "[INFO MD5]\tMD5 check against $file\n";
	chdir ($File::Find::dir) or die ("Could not change directory: $!\n");
	if (-e $file) {
		print "[DEBUG MD5]\tChecking file $file\n";
		my $runCmd="/usr/bin/md5sum -c $file > $t_md5log";
		my $t_exit_code=system($runCmd);
 
		if($t_exit_code!=0)
		{
		  print "[WARN]\tCommand $runCmd failed with an exit code of $t_exit_code.\n";
		  exit($t_exit_code >> 8);
		}
		else
		{ }
	} else {
		print "[ERROR]\tFile does not exist! $file\n";
	}
	# system "/usr/bin/md5sum -c ".$file." > ".$t_md5log;
	print "[INFO MD5]\tCheck $t_md5log\n";
	my @lines=();
	open (MD5CHK, $t_md5log) or die ("Could not open file: $!");
	@lines = <MD5CHK>;
	foreach my $line (@lines){
		if ($line =~ /\: FAILED/) {
			print "ERROR EXTRACTING $line\n";
			$t_counter++;
		}
	}
	close (MD5CHK);
	die "[INFO MD5]\tCheck found $t_counter errors\n" if ($t_counter > 0);
}
 
sub prepare_md5 {
	my $i_md5file = $_[0];
	my $t_md5file = $i_md5file."tmp";
	print "[INFO MD5]\tPrepare $i_md5file\n";
	copy ($i_md5file,$i_md5file.".org") or die ("Could not copy file: $!");
	my @data=();
	open (MD5IN, $i_md5file);
	@data = <MD5IN>;
	foreach my $line (@data) {
		$line =~ s/^;.+$//g;			# ; -> nothing ; delete comments lines
		$line =~ s/\\/\//g;			# \ -> /
		# $line =~ s/\*/\*\.\//;		# * -> *./
		$line =~ s/\*//;		# * -> nothing
		$line =~ s/\*([A-Z]|[a-z])/\*\.\/$1/;		# *R -> *./R
		$line =~ s/\r\n|\n|\r/\n/g;	# end of lines
		open (MD5OUT, '>>'.$t_md5file) or die ("Could not open file: $!");
			print MD5OUT "$line";
		next;
	}
	close (MD5OUT);
	close (MD5IN);
	move ($t_md5file,$i_md5file) or die ("Could not move file: $!");
}
 
sub secondsToReadableTime () {
	my $totalSecondsTmp = shift();
	my $hoursTmp = int($totalSecondsTmp/(60*60));
	my $minsTmp = int($totalSecondsTmp/60)%60;
	my $secondsTmp = int($totalSecondsTmp)%60;
	return "$hoursTmp hours, $minsTmp minutes, $secondsTmp seconds "
}
#---------------------------------------------------------------------------------------------------
 
exit 0;
"""
},
"errorCheck.csh": {
"executable": True,
"content": r"""#!/bin/csh -f
 
# v1.01     20.02.2013
 
if ( $#argv < 1 ) then 
  echo
  echo Usage: $0 log_file_name
  echo
  exit 2;
endif
 
while ( $#argv >= 1 )
  set C_LOGFILE=$1
  shift
  # for new strings, need to be added in two places !
  #-------------------------------------------------------------------------------------------------
  # ERRORS
  #-------------------------------------------------------------------------------------------------
  set c_num_err = `egrep -i -c "(^ORA-|SP2-|error|NoClassDefFoundError|Command not found|segmentation fault|Can not open|Can't open|Can not initialize|assertion failed|contains 0 POI categories|sorry|cannot access|not found in translation file|segment has no name|Fail to initialize|Retrieved 0 POI|No such file or directory|can't find or read input file|Stale NFS file handle|no match|text file busy|set: |Can't|tcsh current memory allocation|not a valid|not completed successfully|uninitialized|permission denied|hangup|You do not have|Undefined variable)" $C_LOGFILE`
  set t_err=`mktemp -t errorCheck_err.XXXXXX` || exit 1
  egrep -i "(^ORA-|SP2-|error|NoClassDefFoundError|Command not found|segmentation fault|Can not open|Can't open|Can not initialize|assertion failed|contains 0 POI categories|sorry|cannot access|not found in translation file|segment has no name|Fail to initialize|Retrieved 0 POI|No such file or directory|can't find or read input file|Stale NFS file handle|no match|text file busy|set: |Can't|tcsh current memory allocation|not a valid|not completed successfully|uninitialized|permission denied|hangup|You do not have|Undefined variable)" $C_LOGFILE | sort -du > $t_err
  #-------------------------------------------------------------------------------------------------
  set c_no_err = `egrep -i -c "(_error_|ErrorNum|no error|no  error|ErrorHandling|ORA-03292: Table to be|Checking Error Log|automatically placed in the error file|check_error|-fno-exceptions|arm_nr_exception_|exception segment|exception info|exceptions|_tmcp_chain_exception|XGetErrorDatabaseText|XGetErrorText|show errors|VALUE_ERROR|Will check log files for errors|Checking for new Errors|Checking for PEL and GPX errors|Checking tfumerge.master log file for errors|- Will check log files for errors|Checking for Feature File errors|checking for errors|R2S_STOP_ON_ERRORS)" $C_LOGFILE`
  set t_no_err=`mktemp -t errorCheck_no_err.XXXXXX` || exit 1
  egrep -i "(_error_|ErrorNum|no error|no  error|ErrorHandling|ORA-03292: Table to be|Checking Error Log|automatically placed in the error file|check_error|-fno-exceptions|arm_nr_exception_|exception segment|exception info|exceptions|_tmcp_chain_exception|XGetErrorDatabaseText|XGetErrorText|show errors|VALUE_ERROR|Will check log files for errors|Checking for new Errors|Checking for PEL and GPX errors|Checking tfumerge.master log file for errors|- Will check log files for errors|Checking for Feature File errors|checking for errors|R2S_STOP_ON_ERRORS)" $C_LOGFILE | sort -du > $t_no_err
  #-------------------------------------------------------------------------------------------------
  # NO ERROS
  #-------------------------------------------------------------------------------------------------
  #TODO: what happens if egrep: .../...name.log: No such file or directory the result will be in else branch !
  set c_result = `expr $c_num_err - $c_no_err`
 
  if ( $c_result > 0 ) then
    echo
    echo "ERRORS were found, view logfile: $C_LOGFILE"
	echo "-----------------------------------------------------------------------------------------"
	comm -3 $t_err $t_no_err
	# grep -v -f $t_err $t_no_err
	echo "-----------------------------------------------------------------------------------------"
	echo
  else
    echo
    echo "OK .log file: $C_LOGFILE"
  endif
end
 
	rm $t_err
	rm $t_no_err
 
exit 0
"""
},
"drop_na_users.sql": {
"executable": False,
"content": r"""set echo on;
set timing on;
set def on;
 
drop user &1 cascade;
 
set echo off;
exit; 
"""
},
"do_offline.csh": {
"executable": True,
"content": r"""#!/bin/csh
####################################################################################################
## FILE         : do_offline.csh
## VERSION      : 00.02
## AUTHOR       : Andrei02, Carp
## DESCRIPTION  : wrapper for screen command, run any command in it's own screen and close it on end
## HISTORY      : 02.07.2012, initial version
##                24.01.2013, delete existing configurations
####################################################################################################
 
## check for arguments
if ($#argv == 0 || $#argv < 2) then
	goto help
endif
 
set SCREEN_NAME = $1
set SCREEN_LOG  = $2
 
## test for correct log name
if ($SCREEN_LOG !~ *".log") then
	echo "ERROR: Log file extension (.log) is missing..."
	goto help
endif
 
if(-e $SCREEN_NAME.cfg) then
	# goto error
	echo ""
	echo "WARN: A screen configuration file with the name $SCREEN_NAME.cfg already exist..."
	cat $SCREEN_NAME.cfg
	echo "The existing : $SCREEN_NAME.cfg will be deleted."
	echo ""
	rm -f $SCREEN_NAME.cfg
endif
 
## create the configuration (screenrc) for the screen
echo "startup_message off" >! $SCREEN_NAME.cfg
echo "logfile $SCREEN_LOG" >> $SCREEN_NAME.cfg
echo "flush 5" >> $SCREEN_NAME.cfg
 
## run the command in the screen using also custom configuration
shift
shift
echo ""
echo "Running command: $*"
echo "Under screen name: $SCREEN_NAME with log file: $SCREEN_LOG"
echo ""
screen -L -A -m -d -c $SCREEN_NAME.cfg -S $SCREEN_NAME $*
## if  ($? != 0) then
if  ($status != 0) then
	echo "ERROR: Screen command failed for some reason..."
	goto error
else 
	goto done
endif
 
## goto labels
help:
	echo ""
	echo "Usage: $0 <SCREEN_NAME> <SCREEN_LOGFILE> <RUN_COMMAND>"
	echo ""
	echo "do_offline.csh anca_test logfile.log anca_eu_prod.csh"
	echo "do_offline.csh anca_test logfile.log ls -all"
	echo ""
	goto error
done:
	exit 0
error:
	exit 1
"""
},
"AbakusRDF.csh": {
"executable": True,
"content": r"""#!/bin/csh
 
#abakus.csh 310 R1 N 311 R0 Y eu2013q1 results
 
echo ---------------------------------------------------------------------------
echo `date`: Abakus RDF Start
echo ---------------------------------------------------------------------------
## set sufix for old users
set OLD = $1
set OLD_V = $2
set OLD_C = $3
## set sufix for new users
set NEW = $4
set NEW_V = $5
set NEW_C = $6
## all results will be under this directory 
set PRODUCT = $7
## set sufix for other/test/temporary users
set TEST = 044
set TEST_V = R
## all results will be also copied under this directory 
set RESULTS = $8
 
if ($#argv != 8) then
	echo "Incorrect number of arguments !"
	exit
endif
 
if ("$OLD_C" == "Y") then
echo Old users $OLD$OLD_V will be counted...
else
echo Old users $OLD$OLD_V will not be counted...
endif
 
if ("$NEW_C" == "Y") then
echo New users $NEW$NEW_V will be counted...
else
echo New users $NEW$NEW_V will not be counted...
endif
 
echo Results path: $ABAKUS_RESULT/count_num/count/$PRODUCT
echo Compare path: $ABAKUS_RESULT/count_num/compare/
 
echo >>! AbakusCount.log
 
if ("$OLD_C" == "Y") then
## COUNT 1
perl /db/tools/Abakus2/bin/start_counting.pl RDF_NA_$OLD 505.19.$OLD.84$OLD_V RDF $PRODUCT/na /nt\#r2g2nsB@lizard1 >> AbakusCount.log
endif
 
if ("$NEW_C" == "Y") then
#NEW 1
perl /db/tools/Abakus2/bin/start_counting.pl RDF_NA_$NEW 505.19.$NEW.84$NEW_V RDF $PRODUCT/na /nt\#r2g2nsB@lizard1 >> AbakusCount.log
endif
 
echo >>! AbakusCompare.log
 
# COMPARE 1
perl /db/tools/Abakus2/bin/compare_dir.pl $PRODUCT/na/505.19.$NEW.84$NEW_V $PRODUCT/na/505.19.$OLD.84$OLD_V >>! AbakusCompare.log
 
# COPY
grep "The result is located at" AbakusCount.log | tee AbakusCount_msg.log
grep "The result is located at" AbakusCompare.log | tee AbakusCompare_msg.log
 
echo 'Total number of Count results:' >>! AbakusCopy.log
grep -c "The result is located at" AbakusCount.log >> AbakusCopy.log
echo 'Total number of Count compare' >> AbakusCopy.log
grep -c "The result is located at" AbakusCompare.log >> AbakusCopy.log
echo 'Total number of Count results unique' >> AbakusCopy.log
grep "The result is located at" AbakusCount.log | sort -u | wc -l >> AbakusCopy.log
echo 'Total number of Count compare uniquie' >> AbakusCopy.log
grep "The result is located at" AbakusCompare.log | sort -u | wc -l >> AbakusCopy.log
 
set TIMESTAMP = `date +%Y%b%d_%Hh%Mm%Ss`
if ( -d $RESULTS) then
	mv $RESULTS $RESULTS\_${TIMESTAMP}
	mkdir $RESULTS
else
	mkdir $RESULTS
endif
 
cp -rfp $ABAKUS_RESULT/count_num/compare/505.19.$NEW.84$NEW_V\_with_505.19.$OLD.84$OLD_V $RESULTS/. >> AbakusCopy.log
 
echo ---------------------------------------------------------------------------
echo `date`: Abakus RDF End
echo ---------------------------------------------------------------------------
"""
},
"space_calculate.sql": {
"executable": False,
"content": r"""set echo off
set verify off
set termout on
set heading off
set pagesize 5000
set feedback off
set newpage none
set linesize 160
set colsep ';'
 
set trimspool on
set trims on
set trimout on
 
set headsep off
 
--spool size_rdf.csv append;
spool size_svf.csv append;
 
 
select 'USER;SIZE (GB);&1' from DUAL; 
select DS.OWNER as "USER", ROUND(SUM(DS.BYTES) / 1024 / 1024 / 1024, 2) as "GB"
FROM DBA_SEGMENTS DS
--where DS.OWNER in ('RDF_EEU_&1')
where DS.OWNER in ('RDF_NA_&1','SVF_DCA1_&1','SVF_DCA2_&1','SVF_DCA3_&1','SVF_DCA4_&1','SVF_DCA5_&1','SVF_DCA6_&1','SVF_DCA7_&1','SVF_DCA8_&1','SVF_DCA9_&1','SVF_DCA10_&1','SVF_DCA11_&1','SVF_DCA12_&1','SVF_DCA13_&1','SVF_DCA14_&1', 'svf_mex_&1','SVF_DCA15_&1')
group BY DS.OWNER;
 
spool off
exit;
"""
},
"drop_users.sql": {
"executable": False,
"content": r"""set echo on;
set timing on;
set def on;
 
drop user ADAS_BA_314 CASCADE;
drop user ADAS_BG_314 CASCADE;
drop user ADAS_ACH_314 CASCADE;
drop user ADAS_BLR_314 CASCADE;
drop user ADAS_EU_312 CASCADE;
drop user ADAS_AL_314 CASCADE;
drop user ADAS_SP_314 CASCADE;
drop user ADAS_BNL_314 CASCADE;
drop user ADAS_CS_314 CASCADE;
drop user ADAS_CZ_314 CASCADE;
drop user ADAS_ELL_314 CASCADE;
drop user ADAS_FALL_314 CASCADE;
drop user ADAS_GALL_314 CASCADE;
drop user ADAS_GR_314 CASCADE;
drop user ADAS_HR_314 CASCADE;
drop user ADAS_HU_314 CASCADE;
drop user ADAS_I_314 CASCADE;
drop user ADAS_MD_314 CASCADE;
drop user ADAS_MK_314 CASCADE;
drop user ADAS_PL_314 CASCADE;
drop user ADAS_RO_314 CASCADE;
drop user ADAS_SC_314 CASCADE;
drop user ADAS_SI_314 CASCADE;
drop user ADAS_SK_314 CASCADE;
drop user ADAS_UK_314 CASCADE;
drop user ADAS_UKR_314 CASCADE;
drop user ADAS_KOS_314 CASCADE;
drop user ADAS_RU_314 CASCADE;
drop user ADAS_TR_314 CASCADE;
drop user ADAS_ISL_314 CASCADE;
drop user ADAS_KAZ_314 CASCADE;
drop user ADAS_MLT_314 CASCADE;
drop user ADAS_CALL_314 CASCADE;
drop user ADAS_CUN_314 CASCADE;
drop user ADAS_NCY_314 CASCADE;
drop user ADAS_EU_314 CASCADE;
drop user ADAS_CS_313 CASCADE;
drop user ADAS_MK_313 CASCADE;
drop user ADAS_KAZ_313 CASCADE;
drop user ADAS_MLT_313 CASCADE;
drop user ADAS_MD_313 CASCADE;
drop user ADAS_ISL_313 CASCADE;
drop user ADAS_BLR_313 CASCADE;
drop user ADAS_BNL_313 CASCADE;
drop user ADAS_CZ_313 CASCADE;
drop user ADAS_ELL_313 CASCADE;
drop user ADAS_FALL_313 CASCADE;
drop user ADAS_GALL_313 CASCADE;
drop user ADAS_GR_313 CASCADE;
drop user ADAS_HR_313 CASCADE;
drop user ADAS_HU_313 CASCADE;
drop user ADAS_I_313 CASCADE;
drop user ADAS_PL_313 CASCADE;
drop user ADAS_RO_313 CASCADE;
drop user ADAS_RU_313 CASCADE;
drop user ADAS_SC_313 CASCADE;
drop user ADAS_SI_313 CASCADE;
drop user ADAS_SK_313 CASCADE;
drop user ADAS_SP_313 CASCADE;
drop user ADAS_UK_313 CASCADE;
drop user ADAS_UKR_313 CASCADE;
drop user ADAS_KOS_313 CASCADE;
drop user ADAS_TR_313 CASCADE;
drop user ADAS_CALL_313 CASCADE;
drop user ADAS_CUN_313 CASCADE;
drop user ADAS_NCY_313 CASCADE;
drop user ADAS_ACH_313 CASCADE;
drop user ADAS_AL_313 CASCADE;
drop user ADAS_BA_313 CASCADE;
drop user ADAS_BG_313 CASCADE;
drop user ADAS_SA_210 CASCADE;
drop user ADAS_SA_211 CASCADE;
drop user ADAS_ARG_212 CASCADE;
drop user ADAS_ISR_311 CASCADE;
drop user SVF_UKR_310 CASCADE;
drop user SVF_BLR_310 CASCADE;
drop user SVF_MD_310 CASCADE;
drop user SVF_MK_310 CASCADE;
drop user SVF_SI_310 CASCADE;
drop user SVF_CUN_310 CASCADE;
drop user SVF_RO_310 CASCADE;
drop user SVF_HR_310 CASCADE;
drop user SVF_PL_310 CASCADE;
drop user SVF_CZ_310 CASCADE;
drop user SVF_HU_310 CASCADE;
drop user SVF_BNL_310 CASCADE;
drop user SVF_I_310 CASCADE;
drop user SVF_SP_310 CASCADE;
drop user SVF_ACH_310 CASCADE;
drop user ADAS_BG_310 CASCADE;
drop user ADAS_ACH_310 CASCADE;
drop user ADAS_CZ_310 CASCADE;
drop user ADAS_PL_310 CASCADE;
drop user ADAS_RO_310 CASCADE;
drop user ADAS_UK_310 CASCADE;
drop user ADAS_UKR_310 CASCADE;
drop user ADAS_TR_310 CASCADE;
drop user ADAS_CALL_310 CASCADE;
drop user ADAS_CY_310 CASCADE;
drop user ADAS_ELL_310 CASCADE;
drop user SVF_DCA1_310 CASCADE;
drop user SVF_DCA13_310 CASCADE;
drop user SVF_DCA8_310 CASCADE;
drop user ADAS_MEX_310 CASCADE;
drop user ADAS_I_311 CASCADE;
drop user ADAS_AL_311 CASCADE;
drop user ADAS_TR_311 CASCADE;
 
set echo off;
exit; 
"""
},
"AbakusSVF.sql": {
"executable": True,
"content": r"""#!/bin/csh
 
# WEU -> ABAKUS SVF for: ach achm   bnl bnlm   fall fallm   gall gallm   i im   sc scm   sp spm   uk ukm
 
#abakus.csh 511 S0 N 540 S0 Y eu2015q4 results
 
echo ---------------------------------------------------------------------------
echo `date`: Abakus SVF Start
echo ---------------------------------------------------------------------------
## set sufix for old users
set OLD = $1
set OLD_V = $2
set OLD_C = $3
## set sufix for new users
set NEW = $4
set NEW_V = $5
set NEW_C = $6
## all results will be under this directory 
set PRODUCT = $7
## set sufix for other/test/temporary users
set TEST = 044
set TEST_V = R
## all results will be also copied under this directory 
set RESULTS = $8
 
if ($#argv != 8) then
	echo "Incorrect number of arguments !"
	exit
endif
 
if ("$OLD_C" == "Y") then
echo Old users $OLD$OLD_V will be counted...
else
echo Old users $OLD$OLD_V will not be counted...
endif
 
if ("$NEW_C" == "Y") then
echo New users $NEW$NEW_V will be counted...
else
echo New users $NEW$NEW_V will not be counted...
endif
 
echo Results path: $ABAKUS_RESULT/count_num/count/$PRODUCT
echo Compare path: $ABAKUS_RESULT/count_num/compare/
 
## WEU -> ach achm   bnl bnlm   fall fallm   gall gallm   i im   sc scm   sp spm   uk ukm  
 
echo >>! AbakusCount.log
 
if ("$OLD_C" == "Y") then
## Count OLD users [count 28 + 2]
perl /db/tools/Abakus2/bin/start_counting.pl svf_dca1_$OLD 505.01.$OLD.84$OLD_V SVF $PRODUCT/dca1 /nt\#r2g2nsB@lizard1 >> AbakusCount.log
perl /db/tools/Abakus2/bin/start_counting.pl svf_dca2_$OLD 505.02.$OLD.84$OLD_V SVF $PRODUCT/dca2 /nt\#r2g2nsB@lizard1 >> AbakusCount.log
perl /db/tools/Abakus2/bin/start_counting.pl svf_dca3_$OLD 505.03.$OLD.84$OLD_V SVF $PRODUCT/dca3 /nt\#r2g2nsB@lizard1 >> AbakusCount.log
perl /db/tools/Abakus2/bin/start_counting.pl svf_dca4_$OLD 505.04.$OLD.84$OLD_V SVF $PRODUCT/dca4 /nt\#r2g2nsB@lizard1 >> AbakusCount.log
perl /db/tools/Abakus2/bin/start_counting.pl svf_dca5_$OLD 505.05.$OLD.84$OLD_V SVF $PRODUCT/dca5 /nt\#r2g2nsB@lizard1 >> AbakusCount.log
perl /db/tools/Abakus2/bin/start_counting.pl svf_dca6_$OLD 505.06.$OLD.84$OLD_V SVF $PRODUCT/dca6 /nt\#r2g2nsB@lizard1 >> AbakusCount.log
perl /db/tools/Abakus2/bin/start_counting.pl svf_dca7_$OLD 505.07.$OLD.84$OLD_V SVF $PRODUCT/dca7 /nt\#r2g2nsB@lizard1 >> AbakusCount.log
perl /db/tools/Abakus2/bin/start_counting.pl svf_dca8_$OLD 505.08.$OLD.84$OLD_V SVF $PRODUCT/dca8 /nt\#r2g2nsB@lizard1 >> AbakusCount.log
perl /db/tools/Abakus2/bin/start_counting.pl svf_dca9_$OLD 505.09.$OLD.84$OLD_V SVF $PRODUCT/dca9 /nt\#r2g2nsB@lizard1 >> AbakusCount.log
perl /db/tools/Abakus2/bin/start_counting.pl svf_dca10_$OLD 505.10.$OLD.84$OLD_V SVF $PRODUCT/dca10 /nt\#r2g2nsB@lizard1 >> AbakusCount.log
perl /db/tools/Abakus2/bin/start_counting.pl svf_dca11_$OLD 505.11.$OLD.84$OLD_V SVF $PRODUCT/dca11 /nt\#r2g2nsB@lizard1 >> AbakusCount.log
perl /db/tools/Abakus2/bin/start_counting.pl svf_dca12_$OLD 505.12.$OLD.84$OLD_V SVF $PRODUCT/dca12 /nt\#r2g2nsB@lizard1 >> AbakusCount.log
perl /db/tools/Abakus2/bin/start_counting.pl svf_dca13_$OLD 505.13.$OLD.84$OLD_V SVF $PRODUCT/dca13 /nt\#r2g2nsB@lizard1 >> AbakusCount.log
perl /db/tools/Abakus2/bin/start_counting.pl svf_dca14_$OLD 505.14.$OLD.84$OLD_V SVF $PRODUCT/dca14 /nt\#r2g2nsB@lizard1 >> AbakusCount.log
perl /db/tools/Abakus2/bin/start_counting.pl svf_mex_$OLD 505.95.$OLD.84$OLD_V SVF $PRODUCT/mex /nt\#r2g2nsB@lizard1 >> AbakusCount.log
perl /db/tools/Abakus2/bin/start_counting.pl svf_dca15_$OLD 505.15.$OLD.84$OLD_V SVF $PRODUCT/dca15 /nt\#r2g2nsB@lizard1 >> AbakusCount.log
endif
 
if ("$NEW_C" == "Y") then
## Count NEW users [count 28 + 2]
perl /db/tools/Abakus2/bin/start_counting.pl svf_dca1_$NEW 505.01.$NEW.84$NEW_V SVF $PRODUCT/dca1 /nt\#r2g2nsB@lizard1 >> AbakusCount.log
perl /db/tools/Abakus2/bin/start_counting.pl svf_dca2_$NEW 505.02.$NEW.84$NEW_V SVF $PRODUCT/dca2 /nt\#r2g2nsB@lizard1 >> AbakusCount.log
perl /db/tools/Abakus2/bin/start_counting.pl svf_dca3_$NEW 505.03.$NEW.84$NEW_V SVF $PRODUCT/dca3 /nt\#r2g2nsB@lizard1 >> AbakusCount.log
perl /db/tools/Abakus2/bin/start_counting.pl svf_dca4_$NEW 505.04.$NEW.84$NEW_V SVF $PRODUCT/dca4 /nt\#r2g2nsB@lizard1 >> AbakusCount.log
perl /db/tools/Abakus2/bin/start_counting.pl svf_dca5_$NEW 505.05.$NEW.84$NEW_V SVF $PRODUCT/dca5 /nt\#r2g2nsB@lizard1 >> AbakusCount.log
perl /db/tools/Abakus2/bin/start_counting.pl svf_dca6_$NEW 505.06.$NEW.84$NEW_V SVF $PRODUCT/dca6 /nt\#r2g2nsB@lizard1 >> AbakusCount.log
perl /db/tools/Abakus2/bin/start_counting.pl svf_dca7_$NEW 505.07.$NEW.84$NEW_V SVF $PRODUCT/dca7 /nt\#r2g2nsB@lizard1 >> AbakusCount.log
perl /db/tools/Abakus2/bin/start_counting.pl svf_dca8_$NEW 505.08.$NEW.84$NEW_V SVF $PRODUCT/dca8 /nt\#r2g2nsB@lizard1 >> AbakusCount.log
perl /db/tools/Abakus2/bin/start_counting.pl svf_dca9_$NEW 505.09.$NEW.84$NEW_V SVF $PRODUCT/dca9 /nt\#r2g2nsB@lizard1 >> AbakusCount.log
perl /db/tools/Abakus2/bin/start_counting.pl svf_dca10_$NEW 505.10.$NEW.84$NEW_V SVF $PRODUCT/dca10 /nt\#r2g2nsB@lizard1 >> AbakusCount.log
perl /db/tools/Abakus2/bin/start_counting.pl svf_dca11_$NEW 505.11.$NEW.84$NEW_V SVF $PRODUCT/dca11 /nt\#r2g2nsB@lizard1 >> AbakusCount.log
perl /db/tools/Abakus2/bin/start_counting.pl svf_dca12_$NEW 505.12.$NEW.84$NEW_V SVF $PRODUCT/dca12 /nt\#r2g2nsB@lizard1 >> AbakusCount.log
perl /db/tools/Abakus2/bin/start_counting.pl svf_dca13_$NEW 505.13.$NEW.84$NEW_V SVF $PRODUCT/dca13 /nt\#r2g2nsB@lizard1 >> AbakusCount.log
perl /db/tools/Abakus2/bin/start_counting.pl svf_dca14_$NEW 505.14.$NEW.84$NEW_V SVF $PRODUCT/dca14 /nt\#r2g2nsB@lizard1 >> AbakusCount.log
perl /db/tools/Abakus2/bin/start_counting.pl svf_mex_$NEW 505.95.$NEW.84$NEW_V SVF $PRODUCT/mex /nt\#r2g2nsB@lizard1 >> AbakusCount.log
perl /db/tools/Abakus2/bin/start_counting.pl svf_dca15_$NEW 505.15.$NEW.84$NEW_V SVF $PRODUCT/dca15 /nt\#r2g2nsB@lizard1 >> AbakusCount.log
endif
 
echo >>! AbakusCompare.log
 
## Compare users [count 28 + 2]
perl /db/tools/Abakus2/bin/compare_dir.pl $PRODUCT/dca1/505.01.$NEW.84$NEW_V $PRODUCT/dca1/505.01.$OLD.84$OLD_V >> AbakusCompare.log
perl /db/tools/Abakus2/bin/compare_dir.pl $PRODUCT/dca2/505.02.$NEW.84$NEW_V $PRODUCT/dca2/505.02.$OLD.84$OLD_V >> AbakusCompare.log
perl /db/tools/Abakus2/bin/compare_dir.pl $PRODUCT/dca3/505.03.$NEW.84$NEW_V $PRODUCT/dca3/505.03.$OLD.84$OLD_V >> AbakusCompare.log
perl /db/tools/Abakus2/bin/compare_dir.pl $PRODUCT/dca4/505.04.$NEW.84$NEW_V $PRODUCT/dca4/505.04.$OLD.84$OLD_V >> AbakusCompare.log
perl /db/tools/Abakus2/bin/compare_dir.pl $PRODUCT/dca5/505.05.$NEW.84$NEW_V $PRODUCT/dca5/505.05.$OLD.84$OLD_V >> AbakusCompare.log
perl /db/tools/Abakus2/bin/compare_dir.pl $PRODUCT/dca6/505.06.$NEW.84$NEW_V $PRODUCT/dca6/505.06.$OLD.84$OLD_V >> AbakusCompare.log
perl /db/tools/Abakus2/bin/compare_dir.pl $PRODUCT/dca7/505.07.$NEW.84$NEW_V $PRODUCT/dca7/505.07.$OLD.84$OLD_V >> AbakusCompare.log
perl /db/tools/Abakus2/bin/compare_dir.pl $PRODUCT/dca8/505.08.$NEW.84$NEW_V $PRODUCT/dca8/505.08.$OLD.84$OLD_V >> AbakusCompare.log
perl /db/tools/Abakus2/bin/compare_dir.pl $PRODUCT/dca9/505.09.$NEW.84$NEW_V $PRODUCT/dca9/505.09.$OLD.84$OLD_V >> AbakusCompare.log
perl /db/tools/Abakus2/bin/compare_dir.pl $PRODUCT/dca10/505.10.$NEW.84$NEW_V $PRODUCT/dca10/505.10.$OLD.84$OLD_V >> AbakusCompare.log
perl /db/tools/Abakus2/bin/compare_dir.pl $PRODUCT/dca11/505.11.$NEW.84$NEW_V $PRODUCT/dca11/505.11.$OLD.84$OLD_V >> AbakusCompare.log
perl /db/tools/Abakus2/bin/compare_dir.pl $PRODUCT/dca12/505.12.$NEW.84$NEW_V $PRODUCT/dca12/505.12.$OLD.84$OLD_V >> AbakusCompare.log
perl /db/tools/Abakus2/bin/compare_dir.pl $PRODUCT/dca13/505.13.$NEW.84$NEW_V $PRODUCT/dca13/505.13.$OLD.84$OLD_V >> AbakusCompare.log
perl /db/tools/Abakus2/bin/compare_dir.pl $PRODUCT/dca14/505.14.$NEW.84$NEW_V $PRODUCT/dca14/505.14.$OLD.84$OLD_V >> AbakusCompare.log
perl /db/tools/Abakus2/bin/compare_dir.pl $PRODUCT/mex/505.95.$NEW.84$NEW_V $PRODUCT/mex/505.95.$OLD.84$OLD_V >> AbakusCompare.log
perl /db/tools/Abakus2/bin/compare_dir.pl $PRODUCT/dca15/505.15.$NEW.84$NEW_V $PRODUCT/dca15/505.15.$OLD.84$OLD_V >> AbakusCompare.log
 
# perl /db/tools/Abakus2/bin/compare_dir.pl $PRODUCT/eu/505.20.$NEW.84$NEW_V $PRODUCT/eu/505.20.$OLD.84$OLD_V >> AbakusCompare.log
# perl /db/tools/Abakus2/bin/compare_dir.pl $PRODUCT/eeu/505.30.$NEW.84$NEW_V $PRODUCT/eeu/505.30.$OLD.84$OLD_V >> AbakusCompare.log
 
## Perform some tests to .log files
grep "The result is located at" AbakusCount.log | tee AbakusCount_msg.log
grep "The result is located at" AbakusCompare.log | tee AbakusCompare_msg.log
 
echo 'Total number of Count results:' >>! AbakusCopy.log
grep -c "The result is located at" AbakusCount.log >> AbakusCopy.log
echo 'Total number of Count compare' >> AbakusCopy.log
grep -c "The result is located at" AbakusCompare.log >> AbakusCopy.log
echo 'Total number of Count results unique' >> AbakusCopy.log
grep "The result is located at" AbakusCount.log | sort -u | wc -l >> AbakusCopy.log
echo 'Total number of Count compare uniquie' >> AbakasCopy.log
grep "The result is located at" AbakusCompare.log | sort -u | wc -l >> AbakusCopy.log
 
set TIMESTAMP = `date +%Y%b%d_%Hh%Mm%Ss`
if ( -d $RESULTS) then
	mv $RESULTS $RESULTS\_${TIMESTAMP}
	mkdir $RESULTS
else
	mkdir $RESULTS
endif
 
## Copy results also to currrent directory for easy access [count 28 + 2]
cp -rfp $ABAKUS_RESULT/count_num/compare/505.01.$NEW.84$NEW_V\_with_505.01.$OLD.84$OLD_V . >> AbakusCopy.log
cp -rfp $ABAKUS_RESULT/count_num/compare/505.02.$NEW.84$NEW_V\_with_505.02.$OLD.84$OLD_V . >> AbakusCopy.log
cp -rfp $ABAKUS_RESULT/count_num/compare/505.03.$NEW.84$NEW_V\_with_505.03.$OLD.84$OLD_V . >> AbakusCopy.log
cp -rfp $ABAKUS_RESULT/count_num/compare/505.04.$NEW.84$NEW_V\_with_505.04.$OLD.84$OLD_V . >> AbakusCopy.log
cp -rfp $ABAKUS_RESULT/count_num/compare/505.05.$NEW.84$NEW_V\_with_505.05.$OLD.84$OLD_V . >> AbakusCopy.log
cp -rfp $ABAKUS_RESULT/count_num/compare/505.06.$NEW.84$NEW_V\_with_505.06.$OLD.84$OLD_V . >> AbakusCopy.log
cp -rfp $ABAKUS_RESULT/count_num/compare/505.07.$NEW.84$NEW_V\_with_505.07.$OLD.84$OLD_V . >> AbakusCopy.log
cp -rfp $ABAKUS_RESULT/count_num/compare/505.08.$NEW.84$NEW_V\_with_505.08.$OLD.84$OLD_V . >> AbakusCopy.log
cp -rfp $ABAKUS_RESULT/count_num/compare/505.09.$NEW.84$NEW_V\_with_505.09.$OLD.84$OLD_V . >> AbakusCopy.log
cp -rfp $ABAKUS_RESULT/count_num/compare/505.10.$NEW.84$NEW_V\_with_505.10.$OLD.84$OLD_V . >> AbakusCopy.log
cp -rfp $ABAKUS_RESULT/count_num/compare/505.11.$NEW.84$NEW_V\_with_505.11.$OLD.84$OLD_V . >> AbakusCopy.log
cp -rfp $ABAKUS_RESULT/count_num/compare/505.12.$NEW.84$NEW_V\_with_505.12.$OLD.84$OLD_V . >> AbakusCopy.log
cp -rfp $ABAKUS_RESULT/count_num/compare/505.13.$NEW.84$NEW_V\_with_505.13.$OLD.84$OLD_V . >> AbakusCopy.log
cp -rfp $ABAKUS_RESULT/count_num/compare/505.14.$NEW.84$NEW_V\_with_505.14.$OLD.84$OLD_V . >> AbakusCopy.log
cp -rfp $ABAKUS_RESULT/count_num/compare/505.95.$NEW.84$NEW_V\_with_505.95.$OLD.84$OLD_V . >> AbakusCopy.log
cp -rfp $ABAKUS_RESULT/count_num/compare/505.15.$NEW.84$NEW_V\_with_505.15.$OLD.84$OLD_V . >> AbakusCopy.log
 
# cp -rfp $ABAKUS_RESULT/count_num/compare/505.20.$NEW.84$NEW_V\_with_505.20.$OLD.84$OLD_V $RESULTS/. >> AbakusCopy.log
# cp -rfp $ABAKUS_RESULT/count_num/compare/505.30.$NEW.84$NEW_V\_with_505.30.$OLD.84$OLD_V $RESULTS/. >> AbakusCopy.log
 
echo ---------------------------------------------------------------------------
echo `date`: Abakus SVF End
echo ---------------------------------------------------------------------------
"""
},
"python_wrapper": {
"executable": True,
"content": r"""#!/bin/csh
 
# The following is needed to force usage of the 32bit version of the OCI
# which is needed by the Arriba test with sqlite
#
# This test loads db/tools/local/lib/sqliface_dll which is a 32 bit compilation
# (see db/tools/local/lib/sqliface_README.txt)
#
# The exact location depends on the host, so it is crucial that $ORACLE_HOME is setproperly
#
# NOTE: because the ORACLE 11 client on LINUX needs libaio.so
#       this file was copied from /usr/lib on rbgs372x to .../tools/linux/local/lib
 
 
# ==================================================================
# Setup Oracle client version:
# ==================================================================
setenv ORA_USER /PROJ/db4/dbteam/oracle
setenv ORA_CLIENTVERSION 19.3_32
setenv ORACLE_BASE /PROJ/db4/dbteam/oracle
setenv ORACLE_HOME "${ORA_USER}/product/${ORA_CLIENTVERSION}"
setenv TNS_ADMIN /PROJ/db4/dbteam/oracle/product/tns_admin/network/admin
 
# ==================================================================
# Set system libraries for Oracle env.
# ==================================================================
setenv ORACLE_LIB ${ORACLE_HOME}/lib:/lib:/usr/lib
setenv LD_LIBRARY_PATH /usr/local/lib:${ORACLE_HOME}/lib:${DBTOOLS}/linux/local/lib
 
# ==================================================================
# ORACLE Settings
# ==================================================================
setenv ORACLE_DOC $ORACLE_HOME/doc
setenv ORACLE_SID GDF 
setenv ORACLE_TERM $TERM
setenv ORA_ROLLBACK_SEGMENT NONE
setenv ORA_NLS33 $ORACLE_HOME/nls/data
 
echo ORACLE_HOME has been set to $ORACLE_HOME
echo LD_LIBRARY_PATH has been set to $LD_LIBRARY_PATH
 
 
# setenv CPPFLAGS -m32
# setenv CFLAGS -m32
# setenv LDFLAGS -m32
 
# setenv DPI_DEBUG_LEVEL 64
 
setenv PYTHONPATH /PROJ/db4/dbteam/tools/linux/localpython/lib:/PROJ/db4/dbteam/tools/linux/localpython/deploy/lib
setenv LD_LIBRARY_PATH /usr/local/lib:/opt/rational/clearcase/lib:/PROJ/db4/dbteam/oracle/product/19.3_32/lib:/PROJ/db4/dbteam/tools/linux/local/lib:/PROJ/db4/dbteam/tools/linux/localpython/libaio-0.3.112/deploy/lib:/PROJ/db4/dbteam/tools/linux/localpython/lib:/PROJ/db4/dbteam/tools/linux/localpython/deploy/lib
 
echo LD_LIBRARY_PATH has been set to $LD_LIBRARY_PATH
 
# setenv C_INCLUDE_PATH /PROJ/db4/dbteam/tools/linux/Python-2.7.18/sqlite-autoconf-3450200/deploy/include 
# setenv CPLUS_INCLUDE_PATH /PROJ/db4/dbteam/tools/linux/Python-2.7.18/sqlite-autoconf-3450200/deploy/include 
# setenv LD_RUN_PATH /PROJ/db4/dbteam/tools/linux/Python-2.7.18/sqlite-autoconf-3450200/deploy/lib
 
 
# Load custom SQLite
# setenv LD_PRELOAD /PROJ/db4/dbteam/tools/linux/Python-2.7.18/sqlite-autoconf-3450200/deploy/lib/libsqlite3.so
 
# /PROJ/db4/dbteam/tools/linux/localpython/bin/python $*
/PROJ/db4/dbteam/tools/linux/localpython/bin/python $*
 
# ./python_wrapper setup.py build
"""
},
"runUT": {
"executable": True,
"content": r"""#!/bin/sh
 
# 610
RDF_COMPILER=/PROJ/db4/db/RDF/NA/2026Q1/2025R4_RDF_North_America_251H0/610/Scripts/compiler
 
# !!! ut.py should be encoded as Unix not DOS !!!
dos2unix $RDF_COMPILER/gdfConvert/util/ut/ut.py
 
os=`uname`
 
if  echo "$os" |grep -i Linux ; then
	 ORACLE_HOME=/PROJ/db4/sviissql/app/oracle/product/client/linux/x86_64/11.2.0
elif echo "$os" |grep -i SunOS ; then
	ORACLE_HOME=/PROJ/sviissql/app/oracle/product/client/sunos/sparc/10.2.0
else echo"OS Exception: This operating sistem is other then Linux/SunOS!"
fi
 
export USER_SFX=$1
export ORACLE_HOME
LD_LIBRARY_PATH=$ORACLE_HOME/lib32:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH
 
###  VW WEU: ->> dca2 dca3 DNK dca4 FIN dca5 I NOR SC SP SWE UK RDF_WEU
 
### RDF NA
python_wrapper $RDF_COMPILER/gdfConvert/util/ut/ut.py  --test_user  rdf_na_610 --spec_id 1804       --test_password nt\#r2g2nsB --test_service lizard1 --user_types "rdf" --trun_context PRODUCTION --trun_label "SVF_KW22_13: rdf_na_$USER_SFX" --root_path $RDF_COMPILER/gdfConvert/util/ut/test_case_root --maxThreads 20 --loc 3 --report_with_variables_list --report_format excel_csv --report_file_name "rdf_na_$USER_SFX.csv" --log_file_name "rdf_na_$USER_SFX.log" --timeout 2000 --property_user "navdb_ro" --property_dsn "(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST=euxb009s.eux.de.int.automotive-wan.com)(PORT=1521)(SEND_BUF_SIZE=)(RECV_BUF_SIZE=))(LOAD_BALANCE=yes))(CONNECT_DATA=(SERVICE_NAME=stemppo_1_p_pdb.eux.de.int.automotive-wan.com)))" --property_password "navdb#r2g2nsb" --report_columns "Case+No.,ID,Expr.+No.,UT_Name,Filename,Line+No.,Backend,Work+Package,Tags,Requirements,Conducted,Passed,Timed+out,Elapsed+[s],Excep.,Var.+uninitialized,Var.+defaulted,Filtered+by+Variable,Cond.+Match,LOC,Severity+(0CBAS),Log+Text,Statement+-+unparsed,Statement+-+PARSED,Orig.+Expr.,Parsed+Expr.,Result+(max.+10+rows),Exception+Text,Type,Qualifier,Orig.+Cond.,Parsed+Cond.,Starttime,Endtime,Dbname+Match,Prod.+Match,Suppl.+Match,U+Match,LOC+Match,ID+Match,Filename+Match"
 
python_wrapper $RDF_COMPILER/gdfConvert/util/ut/ut.py  --test_user  svf_dca2_610 --spec_id 1804      --test_password nt\#r2g2nsB --test_service lizard1 --user_types "svf,rdf+svf" --trun_context PRODUCTION --trun_label "SVF_KW22_13: svf_dca2_$USER_SFX" --root_path $RDF_COMPILER/gdfConvert/util/ut/test_case_root --maxThreads 20 --loc 3 --report_with_variables_list --report_format excel_csv --report_file_name "svf_dca2_$USER_SFX.csv" --log_file_name "svf_dca2_$USER_SFX.log" --timeout 2000 --property_user "navdb_ro" --property_dsn "(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST=euxb009s.eux.de.int.automotive-wan.com)(PORT=1521)(SEND_BUF_SIZE=)(RECV_BUF_SIZE=))(LOAD_BALANCE=yes))(CONNECT_DATA=(SERVICE_NAME=stemppo_1_p_pdb.eux.de.int.automotive-wan.com)))" --property_password "navdb#r2g2nsb" --report_columns "Case+No.,ID,Expr.+No.,UT_Name,Filename,Line+No.,Backend,Work+Package,Tags,Requirements,Conducted,Passed,Timed+out,Elapsed+[s],Excep.,Var.+uninitialized,Var.+defaulted,Filtered+by+Variable,Cond.+Match,LOC,Severity+(0CBAS),Log+Text,Statement+-+unparsed,Statement+-+PARSED,Orig.+Expr.,Parsed+Expr.,Result+(max.+10+rows),Exception+Text,Type,Qualifier,Orig.+Cond.,Parsed+Cond.,Starttime,Endtime,Dbname+Match,Prod.+Match,Suppl.+Match,U+Match,LOC+Match,ID+Match,Filename+Match"
 
python_wrapper $RDF_COMPILER/gdfConvert/util/ut/ut.py  --test_user  svf_dca3_610 --spec_id 1804     --test_password nt\#r2g2nsB --test_service lizard1 --user_types "svf,rdf+svf" --trun_context PRODUCTION --trun_label "SVF_KW22_13: svf_dca3_$USER_SFX" --root_path $RDF_COMPILER/gdfConvert/util/ut/test_case_root --maxThreads 20 --loc 3 --report_with_variables_list --report_format excel_csv --report_file_name "svf_dca3_$USER_SFX.csv" --log_file_name "svf_dca3_$USER_SFX.log" --timeout 2000 --property_user "navdb_ro" --property_dsn "(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST=euxb009s.eux.de.int.automotive-wan.com)(PORT=1521)(SEND_BUF_SIZE=)(RECV_BUF_SIZE=))(LOAD_BALANCE=yes))(CONNECT_DATA=(SERVICE_NAME=stemppo_1_p_pdb.eux.de.int.automotive-wan.com)))" --property_password "navdb#r2g2nsb" --report_columns "Case+No.,ID,Expr.+No.,UT_Name,Filename,Line+No.,Backend,Work+Package,Tags,Requirements,Conducted,Passed,Timed+out,Elapsed+[s],Excep.,Var.+uninitialized,Var.+defaulted,Filtered+by+Variable,Cond.+Match,LOC,Severity+(0CBAS),Log+Text,Statement+-+unparsed,Statement+-+PARSED,Orig.+Expr.,Parsed+Expr.,Result+(max.+10+rows),Exception+Text,Type,Qualifier,Orig.+Cond.,Parsed+Cond.,Starttime,Endtime,Dbname+Match,Prod.+Match,Suppl.+Match,U+Match,LOC+Match,ID+Match,Filename+Match"

python_wrapper $RDF_COMPILER/gdfConvert/util/ut/ut.py  --test_user  svf_dca4_610 --spec_id 1804     --test_password nt\#r2g2nsB --test_service lizard1 --user_types "svf,rdf+svf" --trun_context PRODUCTION --trun_label "SVF_KW22_13: svf_dca4_$USER_SFX" --root_path $RDF_COMPILER/gdfConvert/util/ut/test_case_root --maxThreads 20 --loc 3 --report_with_variables_list --report_format excel_csv --report_file_name "svf_dca4_$USER_SFX.csv" --log_file_name "svf_dca4_$USER_SFX.log" --timeout 2000 --property_user "navdb_ro" --property_dsn "(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST=euxb009s.eux.de.int.automotive-wan.com)(PORT=1521)(SEND_BUF_SIZE=)(RECV_BUF_SIZE=))(LOAD_BALANCE=yes))(CONNECT_DATA=(SERVICE_NAME=stemppo_1_p_pdb.eux.de.int.automotive-wan.com)))" --property_password "navdb#r2g2nsb" --report_columns "Case+No.,ID,Expr.+No.,UT_Name,Filename,Line+No.,Backend,Work+Package,Tags,Requirements,Conducted,Passed,Timed+out,Elapsed+[s],Excep.,Var.+uninitialized,Var.+defaulted,Filtered+by+Variable,Cond.+Match,LOC,Severity+(0CBAS),Log+Text,Statement+-+unparsed,Statement+-+PARSED,Orig.+Expr.,Parsed+Expr.,Result+(max.+10+rows),Exception+Text,Type,Qualifier,Orig.+Cond.,Parsed+Cond.,Starttime,Endtime,Dbname+Match,Prod.+Match,Suppl.+Match,U+Match,LOC+Match,ID+Match,Filename+Match"
 
python_wrapper $RDF_COMPILER/gdfConvert/util/ut/ut.py  --test_user  svf_dca5_610 --spec_id 1804     --test_password nt\#r2g2nsB --test_service lizard1 --user_types "svf,rdf+svf" --trun_context PRODUCTION --trun_label "SVF_KW22_13: svf_dca5_$USER_SFX" --root_path $RDF_COMPILER/gdfConvert/util/ut/test_case_root --maxThreads 20 --loc 3 --report_with_variables_list --report_format excel_csv --report_file_name "svf_dca5_$USER_SFX.csv" --log_file_name "svf_dca5_$USER_SFX.log" --timeout 2000 --property_user "navdb_ro" --property_dsn "(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST=euxb009s.eux.de.int.automotive-wan.com)(PORT=1521)(SEND_BUF_SIZE=)(RECV_BUF_SIZE=))(LOAD_BALANCE=yes))(CONNECT_DATA=(SERVICE_NAME=stemppo_1_p_pdb.eux.de.int.automotive-wan.com)))" --property_password "navdb#r2g2nsb" --report_columns "Case+No.,ID,Expr.+No.,UT_Name,Filename,Line+No.,Backend,Work+Package,Tags,Requirements,Conducted,Passed,Timed+out,Elapsed+[s],Excep.,Var.+uninitialized,Var.+defaulted,Filtered+by+Variable,Cond.+Match,LOC,Severity+(0CBAS),Log+Text,Statement+-+unparsed,Statement+-+PARSED,Orig.+Expr.,Parsed+Expr.,Result+(max.+10+rows),Exception+Text,Type,Qualifier,Orig.+Cond.,Parsed+Cond.,Starttime,Endtime,Dbname+Match,Prod.+Match,Suppl.+Match,U+Match,LOC+Match,ID+Match,Filename+Match"
 
python_wrapper $RDF_COMPILER/gdfConvert/util/ut/ut.py  --test_user  svf_dca6_610 --spec_id 1804     --test_password nt\#r2g2nsB --test_service lizard1 --user_types "svf,rdf+svf" --trun_context PRODUCTION --trun_label "SVF_KW22_13: svf_dca6_$USER_SFX" --root_path $RDF_COMPILER/gdfConvert/util/ut/test_case_root --maxThreads 20 --loc 3 --report_with_variables_list --report_format excel_csv --report_file_name "svf_dca6_$USER_SFX.csv" --log_file_name "svf_dca6_$USER_SFX.log" --timeout 2000 --property_user "navdb_ro" --property_dsn "(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST=euxb009s.eux.de.int.automotive-wan.com)(PORT=1521)(SEND_BUF_SIZE=)(RECV_BUF_SIZE=))(LOAD_BALANCE=yes))(CONNECT_DATA=(SERVICE_NAME=stemppo_1_p_pdb.eux.de.int.automotive-wan.com)))" --property_password "navdb#r2g2nsb" --report_columns "Case+No.,ID,Expr.+No.,UT_Name,Filename,Line+No.,Backend,Work+Package,Tags,Requirements,Conducted,Passed,Timed+out,Elapsed+[s],Excep.,Var.+uninitialized,Var.+defaulted,Filtered+by+Variable,Cond.+Match,LOC,Severity+(0CBAS),Log+Text,Statement+-+unparsed,Statement+-+PARSED,Orig.+Expr.,Parsed+Expr.,Result+(max.+10+rows),Exception+Text,Type,Qualifier,Orig.+Cond.,Parsed+Cond.,Starttime,Endtime,Dbname+Match,Prod.+Match,Suppl.+Match,U+Match,LOC+Match,ID+Match,Filename+Match"
 
python_wrapper $RDF_COMPILER/gdfConvert/util/ut/ut.py  --test_user  svf_dca7_610 --spec_id 1804     --test_password nt\#r2g2nsB --test_service lizard1 --user_types "svf,rdf+svf" --trun_context PRODUCTION --trun_label "SVF_KW22_13: svf_dca7_$USER_SFX" --root_path $RDF_COMPILER/gdfConvert/util/ut/test_case_root --maxThreads 20 --loc 3 --report_with_variables_list --report_format excel_csv --report_file_name "svf_dca7_$USER_SFX.csv" --log_file_name "svf_dca7_$USER_SFX.log" --timeout 2000 --property_user "navdb_ro" --property_dsn "(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST=euxb009s.eux.de.int.automotive-wan.com)(PORT=1521)(SEND_BUF_SIZE=)(RECV_BUF_SIZE=))(LOAD_BALANCE=yes))(CONNECT_DATA=(SERVICE_NAME=stemppo_1_p_pdb.eux.de.int.automotive-wan.com)))" --property_password "navdb#r2g2nsb" --report_columns "Case+No.,ID,Expr.+No.,UT_Name,Filename,Line+No.,Backend,Work+Package,Tags,Requirements,Conducted,Passed,Timed+out,Elapsed+[s],Excep.,Var.+uninitialized,Var.+defaulted,Filtered+by+Variable,Cond.+Match,LOC,Severity+(0CBAS),Log+Text,Statement+-+unparsed,Statement+-+PARSED,Orig.+Expr.,Parsed+Expr.,Result+(max.+10+rows),Exception+Text,Type,Qualifier,Orig.+Cond.,Parsed+Cond.,Starttime,Endtime,Dbname+Match,Prod.+Match,Suppl.+Match,U+Match,LOC+Match,ID+Match,Filename+Match"
 
python_wrapper $RDF_COMPILER/gdfConvert/util/ut/ut.py  --test_user  svf_dca8_610 --spec_id 1804     --test_password nt\#r2g2nsB --test_service lizard1 --user_types "svf,rdf+svf" --trun_context PRODUCTION --trun_label "SVF_KW22_13: svf_dca8_$USER_SFX" --root_path $RDF_COMPILER/gdfConvert/util/ut/test_case_root --maxThreads 20 --loc 3 --report_with_variables_list --report_format excel_csv --report_file_name "svf_dca8_$USER_SFX.csv" --log_file_name "svf_dca8_$USER_SFX.log" --timeout 2000 --property_user "navdb_ro" --property_dsn "(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST=euxb009s.eux.de.int.automotive-wan.com)(PORT=1521)(SEND_BUF_SIZE=)(RECV_BUF_SIZE=))(LOAD_BALANCE=yes))(CONNECT_DATA=(SERVICE_NAME=stemppo_1_p_pdb.eux.de.int.automotive-wan.com)))" --property_password "navdb#r2g2nsb" --report_columns "Case+No.,ID,Expr.+No.,UT_Name,Filename,Line+No.,Backend,Work+Package,Tags,Requirements,Conducted,Passed,Timed+out,Elapsed+[s],Excep.,Var.+uninitialized,Var.+defaulted,Filtered+by+Variable,Cond.+Match,LOC,Severity+(0CBAS),Log+Text,Statement+-+unparsed,Statement+-+PARSED,Orig.+Expr.,Parsed+Expr.,Result+(max.+10+rows),Exception+Text,Type,Qualifier,Orig.+Cond.,Parsed+Cond.,Starttime,Endtime,Dbname+Match,Prod.+Match,Suppl.+Match,U+Match,LOC+Match,ID+Match,Filename+Match"

python_wrapper $RDF_COMPILER/gdfConvert/util/ut/ut.py  --test_user  svf_dca9_610 --spec_id 1804    --test_password nt\#r2g2nsB --test_service lizard1 --user_types "svf,rdf+svf" --trun_context PRODUCTION --trun_label "SVF_KW22_13: svf_dca9_$USER_SFX" --root_path $RDF_COMPILER/gdfConvert/util/ut/test_case_root --maxThreads 20 --loc 3 --report_with_variables_list --report_format excel_csv --report_file_name "svf_dca9_$USER_SFX.csv" --log_file_name "svf_dca9_$USER_SFX.log" --timeout 2000 --property_user "navdb_ro" --property_dsn "(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST=euxb009s.eux.de.int.automotive-wan.com)(PORT=1521)(SEND_BUF_SIZE=)(RECV_BUF_SIZE=))(LOAD_BALANCE=yes))(CONNECT_DATA=(SERVICE_NAME=stemppo_1_p_pdb.eux.de.int.automotive-wan.com)))" --property_password "navdb#r2g2nsb" --report_columns "Case+No.,ID,Expr.+No.,UT_Name,Filename,Line+No.,Backend,Work+Package,Tags,Requirements,Conducted,Passed,Timed+out,Elapsed+[s],Excep.,Var.+uninitialized,Var.+defaulted,Filtered+by+Variable,Cond.+Match,LOC,Severity+(0CBAS),Log+Text,Statement+-+unparsed,Statement+-+PARSED,Orig.+Expr.,Parsed+Expr.,Result+(max.+10+rows),Exception+Text,Type,Qualifier,Orig.+Cond.,Parsed+Cond.,Starttime,Endtime,Dbname+Match,Prod.+Match,Suppl.+Match,U+Match,LOC+Match,ID+Match,Filename+Match"
 
python_wrapper $RDF_COMPILER/gdfConvert/util/ut/ut.py  --test_user  svf_dca10_610 --spec_id 1804    --test_password nt\#r2g2nsB --test_service lizard1 --user_types "svf,rdf+svf" --trun_context PRODUCTION --trun_label "SVF_KW22_13: svf_dca10_$USER_SFX" --root_path $RDF_COMPILER/gdfConvert/util/ut/test_case_root --maxThreads 20 --loc 3 --report_with_variables_list --report_format excel_csv --report_file_name "svf_dca10_$USER_SFX.csv" --log_file_name "svf_dca10_$USER_SFX.log" --timeout 2000 --property_user "navdb_ro" --property_dsn "(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST=euxb009s.eux.de.int.automotive-wan.com)(PORT=1521)(SEND_BUF_SIZE=)(RECV_BUF_SIZE=))(LOAD_BALANCE=yes))(CONNECT_DATA=(SERVICE_NAME=stemppo_1_p_pdb.eux.de.int.automotive-wan.com)))" --property_password "navdb#r2g2nsb" --report_columns "Case+No.,ID,Expr.+No.,UT_Name,Filename,Line+No.,Backend,Work+Package,Tags,Requirements,Conducted,Passed,Timed+out,Elapsed+[s],Excep.,Var.+uninitialized,Var.+defaulted,Filtered+by+Variable,Cond.+Match,LOC,Severity+(0CBAS),Log+Text,Statement+-+unparsed,Statement+-+PARSED,Orig.+Expr.,Parsed+Expr.,Result+(max.+10+rows),Exception+Text,Type,Qualifier,Orig.+Cond.,Parsed+Cond.,Starttime,Endtime,Dbname+Match,Prod.+Match,Suppl.+Match,U+Match,LOC+Match,ID+Match,Filename+Match"
 
python_wrapper $RDF_COMPILER/gdfConvert/util/ut/ut.py  --test_user  svf_dca11_610 --spec_id 1804 	--test_password nt\#r2g2nsB --test_service lizard1 --user_types "svf,rdf+svf" --trun_context PRODUCTION --trun_label "SVF_KW22_13: svf_dca11_$USER_SFX" --root_path $RDF_COMPILER/gdfConvert/util/ut/test_case_root --maxThreads 20 --loc 3 --report_with_variables_list --report_format excel_csv --report_file_name "svf_dca11_$USER_SFX.csv" --log_file_name "svf_dca11_$USER_SFX.log" --timeout 2000 --property_user "navdb_ro" --property_dsn "(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST=euxb009s.eux.de.int.automotive-wan.com)(PORT=1521)(SEND_BUF_SIZE=)(RECV_BUF_SIZE=))(LOAD_BALANCE=yes))(CONNECT_DATA=(SERVICE_NAME=stemppo_1_p_pdb.eux.de.int.automotive-wan.com)))" --property_password "navdb#r2g2nsb" --report_columns "Case+No.,ID,Expr.+No.,UT_Name,Filename,Line+No.,Backend,Work+Package,Tags,Requirements,Conducted,Passed,Timed+out,Elapsed+[s],Excep.,Var.+uninitialized,Var.+defaulted,Filtered+by+Variable,Cond.+Match,LOC,Severity+(0CBAS),Log+Text,Statement+-+unparsed,Statement+-+PARSED,Orig.+Expr.,Parsed+Expr.,Result+(max.+10+rows),Exception+Text,Type,Qualifier,Orig.+Cond.,Parsed+Cond.,Starttime,Endtime,Dbname+Match,Prod.+Match,Suppl.+Match,U+Match,LOC+Match,ID+Match,Filename+Match"
 
python_wrapper $RDF_COMPILER/gdfConvert/util/ut/ut.py   --test_user  svf_dca12_610 --spec_id 1804	--test_password nt\#r2g2nsB --test_service lizard1 --user_types "svf,rdf+svf" --trun_context PRODUCTION --trun_label "SVF_KW22_13: svf_dca12_$USER_SFX" --root_path $RDF_COMPILER/gdfConvert/util/ut/test_case_root --maxThreads 20 --loc 3 --report_with_variables_list --report_format excel_csv --report_file_name "svf_dca12_$USER_SFX.csv" --log_file_name "svf_dca12_$USER_SFX.log" --timeout 2000 --property_user "navdb_ro" --property_dsn "(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST=euxb009s.eux.de.int.automotive-wan.com)(PORT=1521)(SEND_BUF_SIZE=)(RECV_BUF_SIZE=))(LOAD_BALANCE=yes))(CONNECT_DATA=(SERVICE_NAME=stemppo_1_p_pdb.eux.de.int.automotive-wan.com)))" --property_password "navdb#r2g2nsb" --report_columns "Case+No.,ID,Expr.+No.,UT_Name,Filename,Line+No.,Backend,Work+Package,Tags,Requirements,Conducted,Passed,Timed+out,Elapsed+[s],Excep.,Var.+uninitialized,Var.+defaulted,Filtered+by+Variable,Cond.+Match,LOC,Severity+(0CBAS),Log+Text,Statement+-+unparsed,Statement+-+PARSED,Orig.+Expr.,Parsed+Expr.,Result+(max.+10+rows),Exception+Text,Type,Qualifier,Orig.+Cond.,Parsed+Cond.,Starttime,Endtime,Dbname+Match,Prod.+Match,Suppl.+Match,U+Match,LOC+Match,ID+Match,Filename+Match"
 
python_wrapper $RDF_COMPILER/gdfConvert/util/ut/ut.py   --test_user	 svf_dca13_610 --spec_id 1804	--test_password nt\#r2g2nsB --test_service lizard1 --user_types "svf,rdf+svf" --trun_context PRODUCTION --trun_label "SVF_KW22_13: svf_dca13_$USER_SFX" --root_path $RDF_COMPILER/gdfConvert/util/ut/test_case_root --maxThreads 20 --loc 3 --report_with_variables_list --report_format excel_csv --report_file_name "svf_dca13_$USER_SFX.csv" --log_file_name "svf_dca13_$USER_SFX.log" --timeout 2000 --property_user "navdb_ro" --property_dsn "(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST=euxb009s.eux.de.int.automotive-wan.com)(PORT=1521)(SEND_BUF_SIZE=)(RECV_BUF_SIZE=))(LOAD_BALANCE=yes))(CONNECT_DATA=(SERVICE_NAME=stemppo_1_p_pdb.eux.de.int.automotive-wan.com)))" --property_password "navdb#r2g2nsb" --report_columns "Case+No.,ID,Expr.+No.,UT_Name,Filename,Line+No.,Backend,Work+Package,Tags,Requirements,Conducted,Passed,Timed+out,Elapsed+[s],Excep.,Var.+uninitialized,Var.+defaulted,Filtered+by+Variable,Cond.+Match,LOC,Severity+(0CBAS),Log+Text,Statement+-+unparsed,Statement+-+PARSED,Orig.+Expr.,Parsed+Expr.,Result+(max.+10+rows),Exception+Text,Type,Qualifier,Orig.+Cond.,Parsed+Cond.,Starttime,Endtime,Dbname+Match,Prod.+Match,Suppl.+Match,U+Match,LOC+Match,ID+Match,Filename+Match"
 
python_wrapper $RDF_COMPILER/gdfConvert/util/ut/ut.py   --test_user  svf_dca14_610 --spec_id 1804	--test_password nt\#r2g2nsB --test_service lizard1 --user_types "svf,rdf+svf" --trun_context PRODUCTION --trun_label "SVF_KW22_13: svf_dca14_$USER_SFX" --root_path $RDF_COMPILER/gdfConvert/util/ut/test_case_root --maxThreads 20 --loc 3 --report_with_variables_list --report_format excel_csv --report_file_name "svf_dca14_$USER_SFX.csv" --log_file_name "svf_dca14_$USER_SFX.log" --timeout 2000 --property_user "navdb_ro" --property_dsn "(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST=euxb009s.eux.de.int.automotive-wan.com)(PORT=1521)(SEND_BUF_SIZE=)(RECV_BUF_SIZE=))(LOAD_BALANCE=yes))(CONNECT_DATA=(SERVICE_NAME=stemppo_1_p_pdb.eux.de.int.automotive-wan.com)))" --property_password "navdb#r2g2nsb" --report_columns "Case+No.,ID,Expr.+No.,UT_Name,Filename,Line+No.,Backend,Work+Package,Tags,Requirements,Conducted,Passed,Timed+out,Elapsed+[s],Excep.,Var.+uninitialized,Var.+defaulted,Filtered+by+Variable,Cond.+Match,LOC,Severity+(0CBAS),Log+Text,Statement+-+unparsed,Statement+-+PARSED,Orig.+Expr.,Parsed+Expr.,Result+(max.+10+rows),Exception+Text,Type,Qualifier,Orig.+Cond.,Parsed+Cond.,Starttime,Endtime,Dbname+Match,Prod.+Match,Suppl.+Match,U+Match,LOC+Match,ID+Match,Filename+Match"
 
python_wrapper $RDF_COMPILER/gdfConvert/util/ut/ut.py   --test_user	 svf_dca1_610 --spec_id 1804  	--test_password nt\#r2g2nsB --test_service lizard1 --user_types "svf,rdf+svf" --trun_context PRODUCTION --trun_label "SVF_KW22_13: svf_dca1_$USER_SFX" --root_path $RDF_COMPILER/gdfConvert/util/ut/test_case_root --maxThreads 20 --loc 3 --report_with_variables_list --report_format excel_csv --report_file_name "svf_dca1_$USER_SFX.csv" --log_file_name "svf_dca1_$USER_SFX.log" --timeout 2000 --property_user "navdb_ro" --property_dsn "(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST=euxb009s.eux.de.int.automotive-wan.com)(PORT=1521)(SEND_BUF_SIZE=)(RECV_BUF_SIZE=))(LOAD_BALANCE=yes))(CONNECT_DATA=(SERVICE_NAME=stemppo_1_p_pdb.eux.de.int.automotive-wan.com)))" --property_password "navdb#r2g2nsb" --report_columns "Case+No.,ID,Expr.+No.,UT_Name,Filename,Line+No.,Backend,Work+Package,Tags,Requirements,Conducted,Passed,Timed+out,Elapsed+[s],Excep.,Var.+uninitialized,Var.+defaulted,Filtered+by+Variable,Cond.+Match,LOC,Severity+(0CBAS),Log+Text,Statement+-+unparsed,Statement+-+PARSED,Orig.+Expr.,Parsed+Expr.,Result+(max.+10+rows),Exception+Text,Type,Qualifier,Orig.+Cond.,Parsed+Cond.,Starttime,Endtime,Dbname+Match,Prod.+Match,Suppl.+Match,U+Match,LOC+Match,ID+Match,Filename+Match"
 
python_wrapper $RDF_COMPILER/gdfConvert/util/ut/ut.py  --test_user  svf_mex_610 --spec_id 1804   	--test_password nt\#r2g2nsB --test_service lizard1 --user_types "svf,rdf+svf" --trun_context PRODUCTION --trun_label "SVF_KW22_13: svf_mex_$USER_SFX" --root_path $RDF_COMPILER/gdfConvert/util/ut/test_case_root --maxThreads 20 --loc 3 --report_with_variables_list --report_format excel_csv --report_file_name "svf_mex_$USER_SFX.csv" --log_file_name "svf_mex_$USER_SFX.log" --timeout 2000 --property_user "navdb_ro" --property_dsn "(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST=euxb009s.eux.de.int.automotive-wan.com)(PORT=1521)(SEND_BUF_SIZE=)(RECV_BUF_SIZE=))(LOAD_BALANCE=yes))(CONNECT_DATA=(SERVICE_NAME=stemppo_1_p_pdb.eux.de.int.automotive-wan.com)))" --property_password "navdb#r2g2nsb" --report_columns "Case+No.,ID,Expr.+No.,UT_Name,Filename,Line+No.,Backend,Work+Package,Tags,Requirements,Conducted,Passed,Timed+out,Elapsed+[s],Excep.,Var.+uninitialized,Var.+defaulted,Filtered+by+Variable,Cond.+Match,LOC,Severity+(0CBAS),Log+Text,Statement+-+unparsed,Statement+-+PARSED,Orig.+Expr.,Parsed+Expr.,Result+(max.+10+rows),Exception+Text,Type,Qualifier,Orig.+Cond.,Parsed+Cond.,Starttime,Endtime,Dbname+Match,Prod.+Match,Suppl.+Match,U+Match,LOC+Match,ID+Match,Filename+Match"
 
python_wrapper $RDF_COMPILER/gdfConvert/util/ut/ut.py   --test_user  svf_dca15_610 --spec_id 1804	--test_password nt\#r2g2nsB --test_service lizard1 --user_types "svf,rdf+svf" --trun_context PRODUCTION --trun_label "SVF_KW22_13: svf_dca15_$USER_SFX" --root_path $RDF_COMPILER/gdfConvert/util/ut/test_case_root --maxThreads 20 --loc 3 --report_with_variables_list --report_format excel_csv --report_file_name "svf_dca15_$USER_SFX.csv" --log_file_name "svf_dca15_$USER_SFX.log" --timeout 2000 --property_user "navdb_ro" --property_dsn "(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST=euxb009s.eux.de.int.automotive-wan.com)(PORT=1521)(SEND_BUF_SIZE=)(RECV_BUF_SIZE=))(LOAD_BALANCE=yes))(CONNECT_DATA=(SERVICE_NAME=stemppo_1_p_pdb.eux.de.int.automotive-wan.com)))" --property_password "navdb#r2g2nsb" --report_columns "Case+No.,ID,Expr.+No.,UT_Name,Filename,Line+No.,Backend,Work+Package,Tags,Requirements,Conducted,Passed,Timed+out,Elapsed+[s],Excep.,Var.+uninitialized,Var.+defaulted,Filtered+by+Variable,Cond.+Match,LOC,Severity+(0CBAS),Log+Text,Statement+-+unparsed,Statement+-+PARSED,Orig.+Expr.,Parsed+Expr.,Result+(max.+10+rows),Exception+Text,Type,Qualifier,Orig.+Cond.,Parsed+Cond.,Starttime,Endtime,Dbname+Match,Prod.+Match,Suppl.+Match,U+Match,LOC+Match,ID+Match,Filename+Match"
"""
}
}

def main():
    for name, meta in files.items():
        with open(name, 'w', newline='\n') as f:
            f.write(meta["content"])
        if meta.get("executable"):
            st = os.stat(name)
            os.chmod(name, st.st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
        print(f"Created: {name}")
    print("All files generated in: " + os.getcwd())

if __name__ == "__main__":
    main()
