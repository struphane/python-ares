""" Mailer - Email module

LICENSE
-------
Copyright 2017 Alfredo Mungo <alfredo.mungo@protonmail.ch>

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

  1. Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

  2. Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

  3. Neither the name of the copyright holder nor the names of its contributors
  may be used to endorse or promote products derived from this software without
  specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.""
"""


import email
import email.mime
import email.mime.image
import email.mime.text
import email.mime.application
import email.mime.multipart
import email.mime.message
import smtplib
import sys
import logging

_DEBUG = False
_PY3 = sys.version_info.major == 3
_STRING_TYPES = (str,) if _PY3 else (str, unicode)
_str = str if _PY3 else unicode


class Attachment(object):
  """Email attachment class.

  This instantiates a proxy object that will only read
  the data whenever the `data` property is read. This
  class is not suitable for huge files.

  INSTANCE PROPERTIES
  -------------------
  filename (rw): The filename to give to the attachment
  fileobj (rw): The file object to read the data from
  data (r): The data read from the file object
  mimetype (rw): The MIME type of the data
  """
  def __init__(self, filename, fileobj, mimetype='application/octet-stream'):
    """Create an attachment object

    ARGUMENTS
    ---------
    (See instance properties)
    """
    self.filename = filename
    self.fileobj = fileobj
    self.mimetype = mimetype
    self.__data = None # Raw file data

  @property
  def data(self):
    if self.__data is None:
      self.__data = self.fileobj.read()
    
    return self.__data


class Address(object):
  """Represents an email address.

  This class can be used to add email addresses to emails with attached name
  information.
  """
  def __init__(self, email, name=None):
    self.name = name
    self.email = email

  def __str__(self):
    return _str(
      '%s%s' % (
        (('%s ' % self.name) if self.name is not None else ''),
        '<%s>' % self.email
      )
    )

  def __eq__(self, other):
    if isinstance(other, _STRING_TYPES):
      return self.email == other or _str(Address(self.email)) == other or _str(self) == other
    elif isinstance(other, self.__class__):
      return self.email == other.email and self.name == other.name
    else:
      raise ValueError('Only string and Address objects can be compared with an Address object')


class Email(object):
  def __init__(self, sender, recipients, subject, content, attachments=None, headers=None, mimetype='text/plain', charset='utf8'):
    """
    ARGUMENTS
    ---------
    sender: Email sender
    recipients: Iterable object of recipients (can be both strings or Address objects)
    subject: Email subject
    content: Email content
    attachments: Optional iterable of Attachment objects
    headers: Optional dictionary of additional headers in the form {header_name: header_value}
    mimetype: The content type of the message
    charset: Optional charset
    """
    self.sender = sender
    self.recipients = tuple(map(lambda r: r if isinstance(r, Address) else Address(r), recipients))
    self.subject = subject
    self.content = content
    self.attachments = tuple(attachments or ()) # TODO: Test attachment file names
    self.headers = tuple(headers or ())
    self.mimetype = mimetype
    self.charset = charset

  def to_mime(self):
    """Return a MIME representation of this object - used internally"""
    e = email.mime.multipart.MIMEMultipart()

    e.set_charset(self.charset)
    e['Subject'] = self.subject

    maintype, subtype = self.mimetype.lower().split('/', 1)
    m = email.mime.text.MIMEText(self.content, _subtype=subtype, _charset=self.charset)

    e.attach(m)

    for h, hv in self.headers:
      e[h] = hv

    for a in self.attachments:
      maintype, subtype = a.mimetype.lower().split('/', 1)

      if maintype == 'image':
        aclass = email.mime.image.MIMEImage
      else:
        aclass = email.mime.application.MIMEApplication

      mimea = aclass(a.data, _subtype=subtype)
      mimea.add_header('Content-Disposition', 'attachment', filename=a.filename)

      e.attach(mimea)
    
    return e


class SMTPServer(object):
  """SMTP server class.

  This class is used to represent a SMTP server and a connection to it.
  """
  ENCRYPTION_METHODS = ('tls', 'ssl', '') # Supported connection encryption methods

  def __init__(self, hostname, port, encryption='tls'):
    """Initialise a new instance of this class.

    ARGUMENTS
    ---------
    hostname: SMTP server hostname
    port: SMTP server port
    encryption: String specifying the form of encryption required for the connection
      Must be one of `Server.ENCRYPTION_METHODS`
    """
    self.hostname = hostname
    self.port = port
    self.encryption = encryption.lower()
    self.server = None

    if self.encryption not in self.__class__.ENCRYPTION_METHODS:
      raise ValueError('encryption must be one of %s', repr(self.__class__.ENCRYPTION_METHODS))

  def connect(self, **kwargs):
    """Connect to a SMTP server.

    OPTIONAL KEYWORD ARGUMENTS
    -----------------
    keyfile, certfile, context: Key/certificate file and TLS context for the STARTTLS method
    user, password: Login credentials
    """
    ssl = self.encryption == 'ssl'
    tls = self.encryption == 'tls'
    cls = smtplib.SMTP if not ssl else smtplib.SMTP_SSL
    srv = cls(host=self.hostname, port=self.port)

    if _DEBUG:
      srv.set_debuglevel(1)

    if tls:
      srv.starttls(
        kwargs.get('keyfile', None),
        kwargs.get('certfile', None),
        kwargs.get('context', None)
      )

    try:
      user = kwargs['user']
      password = kwargs['password']

      srv.login(user, password)
    except KeyError:
      logging.debug('No login information provided %s' % e, exc_info=True)

    self.server = srv

  def disconnect(self):
    """Disconnect from the SMTP server"""
    if self.is_connected:
      self.server.quit()
      self.server = None

  @property
  def is_connected(self):
    """Evaluates to `True` if the object represents a connected instance"""
    return self.server is not None

  def sendmail(self, email, **kwargs):
    """Send an email.

    ARGUMENTS
    ---------
    email: The `Email` object to send

    OPTIONAL KEYWORD ARGUMENTS
    -----------------
    (Directly passed to `server.sendmessage()`)
    """
    if not self.is_connected:
      self.connect()

    self.server.sendmail(
      _str(email.sender),
      tuple(_str(x) for x in email.recipients),
      email.to_mime().as_string(),
      **kwargs
    )
