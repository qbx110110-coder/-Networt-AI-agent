"""Tests for network connection modules"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.network.ssh_handler import SSHHandler
from src.network.telnet_handler import TelnetHandler


class TestSSHHandler(unittest.TestCase):
    """Tests for SSH handler"""

    def setUp(self):
        """Set up test fixtures"""
        self.config = {
            "host": "192.168.1.1",
            "port": 22,
            "username": "admin",
            "password": "password",
            "timeout": 30,
        }

    @patch("src.network.ssh_handler.paramiko.SSHClient")
    def test_ssh_connect_success(self, mock_ssh_client):
        """Test successful SSH connection"""
        handler = SSHHandler(self.config)

        # Mock successful connection
        mock_client_instance = MagicMock()
        mock_ssh_client.return_value = mock_client_instance
        mock_shell = MagicMock()
        mock_client_instance.invoke_shell.return_value = mock_shell
        mock_shell.recv.return_value = b""

        # Test connection
        result = handler.connect()
        self.assertTrue(result)
        self.assertTrue(handler.is_connected())

    @patch("src.network.ssh_handler.paramiko.SSHClient")
    def test_ssh_connect_failure(self, mock_ssh_client):
        """Test failed SSH connection"""
        handler = SSHHandler(self.config)

        # Mock connection failure
        mock_ssh_client.return_value.connect.side_effect = ConnectionError("Connection failed")

        with self.assertRaises(ConnectionError):
            handler.connect()


class TestTelnetHandler(unittest.TestCase):
    """Tests for Telnet handler"""

    def setUp(self):
        """Set up test fixtures"""
        self.config = {
            "host": "192.168.1.1",
            "port": 23,
            "username": "admin",
            "password": "password",
            "timeout": 30,
        }

    @patch("src.network.telnet_handler.socket.socket")
    def test_telnet_connect_success(self, mock_socket):
        """Test successful Telnet connection"""
        handler = TelnetHandler(self.config)

        # Mock successful connection
        mock_socket_instance = MagicMock()
        mock_socket.return_value = mock_socket_instance
        mock_socket_instance.recv.return_value = b"login: "

        # Test connection
        result = handler.connect()
        self.assertTrue(result)
        self.assertTrue(handler.is_connected())

    @patch("src.network.telnet_handler.socket.socket")
    def test_telnet_send_command(self, mock_socket):
        """Test Telnet command sending"""
        handler = TelnetHandler(self.config)

        # Setup mock
        mock_socket_instance = MagicMock()
        mock_socket.return_value = mock_socket_instance
        mock_socket_instance.recv.return_value = b"output"

        handler.connect()

        # Test sending command
        output = handler.send_command("show version")
        self.assertIsNotNone(output)


if __name__ == "__main__":
    unittest.main()
