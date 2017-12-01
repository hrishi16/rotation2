#!/usr/bin/env python

"""rotation_2.py: 

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import sys
import os
import urllib2
from bs4 import BeautifulSoup
import query_pimadb
import pickle

tempdir = '_temp' 
if not os.path.isdir( tempdir ):
    os.makedirs( tempdir )

def get_chain( nid ):

    print( '[INFO] Getting ids for chain %s' % nid )
    url = 'http://caps.ncbs.res.in/cgi-bin/pimadb/show_list_by_chain_number.py?num_chains=%s' % nid 
    html = urllib2.urlopen( url ).read( )
    soup = BeautifulSoup( html, "lxml" )

    idsToDownload = [ ]
    for i, tr in enumerate( soup.find_all( 'tr' ) ):
        _id = tr.find( 'td' )    # first td has the id.
        if _id:
            idsToDownload.append( _id.text.strip( ) )

    idsToDownload = filter( lambda x: len( x ) == 4 and x[0].isdigit( )
            , idsToDownload 
            )

    data = dict( )
    for i, _id in enumerate( idsToDownload ):
        entryFile = os.path.join( tempdir, '%s_%s.pickle' % (nid,_id) )
        if not os.path.exists( entryFile ):
            print( '[%d/%d] Downloading %s' % (i, len(idsToDownload), _id))
            res = query_pimadb.query_db( _id, [0, 4, 5] )

            with open( entryFile, 'wb' ) as f:
                print( '   Saving to %s' % entryFile )
                pickle.dump( res, f )
        else:
            print( '[%d/%d] already downloaded %s' % (i, len(idsToDownload), _id))

        entry = { }
        with open( entryFile, 'rb' ) as f:
            res = pickle.load( f )

        for r in filter( lambda x: len(x) == 3, res):
            entry[r[0]] = float(r[1])/float(r[2])
        data[ _id ] = entry

    outfile = '%s_chain.pickle' % nid 
    with open( outfile, 'wb' ) as f:
        pickle.dump( data, f )
    print( 'Saved to %s' % outfile )


def main( ):
    numChains = sys.argv[1]
    ids = get_chain( numChains )


if __name__ == '__main__':
    main()



