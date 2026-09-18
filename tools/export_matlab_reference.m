function export_matlab_reference(upstreamRoot, outputFile)
% Reproduce fixtures using unmodified WarpFactory at the pinned commit.
addpath(genpath(upstreamRoot));
if isempty(ver('parallel'))
    addpath(fullfile(fileparts(mfilename('fullpath')),'matlab_cpu_compat'),'-begin');
end
output.commit = '03b10cb02e73998af28db87201a43f2fa0e30319';
output.runtime = version;
output.generated_utc = char(datetime('now','TimeZone','UTC'));
output.c = c;
output.G = G;
cases = {'minkowski', 'alcubierre_static', 'alcubierre_dynamic'};
for ci = 1:length(cases)
    name = cases{ci};
    grid = [5,5,5,5];
    spacing = [0.25/c, 0.5, 0.5, 0.5];
    center = (grid+1)/2.*spacing;
    velocity = 0.2;
    if strcmp(name,'minkowski')
        metric = metricGet_Minkowski(grid,spacing);
    else
        if strcmp(name,'alcubierre_static')
            grid = [1,5,5,5]; center = (grid+1)/2.*spacing;
        end
        metric = metricGet_Alcubierre(grid,center,velocity,0.8,2,spacing);
    end
    item.grid = grid; item.spacing = spacing; item.center = center;
    item.metric = packTensor(metric.tensor,grid);
    inverse = c4Inv(metric.tensor);
    item.ricci_second = packTensor(ricciT2(inverse,metric.tensor,spacing),grid);
    item.ricci_fourth = packTensor(ricciT(inverse,metric.tensor,spacing),grid);
    energy2 = getEnergyTensor(metric,0,'second');
    energy4 = getEnergyTensor(metric,0,'fourth');
    item.energy_second = packTensor(energy2.tensor,grid);
    item.energy_fourth = packTensor(energy4.tensor,grid);
    frame = doFrameTransfer(metric,energy4,'Eulerian');
    item.eulerian = packTensor(frame.tensor,grid);
    [expansion,shear,vorticity] = getScalars(metric);
    item.expansion = packArray(expansion,grid);
    item.shear = packArray(shear,grid);
    item.vorticity = packArray(vorticity,grid);
    item.null = packArray(getEnergyConditions(energy4,metric,'Null',12,3,0),grid);
    item.weak = packArray(getEnergyConditions(energy4,metric,'Weak',12,3,0),grid);
    item.strong = packArray(getEnergyConditions(energy4,metric,'Strong',12,3,0),grid);
    item.dominant = packArray(getEnergyConditions(energy4,metric,'Dominant',12,3,0),grid);
    output.(name) = item;
end
fid=fopen(outputFile,'w');
assert(fid ~= -1,'Cannot open output file');
cleanup=onCleanup(@() fclose(fid));
fwrite(fid,jsonencode(output),'char');
fprintf('Exported independent MATLAB reference to %s\n',outputFile);
end

function packed = packTensor(tensor,grid)
array=zeros([4,4,grid]);
for i=1:4
    for j=1:4
        array(i,j,:,:,:,:) = reshape(tensor{i,j},[1,1,grid]);
    end
end
packed=packArray(array,[4,4,grid]);
end

function packed = packArray(array,shape)
packed.shape=shape;
packed.data=array(:);
end
