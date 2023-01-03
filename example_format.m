% Code to change the format of the complete database and make it suitable for
% further processing and analysis of the data. 
namein='data_2005_2022.mat';
header={'Port','Embarcacio','Kg','Volum','Fusta','MO','Plastics','Olis',...
    'Algues','Altres','Total','Rutes','Latitud_1','Longitud_1',...
    'Latitud_2','Longitud_2','distancia12','Ajuntament',...
    'Observacions','ObservacionsBoolean','Data'};

%%%%%%%%%%%%
load(namein)
% Ho col.locam per dies
DATA=struct('Time',[],'Boat',{});

icounter=0;
for nmonth=1:length(dades)
    dum=dades(nmonth).data;
    for nday=1:length(dum)
        icounter=icounter+1;
        disp(sprintf('>>> Count = %03i Nmonth=%02i Nday=%02i',icounter,nmonth,nday))
        toto=dum{nday};
        % Check the data
        tlist=nan(size(toto,1),1);
        for nboat=1:size(toto,1)
            tlist(nday)=datenum(toto{nboat,end});   %  
        end
        if nanstd(tlist)>0
            % Control to ensure dates are reasonable
            error(sprintf('Problem with the dates in month = %i and day = %i',nmonth,nday))
        end
        DATA(icounter).Time=nanmean(tlist); % Save the date in Matlab format
        % Information for the specific day
        boat=struct([]);
        for nboat=1:size(toto,1)
            for nfield=1:length(header)
                eval(['boat(' num2str(nboat) ').' header{nfield} '=toto{' num2str(nboat) ',' num2str(nfield) '};'])
            end
        end
        DATA(icounter).Boat=boat;
    end
end
      
nameout=[namein(1:end-4) '_newformat_prueba.mat'];
save(nameout,'DATA')

        
