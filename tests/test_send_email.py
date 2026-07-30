import smtplib
import unittest
from email.mime.text import MIMEText
from unittest.mock import ANY, Mock, call, patch

from utils.send_email import send_email


class TestSendEmail(unittest.TestCase):
    def setUp(self):
        self.sender = "sender@qq.com"
        self.receivers = ["first@example.com", "second@example.com"]
        self.content = MIMEText("offline mock only", "plain", "utf-8")

        smtp_patcher = patch("utils.send_email.smtplib.SMTP_SSL")
        self.addCleanup(smtp_patcher.stop)
        self.smtp_ssl = smtp_patcher.start()
        self.server = self.smtp_ssl.return_value

    def test_sends_to_every_recipient_and_quits(self):
        result = send_email(self.sender, self.receivers, self.content)

        self.assertTrue(result)
        self.assertEqual(
            self.server.sendmail.call_args_list,
            [
                call(self.sender, self.receivers[0], ANY),
                call(self.sender, self.receivers[1], ANY),
            ],
        )
        self.server.quit.assert_called_once_with()

    def test_quits_and_reraises_when_second_send_fails(self):
        send_error = smtplib.SMTPException("second send failed")
        self.server.sendmail.side_effect = [None, send_error]

        with self.assertRaises(smtplib.SMTPException) as raised:
            send_email(self.sender, self.receivers, self.content)

        self.assertIs(raised.exception, send_error)
        self.assertEqual(self.server.sendmail.call_count, 2)
        self.server.quit.assert_called_once_with()

    def test_quit_failure_does_not_replace_send_failure(self):
        send_error = smtplib.SMTPException("second send failed")
        self.server.sendmail.side_effect = [None, send_error]
        self.server.quit.side_effect = smtplib.SMTPException("quit failed")

        with self.assertRaises(smtplib.SMTPException) as raised:
            send_email(self.sender, self.receivers, self.content)

        self.assertIs(raised.exception, send_error)
        self.assertEqual(self.server.sendmail.call_count, 2)
        self.server.quit.assert_called_once_with()

    def test_quit_failure_does_not_replace_login_failure(self):
        login_error = smtplib.SMTPException("login failed")
        self.server.login.side_effect = login_error
        self.server.quit.side_effect = smtplib.SMTPException("quit failed")

        with self.assertRaises(smtplib.SMTPException) as raised:
            send_email(self.sender, self.receivers, self.content)

        self.assertIs(raised.exception, login_error)
        self.server.sendmail.assert_not_called()
        self.server.quit.assert_called_once_with()

    def test_quit_failure_does_not_replace_starttls_failure(self):
        starttls_error = smtplib.SMTPException("starttls failed")
        server = Mock()
        server.starttls.side_effect = starttls_error
        server.quit.side_effect = smtplib.SMTPException("quit failed")

        with patch("utils.send_email.smtplib.SMTP", return_value=server):
            with self.assertRaises(smtplib.SMTPException) as raised:
                send_email("sender@gmail.com", self.receivers, self.content)

        self.assertIs(raised.exception, starttls_error)
        server.login.assert_not_called()
        server.quit.assert_called_once_with()

    def test_quit_failure_does_not_replace_connect_failure(self):
        connect_error = smtplib.SMTPException("connect failed")
        server = Mock()
        server.connect.side_effect = connect_error
        server.quit.side_effect = smtplib.SMTPException("quit failed")

        with patch("utils.send_email.smtplib.SMTP", return_value=server):
            with self.assertRaises(smtplib.SMTPException) as raised:
                send_email("sender@163.com", self.receivers, self.content)

        self.assertIs(raised.exception, connect_error)
        server.login.assert_not_called()
        server.quit.assert_called_once_with()

    def test_empty_receivers_return_none_without_connecting(self):
        result = send_email(self.sender, [], self.content)

        self.assertIsNone(result)
        self.smtp_ssl.assert_not_called()


if __name__ == "__main__":
    unittest.main()
