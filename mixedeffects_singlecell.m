tbl = readtable('/Users/miramota/Desktop/Graphs/DataSheets/WIN_single_cell.xlsx');

[uniqueIDs, ~, ic] = unique(tbl.cell_ID);
counts = accumarray(ic, 1);


% Find cell_IDs that appear only once
singleOccurrenceIDs = uniqueIDs(counts == 1);


% Remove rows where cell_ID appears only once
ol_analysis = tbl(~ismember(tbl.cell_ID, singleOccurrenceIDs), :);
ol_analysis = ol_analysis(ol_analysis.cond ~= 0.5, :);


ol_analysis.cell_ID = categorical(ol_analysis.cell_ID);
ol_analysis.fish_ID = categorical(ol_analysis.fish_ID);
ol_analysis.cond = categorical(ol_analysis.cond);

mdl_nosheath_all = fitglme(ol_analysis, 'no_sheaths ~ cond*cell_age + (1|cell_ID) + (1|fish_ID)', FitMethod= 'REMPL')
mdl_nosheath_cell = fitglme(ol_analysis, 'no_sheaths ~ cond*cell_age + (1|cell_ID)', FitMethod='REMPL')
mdl_nosheath_fish = fitglme(ol_analysis, 'no_sheaths ~ cond*cell_age + (1|fish_ID)', FitMethod= 'REMPL')

mdl_avgsheath_all = fitglme(ol_analysis, 'avg_sheath_len ~ cond*cell_age + (1|cell_ID) + (1|fish_ID)', FitMethod= 'REMPL')
mdl_avgsheath_cell = fitglme(ol_analysis, 'avg_sheath_len ~ cond*cell_age + (1|cell_ID)', FitMethod= 'REMPL')
mdl_avgsheath_fish = fitglme(ol_analysis, 'avg_sheath_len ~ cond*cell_age + (1|fish_ID)', FitMethod= 'REMPL')

mdl_total_all = fitglme(ol_analysis, 'total_output ~ cond*cell_age + (1|cell_ID) + (1|fish_ID)', FitMethod= 'REMPL')

% these two are better than adding both random variables 
mdl_total_cell = fitglme(ol_analysis, 'avg_sheath_len ~ cond*cell_age + (1|cell_ID)', FitMethod= 'REMPL')
mdl_total_fish = fitglme(ol_analysis, 'avg_sheath_len ~ cond*cell_age + (1|fish_ID)', FitMethod= 'REMPL')

plotResiduals(mdl_nosheath_all)
plotResiduals(mdl_avgsheath_all)

