from __future__ import annotations

import smtplib
import typing
from email.message import EmailMessage

import typer

from ._policy import Policies


class Email:
    # version 0.1.0 will encompass a simple plaintext mail; then iterate.
    def __init__(self, *, frm: str, to: str, policy: str, subject: str, message: str):
        self.delegate = EmailMessage(Policies.get(policy))
        self.add_header("From", frm)
        self.add_header("To", to)
        self.add_header("Subject", subject)
        self.set_payload(message)

    def __str__(self) -> str:
        return str(self.delegate)

    def __bytes__(self) -> bytes:
        return bytes(self.delegate)

    def add_header(self, name: str, value: typing.Any, **params) -> Email:
        self.delegate.add_header(name, value, **params)
        return self

    def get_content_type(self) -> str:
        return self.delegate.get_content_type()

    def set_payload(self, payload: str, charset=None) -> Email:
        self.delegate.set_payload(payload, charset)
        return self


class Dispatcher:
    def __init__(
        self,
        *,
        message: Email,
        host: str = "",
        port: int = 0,
        # Todo: More options.
    ) -> None:
        self.message = message
        self.host = host
        self.port = port

    def send(self) -> Email:
        with smtplib.SMTP(self.host, port=self.port) as smtp:
            result = smtp.sendmail(self.message.delegate["From"], [self.message.delegate["To"]], str(self.message))
            typer.secho(result, fg=typer.colors.GREEN, bold=True)
        return self.message


class EmailFactory:
    # Todo: Apply the pattern fully.

    @classmethod
    def create(cls, *, frm: str, to: str, subject: str = "", message: str = "", policy: str = "default") -> Email:
        return Email(frm=frm, to=to, policy=policy, subject=subject, message=message)
