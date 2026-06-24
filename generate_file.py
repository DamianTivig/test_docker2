#!/usr/bin/env python3
"""
Script to generate all configuration/script files for RDF/SVF pipeline.
"""

import os
import stat

def write_file(filename, content, executable=False):
    """Write content to a file and optionally make it executable."""
    with open(filename, 'w', newline='\n') as f:
        f.write(content)
    if executable:
        st = os.stat(filename)
        os.chmod(filename, st.st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
    print(f"  Created: {filename}")


def generate_svf_patch_csh():
    content = r"""#!/bin/csh
 
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
    write_file("SVF_PATCH.csh", content, executable=True)


def generate_rdf_na_611_xml():
    content = r"""<?xml version="1.0" encoding="UTF-8"?>
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
    write_file("RDF_NA_611.XML", content)


def generate_r2s_na_611_cfg():
    content = r""";#################################################################################
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
    write_file("R2S_NA_611.CFG", content)


def generate_log_checker_pl():
    content = r"""#!/usr/bin/perl -w
 
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
    write_file("log_checker.pl", content, executable=True)


def generate_load_na_611_csh():
    content = r"""#!/bin/csh
 
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
    write_file("LOAD_NA_611.CSH", content, executable=True)


def generate_load_cfg_na_cfg():
    content = r"""#!/bin/csh
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
    write_file("LOAD_CFG_NA.cfg", content)


def generate_extract_2_load_pl():
    content = r"""#!/usr/bin/perl -w
 
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
    write_file("extract_2_load.pl", content, executable=True)


def generate_errorcheck_csh():
    content = r"""#!/bin/csh -f
 
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
  # for new strings, need to be added in