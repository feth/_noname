from django import template

register = template.Library()


#simple xml output maker: maybe borrow a real one
def _attribute(name, value):
    if not value:
        return u''
    return u"%s=%s" % (name, value)

def _element(tag, content, **attributes):
    xmlattrs = u' '.join(_attribute(key, val) for key, val in attributes.iteritems())
    if not content:
        return u"<%s %s/>" % (tag, xmlattrs)
    return u"<%s %s>%s</%s>" % (tag, xmlattrs, content, tag)

def _a(url, linked_item, **attributes):
    attributes['href'] = url
    return _element('a', linked_item, **attributes)

def _ul_li(iterable):
    return _element('ul', ''.join(_element('li', unicode(item)) for item in iterable))

def _table_row(iterable):
    return _element('tr', ''.join(_element('td', unicode(item)) for item in iterable))

def table(structure, eltclass, eltid):
    """
    structure is an iterable of iterables
    [
      ["a1", "a2", "a3"]
      ["b1", "b2", "b3"]
    ]
    """
    return _element('table', '\n'.join(_table_row(row) for row in structure),
        **{"class": eltclass, "id": eltid})

register.simple_tag(table)

