%  Lanyu BSRN Radiation Observation
%  Level 0 to Level 1 Processing Program

clc;
clear all;
close all;

%% read filtering information

filter_head = 24;           % data_filter中 包含 "Start time(LT), End time(LT), Flag" 此行之前的行數
filter = importdata('./data_filter.txt',',',filter_head);

for i = filter_head + 1:size(filter.textdata,1)
    filter_start(i-filter_head,1:19) = filter.textdata{i,1}(1,1:19);
    filter_end(i-filter_head,1:19) = filter.textdata{i,2}(1,1:19);
end

for i = 1:size(filter.data,1)
    flag(i) = filter.data(i,1);
end

%% read L0 data

fid = fopen('Z:\Data\Instrument\Datalogger\CR1000_81819_Lanyu\L0\20180723_20180801\CR1000_81819_Lanyu_Rad_minute.dat','r');
tmp = textscan(fid,'%s',1,'headerlines',3);
tmp = tmp{1}(1:end);
item = length(strfind(tmp{1},',')) + 1;
form = repmat(' %s',[1 item]);
frewind(fid)
N = textscan(fid,form,3,'Delimiter',',','Headerlines',1);
form = repmat(' %f',[1 item-1]);
form = [' %s' form];
M = textscan(fid,form,'Delimiter',',');

for i = 2:size(M,2)
  M{i}(M{i}(:)<-200) = -999.99;
  M{i}(M{i}(:)>2500) = -999.99;
end

for i = 1:size(M{1},1)
    DATE(i,1) = M{1}(i);
    DATETIME(i)=datenum([str2num(DATE{i}(2:5)) str2num(DATE{i}(7:8)) str2num(DATE{i}(10:11)) ...
                         str2num(DATE{i}(13:14)) str2num(DATE{i}(16:17)) str2num(DATE{i}(19:20))]);
end

for i = 2:size(M,2)
  eval([N{i}{1}(2:end-1) '= M{i} ;']) ;
end

%% arrange data

output_time = DATETIME(1):1/1440:DATETIME(end);      % time in UTC

Batt_V(1,1:length(output_time)) = -999.99;
SWD_tot(1,1:length(output_time)) = -999.99;
SWD_dif(1,1:length(output_time)) = -999.99;
SWD_dir(1,1:length(output_time)) = -999.99;
LWD(1,1:length(output_time)) = -999.99;
UVB(1,1:length(output_time)) = -999.99;
UVE(1,1:length(output_time)) = -999.99;
PAR(1,1:length(output_time)) = -999.99;
mt_flag(1,1:length(output_time)) = -999.99;

for i = 1:length(DATETIME)
    
    xxx = find(abs(DATETIME(i) - output_time) < 0.00001);
    
    if (isempty(xxx) == 0)
        Batt_V(xxx(1)) = BattV_Min(i);
        SWD_tot(xxx(1)) = SWD_tot_watt_Avg(i);
        SWD_dif(xxx(1)) = SWD_dif_watt_Avg(i);
        SWD_dir(xxx(1)) = SWD_dir_watt_Avg(i);
        LWD(xxx(1)) = LWD_watt_Avg(i);
        UVB(xxx(1)) = UVB_watt_Avg(i);
        UVE(xxx(1)) = UVE_watt_Avg(i);
        PAR(xxx(1)) = PAR_watt_Avg(i);
        mt_flag(xxx(1)) = mt_flag_Tot(i);
    end
    
end

%% filter data by filtering information

% filter radiation data when doing maintenance 
maintain = find(mt_flag > 0);

SWD_tot(maintain) = -888.88;
SWD_dif(maintain) = -888.88;
SWD_dir(maintain) = -888.88;
LWD(maintain) = -888.88;
UVB(maintain) = -888.88;
UVE(maintain) = -888.88;
PAR(maintain) = -888.88;

for i = 1:size(flag,2)
    
    if flag(i) == 1           % wrong data (all sensors are suspected)
       f1 = find(output_time + datenum([0 0 0 8 0 0]) >=  datenum(filter_start(i,1:19)) & output_time + datenum([0 0 0 8 0 0]) <=  datenum(filter_end(i,1:19)));
       SWD_tot(f1) = -888.88;
       SWD_dif(f1) = -888.88;
       SWD_dir(f1) = -888.88;
       LWD(f1) = -888.88;
       UVB(f1) = -888.88;
       UVE(f1) = -888.88;
       PAR(f1) = -888.88;
       
    elseif flag(i) == 2       % power outage (SOLYS tracker didn't work. Incorrect CMP21D, CHP1, and CGR4 data)
       f2 = find(output_time + datenum([0 0 0 8 0 0]) >=  datenum(filter_start(i,1:19)) & output_time + datenum([0 0 0 8 0 0]) <=  datenum(filter_end(i,1:19)));
       SWD_dif(f2) = -888.88;
       SWD_dir(f2) = -888.88;
       LWD(f2) = -888.88;
       
    elseif flag(i) == 3       % shading problem (SOLYS tracker still working, but can't aim the Sun. Incorrect CMP21D, CHP1, and CGR4 data)
       f3 = find(output_time + datenum([0 0 0 8 0 0]) >=  datenum(filter_start(i,1:19)) & output_time + datenum([0 0 0 8 0 0]) <=  datenum(filter_end(i,1:19)));
       SWD_dif(f3) = -888.88;
       SWD_dir(f3) = -888.88;
       LWD(f3) = -888.88;
       
    elseif flag(i) == 4       % suspected data remove all SOLYS tracker data by personal judgement
       f4 = find(output_time + datenum([0 0 0 8 0 0]) >=  datenum(filter_start(i,1:19)) & output_time + datenum([0 0 0 8 0 0]) <=  datenum(filter_end(i,1:19)));
       SWD_dif(f4) = -888.88;
       SWD_dir(f4) = -888.88;
       LWD(f4) = -888.88;
       
    elseif flag(i) == 5       % suspected data remove all radiation platform data by personal judgement
       f5 = find(output_time + datenum([0 0 0 8 0 0]) >=  datenum(filter_start(i,1:19)) & output_time + datenum([0 0 0 8 0 0]) <=  datenum(filter_end(i,1:19)));
       SWD_tot(f5) = -888.88;
       UVB(f5) = -888.88;
       UVE(f5) = -888.88;
       PAR(f5) = -888.88;
       
    elseif flag(i) == 71      % wrong CMP21D (on SOLYS tracker)
       f71 = find(output_time + datenum([0 0 0 8 0 0]) >=  datenum(filter_start(i,1:19)) & output_time + datenum([0 0 0 8 0 0]) <=  datenum(filter_end(i,1:19)));
       SWD_dif(f71) = -888.88;
       
    elseif flag(i) == 72      % wrong CHP1 (on SOLYS tracker)
       f72 = find(output_time + datenum([0 0 0 8 0 0]) >=  datenum(filter_start(i,1:19)) & output_time + datenum([0 0 0 8 0 0]) <=  datenum(filter_end(i,1:19)));
       SWD_dir(f72) = -888.88;

    elseif flag(i) == 73      % wrong CGR4 (on SOLYS tracker)
       f73 = find(output_time + datenum([0 0 0 8 0 0]) >=  datenum(filter_start(i,1:19)) & output_time + datenum([0 0 0 8 0 0]) <=  datenum(filter_end(i,1:19)));
       LWD(f73) = -888.88;
       
    elseif flag(i) == 81      % wrong CMP21T (on radiation platform)
       f81 = find(output_time + datenum([0 0 0 8 0 0]) >=  datenum(filter_start(i,1:19)) & output_time + datenum([0 0 0 8 0 0]) <=  datenum(filter_end(i,1:19)));
       SWD_tot(f81) = -888.88;
       
    elseif flag(i) == 82      % wrong UVB (on radiation platform)
       f82 = find(output_time + datenum([0 0 0 8 0 0]) >=  datenum(filter_start(i,1:19)) & output_time + datenum([0 0 0 8 0 0]) <=  datenum(filter_end(i,1:19)));
       UVB(f82) = -888.88;
       
    elseif flag(i) == 83      % wrong UVE (on radiation platform) 
       f83 = find(output_time + datenum([0 0 0 8 0 0]) >=  datenum(filter_start(i,1:19)) & output_time + datenum([0 0 0 8 0 0]) <=  datenum(filter_end(i,1:19)));
       UVE(f83) = -888.88;
       
    elseif flag(i) == 84      % wrong PAR (on radiation platform)
       f84 = find(output_time + datenum([0 0 0 8 0 0]) >=  datenum(filter_start(i,1:19)) & output_time + datenum([0 0 0 8 0 0]) <=  datenum(filter_end(i,1:19)));
       PAR(f84) = -888.88;
       
    elseif flag(i) == 41      % no observation CMP21D (on SOLYS tracker)
       f41 = find(output_time + datenum([0 0 0 8 0 0]) >=  datenum(filter_start(i,1:19)) & output_time + datenum([0 0 0 8 0 0]) <=  datenum(filter_end(i,1:19)));
       SWD_dif(f41) = -999.99;
       
    elseif flag(i) == 42      % no observation CHP1 (on SOLYS tracker)
       f42 = find(output_time + datenum([0 0 0 8 0 0]) >=  datenum(filter_start(i,1:19)) & output_time + datenum([0 0 0 8 0 0]) <=  datenum(filter_end(i,1:19)));
       SWD_dir(f42) = -999.99;

    elseif flag(i) == 43      % no observation CGR4 (on SOLYS tracker)
       f43 = find(output_time + datenum([0 0 0 8 0 0]) >=  datenum(filter_start(i,1:19)) & output_time + datenum([0 0 0 8 0 0]) <=  datenum(filter_end(i,1:19)));
       LWD(f43) = -999.99;
       
    elseif flag(i) == 51      % no observation CMP21T (on radiation platform)
       f51 = find(output_time + datenum([0 0 0 8 0 0]) >=  datenum(filter_start(i,1:19)) & output_time + datenum([0 0 0 8 0 0]) <=  datenum(filter_end(i,1:19)));
       SWD_tot(f51) = -999.99;
       
    elseif flag(i) == 52      % no observation UVB (on radiation platform)
       f52 = find(output_time + datenum([0 0 0 8 0 0]) >=  datenum(filter_start(i,1:19)) & output_time + datenum([0 0 0 8 0 0]) <=  datenum(filter_end(i,1:19)));
       UVB(f52) = -999.99;
       
    elseif flag(i) == 53      % no observation UVE (on radiation platform) 
       f53 = find(output_time + datenum([0 0 0 8 0 0]) >=  datenum(filter_start(i,1:19)) & output_time + datenum([0 0 0 8 0 0]) <=  datenum(filter_end(i,1:19)));
       UVE(f53) = -999.99;
       
    elseif flag(i) == 54      % no observation PAR (on radiation platform)
       f54 = find(output_time + datenum([0 0 0 8 0 0]) >=  datenum(filter_start(i,1:19)) & output_time + datenum([0 0 0 8 0 0]) <=  datenum(filter_end(i,1:19)));
       PAR(f54) = -999.99;
    else
        
    end
    
end

%% filter radiation data when doing maintenance (已移到上方)

% maintain = find(mt_flag ~= 0);
% 
% SWD_tot(maintain) = -888.88;
% SWD_dif(maintain) = -888.88;
% SWD_dir(maintain) = -888.88;
% LWD(maintain) = -888.88;
% UVB(maintain) = -888.88;
% UVE(maintain) = -888.88;
% PAR(maintain) = -888.88;

%% write out to SOLARNET format

startday = datestr(fix(DATETIME(1)),'yyyymmdd');
endday = datestr(fix(DATETIME(end)),'yyyymmdd');

header = importdata('header.txt');

fid1 = fopen(['Z:\Data\Instrument\Datalogger\CR1000_81819_Lanyu\L1\' startday '_' endday '_Lanyu_L1.dat'],'w');

for i = 1:size(header,1)
    fprintf(fid1,'%1s\r\n', header{i,1});
end

output_date = datestr(output_time,'yyyy-mm-dd HH:MM:SS');

for i=1:length(output_time)
    fprintf(fid1,'"%19s",%7.2f,%7.2f,%7.2f,%7.2f,%7.2f,%7.2f,%7.2f,%7.2f \r\n',...
            output_date(i,:),Batt_V(i),SWD_tot(i),SWD_dif(i),SWD_dir(i),LWD(i),UVB(i),UVE(i),PAR(i));
end

fclose(fid1);

