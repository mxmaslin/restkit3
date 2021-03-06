# -*- coding: utf-8 -
#
# This file is part of restkit released under the MIT license.
# See the NOTICE for more information.

import io
import mimetypes
import os
import re

from restkit.py3compat import (text_type, unicode_to_str, string_types,
        str_to_bytes, bytes_to_str, iscallable)
from restkit.util import to_bytestring, url_quote, url_encode

MIME_BOUNDARY = 'END_OF_PART'
CRLF = '\r\n'

def form_encode(obj, charset="utf8"):
    encoded = url_encode(obj, charset=charset)
    return to_bytestring(encoded)


class BoundaryItem(object):
    def __init__(self, name, value, fname=None, filetype=None, filesize=None,
                 quote=url_quote):
        self.quote = quote
        self.name = quote(name)

        self.size = 0
        # set value
        if value is not None and not hasattr(value, 'read'):
            value = self.encode_unreadable_value(value)
            self.size = len(value)
        else:
            if hasattr(value, 'fileno') and filesize is None:
                try:
                    value.flush()
                except IOError:
                    pass

                if iscallable(value.fileno):
                    try:
                        self.size = int(os.fstat(value.fileno())[6])
                    except io.UnsupportedOperation:
                        if hasattr(value, "getvalue"):
                            self.size = len(value.getvalue())
                        else:
                            raise
            else:
                self.size = int(os.fstat(value.fileno)[6])

        self.value = value

        # set filename
        if fname is not None:
            if isinstance(fname, text_type):
                fname = unicode_to_str(fname)
                fname = fname.encode("unicode-escape").replace(b'"', b'\\"')
            else:
                fname = fname.replace(b'"', b'\\"')
        self.fname = fname

        # set filetype if needed
        if filetype is not None:
            filetype = to_bytestring(filetype)
        self.filetype = filetype


        self._encoded_hdr = None
        self._encoded_bdr = None

    def encode_hdr(self, boundary):
        """Returns the header of the encoding of this parameter"""
        if not self._encoded_hdr or self._encoded_bdr != boundary:
            boundary = self.quote(boundary)
            self._encoded_bdr = boundary
            headers = ["--%s" % boundary]
            if self.fname:
                disposition = 'form-data; name="%s"; filename="%s"' % (self.name,
                        os.path.basename(bytes_to_str(self.fname)))
            else:
                disposition = 'form-data; name="%s"' % self.name
            headers.append("Content-Disposition: %s" % disposition)
            if self.filetype:
                filetype = self.filetype
            else:
                filetype = "text/plain; charset=utf-8"
            headers.append("Content-Type: %s" % filetype)
            headers.append("Content-Length: %i" % self.size)
            self._encoded_hdr = "\r\n".join(headers)
        return str_to_bytes(self._encoded_hdr)

    def encode(self, boundary):
        """Returns the string encoding of this parameter"""
        value = self.value
        if re.search(str_to_bytes("^--%s$" % re.escape(boundary)), value, re.M):
            raise ValueError("boundary found in encoded string")

        return b"".join([self.encode_hdr(boundary), value, b"\r\n"])


    def get_size(self, boundary):
        return len(self.encode_hdr(boundary)) + self.size + 2

    def iter_encode(self, boundary, blocksize=16384):
        if not hasattr(self.value, "read"):
            yield self.encode(boundary)
        else:
            if hasattr(self.value, 'seek'):
                try:
                    self.value.seek(0)
                except:
                    pass

            yield self.encode_hdr(boundary)
            while True:
                block = self.value.read(blocksize)
                if not block:
                    break
                yield block
            yield b"\r\n"

    def encode_unreadable_value(self, value):
        """ encode the value to bytes if needed """
        if isinstance(value, string_types):
            value = str_to_bytes(value)
        return value


class MultipartForm(object):
    def __init__(self, params, boundary, headers, bitem_cls=BoundaryItem,
                 quote=url_quote):
        self.boundary = boundary
        self.tboundary = str_to_bytes("--%s--\r\n" % boundary)
        self.boundaries = []
        self._clen = headers.get('Content-Length')

        if hasattr(params, 'items'):
            params = list(params.items())

        for param in params:
            name, value = param
            if hasattr(value, "read"):
                fname = getattr(value, 'name')
                if fname is not None:
                    filetype = ';'.join([_f for _f in mimetypes.guess_type(fname) if _f])
                else:
                    filetype = None

                # pass the full value
                # should be improved later by streaming the content
                # instead of keeping it in memory
                if not hasattr(value, 'fileno') and self._clen is None:
                    value = value.read()

                boundary = bitem_cls(name, value, fname, filetype, quote=quote)
                self.boundaries.append(boundary)
            elif isinstance(value, list):
                for v in value:
                    boundary = bitem_cls(name, v, quote=quote)
                    self.boundaries.append(boundary)
            else:
                boundary = bitem_cls(name, value, quote=quote)
                self.boundaries.append(boundary)

    def get_size(self, recalc=False):
        if self._clen is None or recalc:
            self._clen = 0
            for boundary in self.boundaries:
                self._clen += boundary.get_size(self.boundary)
            self._clen += len(self.tboundary)
        return self._clen

    def __iter__(self):
        for boundary in self.boundaries:
            for block in boundary.iter_encode(self.boundary):
                yield block
        yield self.tboundary

def multipart_form_encode(params, headers, boundary, quote=url_quote):
    """Creates a tuple with MultipartForm instance as body and dict as headers

    params
      dict with fields for the body

    headers
      dict with fields for the header

    boundary
      string to use as boundary

    quote (default: url_quote)
      some callable expecting a string an returning a string. Use for quoting of
      boundary and form-data keys (names).
    """
    headers = headers or {}
    boundary = quote(boundary)
    body = MultipartForm(params, boundary, headers, quote=quote)
    headers['Content-Type'] = "multipart/form-data; boundary=%s" % boundary
    headers['Content-Length'] = str(body.get_size())
    return body, headers
