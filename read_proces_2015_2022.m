clear all
close all
clc

myFolder = 'C:\Users\diego.vega\Desktop\Datos\datos_i_2015_2022';

% Make sure that the file exists, otherwise 'Warn user'.

if ~isfolder(myFolder)
    errorMessage = sprintf('Error: The following folder does not exist:\n%s\nPlease specify a new folder.', myFolder);
    uiwait(warndlg(errorMessage));
    myFolder = uigetdir(); % Ask for a new one.
    if myFolder == 0
         return;
    end
end

% Create a list of all .xlsx files in the subfolders   
filePattern = fullfile(myFolder, '**/*.xlsx');
theFiles = dir(filePattern);
for k = 1 : length(theFiles) % k is equal to the total number of days, start: 2015,05,01 end: 2022,09,30 
    baseFileName = theFiles(k).name;
    fullFileName = fullfile(theFiles(k).folder, baseFileName);

%   add all necessary parameters for each season from 2015 to 2022

    if fileparts(fileparts(fullFileName)) == fullfile('C:\Users\diego.vega\Desktop\Datos\datos_i_2015_2021\R2015')
        V1mal=1:33;
        V1men=35:50;
        V1eiv=52:62;
        V1for=63:64;
        V2mal=1:13;
        V2men=15:20;
        V2eiv=22:26;
        V2for=[];

        sheetname='Virot 2';

        route='C:\Users\diego.vega\Desktop\Datos\Rutas\dades_rutes_2015-16.xlsx';
        routemal=1:46;
        routemen=48:69;
        routeeiv=71:86;
        routefor=88:89;

        t2015=datetime(2015,05,01):datetime(2015,09,30);

    elseif fileparts(fileparts(fullFileName)) == fullfile('C:\Users\diego.vega\Desktop\Datos\datos_i_2015_2021\R2016')
        V1mal=1:33;
        V1men=35:50;
        V1eiv=52:62;
        V1for=63:64;
        V2mal=1:13;
        V2men=15:20;
        V2eiv=22:26;
        V2for=[];

        sheetname='Virot 2';

        route='C:\Users\diego.vega\Desktop\Datos\Rutas\dades_rutes_2016.xlsx';
        routemal=1:46;
        routemen=48:69;
        routeeiv=71:86;
        routefor=88:89;

        t2016=datetime(2016,06,01):datetime(2016,09,30);

    elseif fileparts(fileparts(fullFileName)) == fullfile('C:\Users\diego.vega\Desktop\Datos\datos_i_2015_2021\R2017')
        V1mal=1:33;
        V1men=35:50;
        V1eiv=52:62;
        V1for=63:64;
        V2mal=1:11;
        V2men=13:16;
        V2eiv=18:20;
        V2for=[];
        
        sheetname='VIROT2';

        route='C:\Users\diego.vega\Desktop\Datos\Rutas\dades_rutes_2017.xlsx';
        routemal=1:44;
        routemen=46:65;
        routeeiv=67:80;
        routefor=82:83;

        t2017=datetime(2017,07,01):datetime(2017,09,30);

    elseif fileparts(fileparts(fullFileName)) == fullfile('C:\Users\diego.vega\Desktop\Datos\datos_i_2015_2021\R2018')
        V1mal=1:30;
        V1men=32:48;
        V1eiv=50:61;
        V1for=63:64;
        V2mal=1:13;
        V2men=15:19;
        V2eiv=21:24;
        V2for=26;
        
        sheetname='VIROT 2';

        route='C:\Users\diego.vega\Desktop\Datos\Rutas\dades_rutes_2018.xlsx';
        routemal=1:43;
        routemen=45:66;
        routeeiv=68:83;
        routefor=85:87;

        t2018=datetime(2018,05,01):datetime(2018,09,30);

    elseif fileparts(fileparts(fullFileName)) == fullfile('C:\Users\diego.vega\Desktop\Datos\datos_i_2015_2021\R2019')
        V1mal=1:30;
        V1men=32:48;
        V1eiv=50:61;
        V1for=63:64;
        V2mal=1:13;
        V2men=15:19;
        V2eiv=21:24;
        V2for=26;

        sheetname='VIROT 2';

        route='C:\Users\diego.vega\Desktop\Datos\Rutas\dades_rutes_2019.xlsx';
        routemal=1:43;
        routemen=45:66;
        routeeiv=68:83;
        routefor=85:87;

        t2019=datetime(2019,05,01):datetime(2019,09,30);

    elseif fileparts(fileparts(fullFileName)) == fullfile('C:\Users\diego.vega\Desktop\Datos\datos_i_2015_2021\R2021')
        V1mal=1:30;
        V1men=32:48;
        V1eiv=50:61;
        V1for=63:64;
        V2mal=1:14;
        V2men=16:20;
        V2eiv=22:25;
        V2for=27;

        sheetname='VIROT-LITORAL 2';

        route='C:\Users\diego.vega\Desktop\Datos\Rutas\dades_rutes_2021.xlsx';
        routemal=1:44;
        routemen=46:67;
        routeeiv=69:84;
        routefor=86:88;

        t2021=datetime(2021,06,01):datetime(2021,09,30);

    elseif fileparts(fileparts(fullFileName)) == fullfile('C:\Users\diego.vega\Desktop\Datos\datos_i_2015_2021\R2022')
        V1mal=1:30;
        V1men=32:48;
        V1eiv=50:61;
        V1for=63:64;
        V2mal=1:14;
        V2men=16:20;
        V2eiv=22:25;
        V2for=27;

        sheetname='VIROT-LITORAL 2';

        route='C:\Users\diego.vega\Desktop\Datos\Rutas\dades_rutes_2021.xlsx';
        routemal=1:44;
        routemen=46:67;
        routeeiv=69:84;
        routefor=86:88;

        t2021=datetime(2022,06,01):datetime(2022,09,30);
    end

    fprintf(1, 'Now reading %s\n', fullFileName);

%   ----------- READ THE FIRST SHEET OF EACH EXCEL (VIROT 1) --------------

    virot1{k}=readtable(fullfile(fullFileName)); 
    virot1{k}=table2cell(virot1{k}); 

    for ix=2:size(virot1{1,k},1) % Add the name of the port to each route
        if isempty(virot1{k}{ix,2})
            virot1{k}{ix,2} = virot1{k}{ix-1,2};
        end
    end

    for ix=2:size(virot1{1,k},1) % Add the name of the ships to each route
        if isempty(virot1{k}{ix,3})
            virot1{k}{ix,3} = virot1{k}{ix-1,3};
        end
    end

    virot1{k}=virot1{k}(~any(cellfun(@isempty,virot1{k}(:,16)),2),:); % delete rows without associated routes
    

%     mallorca1{k}=virot1{k}(V1mal,[2:3,7:end]); 
%     menorca1{k}=virot1{k}(V1men,[2:3,7:end]);
%     eivissa1{k}=virot1{k}(V1eiv,[2:3,7:end]);
%     formentera1{k}=virot1{k}(V1for,[2:3,7:end]);

    %----------- READ TEH SECOND SHEET OF EACH EXCEL (VIROT 2) -----------

    virot2{k}=readtable(fullfile(fullFileName), 'Sheet', sheetname); 
    virot2{k}=table2cell(virot2{k}); 
   
    for ix=2:size(virot2{1,k},1) % Add the name of the port to each route
        if isempty(virot2{k}{ix,2})
            virot2{k}{ix,2} = virot2{k}{ix-1,2};
        end
    end

    for ix=2:size(virot2{1,k},1) % Add the name of the ships to each route
        if isempty(virot2{k}{ix,3})
            virot2{k}{ix,3} = virot2{k}{ix-1,3};
        end
    end
%     
    virot2{k}=virot2{k}(~any(cellfun(@isempty,virot2{k}(:,16)),2),:); % delete rows without associated routes
%   
%     mallorca2{k}=virot2{k}(V2mal,[2:3,7:end]); 
%     menorca2{k}=virot2{k}(V2men,[2:3,7:end]);
%     eivissa2{k}=virot2{k}(V2eiv,[2:3,7:end]);
%     formentera2{k}=virot2{k}(V2for,[2:3,7:end]);
% 
%   -------- CONCATENATE THE DATA OF THE TWO SHEETS -----------------------
% 
    Mallorca{k}=cat(1,mallorca1{k},mallorca2{k});
    Menorca{k}=cat(1,menorca1{k},menorca2{k});
    Eivissa{k}=cat(1,eivissa1{k},eivissa2{k});
    Formentera{k}=cat(1,formentera1{k},formentera2{k});
% 
% 
%     % -------------- ADDING ROUTES --------------------------------------
% 
%   MALLORCA
    routes=readtable(route);
    routes=table2cell(routes);
    Mallorca=[Mallorca';routes(routemal,:)]';
%   Mallorca{k}(:,16:18)=[]

%   MENORCA
    routes=readtable(route);
    routes=table2cell(routes);
    Menorca=[Menorca';routes(routemen,:)]';
%   Menorca{k}(:,16:18)=[]

%   EIVISSA
    routes=readtable(route);
    routes=table2cell(routes);
    Eivissa=[Eivissa';routes(routeeiv,:)]';
%   Eivissa{k}(:,16:18)=[]

%   FORMENTERA
    routes=readtable(route);
    routes=table2cell(routes);
    Formentera=[Formentera';routes(routefor,:)]';
%   Formentera{k}(:,16:18)=[]

%     % -------------- ADD BINARY COLUMN DEPENDING ON PRESENCE OF COMMENTS -----------------------------------------
%     
%     for j = Mallorca{k,1}(:,14);
%             obs=cellfun(@isnan,j,'UniformOutput', false);
%     end
%     Mallorca=[Mallorca{k},obs];
% 
%     for j = Menorca{k,1}(:,14);
%             obs=cellfun(@isnan,j,'UniformOutput', false);
%     end
%     Menorca=[Menorca{k},obs];
% 
%     for j = Eivissa{k,1}(:,14);
%             obs=cellfun(@isnan,j,'UniformOutput', false);
%     end
%     Eivissa=[Eivissa{k},obs];
% 
%     for j = Formentera{k,1}(:,14);
%             obs=cellfun(@isnan,j,'UniformOutput', false);
%     end
%     Formentera=[Formentera{k},obs];

    %  ------------- COMPROVAM QUE LES DADES SIGUIN CORRECTES -------------
    
    for i = 1:size(Mallorca{1},1)
        if Mallorca{i}(1,12)~=Mallorca{i}(1,18)
        if ~isequal(Mallorca{i}(1,12),Mallorca{i}(1,18))
            errorMessage = sprintf('Error: Routes and Data do not match:\n%s\n.', 'Mallorca{i}{1,12}');
            uiwait(warndlg(errorMessage))
        end
    end
     
end

% -------------- ADD DATES TO EACH ROW -------------------------------------

    t=[t2015,t2016,t2017,t2018,t2019,t2021,t2022]';
    dates=cellstr(t);
    Mallorca=[Mallorca',dates];
    Menorca=[Menorca', dates];
    Eivissa=[Eivissa', dates];
    Formentera=[Formentera', dates];
    
    save('Mallorca2015-21.mat','Mallorca');
    save('Menorca2015-21.mat','Menorca');
    save('Eivissa2015-21.mat','Eivissa');
    save('Formentera2015-21.mat',"Formentera");
