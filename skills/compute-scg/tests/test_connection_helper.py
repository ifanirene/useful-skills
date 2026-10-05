"""Exercise SSH recovery with fake SSH and real local sockets.

No cluster access, credentials, or personal configuration is used.
"""

import os
from pathlib import Path
import pty
import shutil
import socket
import subprocess
import sys
import tempfile
import unittest


HELPER = Path(__file__).resolve().parents[1] / "scripts" / "ssh-connect"
FAKE_SSH = r'''#!/usr/bin/env bash
set -e
printf '%s\n' "$*" >> "$TEST_SSH_LOG"
control_path="$TEST_CONTROL_PATH"
previous=''
for argument in "$@"; do
    if [[ "$previous" == '-o' && "$argument" == ControlPath=* ]]; then
        control_path=${argument#ControlPath=}
        control_path=${control_path//%C/test-hash}
    fi
    previous=$argument
done
if [[ "$TEST_REAL_CONFIG" == 'yes' ]]; then
    resolved=$("$TEST_REAL_SSH" -F "$TEST_EMPTY_CONFIG" -G "$@" 2>/dev/null)
    control_path=$(printf '%s\n' "$resolved" | awk '$1 == "controlpath" { print substr($0, index($0, " ") + 1); exit }')
fi
if [[ " $* " == *' -G '* ]]; then
    if [[ "$TEST_REAL_CONFIG" == 'yes' ]]; then
        printf '%s\n' "$resolved"
        exit 0
    fi
    printf 'hostname cluster.example.org\nuser testuser\n'
    printf 'controlpath %s\ncontrolpersist no\n' "$control_path"
    exit 0
fi
if [[ " $* " == *' -O check '* ]]; then
    [[ "$TEST_MASTER" == 'yes' ]]
    exit $?
fi
if [[ " $* " == *' -MNf '* ]]; then
    if [[ "$TEST_ALLOW_AUTH" == 'yes' ]]; then
        touch "$TEST_AUTH_MARKER"
        exit 0
    fi
    echo 'Unexpected interactive authentication during test.' >&2
    exit 99
fi
if [[ "$TEST_LIVE" != 'yes' && ! -f "$TEST_AUTH_MARKER" ]]; then
    printf '%s\n' "$TEST_FAILURE" >&2
    exit 255
fi
if [[ "$TEST_AUTO_SOCKET" == 'yes' && ! -S "$control_path" ]]; then
    "$TEST_PYTHON" -c 'import socket, sys; s=socket.socket(socket.AF_UNIX); s.bind(sys.argv[1]); s.close()' "$control_path"
fi
if [[ "${*: -1}" != 'true' ]]; then
    printf 'remote-output\n'
    exit "$TEST_COMMAND_EXIT"
fi
exit 0
'''


class ConnectionHelperTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="ssh-skill-test-")
        self.root = Path(self.temp.name).resolve()
        self.bin_dir = self.root / "bin"
        self.bin_dir.mkdir()
        fake = self.bin_dir / "ssh"
        fake.write_text(FAKE_SSH)
        fake.chmod(0o700)
        self.socket_path = self.root / "arbitrary socket name"
        self.master_socket = socket.socket(socket.AF_UNIX)
        self.master_socket.bind(str(self.socket_path))
        self.log = self.root / "ssh.log"
        self.empty_config = self.root / "empty-ssh-config"
        self.empty_config.write_text("")
        self.env = dict(os.environ)
        self.env.update(
            PATH=f"{self.bin_dir}{os.pathsep}{os.environ['PATH']}",
            TEST_SSH_LOG=str(self.log),
            TEST_CONTROL_PATH=str(self.socket_path),
            TEST_MASTER="yes",
            TEST_LIVE="yes",
            TEST_FAILURE="Permission denied (keyboard-interactive).",
            TEST_ALLOW_AUTH="no",
            TEST_AUTH_MARKER=str(self.root / "authenticated"),
            TEST_AUTO_SOCKET="no",
            TEST_PYTHON=sys.executable,
            TEST_COMMAND_EXIT="0",
            TEST_REAL_CONFIG="no",
            TEST_REAL_SSH=shutil.which("ssh") or "",
            TEST_EMPTY_CONFIG=str(self.empty_config),
        )

    def tearDown(self) -> None:
        self.master_socket.close()
        self.temp.cleanup()

    def run_helper(self, *arguments: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["bash", str(HELPER), "--host", "lab-cluster", *arguments],
            env=self.env,
            capture_output=True,
            text=True,
            timeout=10,
            cwd=self.root,
        )

    def assert_no_authentication(self) -> None:
        self.assertNotIn("-MNf", self.log.read_text())

    def test_connection_reuses_master(self) -> None:
        result = self.run_helper("--non-interactive")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("SSH connection verified", result.stdout)
        self.assert_no_authentication()

    def test_missing_auth_never_prompts_noninteractively(self) -> None:
        self.env.update(TEST_LIVE="no", TEST_MASTER="no")
        result = self.run_helper("--non-interactive")
        self.assertEqual(result.returncode, 2)
        self.assertIn("Run this helper once in your Terminal", result.stderr)
        self.assert_no_authentication()

    def test_interactive_recovery_authenticates_once(self) -> None:
        self.env.update(TEST_LIVE="no", TEST_MASTER="no", TEST_ALLOW_AUTH="yes")
        master_fd, terminal_fd = pty.openpty()
        try:
            process = subprocess.Popen(
                ["bash", str(HELPER), "--host", "lab-cluster"],
                env=self.env,
                stdin=terminal_fd,
                stdout=terminal_fd,
                stderr=subprocess.PIPE,
                text=True,
            )
            _, errors = process.communicate(timeout=10)
            self.assertEqual(process.returncode, 0, errors)
            self.assertEqual(self.log.read_text().count("-MNf"), 1)
        finally:
            os.close(terminal_fd)
            os.close(master_fd)

    def test_unresponsive_master_is_not_restarted(self) -> None:
        self.env["TEST_LIVE"] = "no"
        result = self.run_helper("--non-interactive")
        self.assertEqual(result.returncode, 2)
        self.assertIn("local master exists", result.stderr)
        self.assert_no_authentication()

    def test_network_error_does_not_request_authentication(self) -> None:
        self.env.update(
            TEST_LIVE="no",
            TEST_MASTER="no",
            TEST_FAILURE="Could not resolve hostname cluster.example.org",
        )
        result = self.run_helper()
        self.assertEqual(result.returncode, 2)
        self.assertIn("Resolve the network", result.stderr)
        self.assertNotIn("Run this helper once in your Terminal", result.stderr)
        self.assert_no_authentication()

    def test_unconfigured_account_builds_and_reuses_connection(self) -> None:
        self.env.update(TEST_CONTROL_PATH="none", TEST_AUTO_SOCKET="yes")
        state = self.root / "new-state"
        options = ("--user", "newuser", "--socket-dir", str(state), "--non-interactive")
        first = self.run_helper(*options)
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(state.stat().st_mode & 0o777, 0o700)
        self.assertTrue((state / "cm-test-hash").exists())
        second = self.run_helper(*options, "--command", "hostname; whoami")
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(second.stdout, "remote-output\n")
        self.assertIn("-l newuser", self.log.read_text())
        self.assert_no_authentication()

    def test_remote_command_failure_is_returned_without_reauthentication(self) -> None:
        self.env["TEST_COMMAND_EXIT"] = "7"
        result = self.run_helper("--non-interactive", "--command", "exit 7")
        self.assertEqual(result.returncode, 7)
        self.assert_no_authentication()

    def test_symlinked_state_directory_is_rejected(self) -> None:
        directory = self.root / "state"
        directory.mkdir()
        link = self.root / "state-link"
        link.symlink_to(directory, target_is_directory=True)
        result = self.run_helper("--socket-dir", str(link), "--non-interactive")
        self.assertEqual(result.returncode, 2)
        self.assertIn("must not be a symlink", result.stderr)

    def test_key_path_is_forwarded_as_one_argument(self) -> None:
        identity = self.root / "key with spaces"
        result = self.run_helper("--identity", str(identity), "--non-interactive")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(f"-i {identity}", self.log.read_text())
        self.assert_no_authentication()

    def test_real_openssh_expands_separate_sockets_for_each_account(self) -> None:
        if not self.env["TEST_REAL_SSH"]:
            self.skipTest("OpenSSH unavailable")
        self.env.update(TEST_REAL_CONFIG="yes", TEST_AUTO_SOCKET="yes")
        # AF_UNIX socket paths are short on macOS; use a short test root.
        with tempfile.TemporaryDirectory(prefix="ss-", dir="/tmp") as directory:
            state = Path(directory).resolve()
            for username in ("labuser_one", "labuser_two"):
                result = self.run_helper(
                    "--user", username, "--socket-dir", str(state), "--non-interactive"
                )
                self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(len(list(state.glob("cm-*"))), 2)
        self.assert_no_authentication()
if __name__ == "__main__":
    unittest.main()
