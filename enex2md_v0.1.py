# A simple tool to convert .enex file to .md file.

import os
import sys
import base64
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET


def write_note(title, created, updated, content):
    filename = nb_name + '/' + title + '.md'
    f = open(filename, "w")
    f.write('# ' + title + '\n')
    f.write('---' + '\n')
    f.write('created date: ' + created + '\n')
    f.write('modified date: ' + updated + '\n')
    f.write('---' + '\n\n')
    f.write(content)
    f.close()


def write_file(data, filetype, filename):
    filename = nb_name + '/att/' + filename + '.' + filetype
    with open(filename, 'wb') as f:
        f.write(base64.b64decode(data))


def parse_html(content):
    soup = BeautifulSoup(content, 'html.parser')
    str1 = ''
    for element in soup.find('en-note'):
        if element.find('div') is not None:
            for sub_element in element:
                if sub_element.find('en-media') is not None and sub_element.find('en-media').get('type').split('/')[0] == 'image':
                    str1 = "{0}![](att/{1}.{2}) \n".format(str1, str(sub_element.find('en-media').get('hash')), sub_element.find('en-media').get('type').split('/')[1])
                if sub_element.name == 'hr':
                    str1 = str1 + '--- \n'
                if sub_element.name == 'div':
                    if sub_element.find('div') is not None:
                        str1 = str1 + str(sub_element.find('div').get_text('\n')) + "\n"
                    else:
                        str1 = str1 + str(sub_element.get_text('\n')) + "\n"
        else:
            if element.find('en-media') is not None and element.find('en-media').get('type').split('/')[0] == 'image':
                str1 = "{0}![](att/{1}.{2}) \n".format(str1, str(element.find('en-media').get('hash')), element.find('en-media').get('type').split('/')[1])
            if element.name == 'hr':
                str1 = str1 + '--- \n'
            if element.name == 'div':
                if element.find('div') is not None:
                    str1 = str1 + str(element.find('div').get_text('\n')) + "\n"
                else:
                    str1 = str1 + str(element.get_text('\n')) + "\n"
    return str1


def parse_enex(enex_file):
    tree = ET.parse(enex_file)
    root = tree.getroot()
    for article in root.findall('note'):
        title = article.find('title').text
        created = article.find('created').text
        updated = article.find('updated').text
        content = parse_html(article.find('content').text)
        write_note(title, created, updated, content)
        for resource in article.findall('resource'):
            data = resource.find('data').text
            filetype = resource.find('mime').text.split('/')[1]
            filename = resource.find('resource-attributes').find('source-url').text.split('+')[2]
            write_file(data, filetype, filename)


nb_name = sys.argv[1].split('.')[0]
if not os.path.exists(nb_name):
    os.makedirs(nb_name)
if not os.path.exists(nb_name + '/att'):
    os.makedirs(nb_name + '/att')

parse_enex(sys.argv[1])
