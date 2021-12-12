"""
-- MailException
    -- InvalidAttachmentException
        -- NoSuchAttachment
    -- SMTPException
"""


class MailieException(Exception):
    """Generic Mailie exception, everything will stem from this"""


class InvalidAttachmentException(MailieException):
    """Raised when an email is provided an attachment path that is non existent or problematic"""


class NoSuchAttachment(InvalidAttachmentException):
    """Raised when the file path given for an attachment does not exist on disk"""


class SMTPException(MailieException):
    """Raised when an exception occurs during the SMTP conversation with the smtp server"""
