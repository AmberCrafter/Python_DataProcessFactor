How to use it?
1. Setting information in "/config/config.json"
    a. ["Backup"]["RawfilePath"]=${Original_file_path}
    b. If need to specify some file, please entry them into ["Backup"]["RawfileList"] by sring format in list.
2. <Note> Output folder can't specify now, please move the output file by manual.
3. main.py is single process choose, or use scheduleRun.py to set the program auto run.

<!!--NOTE--!!>
當程式無預期當機後，請務必檢查以下各點的資料是否同步，若無同步，請手動同步到標準資料時間，再啟動此程式。
1. Rawfile.
2. logfile recode context in type "INFO".
3. All files in temp folder please "BACKUP" and remove first.  <BACKUP is important>.
3. L0, L1 datafiles in L0 and L1 folder.

Change Log
<v1.1.5 and below>
1. Fix DataQC filelist is not correct, which transport from L0 filelist.
2. Append logging module to recode backup_copy.py INFO, which recode the last row of number in this cycle done in Rawfile(LoggerNet).
3. Recode all the bugs that I known and not fix.
4. Append the process how to do in this code.

<v1.1.1>
1. Append backup copy process.
2. Append schedule setting.
3. Fix DataQC Bug when L0 or L1 are not a new file.

<v1.0.0>
1. First Edition of auto processing data.
Note. This code need a lot of optimization and arrange.

<v0.0.1>
1. Recode some test code.
