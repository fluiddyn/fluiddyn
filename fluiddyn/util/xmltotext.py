"""Formatted xml text from xml element (:mod:`fluiddyn.util.xmltotext`)


"""

from __future__ import print_function


def produce_text_element(elem, level=0):
    lines = []
    indent_base = ' '*2
    indent = indent_base*level

    children = [child for child in elem]
    if elem.text is not None:
        text = elem.text.strip()
    else:
        text = ''
    attr_text = ' '.join([k+'="'+v+'"' for k, v in elem.attrib.items()])

    if len(children) == 0 and len(text) == 0:
        if len(attr_text) > 0:
            tag_start = '<'+elem.tag+' '+attr_text+'/>'
        else:
            tag_start = '<'+elem.tag+'/>'
        tag_end = ''
    else:
        if len(attr_text) > 0:
            tag_start = '<'+elem.tag+' '+attr_text+'>'
        else:
            tag_start = '<'+elem.tag+'>'
        tag_end = '</'+elem.tag+'>'

    if len(children) > 0 or '\n' in text or len(text) > 30:
        # "long" element
        lines.append(format_too_long_tagstart(indent+tag_start))
        if len(text) > 0:
            lines.append(format_too_long_text(indent+indent_base+text))
        for child in children:
            lines.append(produce_text_element(child, level=level+1))
        lines.append(indent+tag_end)
    else:
        lines.append(
            format_too_long_tagstart(indent+tag_start)+' '+text+' '+tag_end)

    return '\n'.join(lines)+'\n'





def get_position_first_letter(text):
    i = 0
    pos_space = text.find(' ', i)
    while i == pos_space:
        i += 1
        pos_space = text.find(' ', i)
    return i


def format_too_long_text(text, lengthmax=79):
    if len(text) <= lengthmax:
        return text
    lines = []
    position_first_letter = get_position_first_letter(text)
    indent = ' '*position_first_letter
    line = indent
    for word in text.split(' '):
        if len(line+word) > lengthmax:
            lines.append(line)
            line = indent+word
        else:
            if line.endswith(' '):
                line = line+word
            else:
                line = line+' '+word
    lines.append(line)

    return '\n'.join(lines)



def get_indent_after_tag(text):
    i = 0
    pos_space = text.find(' ', i)
    while i == pos_space:
        i += 1
        pos_space = text.find(' ', i)
    if pos_space == -1:
        nb_space_indent = 0
    else:
        nb_space_indent = pos_space+1
    return ' '*nb_space_indent


def format_too_long_tagstart(text, lengthmax=79):
    if len(text) <= lengthmax:
        return text
    lines = []
    words = text.split(' ')

    position_first_letter = get_position_first_letter(text)
    line = ' '*position_first_letter+words[0]
    indent = get_indent_after_tag(text)

    for word in words[1:]:
        if len(line+word) > lengthmax:
            lines.append(line)
            line = indent+word
        else:
            if line.endswith(' '):
                line = line+word
            else:
                line = line+' '+word
    lines.append(line)

    return '\n'.join(lines)


if __name__ == '__main__':


    try:
        from lxml import etree
    except ImportError:
        import xml.etree.ElementTree as etree


    xmltext = """
<data>
    <country name="Liechtenstein">
        <rank updated="yes">2</rank>
        <year>2008</year>
        <gdppc>141100</gdppc>
        <neighbor name="Austria" direction="E" attr1="long long long" attr2="long long long" attr3="long long long">

    blablabla bliblibli bloublou blublu bloblo blablabla bliblibli bloublou blublu bloblo blablabla bliblibli bloublou blublu bloblo

        </neighbor>

        <neighbor name="Switzerland" direction="W"/>
    </country>

    <country name="Singapore">

 <rank updated="yes">5 and a text which can actually be very very long something quite long long long long long.</rank>

        <year>2011</year>
        <gdppc>59900</gdppc>
        <neighbor name="Malaysia" direction="N"/>
    </country>
    <country name="Panama">
        <rank updated="yes">69</rank>
        <year>2011</year>
        <gdppc>13600</gdppc>
        <neighbor name="Costa Rica" direction="W"/>
        <neighbor name="Colombia" direction="E"/>
    </country>
</data>

"""



    elem = etree.fromstring(xmltext)


    print(produce_text_element(elem))
