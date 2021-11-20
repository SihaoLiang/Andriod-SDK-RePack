# -*- coding:utf-8 -*-
from xml.dom import minidom

def get_attrvalue(node, attrname):
     return node.getAttribute(attrname) if node else ''

def get_nodevalue(node, index = 0):
    return node.childNodes[index].nodeValue if node else ''

def get_xmlnode(node,name):
    return node.getElementsByTagName(name) if node else []

def xml_to_string(filename):
    doc = minidom.parse(filename)
    return doc.toxml('utf-8')

def get_xml_data(filename):
    doc = minidom.parse(filename) 
    root = doc.documentElement
    user_nodes = get_xmlnode(root,'config')
    for node in user_nodes:
        print get_nodevalue(node) 

def test_xmltostring():
    print xml_to_string()
    
