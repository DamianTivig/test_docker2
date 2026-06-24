#!/bin/bash

set -e

read -p "Enter BASE path: " BASE
read -p "Enter DELIVERY name: " DELIVERY
read -p "Enter VERSION: " VERSION

REMOTE_USER="uie74356"
REMOTE_HOST="10.198.127.171"
REMOTE_BASE="${BASE}/${DELIVERY}/${VERSION}"

echo "Connecting to server..."

# Step 1: Create directory structure
ssh -o StrictHostKeyChecking=no ${REMOTE_USER}@${REMOTE_HOST} "
export TERM=xterm
mkdir -p ${REMOTE_BASE}/Scripts
mkdir -p ${REMOTE_BASE}/Tests/RDF
mkdir -p ${REMOTE_BASE}/Tests/SIZE
mkdir -p ${REMOTE_BASE}/Tests/SVF
mkdir -p ${REMOTE_BASE}/Tests/UT
mkdir -p ${REMOTE_BASE}/Tests/load/allfiles
mkdir -p ${REMOTE_BASE}/Tests/load/rdfdeploy
mkdir -p ${REMOTE_BASE}/patches
echo 'Directory structure created.'
"

# Step 2: Create generate_files.py locally in /tmp, then scp it
TMPFILE=$(mktemp /tmp/generate_files_XXXXXX.py)

cat > "$TMPFILE" << 'PYEOF'
#!/usr/bin/env python3
"""
Generates all configuration/script files into the correct subdirectories.
Run this from the VERSION root directory (parent of Scripts/, Tests/).
"""
import os
import stat

def write_file(filepath, content, executable=False):
    dirpath = os.path.dirname(filepath)
    if dirpath and not os.path.exists(dirpath):
        os.makedirs(dirpath, exist_ok=True)
    with open(filepath, 'w', newline='\n') as f:
        f.write(content)
    if executable:
        st = os.stat(filepath)
        os.chmod(filepath, st.st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
    print(f"  Created: {filepath}")

# ============================================================
# SCRIPTS DIRECTORY FILES
# ============================================================

scripts_files = {}

scripts_files["Scripts/SVF_PATCH.csh"] = {"executable": True, "content": r"""#!/bin/csh
 
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
"""}

scripts_files["Scripts/RDF_NA_611.XML"] = {"executable": False, "content": r"""<?xml version="1.0" encoding="UTF-8"?>
<Workflow xmlns="http://navtech.com" 
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
    xmlns:log4j="http://jakarta.apache.org/log4j/" 
    xsi:schemaLocation="http://navtech.com RDFConfigSchema.xsd"
>
<GlobalConfiguration>
    <Property Name="echo" Value="on"/>
    <Property Name="timing" Value="on"/>
    <Property Name="ParallelFactor" Value="4"/>
    <Property Name="LoaderFilePath" Value="LOADER_FILES"/>
    <Property Name="DBUser" Value="RDF_NA_610"/>
    <Property Name="DBPassword" Value="nt#r2g2nsB"/>
    <Property Name="JDBCURL" Value="jdbc:oracle:thin:RDF_NA_610/atadmin@//iadb101v.ia.ro.int.automotive-wan.com:1521/sgdf_1_P_PDB.ia.ro.int.automotive-wan.com" />
    <Property Name="SID" Value="lizard1"/>
    <SQLConnection Name="default" User="${DBUser}" Password="${DBPassword}" Instance="${SID}" Url="${JDBCURL}" />
    <Transport Name="default" type="JDBCTransportType" Code="JDBC" Default="true">
        <Class>com.navtech.maptools.transport.jdbc.JDBCTransport</Class>
        <JDBCDriver>oracle.jdbc.driver.OracleDriver</JDBCDriver>
        <ConnectionString>${JDBCURL}</ConnectionString>
        <DatabaseUser>${DBUser}</DatabaseUser>
        <DatabasePassword>${DBPassword}</DatabasePassword>
    </Transport>
</GlobalConfiguration>
<log4j:configuration xmlns:log4j="http://jakarta.apache.org/log4j/">
    <appender name="STDOUT" class="org.apache.log4j.ConsoleAppender">
        <layout class="org.apache.log4j.PatternLayout">
            <param name="ConversionPattern" value="[%r] - %-5p-> %m%n"/>
        </layout>
    </appender>
    <appender name="LogFile" class="org.apache.log4j.FileAppender">
        <param name="File" value="RDF_NA_610.LOG"/>
        <param name="Append" value="true"/>
        <layout class="org.apache.log4j.PatternLayout">
            <param name="ConversionPattern" value="%d %-5p - %m%n"/>
        </layout>
    </appender>
    <category name="com.navtech">
        <priority value="info"/>
        <Param name="Additivity" value="false" />
        <appender-ref ref="LogFile"/>
    </category>
    <category name="com.navtech.util.framework.WorkflowController">
        <priority value="info"/>
    </category>
    <root>
        <priority value="warn"/>
        <appender-ref ref="STDOUT"/>
    </root>
</log4j:configuration>
</Workflow>
"""}

scripts_files["Scripts/R2S_NA_611.CFG"] = {"executable": False, "content": r""";#################################################################################
;R2S generic 
;#################################################################################
R2S_RDF_AREA = NA
R2S_RUN_RDF_CHECK=yes
R2S_RUN_PART1=yes
R2S_RUN_PART2=yes
R2S_RDF_OLD_DB_USER = RDF_NA_510
R2S_RDF_OLD_DB_PASSWORD = nt#r2g2nsB
R2S_RDF_OLD_DB_SERVICE = lizard1
R2S_LOG_DIR=log
R2S_SCRIPTS =/PROJ/db4/db/RDF/NA/2026Q1_SeSp/2025R4_RDF_North_America_251H0/611/Scripts/compiler/gdfConvert/svf/RDF2SVF
R2S_COMMON_SCRIPTS=/PROJ/db4/db/RDF/NA/2026Q1_SeSp/2025R4_RDF_North_America_251H0/611/Scripts/compiler/gdfConvert/scripts
R2S_DATAMODEL_SCRIPTS=/PROJ/db4/db/RDF/NA/2026Q1_SeSp/2025R4_RDF_North_America_251H0/611/Scripts/compiler/gdfConvert/svf/data_model
R2S_RDF_DB_USER = RDF_NA_611
R2S_RDF_DB_PASSWORD = nt#r2g2nsB
R2S_RDF_DB_SERVICE = lizard1
R2S_STOP_ON_ERRORS = no
;#################################################################################
;R2S Part 1
;#################################################################################
R2SP1_DROP_TMP_TABLES = no
R2S_BUA_LOAD = no
R2S_BUA_PATH =
R2S_BUA_FILE =
;#################################################################################
;R2S Part 2
;#################################################################################
R2SP2_DB_ADMIN_USER=atadmin
R2SP2_DB_ADMIN_PASSW=At1dm3nS
R2SP2_PARALLEL=3
R2SP2_DROP_TMP_TABLES = no   
R2SP2_STOP_IF_SVF_USERS_EXIST = no 
R2SP2_TO_RUN= DCA1 DCA2 DCA3 DCA4 DCA5 DCA6 DCA7 DCA8 DCA9 DCA10 DCA11 DCA12 DCA13 DCA14 MEX DCA15
DCA1=SVF_DCA1_611 nt#r2g2nsB 921 0 lizard1
DCA2=SVF_DCA2_611 nt#r2g2nsB 922 0 lizard1
DCA3=SVF_DCA3_611 nt#r2g2nsB 923 0 lizard1
DCA4=SVF_DCA4_611 nt#r2g2nsB 924 0 lizard1
DCA5=SVF_DCA5_611 nt#r2g2nsB 925 0 lizard1
DCA6=SVF_DCA6_611 nt#r2g2nsB 926 0 lizard1
DCA7=SVF_DCA7_611 nt#r2g2nsB 927 0 lizard1
DCA8=SVF_DCA8_611 nt#r2g2nsB 928 0 lizard1
DCA9=SVF_DCA9_611 nt#r2g2nsB 929 0 lizard1
DCA10=SVF_DCA10_611 nt#r2g2nsB 930 0 lizard1
DCA11=SVF_DCA11_611 nt#r2g2nsB 931 0 lizard1
DCA12=SVF_DCA12_611 nt#r2g2nsB 932 0 lizard1
DCA13=SVF_DCA13_611 nt#r2g2nsB 933 0 lizard1
DCA14=SVF_DCA14_611 nt#r2g2nsB 934 0 lizard1
DCA15=SVF_DCA15_611 nt#r2g2nsB 935 0 lizard1
MEX=SVF_MEX_611 nt#r2g2nsB 484 0 lizard1
R2S_META_SVF_SPEC_VER=3.20
R2S_META_RELEASE_VER=R2S_1.17.2_RC2
R2S_META_RELEASE_DATE=100226
R2S_META_COMPATIBILITY=2025R4
"""}

scripts_files["Scripts/LOAD_CFG_NA.cfg"] = {"executable": True, "content": r"""#!/bin/csh
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
set SP_SERVER=dragon1
set SP_USER=atadmin
set SP_PASS=At1dm3nS
set SVF_PATCH_LINE="source $SCRIPTS_HOME/SVF_PATCH.csh"
###############################################################################################################
set BRANCH_NAME=R2S_1.17.2_RC2
set BRANCH_NAME_UT=UTSQL_2.6_RC3
set UID=uie74356
###############################################################################################################
set MAIN_AREA=na
set RDF_AREA=NA
set RDF_CN=19
set RDF_USER="RDF_${RDF_AREA}_${DSUFIX}"
set CFG_XML="RDF_${RDF_AREA}_${DSUFIX}.XML"
set R2S_CFG="$SCRIPTS_HOME/R2S_${RDF_AREA}_${DSUFIX}.CFG"
###############################################################################################################
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
###########################
"""}

scripts_files["Scripts/LOAD_NA_611.CSH"] = {"executable": True, "content": r"""#!/bin/csh
 
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
 
set SOURCE_CFG=LOAD_CFG_NA.cfg
source ./$SOURCE_CFG
echo RDF home directory is: $RDF_HOME
echo SCRIPTS home directory is: $SCRIPTS_HOME
 
set LOGS_DIR=log
 
if ( -d $LOGS_DIR) then
	mv -v $LOGS_DIR $LOGS_DIR\_${TIMESTAMP}
	mkdir -p $LOGS_DIR
else
	mkdir -p $LOGS_DIR
endif
 
cat $SOURCE_CFG > $LOGS_DIR/${TIMESTAMP}_${SOURCE_CFG}

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

source ./$SOURCE_CFG
 
if ($COPY_DATA == "1") then
echo ===============================================================================================
echo `date`: Part I -- Prepare all files for Load
echo ===============================================================================================
cd $RDF_HOME
mkdir -p load
cd load
cp -v $ARCHIVE_CORE_DATA/*.* .
cp -v $ARCHIVE_SLOPE_DATA/*.* .
cd $SCRIPTS_HOME
endif

source ./$SOURCE_CFG
 
if ($EXTRACT_2_LOAD == "1") then
perl $SCRIPTS_HOME/extract_2_load.pl $SCRIPTS_HOME/../../load |& tee $SCRIPTS_HOME/$LOGS_DIR/extract_2_load.log
./errorCheck.csh $SCRIPTS_HOME/$LOGS_DIR/extract_2_load.log
cd $SCRIPTS_HOME
echo "Subject: $RDF_AREA $DSUFIX EXTRACT TO LOAD finished..." | sendmail $MY_EMAIL
echo Pause 1 minute...
sleep 60
endif

source ./$SOURCE_CFG

if ($GREP_MD5 == "1") then
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
cd $SCRIPTS_HOME
endif

source ./$SOURCE_CFG

if ($REN_RDF_CUS_SOFT == "1") then
cd $RDF_HOME/load
if ( -d rdfdeploy ) then
	rm -rf rdfdeploy
	echo Old rdfdeploy folder was found and removed for new one ...
else
	echo Renaming rdf_customer_software to rdfdeploy started ...
endif
find . -depth -type d -name '*rdf_customer_software' -exec mv {} rdfdeploy \;
cd $SCRIPTS_HOME
endif

source ./$SOURCE_CFG

if ($CP_MV_ALLFILES == "1") then
cd $RDF_HOME/load
mkdir -p $RDF_TOOL/RDF/LOADER_FILES/CORE/
mkdir -p $RDF_TOOL/RDF/LOADER_FILES/ADAS/
cp -r *CORE*/CORE/*.* $RDF_TOOL/RDF/LOADER_FILES/CORE/
cp -r *ADAS*/ADAS/*.* $RDF_TOOL/RDF/LOADER_FILES/ADAS/
cd $RDF_HOME/load
mkdir -p allfiles
foreach i (`ls $RDF_HOME/load | grep -vw "allfiles" | grep -vw "rdfdeploy" | grep -vE '^\.{1,2}'`)
mv -v $RDF_HOME/load/$i $RDF_HOME/load/allfiles/
end
echo "Subject: $RDF_AREA $DSUFIX Prepare RDF & Load finished..." | sendmail $MY_EMAIL
cd $SCRIPTS_HOME
endif

source ./$SOURCE_CFG

if ($CLEAN_USERS == "1") then
cd $SCRIPTS_HOME
sqlplus atadmin/At1dm3nS@lizard1 @drop_users.sql >& drop_users.log
./errorCheck.csh $SCRIPTS_HOME/drop_users.log
cd $SCRIPTS_HOME
echo Pause 1 minute...
sleep 60
endif

cd $SCRIPTS_HOME
source ./$SOURCE_CFG

if ($START_RDF == "1") then
echo ===============================================================================================
echo `date`: START_RDF
echo ===============================================================================================
cd $SCRIPTS_HOME
$RDF_COMPILER/gdfConvert/scripts/create_oracle_user.csh atadmin At1dm3nS $RDF_USER $PASSWORD $SERVER |& tee $SCRIPTS_HOME/$LOGS_DIR/create_user_$RDF_USER.log
./errorCheck.csh $SCRIPTS_HOME/$LOGS_DIR/create_user_$RDF_USER.log
echo "Subject: `date` $RDF_AREA $DSUFIX RDF_USER done..." | sendmail $MY_EMAIL
chmod 775 $SCRIPTS_HOME/$CFG_XML
chmod 775 $RDF_TOOL/RDF/rdf_installer.*
chmod -R 775 $RDF_TOOL/RDF/LOADER_FILES
chmod -R 775 $RDF_HOME/load
cp -vf $SCRIPTS_HOME/$CFG_XML $RDF_TOOL/RDF/BIN/etc/xml/$CFG_XML
cd $RDF_TOOL/RDF
./rdf_installer.sh $RDF_BIN/etc/xml/$CFG_XML loadrdfCore |& tee $SCRIPTS_HOME/$LOGS_DIR/$RDF_USER.loadrdfCore.log
cd $SCRIPTS_HOME
source ./$SOURCE_CFG
set dir=$ADAS_DIR
set c=0
if ( -d ${dir} ) then
    set c=`ls -a ${dir} | wc | awk '{print $1}'`
    if ( "${c}" == 2 ) then
		echo "Empty directory - "${dir}
    else
		echo "Dir has files - "${dir}
		cd $RDF_TOOL/RDF
		./rdf_installer.sh $RDF_BIN/etc/xml/$CFG_XML loadADAS |& tee $SCRIPTS_HOME/$LOGS_DIR/$RDF_USER.loadADAS.log
    endif
else
      echo "Error: Not a directory"
endif
cd $SCRIPTS_HOME
source ./$SOURCE_CFG
cd $RDF_TOOL/RDF
./rdf_installer.sh $RDF_BIN/etc/xml/$CFG_XML PostImportStats |& tee $SCRIPTS_HOME/$LOGS_DIR/$RDF_USER.PostImportStats.log
cd $SCRIPTS_HOME
source ./$SOURCE_CFG
echo "Subject: $RDF_AREA $DSUFIX `date` CHECK WORKFLOW..." | sendmail $MY_EMAIL
egrep 'Workflow success.|Workflow FAILED. ' $SCRIPTS_HOME/$LOGS_DIR/*.{load,Post}*.log
echo "Subject: $RDF_AREA $DSUFIX Load finished..." | sendmail $MY_EMAIL
cd $SCRIPTS_HOME
endif

source ./$SOURCE_CFG

if ($START_R2S == "1") then
cd $SCRIPTS_HOME/$LOGS_DIR
$RDF_COMPILER/gdfConvert/svf/RDF2SVF/bin/r2s.pl $R2S_CFG |& tee $SCRIPTS_HOME/$LOGS_DIR/$RDF_USER.log
$SCRIPTS_HOME/errorCheck.csh $SCRIPTS_HOME/$LOGS_DIR/$RDF_USER.log
echo "Subject: $RDF_AREA $DSUFIX  R2S finished..." | sendmail $MY_EMAIL
cd $SCRIPTS_HOME
endif

cd $SCRIPTS_HOME
source ./$SOURCE_CFG

if ($RUN_PATCH == "1") then
eval $SVF_PATCH_LINE
cd $SCRIPTS_HOME
echo "Subject: $RDF_AREA $DSUFIX SVF PATCHES finished..." | sendmail $MY_EMAIL
endif

source ./$SOURCE_CFG

if ($RDF_ABAKUS == "1") then
cd $SCRIPTS_TEST/RDF
AbakusRDF.csh $OSUFIX R0 Y $DSUFIX R1 Y $ABAKUS_PROD results
cd $SCRIPTS_HOME
echo "Subject:RDF_ABAKUS finished..." | sendmail $MY_EMAIL
endif

source ./$SOURCE_CFG

if ($SVF_ABAKUS == "1") then
cd $SCRIPTS_TEST/SVF
AbakusSVF.csh $OSUFIX S0 Y $DSUFIX S1 Y $ABAKUS_PROD results
cd $SCRIPTS_HOME
echo "Subject: $RDF_AREA $DSUFIX SVF_ABAKUS finished..." | sendmail $MY_EMAIL
endif

source ./$SOURCE_CFG

if ($START_UTSQL == "1") then
cd $SCRIPTS_TEST/UT
runUT $DSUFIX >& runUT_$$.log
cd $SCRIPTS_HOME
echo "Subject: $RDF_AREA $DSUFIX  UTSQL finished..." | sendmail $MY_EMAIL
endif

source ./$SOURCE_CFG

if ($CALCULATE_SPACE == "1") then
cd $SCRIPTS_TEST/SIZE
sqlplus $SP_USER/$SP_PASS@$SP_SERVER @space_calculate.sql $DSUFIX >& space_calculate_${TIMESTAMP}.log
cd $SCRIPTS_HOME
echo "Subject: $RDF_AREA $DSUFIX CALCULATE_SPACE finished..." | sendmail $MY_EMAIL
endif

echo "Subject: $RDF_AREA $DSUFIX Tests on R2S & Load finished..." | sendmail $MY_EMAIL
"""}

scripts_files["Scripts/errorCheck.csh"] = {"executable": True, "content": r"""#!/bin/csh -f
 
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
  set c_num_err = `egrep -i -c "(^ORA-|SP2-|error|NoClassDefFoundError|Command not found|segmentation fault|Can not open|Can't open|Can not initialize|assertion failed|contains 0 POI categories|sorry|cannot access|not found in translation file|segment has no name|Fail to initialize|Retrieved 0 POI|No such file or directory|can't find or read input file|Stale NFS file handle|no match|text file busy|set: |Can't|tcsh current memory allocation|not a valid|not completed successfully|uninitialized|permission denied|hangup|You do not have|Undefined variable)" $C_LOGFILE`
  set t_err=`mktemp -t errorCheck_err.XXXXXX` || exit 1
  egrep -i "(^ORA-|SP2-|error|NoClassDefFoundError|Command not found|segmentation fault|Can not open|Can't open|Can not initialize|assertion failed|contains 0 POI categories|sorry|cannot access|not found in translation file|segment has no name|Fail to initialize|Retrieved 0 POI|No such file or directory|can't find or read input file|Stale NFS file handle|no match|text file busy|set: |Can't|tcsh current memory allocation|not a valid|not completed successfully|uninitialized|permission denied|hangup|You do not have|Undefined variable)" $C_LOGFILE | sort -du > $t_err
  set c_no_err = `egrep -i -c "(_error_|ErrorNum|no error|no  error|ErrorHandling|ORA-03292: Table to be|Checking Error Log|automatically placed in the error file|check_error|-fno-exceptions|arm_nr_exception_|exception segment|exception info|exceptions|_tmcp_chain_exception|XGetErrorDatabaseText|XGetErrorText|show errors|VALUE_ERROR|Will check log files for errors|Checking for new Errors|Checking for PEL and GPX errors|Checking tfumerge.master log file for errors|- Will check log files for errors|Checking for Feature File errors|checking for errors|R2S_STOP_ON_ERRORS)" $C_LOGFILE`
  set t_no_err=`mktemp -t errorCheck_no_err.XXXXXX` || exit 1
  egrep -i "(_error_|ErrorNum|no error|no  error|ErrorHandling|ORA-03292: Table to be|Checking Error Log|automatically placed in the error file|check_error|-fno-exceptions|arm_nr_exception_|exception segment|exception info|exceptions|_tmcp_chain_exception|XGetErrorDatabaseText|XGetErrorText|show errors|VALUE_ERROR|Will check log files for errors|Checking for new Errors|Checking for PEL and GPX errors|Checking tfumerge.master log file for errors|- Will check log files for errors|Checking for Feature File errors|checking for errors|R2S_STOP_ON_ERRORS)" $C_LOGFILE | sort -du > $t_no_err
  set c_result = `expr $c_num_err - $c_no_err`
  if ( $c_result > 0 ) then
    echo
    echo "ERRORS were found, view logfile: $C_LOGFILE"
	echo "-----------------------------------------------------------------------------------------"
	comm -3 $t_err $t_no_err
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
"""}

scripts_files["Scripts/log_checker.pl"] = {"executable": True, "content": r"""#!/usr/bin/perl -w
=comment
06.05.2013 Andrei Carp
=cut
use warnings;
use Cwd;
use Cwd 'abs_path';
use File::Basename;
use lib dirname(abs_path($0)); use List::MoreUtils qw(uniq);
my @bad_types = ("^ORA-","SP2-","error","NoClassDefFoundError","Command not found","segmentation fault","Can not open","Can not initialize","assertion failed","contains 0 POI categories","sorry","cannot access","not found in translation file","segment has no name","Fail to initialize","Retrieved 0 POI","No such file or directory","can't find or read input file","Stale NFS file handle","no match","text file busy","cannot create");
my @good_types = ("_error_","ErrorNum","no error","no  error","No error(s)","ErrorHandling","ORA-03292: Table to be","Checking Error Log","automatically placed in the error file","check_error","-fno-exceptions","arm_nr_exception_","exception segment","exception info","exceptions","_tmcp_chain_exception","XGetErrorDatabaseText","XGetErrorText","show errors","VALUE_ERROR","Will check log files for errors","Checking for new Errors","Checking for PEL and GPX errors","Checking tfumerge.master log file for errors","- Will check log files for errors");
my $print_equal = "=" x 100;
my $print_line = "-" x 100;
my $numArgs = $#ARGV + 1;
print "\nThanks, you gave me $numArgs command-line arguments.\n\n";
foreach my $arg (@ARGV) { print $arg, "\n"; }
print "\n\n";
my $cwd = getcwd();
my $log;
if ($numArgs == 0) {
    opendir LOGS, $cwd or die "Directory error: $!\n";
    my @files = grep /\.log$/, readdir LOGS;
    closedir LOGS;
    for $log (@files) { porcess_file($log); }
} elsif ($numArgs >= 1) {
    for $log (@ARGV) { porcess_file($log); }
} else { print "\tusage:\t$0 <logfile(s)>\n"; exit; }

sub porcess_file {
    my $logfile = $_[0]; my $type; my $line;
    my @bad_errors = (); my @good_errors = (); my @bad_errors_u = (); my @good_errors_u = (); my $result;
    open(LOGFILE,$logfile) or die("Could not open log file: $!\n");
    foreach $line (<LOGFILE>) {
        foreach $type (@bad_types) { if ($line =~ /$type/) { push(@bad_errors, $line); } }
        foreach $type (@good_types) { if ($line =~ /$type/) { push(@good_errors, $line); } }
    }
    close(LOGFILE) or die $!;
    $result = $#bad_errors-$#good_errors;
    if ($result > 0) {
        print "[NOK]\t$logfile\n";
        @bad_errors_u = uniq(@bad_errors); @good_errors_u = uniq(@good_errors);
        if ($#bad_errors+1 >= 1) { print_header("BAD ERRORS"); print join("", @bad_errors_u); }
        if ($#good_errors+1 >= 1) { print_header("GOOD ERRORS"); print join("", @good_errors_u); }
        print "$print_equal\n";
    } else { print "[ OK]\t$logfile\n"; }
}
sub print_header {
    my($h) = @_; my $s = ((100-length($h))/2);
    print "$print_line\n"; print " " x int($s),$h," " x int($s),"\n"; print "$print_line\n";
}
__END__
"""}

scripts_files["Scripts/extract_2_load.pl"] = {"executable": True, "content": r"""#!/usr/bin/perl -w
####################################################################################################
#  Script     : extract_2_load.pl
#  Author     : Andrei Carp
#  Date       : 07/19/2015
#  Last Edited: 08/20/2015, uidn3623
#  Description: extract recursively tar and gz archives
####################################################################################################
use strict;
use Cwd;
use File::Copy;
use Data::Dumper;
use File::Find;
use File::Basename;
my $delete_archives=0;
my $num_args = $#ARGV + 1;
if ($num_args != 1) { print "\nUsage: $0 [directory]\n"; exit; }
my $g_start_time = time();
my $echo_minus = '-' x 83;
my $echo_equal = '=' x 83;
my $directory = $ARGV[0];
my @array_files=();
print "\n"; print "$echo_equal\n";
&check_tool("tar"); &check_tool("gzip");
print "$echo_equal\n";
find(\&do_something_with_file, $directory);
@array_files = map { $_->[0] } sort { $a->[1] <=> $b->[1] } map { [ $_, !/\.tar$/ ] } @array_files;
while(my $archive = shift(@array_files)) { &do_extract($archive); }
print "\n"; print "$echo_equal\n";
my $g_end_time = time();
my $g_elapsed_time = sprintf("%d", $g_end_time - $g_start_time);
print "START TIME         : ". localtime($g_start_time) . "\n";
print "END TIME           : ". localtime($g_end_time) . "\n";
print "TOTAL ELAPSED TIME : ". &secondsToReadableTime($g_elapsed_time) . "\n";
print "$echo_equal\n"; print "\n";

sub do_something_with_file {
	my $file = $_;
	return unless (-f $file);
	return unless ($file =~ /\.tar$/) or ($file =~ /\.gz$/);
	push @array_files, $File::Find::name;
}
sub do_extract {
	my $i_file = $_[0];
	my($filename, $dirs, $suffix) = fileparse($i_file, qr/\.[^.]*/);
	chdir $dirs or die "Can't chdir into path: $dirs";
	for ($suffix) {
		if (/tar/) {
			mkdir $filename, 0775 or die "Warning: Cannot make ".$filename." directory: $!\n" if(!-d $filename);
			chdir $filename or die "Can't chdir into path: $filename";
			if ($delete_archives) { system "tar -xvf $i_file && rm $i_file"; }
			else { system "tar -xvf $i_file"; }
			find(\&do_something_with_md5, $dirs.$filename);
			find(\&do_something_with_file, $dirs.$filename);
		} elsif (/gz/) {
			system "gzip -dfv $i_file";
			find(\&do_something_with_file, $dirs.$filename);
		} else { print "[WARN]\tUnexpected extension: $filename$suffix\n"; }
	}
}
sub check_tool {
	my $i_toolname = $_[0]; my $tool_path = '';
	for my $path ( split /:/, $ENV{PATH} ) {
		if ( -f "$path/$i_toolname" && -x _ ) { $tool_path = "$path/$i_toolname"; last; }
	}
	die "No $i_toolname command available\n" unless ( $tool_path );
}
sub do_something_with_md5 {
	my $file = $_; my $t_md5log = "MD5result.log"; my $t_counter = 0;
	return unless (-f $file);
	return unless ($file =~ /MD5loaderfiles.txt$/) or ($file =~ /md5software.txt$/);
	&prepare_md5($File::Find::name);
	chdir ($File::Find::dir) or die ("Could not change directory: $!\n");
	if (-e $file) {
		my $runCmd="/usr/bin/md5sum -c $file > $t_md5log";
		my $t_exit_code=system($runCmd);
		if($t_exit_code!=0) { print "[WARN]\tCommand failed: $t_exit_code.\n"; exit($t_exit_code >> 8); }
	} else { print "[ERROR]\tFile does not exist! $file\n"; }
	my @lines=();
	open (MD5CHK, $t_md5log) or die ("Could not open file: $!");
	@lines = <MD5CHK>;
	foreach my $line (@lines){ if ($line =~ /\: FAILED/) { $t_counter++; } }
	close (MD5CHK);
	die "[INFO MD5]\tCheck found $t_counter errors\n" if ($t_counter > 0);
}
sub prepare_md5 {
	my $i_md5file = $_[0]; my $t_md5file = $i_md5file."tmp";
	copy ($i_md5file,$i_md5file.".org") or die ("Could not copy file: $!");
	my @data=();
	open (MD5IN, $i_md5file); @data = <MD5IN>;
	foreach my $line (@data) {
		$line =~ s/^;.+$//g; $line =~ s/\\/\//g; $line =~ s/\*//;
		$line =~ s/\*([A-Z]|[a-z])/\*\.\/$1/; $line =~ s/\r\n|\n|\r/\n/g;
		open (MD5OUT, '>>'.$t_md5file) or die ("Could not open file: $!");
		print MD5OUT "$line"; next;
	}
	close (MD5OUT); close (MD5IN);
	move ($t_md5file,$i_md5file) or die ("Could not move file: $!");
}
sub secondsToReadableTime () {
	my $t = shift(); my $h = int($t/(60*60)); my $m = int($t/60)%60; my $s = int($t)%60;
	return "$h hours, $m minutes, $s seconds ";
}
exit 0;
"""}

scripts_files["Scripts/drop_na_users.sql"] = {"executable": False, "content": r"""set echo on;
set timing on;
set def on;
drop user &1 cascade;
set echo off;
exit; 
"""}

scripts_files["Scripts/do_offline.csh"] = {"executable": True, "content": r"""#!/bin/csh
####################################################################################################
## FILE         : do_offline.csh
## VERSION      : 00.02
## AUTHOR       : Andrei02, Carp
## DESCRIPTION  : wrapper for screen command
####################################################################################################
if ($#argv == 0 || $#argv < 2) then
	goto help
endif
set SCREEN_NAME = $1
set SCREEN_LOG  = $2
if ($SCREEN_LOG !~ *".log") then
	echo "ERROR: Log file extension (.log) is missing..."
	goto help
endif
if(-e $SCREEN_NAME.cfg) then
	echo "WARN: $SCREEN_NAME.cfg already exists, deleting..."
	rm -f $SCREEN_NAME.cfg
endif
echo "startup_message off" >! $SCREEN_NAME.cfg
echo "logfile $SCREEN_LOG" >> $SCREEN_NAME.cfg
echo "flush 5" >> $SCREEN_NAME.cfg
shift
shift
echo "Running command: $*"
echo "Under screen name: $SCREEN_NAME with log file: $SCREEN_LOG"
screen -L -A -m -d -c $SCREEN_NAME.cfg -S $SCREEN_NAME $*
if  ($status != 0) then
	echo "ERROR: Screen command failed..."
	goto error
else 
	goto done
endif
help:
	echo "Usage: $0 <SCREEN_NAME> <SCREEN_LOGFILE> <RUN_COMMAND>"
	goto error
done:
	exit 0
error:
	exit 1
"""}

# ============================================================
# Tests/RDF DIRECTORY FILES
# ============================================================

scripts_files["Tests/RDF/AbakusRDF.csh"] = {"executable": True, "content": r"""#!/bin/csh

#abakus.csh 310 R1 N 311 R0 Y eu2013q1 results

echo ---------------------------------------------------------------------------
echo `date`: Abakus RDF Start
echo ---------------------------------------------------------------------------
set OLD = $1
set OLD_V = $2
set OLD_C = $3
set NEW = $4
set NEW_V = $5
set NEW_C = $6
set PRODUCT = $7
set TEST = 044
set TEST_V = R
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
perl /db/tools/Abakus2/bin/start_counting.pl RDF_NA_$OLD 505.19.$OLD.84$OLD_V RDF $PRODUCT/na /nt\#r2g2nsB@lizard1 >> AbakusCount.log
endif

if ("$NEW_C" == "Y") then
perl /db/tools/Abakus2/bin/start_counting.pl RDF_NA_$NEW 505.19.$NEW.84$NEW_V RDF $PRODUCT/na /nt\#r2g2nsB@lizard1 >> AbakusCount.log
endif

echo >>! AbakusCompare.log

perl /db/tools/Abakus2/bin/compare_dir.pl $PRODUCT/na/505.19.$NEW.84$NEW_V $PRODUCT/na/505.19.$OLD.84$OLD_V >>! AbakusCompare.log

grep "The result is located at" AbakusCount.log | tee AbakusCount_msg.log
grep "The result is located at" AbakusCompare.log | tee AbakusCompare_msg.log

echo 'Total number of Count results:' >>! AbakusCopy.log
grep -c "The result is located at" AbakusCount.log >> AbakusCopy.log
echo 'Total number of Count compare' >> AbakusCopy.log
grep -c "The result is located at" AbakusCompare.log >> AbakusCopy.log

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
"""}

# ============================================================
# Tests/SVF DIRECTORY FILES
# ============================================================

scripts_files["Tests/SVF/AbakusSVF.csh"] = {"executable": True, "content": r"""#!/bin/csh

#abakus.csh 511 S0 N 540 S0 Y eu2015q4 results

echo ---------------------------------------------------------------------------
echo `date`: Abakus SVF Start
echo ---------------------------------------------------------------------------
set OLD = $1
set OLD_V = $2
set OLD_C = $3
set NEW = $4
set NEW_V = $5
set NEW_C = $6
set PRODUCT = $7
set TEST = 044
set TEST_V = R
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
foreach region (dca1 dca2 dca3 dca4 dca5 dca6 dca7 dca8 dca9 dca10 dca11 dca12 dca13 dca14 dca15 mex)
set rnum = `echo $region | sed 's/dca//' | sed 's/mex/95/'`
perl /db/tools/Abakus2/bin/start_counting.pl svf_${region}_$OLD 505.${rnum}.$OLD.84$OLD_V SVF $PRODUCT/$region /nt\#r2g2nsB@lizard1 >> AbakusCount.log
end
endif

if ("$NEW_C" == "Y") then
foreach region (dca1 dca2 dca3 dca4 dca5 dca6 dca7 dca8 dca9 dca10 dca11 dca12 dca13 dca14 dca15 mex)
set rnum = `echo $region | sed 's/dca//' | sed 's/mex/95/'`
perl /db/tools/Abakus2/bin/start_counting.pl svf_${region}_$NEW 505.${rnum}.$NEW.84$NEW_V SVF $PRODUCT/$region /nt\#r2g2nsB@lizard1 >> AbakusCount.log
end
endif

echo >>! AbakusCompare.log

foreach region (dca1 dca2 dca3 dca4 dca5 dca6 dca7 dca8 dca9 dca10 dca11 dca12 dca13 dca14 dca15 mex)
set rnum = `echo $region | sed 's/dca//' | sed 's/mex/95/'`
perl /db/tools/Abakus2/bin/compare_dir.pl $PRODUCT/$region/505.${rnum}.$NEW.84$NEW_V $PRODUCT/$region/505.${rnum}.$OLD.84$OLD_V >> AbakusCompare.log
end

grep "The result is located at" AbakusCount.log | tee AbakusCount_msg.log
grep "The result is located at" AbakusCompare.log | tee AbakusCompare_msg.log

echo 'Total number of Count results:' >>! AbakusCopy.log
grep -c "The result is located at" AbakusCount.log >> AbakusCopy.log
echo 'Total number of Count compare' >> AbakusCopy.log
grep -c "The result is located at" AbakusCompare.log >> AbakusCopy.log

set TIMESTAMP = `date +%Y%b%d_%Hh%Mm%Ss`
if ( -d $RESULTS) then
	mv $RESULTS $RESULTS\_${TIMESTAMP}
	mkdir $RESULTS
else
	mkdir $RESULTS
endif

foreach region (dca1 dca2 dca3 dca4 dca5 dca6 dca7 dca8 dca9 dca10 dca11 dca12 dca13 dca14 dca15 mex)
set rnum = `echo $region | sed 's/dca//' | sed 's/mex/95/'`
cp -rfp $ABAKUS_RESULT/count_num/compare/505.${rnum}.$NEW.84$NEW_V\_with_505.${rnum}.$OLD.84$OLD_V . >> AbakusCopy.log
end

echo ---------------------------------------------------------------------------
echo `date`: Abakus SVF End
echo ---------------------------------------------------------------------------
"""}

# ============================================================
# Tests/SIZE DIRECTORY FILES
# ============================================================

scripts_files["Tests/SIZE/drop_users.sql"] = {"executable": False, "content": r"""set echo on;
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
drop user SVF_DCA1_310 CASCADE;
drop user SVF_DCA13_310 CASCADE;
drop user SVF_DCA8_310 CASCADE;
drop user ADAS_MEX_310 CASCADE;

set echo off;
exit; 
"""}

scripts_files["Tests/SIZE/space_calculate.sql"] = {"executable": False, "content": r"""set echo off
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

spool size_svf.csv append;

select 'USER;SIZE (GB);&1' from DUAL; 
select DS.OWNER as "USER", ROUND(SUM(DS.BYTES) / 1024 / 1024 / 1024, 2) as "GB"
FROM DBA_SEGMENTS DS
where DS.OWNER in ('RDF_NA_&1','SVF_DCA1_&1','SVF_DCA2_&1','SVF_DCA3_&1','SVF_DCA4_&1','SVF_DCA5_&1','SVF_DCA6_&1','SVF_DCA7_&1','SVF_DCA8_&1','SVF_DCA9_&1','SVF_DCA10_&1','SVF_DCA11_&1','SVF_DCA12_&1','SVF_DCA13_&1','SVF_DCA14_&1', 'svf_mex_&1','SVF_DCA15_&1')
group BY DS.OWNER;

spool off
exit;
"""}

# ============================================================
# Tests/UT DIRECTORY FILES
# ============================================================

scripts_files["Tests/UT/python_wrapper"] = {"executable": True, "content": r"""#!/bin/csh

setenv ORA_USER /PROJ/db4/dbteam/oracle
setenv ORA_CLIENTVERSION 19.3_32
setenv ORACLE_BASE /PROJ/db4/dbteam/oracle
setenv ORACLE_HOME "${ORA_USER}/product/${ORA_CLIENTVERSION}"
setenv TNS_ADMIN /PROJ/db4/dbteam/oracle/product/tns_admin/network/admin

setenv ORACLE_LIB ${ORACLE_HOME}/lib:/lib:/usr/lib
setenv LD_LIBRARY_PATH /usr/local/lib:${ORACLE_HOME}/lib:${DBTOOLS}/linux/local/lib

setenv ORACLE_DOC $ORACLE_HOME/doc
setenv ORACLE_SID GDF 
setenv ORACLE_TERM $TERM
setenv ORA_ROLLBACK_SEGMENT NONE
setenv ORA_NLS33 $ORACLE_HOME/nls/data

echo ORACLE_HOME has been set to $ORACLE_HOME
echo LD_LIBRARY_PATH has been set to $LD_LIBRARY_PATH

setenv PYTHONPATH /PROJ/db4/dbteam/tools/linux/localpython/lib:/PROJ/db4/dbteam/tools/linux/localpython/deploy/lib
setenv LD_LIBRARY_PATH /usr/local/lib:/opt/rational/clearcase/lib:/PROJ/db4/dbteam/oracle/product/19.3_32/lib:/PROJ/db4/dbteam/tools/linux/local/lib:/PROJ/db4/dbteam/tools/linux/localpython/libaio-0.3.112/deploy/lib:/PROJ/db4/dbteam/tools/linux/localpython/lib:/PROJ/db4/dbteam/tools/linux/localpython/deploy/lib

echo LD_LIBRARY_PATH has been set to $LD_LIBRARY_PATH

/PROJ/db4/dbteam/tools/linux/localpython/bin/python $*
"""}

scripts_files["Tests/UT/runUT"] = {"executable": True, "content": r"""#!/bin/sh

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

COMMON_ARGS="--test_password nt\#r2g2nsB --test_service lizard1 --trun_context PRODUCTION --root_path $RDF_COMPILER/gdfConvert/util/ut/test_case_root --maxThreads 20 --loc 3 --report_with_variables_list --report_format excel_csv --timeout 2000 --property_user navdb_ro --property_dsn (DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST=euxb009s.eux.de.int.automotive-wan.com)(PORT=1521)(SEND_BUF_SIZE=)(RECV_BUF_SIZE=))(LOAD_BALANCE=yes))(CONNECT_DATA=(SERVICE_NAME=stemppo_1_p_pdb.eux.de.int.automotive-wan.com))) --property_password navdb#r2g2nsb --report_columns Case+No.,ID,Expr.+No.,UT_Name,Filename,Line+No.,Backend,Work+Package,Tags,Requirements,Conducted,Passed,Timed+out,Elapsed+[s],Excep.,Var.+uninitialized,Var.+defaulted,Filtered+by+Variable,Cond.+Match,LOC,Severity+(0CBAS),Log+Text,Statement+-+unparsed,Statement+-+PARSED,Orig.+Expr.,Parsed+Expr.,Result+(max.+10+rows),Exception+Text,Type,Qualifier,Orig.+Cond.,Parsed+Cond.,Starttime,Endtime,Dbname+Match,Prod.+Match,Suppl.+Match,U+Match,LOC+Match,ID+Match,Filename+Match"

### RDF NA
python_wrapper $RDF_COMPILER/gdfConvert/util/ut/ut.py --test_user rdf_na_610 --spec_id 1804 --user_types "rdf" --trun_label "SVF_KW22_13: rdf_na_$USER_SFX" --report_file_name "rdf_na_$USER_SFX.csv" --log_file_name "rdf_na_$USER_SFX.log" $COMMON_ARGS

### SVF users
for region in dca2 dca3 dca4 dca5 dca6 dca7 dca8 dca9 dca10 dca11 dca12 dca13 dca14 dca1 dca15 mex; do
python_wrapper $RDF_COMPILER/gdfConvert/util/ut/ut.py --test_user svf_${region}_610 --spec_id 1804 --user_types "svf,rdf+svf" --trun_label "SVF_KW22_13: svf_${region}_$USER_SFX" --report_file_name "svf_${region}_$USER_SFX.csv" --log_file_name "svf_${region}_$USER_SFX.log" $COMMON_ARGS
done
"""}

# ============================================================
# MAIN
# ============================================================

def main():
    for filepath, meta in scripts_files.items():
        write_file(filepath, meta["content"], meta.get("executable", False))
    print("\n===== All files generated successfully =====")
    print("Generated in: " + os.getcwd())

if __name__ == "__main__":
    main()
PYEOF

# Step 3: Copy generate_files.py to remote server root VERSION directory
scp -o StrictHostKeyChecking=no "$TMPFILE" ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_BASE}/generate_files.py

# Step 4: Run it remotely from the VERSION root directory
ssh -o StrictHostKeyChecking=no ${REMOTE_USER}@${REMOTE_HOST} "
export TERM=xterm
cd ${REMOTE_BASE} || exit 1
python3 generate_files.py

echo ''
echo '========================================='
echo 'FILE LAYOUT:'
echo '========================================='
find . -type f | sort
echo '========================================='
echo 'DONE'
"

# Cleanup
rm -f "$TMPFILE"

echo ""
echo "All done! Files generated on remote server at: ${REMOTE_BASE}"
