#!/usr/bin/python

###########################################################################
#
# name          : certificate.py
#
# purpose       : make certificate
#
# usage         : import certificate.py
#
# description   :
#
###########################################################################


import base64
import datetime
import json

from string import Template

IMG_PRE = "data:image/svg+xml;base64,"
JSON_PRE = "data:application/json;base64,"

def create_certificate( options, output=False ) :

    cert = None
    parameters = {}
    parameters[ "width" ] = 1600
    parameters[ "height" ] = 800
    parameters[ "vbx1" ] = -200
    parameters[ "vby1" ] = -200
    parameters[ "vbx2" ] = 400
    parameters[ "vby2" ] = 200
    parameters[ "fx1" ] = -200
    parameters[ "fx2" ] = -198
    parameters[ "fx3" ] = -190
    parameters[ "fx4" ] = -188
    parameters[ "fy1" ] = -200
    parameters[ "fy2" ] = -198
    parameters[ "fy3" ] = -190
    parameters[ "fy4" ] = -188
    parameters[ "fw1" ] = 300
    parameters[ "fw2" ] = 296
    parameters[ "fw3" ] = 280
    parameters[ "fw4" ] = 276
    parameters[ "fh1" ] = 200
    parameters[ "fh2" ] = 196
    parameters[ "fh3" ] = 180
    parameters[ "fh4" ] = 176
    parameters[ "rx" ] = 2
    parameters[ "color1" ] = "#FFFFFF"
    parameters[ "color2" ] = "#F1D592"
    parameters[ "cx1" ] = -190
    parameters[ "cx2" ] = -190
    parameters[ "cx3" ] = 90
    parameters[ "cx4" ] = 90
    parameters[ "cy1" ] = -190
    parameters[ "cy2" ] = -10
    parameters[ "cy3" ] = -10
    parameters[ "cy4" ] = -190
    parameters[ "radius" ] = 5
    parameters[ "tx1" ] = -50
    parameters[ "tx2" ] = -50
    parameters[ "tx3" ] = -50
    parameters[ "ty1" ] = -150
    parameters[ "ty2" ] = -100
    parameters[ "ty3" ] = -50
    parameters[ "title" ] = options.title
    parameters[ "name" ] = options.name
    parameters[ "course" ] = options.course

    with open( "certificate.txt", 'r' ) as f :
        cert = Template( f.read() )

    cert_final = cert.substitute( parameters )
    dt = datetime.datetime.now().strftime( "%Y%m%d%H%M%S" )

    if output :
        with open( f"{dt}_certificate.html", 'w' ) as f :
            f.write( cert_final )

    return cert_final


def create_metadata( options ) :
    svg = create_certificate( options )
    svg_encoded = base64.b64encode( svg.encode() )
    svg_final = IMG_PRE + svg_encoded.decode( "utf-8" )
    meta = {}
    meta[ "name" ] = "Soulbound Certficate"
    meta[ "image" ] = svg_final
    meta[ "attributes" ] = [
            { "trait_type" : "course", "value" : options.course },
            { "trait_type" : "name", "value" : options.name },
            { "trait_type" : "title", "value" : options.title }
    ]
    meta_encoded = base64.b64encode( json.dumps( meta ).encode() )
    meta_final = JSON_PRE + meta_encoded.decode( "utf-8" ) 
    return meta_final


if __name__ == "__main__" :
    import optparse
    parser = optparse.OptionParser()
    parser.add_option( "-H", "--html", dest="html", 
            action="store_true", default=False, help="Generate HTML", metavar="BOOL" )
    parser.add_option( "-s", "--svg", dest="svg", 
            action="store_true", default=False, help="Generate SVG", metavar="BOOL" )
    parser.add_option( "-m", "--metadata", dest="metadata", 
            action="store_true", default=False, help="Generate Metadata", metavar="BOOL" )

    parser.add_option( "-c", "--course", dest="course", 
            action="store", default="General Awesomeness", help="Course", metavar="STRING" )
    parser.add_option( "-n", "--name", dest="name", 
            action="store", default="Daniel Kovach", help="Name", metavar="STRING" )
    parser.add_option( "-t", "--title", dest="title", 
            action="store", default="Certificate", help="Certificate title", metavar="STRING" )
    ( options, args ) = parser.parse_args()


    if options.html :
        html_body = create_certificate( options.course, options.name, options.title )
        html = "<html>\n" + html_body + "\n</html>"
        print( html )
        
    if options.svg :
        svg = create_certificate( options.course, options.name, options.title )
        svg_encoded = base64.b64encode( svg.encode() )
        svg_final = IMG_PRE + svg_encoded.decode( "utf-8" )
        print( svg_final )

    if options.metadata :
        meta_final = create_metadata( options )
        print( meta_final )
