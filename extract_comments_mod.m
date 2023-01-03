% Example of how to read the comments associated with each of the working 
% days of the marine debris collection service carried out by the Balearic 
% Agency for Water and Environmental Quality (ABAQUA).
% Diego Vega Gimenez, 10/8/2022

clc
clear 
close all

% List all comments
load 'Mallorca2005_2022_concat_dates_illa.mat'
Mal=table2cell(Mal); % For convenience

allcom={};
% for nf=1:size(D,1)
    comment=D(:,14);
    iok=~cellfun(@isempty,comment);
%     disp(comment(iok))
    allcom=cat(1,allcom,comment(iok));
% end
   
% Eiminate unusable rows 
ibad=cellfun(@ischar,allcom(:)); % identify rows that are not 'char'
ibadlist=find(ibad~=1);          % Select all comments except those of ibad
for nf=1:length(ibadlist)
    allcom{ibadlist(nf)}='empty'; % Fill in the blanks with 'empty'.
end

% Comments list
typcom=unique(allcom);
% disp(typcom)

% Seeing the comments we can establish some rules - For example with this 
% rule we find the comments associated with having bad sea and we can put a 
% "Flag" in case we want to discard them later these entries

% nindex=find((contains(D(:,14),'mal') | contains(D(:,14),'Mal') | contains(D(:,14),'MAL')| ...
%     contains(D(:,14),'Avaria')| contains(D(:,14),'AVARIA')| contains(D(:,14),'avaria')| ...
%     contains(D(:,14),'Averia')| contains(D(:,14),'AVERIA')| contains(D(:,14),'averia')| ...
%     contains(D(:,14),'Patro')| contains(D(:,14),'PATRO')| contains(D(:,14),'patro')) ...
%     & ~contains(D(:,14),'malalt'));

nindex=find((contains(typcom,'mal') | contains(typcom,'Mal') | contains(typcom,'MAL')| ...
    contains(typcom,'Avaria')| contains(typcom,'AVARIA')| contains(typcom,'avaria')| ...
    contains(typcom,'Averia')| contains(typcom,'AVERIA')| contains(typcom,'averia')| ...
    contains(typcom,'Patro')| contains(typcom,'PATRO')| contains(typcom,'patro')) ...
    & ~contains(typcom,'malalt'));

com={};
for i =1:length(D(:,14))
    if ~isempty(D(i,14))
        print(i)
        find((contains(i,'mal') | contains(i,'Mal') | contains(i,'MAL')| ...
            contains(i,'Avaria')| contains(i,'AVARIA')| contains(i,'avaria')| ...
            contains(i,'Averia')| contains(i,'AVERIA')| contains(i,'averia')| ...
            contains(i,'Patro')| contains(i,'PATRO')| contains(i,'patro')) ...
            & ~contains(i,'malalt'))
    end
end
    

% Extract how many unique routes there are

Rutes={D{:,12}};
RutesCheck={D{:,17}};
RutesUniques=unique(Rutes);
RutesUniquesCheck=unique(RutesCheck);

% Confirm that routes are correct
rutesok = find(cellfun(@isequal,RutesCheck,Rutes));
