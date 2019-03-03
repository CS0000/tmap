import pandas as pd
import csv,os
import pickle
import random
import string
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype
import numpy as np


def logger(*args,verbose=0):
    if verbose !=0:
        print(' '.join([str(_) for _ in args]))
    else:
        pass

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(stringLength))

def data_parser(path, ft='csv',verbose=1,**kwargs):
    if type(path) != str:
        df = path.copy()
        if type(df) != pd.DataFrame:
            df = pd.DataFrame(df)
        logger('Input data is a matrix: ', verbose=verbose)
    else:
        if ft == 'csv':
            sniffer = csv.Sniffer()
            sniffer.preferred = [',', '\t', '|']
            dialect = sniffer.sniff(open(path,'r').readline().strip('\n'))
            df = pd.read_csv(path, sep=dialect.delimiter,index_col=0, header=0, **kwargs)
        else:
            df = pd.read_excel(path, index_col=0, header=0, **kwargs)
        logger('Input data path: ', path,verbose=verbose)
    logger('Shape of Input data: ', df.shape,verbose=verbose)
    logger("Focus, this data means %s samples, and %s features. " % (str(df.shape[0]),
                                                                            str(df.shape[1])),verbose=verbose)
    return df

def preprocess_metadata_beta(data,metadata,drop_threshold=0.6,verbose=1):
    metadata = metadata.loc[data.index,:]
    if metadata.shape[0] == 0:
        logger("Couldn't find corresponding index from data into metadata",verbose=1)
        return
    # divide numeral cols and categorical cols
    numeric_cols = [col for col in metadata.columns if is_numeric_dtype(metadata.loc[:,col])]
    str_cols = [col for col in metadata.columns if is_string_dtype(metadata.loc[:, col])]
    sub_numeric = metadata.loc[:,numeric_cols]
    sub_str = metadata.loc[:,str_cols]
    # fill nan numeral cols
    drop_cols = []
    na_percent = sub_numeric.count(0)/sub_numeric.shape[0]
    drop_cols += list(sub_numeric.columns[na_percent <= drop_threshold])
    ### drop too much nan columns.
    logger('drop cols which nan values is over %s percent : ' % drop_threshold,','.join(drop_cols),verbose=verbose)
    sub_numeric = sub_numeric.loc[:,na_percent > drop_threshold]
    sub_numeric = sub_numeric.fillna({col:sub_numeric.median()[col] for col in sub_numeric.columns})
    # one hot / get dummy categorical cols
    drop_cols = []
    num_cat = np.array([len(set(sub_str.loc[:,col])) for col in sub_str.columns])
    #### num_cat == 1
    drop_cols += list(sub_str.columns[num_cat == 1])
    #### num_cat >= sub_str.shape[0] * drop_threshold
    drop_cols += list(sub_str.columns[num_cat >= sub_str.shape[0] * drop_threshold])
    logger('drop cols which is meanless or too much values', ','.join(drop_cols), verbose=verbose)
    sub_str = sub_str.loc[:,sub_str.columns.difference(drop_cols)]
    if sub_str.shape[1] != 0:
        sub_str = pd.get_dummies(sub_str)
    # merge and output
    if sub_numeric.shape[1] == 0 and sub_str.shape[1] == 0:
        final_metadata = None
        logger("No metadata is survived.......",verbose=1)
    elif sub_str.shape[1] ==0:
        final_metadata = sub_numeric
    elif sub_numeric.shape[1] ==0:
        final_metadata = sub_str
    else:
        final_metadata = pd.concat([sub_numeric,sub_str],axis=1)
    return final_metadata

def write_data(data,prefix,suffix='',mode='df',verbose=1, **kwargs):
    if mode =='df':
        if suffix:
            data.to_csv('_'.join([prefix,suffix])+'.csv',sep=',',index=1)
        else:
            data.to_csv(prefix + '.csv', sep=',', index=1)
        logger("Data with prefix %s has been output." % prefix, verbose=verbose)
    elif mode == 'multidf':
        cols = kwargs['df2cols']
        logger("There are multiple data matrixs need to output. Inclduing", '\n'.join([os.path.basename(_) for _ in cols.keys()]),verbose=verbose)
        for name,col in cols.items():
            subdata = data.loc[:,col]
            subdata.to_csv(prefix +'_%s.csv' % '_'.join([name,suffix]) ,sep=',',index=1)
        logger("Data with prefix %s has been output." % prefix, verbose=verbose)
    elif mode == 'html':
        pass
