# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jeremy Brubaker <jbrubake@orionarts.io>
# Based on ansible.builtin.get_url Copyright: (c) 2012, Jan-Piet Mens <jpmens () gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations


DOCUMENTATION = r"""
---
module: ubi
short_description: Downloads binaries using the Universal Binary Installer
description:
     - Downloads binaries from various sources to the remote server using the
       Universal Binary Installer (https://github.com/houseabsolute/ubi). The
       remote server I(must) have direct access to the remote resource.
version_added: '1.0'
options:
  url:
    description:
      - The URL of the file to download.
    type: str
    required: true
  dest:
    description:
      - Absolute path of where to download the file to.
      - O(dest) must be the path to a file, not a directory.
    type: path
    required: true
  tmp_dest:
    description:
      - Absolute path of where temporary file is downloaded to.
      - When run on Ansible 2.5 or greater, path defaults to ansible's C(remote_tmp) setting.
      - When run on Ansible prior to 2.5, it defaults to E(TMPDIR), E(TEMP) or E(TMP) env variables or a platform specific value.
      - U(https://docs.python.org/3/library/tempfile.html#tempfile.tempdir).
    type: path
  force:
    description:
      - If V(true), will download the file every time and replace the file if
        the contents change. If V(false), the file will only be downloaded if
        the destination does not exist. Generally should be V(true) only for
        small local files.
      - Prior to 0.6, this module behaved as if V(true) was the default.
    type: bool
    default: no
  backup:
    description:
      - Create a backup file including the timestamp information so you can get
        the original file back if you somehow clobbered it incorrectly.
    type: bool
    default: no
  checksum:
    description:
      - 'If a checksum is passed to this parameter, the digest of the
        destination file will be calculated after it is downloaded to ensure
        its integrity and verify that the transfer completed successfully.
        Format: <algorithm>:<checksum|url>, for example C(checksum="sha256:D98291AC[...]B6DC7B97"),
        C(checksum="sha256:http://example.com/path/sha256sum.txt").'
      - If you worry about portability, only the sha1 algorithm is available
        on all platforms and python versions.
      - The Python C(hashlib) module is responsible for providing the available algorithms.
        The choices vary based on Python version and OpenSSL version.
      - On systems running in FIPS compliant mode, the C(md5) algorithm may be unavailable.
      - Additionally, if a checksum is supplied to this parameter, and the file exists under
        the O(dest) location, the C(destination_checksum) would be calculated; and if
        checksum equals C(destination_checksum), the file download would be skipped
        (unless O(force=true)). If the checksum does not equal C(destination_checksum),
        the destination file is replaced with the newly downloaded file.
      - If the checksum URL requires username and password, O(url_username) and O(url_password) are used
        to download the checksum file.
    type: str
    default: ''
  timeout:
    description:
      - Timeout in seconds for ubi download request.
    type: int
    default: 10

  project:
    description:
      - The project you want to install such as C(houseabsolute/precious).
      - The project will be searched for in GitLab, GitHub and Forgejo, in that
        order.
      - This option cannot be used with O(url).
    type: str
  tag:
    description:
      - The project tag to download.
      - This option can only be used with O(project) and only if O(min_age_days)
        is not used.
    type: str
    default: latest
  exe:
    description:
      - The name of the file to look for in an archive file, or the name of the
        downloadable file excluding its extension, e.g. `ubi.gz`.
      - By default this is the same as the project name, so for
        C(houseabsolute/precious) we look for C(precious) or C(precious.exe).
        When running on Windows the C(.exe) suffix will be added, as needed.
    type: str
  forge:
    description:
      - The source forge to use.
    type: str
    default: github
    choices:
      - github
      - gitlab
      - forgejo
  min_age_days:
    description:
      - Minimum age in days for releases. Only releases at least this many days
        old will be installed.
      - This is useful for mitigating supply chain attacks. It's especially
        useful for projects that use GitHub's immutable releases feature.
      - This option can only be used with O(project) and only if O(tag)
        is not used.
    type: int
  matching:
    description:
      - A string that will be matched against the release filename when there
        are multiple matching files for your OS/architecture.
      - For example, there may be multiple releases for an OS/architecture that
        differ by compiler (e.g., MSVC vs. gcc) or linked libc (glibc vs. musl).
      - Note that this option will be ignored if there is only one matching
        release filename for your OS/architecture.
    type: str
  regex:
    description:
      - A regular expression string that will be matched against release
        filenames before matching against your OS/architecture.
      - If the pattern yields a single match, that release will be selected.
      - If no matches are found, this will result in an error.
    type: str
# informational: requirements for nodes
extends_documentation_fragment:
    - files
    - action_common_attributes
attributes:
    check_mode:
        details: the changed status will reflect comparison to an empty source file
        support: partial
    diff_mode:
        support: none
seealso:
- name: The Universal Binary Installer
  link: https://github.com/houseabsolute/ubi
requirements:
- ubi
author:
- Jeremy Brubaker
"""

EXAMPLES = r"""
- name: Install foo/bar from GitHub as bar.sh
  ubi:
    project: foo/bar
    dest: /usr/local/bin/bar.sh

- name: Install foo/bar from GitLab as bar
  ubi:
    project: foo/bar
    forge: gitlab
    dest: /usr/local/bin/bar

- name: Install v2.3 of foo/bar
  ubi:
    project: foo/bar
    tag: v2.3
    dest: /usr/local/bin/bar

- name: Install baz/quz from a custom source forge
  ubi:
    url: http://myforge.com/baz/quz
    dest: /usr/local/bin/quz

- name: Install a bob/app when the exact name is known
  ubi:
    project: bob/app
    exe: app-x86_64.AppImage
    dest: /opt/bob/app

- name: Install alice/myapp when only a portion of the name is known
  ubi:
    project: alice/myapp
    regex: alice-.*-x86_64
    dest: /bin/myapp

- name: Install foo/bar with check (sha256)
  ubi:
    project: foo/bar
    dest: /usr/bin/bar
    checksum: sha256:b5bb9d8014a0f9b1d61e21e796d78dccdf1352f23cd32812f4850b878ae4944c
"""

RETURN = r"""
backup_file:
    description: name of backup file created after download
    returned: changed and if backup=yes
    type: str
    sample: /path/to/file.txt.2015-02-12@22:09~
checksum_dest:
    description: sha1 checksum of the file after copy
    returned: success
    type: str
    sample: 6e642bb8dd5c2e027bf21dd923337cbb4214f827
checksum_src:
    description: sha1 checksum of the file
    returned: success
    type: str
    sample: 6e642bb8dd5c2e027bf21dd923337cbb4214f827
dest:
    description: destination file/path
    returned: success
    type: str
    sample: /path/to/file.txt
elapsed:
    description: The number of seconds that elapsed while performing the download
    returned: always
    type: int
    sample: 23
gid:
    description: group id of the file
    returned: success
    type: int
    sample: 100
group:
    description: group of the file
    returned: success
    type: str
    sample: "httpd"
md5sum:
    description: md5 checksum of the file after download
    returned: when supported
    type: str
    sample: "2a5aeecc61dc98c4d780b14b330e3282"
mode:
    description: permissions of the target
    returned: success
    type: str
    sample: "0644"
msg:
    description: the HTTP message from the request
    returned: always
    type: str
    sample: OK (unknown bytes)
owner:
    description: owner of the file
    returned: success
    type: str
    sample: httpd
secontext:
    description: the SELinux security context of the file
    returned: success
    type: str
    sample: unconfined_u:object_r:user_tmp_t:s0
size:
    description: size of the target
    returned: success
    type: int
    sample: 1220
src:
    description: source file used after download
    returned: always
    type: str
    sample: /tmp/tmpAdFLdV
state:
    description: state of the target
    returned: success
    type: str
    sample: file
status_code:
    description: the HTTP status code from the request
    returned: always
    type: int
    sample: 200
uid:
    description: owner id of the file, after execution
    returned: success
    type: int
    sample: 100
url:
    description: the actual URL used for the request
    returned: always
    type: str
    sample: https://www.ansible.com/
"""

import os
import re
import subprocess
import sys
import tempfile

from datetime import datetime, timezone

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_native

# ==============================================================
# url handling

def ubi_get(module, url=None, project=None, forge="github", tag=None, min_age_days=0, exe=None, matching=None, regex=None, tmp_dest=None, timeout=0):
    """
    Download a file using ubi and store in a temporary file.

    Return tempfile
    """

    # Build ubi command line
    #
    cmd = ['ubi']
    if project:
        cmd.append('--project')
        cmd.append(project)
    if tag:
        cmd.append('--tag')
        cmd.append(tag)
    if min_age_days:
        cmd.append('--min-age_days')
        cmd.append(min_age_days)
    if forge:
        cmd.append('--forge')
        cmd.append(forge)
    if url:
        cmd.append('--url')
        cmd.append(url)
    if exe:
        cmd.append('--exe')
        cmd.append(exe)
    if matching:
        cmd.append('--matching')
        cmd.append(matching)
    if regex:
        cmd.append('--matching-regex')
        cmd.append(regex)

    # create a temporary directory
    if tmp_dest:
        # tmp_dest should be an existing dir
        tmp_dest_is_dir = os.path.isdir(tmp_dest)
        if not tmp_dest_is_dir:
            if os.path.exists(tmp_dest):
                module.fail_json(msg=f"{tmp_dest} is a file but should be a directory.")
            else:
                module.fail_json(msg=f"{tmp_dest} directory does not exist.")
    else:
        tmp_dest = module.tmpdir

    fd, tempname = tempfile.mkstemp(dir=tmp_dest)

    f = os.fdopen(fd, 'wb')

    cmd.append('--rename-exe')
    cmd.append(os.path.basename(tempname))

    cmd.append('--in')
    cmd.append(tmp_dest)

    start = datetime.now(timezone.utc)

    print(cmd)
    try:
        subprocess.check_output(cmd, stderr=subprocess.PIPE, timeout=timeout)

    # Handle ubi errors
    except subprocess.CalledProcessError as e:
        elapsed = (datetime.now(timezone.utc) - start).seconds
        msg = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])').sub('', e.stderr.decode(sys.getfilesystemencoding()))
        module.fail_json(msg=msg, elapsed=elapsed, changed=False)

    except OSError as e:
        elapsed = (datetime.now(timezone.utc) - start).seconds
        if e.errno == errno.ENOENT:
            module.fail_json(msg='ubi not found', elapsed=elapsed, changed=False)
        else:
            module.fail_json(msg='error', elapsed=elapsed, changed=False)

    f.close()

    return tempname


# ==============================================================
# main
def main():
    argument_spec = dict(
        attributes    = dict(type = 'str'),
        backup        = dict(type = 'bool'),
        checksum      = dict(type = 'str',  default   = ''),
        dest          = dict(type = 'path', required = True),
        force         = dict(type = 'bool', default  = False),
        group         = dict(type = 'str'),
        mode          = dict(type = 'str'),
        owner         = dict(type = 'str'),
        selevel       = dict(type = 'str'),
        serole        = dict(type = 'str'),
        setype        = dict(type = 'str'),
        seuser        = dict(type = 'str'),
        timeout       = dict(type = 'int'),
        tmp_dest      = dict(type = 'path'),
        unsafe_writes = dict(type = 'bool', default  = False),

        exe           = dict(type = 'str'),
        forge         = dict(type = 'str'),
        matching      = dict(type = 'str'),
        min_age_days  = dict(type = 'int'),
        project       = dict(type = 'str'),
        regex         = dict(type = 'str'),
        tag           = dict(type = 'str'),
        url           = dict(type = 'str'),
    )

    # setup aliases
    argument_spec['attributes']['aliases'] = ['attr']

    module = AnsibleModule(
        # not checking because of daisy chain to file module
        argument_spec        = argument_spec,
        add_file_common_args = True,
        supports_check_mode  = True,

        required_one_of    = [('project', 'url')],
        mutually_exclusive = [('project', 'url'),
                              ('tag', 'min_age_days')],
        required_by        = {'tag': 'project',
                              'min_age_days': 'project'},
    )

    backup        = module.params['backup']
    checksum      = module.params['checksum']
    dest          = module.params['dest']
    force         = module.params['force']
    timeout       = module.params['timeout']
    tmp_dest      = module.params['tmp_dest']

    exe           = module.params['exe']
    forge         = module.params['forge']
    matching      = module.params['matching']
    min_age_days  = module.params['min_age_days']
    project       = module.params['project']
    regex         = module.params['regex']
    tag           = module.params['tag']
    url           = module.params['url']

    result = dict(
        changed=False,
        checksum_dest=None,
        checksum_src=None,
        dest=dest,
        elapsed=0,
    )

    if os.path.isdir(dest):
        module.fail_json(msg=f"Destination {dest} is a directory", **result)

    last_mod_time = None

    # checksum specified, parse for algorithm and checksum
    if checksum:
        try:
            algorithm, checksum = checksum.split(':', 1)
        except ValueError:
            module.fail_json(msg="The checksum parameter has to be in format <algorithm>:<checksum>", **result)

        # Remove any non-alphanumeric characters, including the infamous
        # Unicode zero-width space
        checksum = re.sub(r'\W+', '', checksum).lower()
        # Ensure the checksum portion is a hexdigest
        try:
            int(checksum, 16)
        except ValueError:
            module.fail_json(msg='The checksum format is invalid', **result)

    if os.path.exists(dest):
        checksum_mismatch = False

        # If the download is not forced and there is a checksum, allow
        # checksum match to skip the download.
        if not force and checksum != '':
            destination_checksum = module.digest_from_file(dest, algorithm)

            if checksum != destination_checksum:
                checksum_mismatch = True

        # Not forcing redownload, unless checksum does not match
        if not force and checksum and not checksum_mismatch:
            # Not forcing redownload, unless checksum does not match
            # allow file attribute changes
            file_args = module.load_file_common_arguments(module.params, path=dest)
            result['changed'] = module.set_fs_attributes_if_different(file_args, False)
            if result['changed']:
                module.exit_json(msg="file already exists but file attributes changed", **result)
            module.exit_json(msg="file already exists", **result)

        # If the file already exists, prepare the last modified time for the
        # request.
        mtime = os.path.getmtime(dest)
        last_mod_time = datetime.fromtimestamp(mtime, timezone.utc)

        # If the checksum does not match we have to force the download
        # because last_mod_time may be newer than on remote
        if checksum_mismatch:
            force = True

    # download to tmpsrc
    start = datetime.now(timezone.utc)
    tmpsrc = ubi_get(module,
        url          = url,
        project      = project,
        forge        = forge,
        tag          = tag,
        min_age_days = min_age_days,
        exe          = exe,
        matching     = matching,
        regex        = regex,
        tmp_dest     = tmp_dest,
        timeout      = timeout,
        )

    result['elapsed'] = (datetime.now(timezone.utc) - start).seconds
    result['src'] = tmpsrc

    # Now the request has completed, we can finally generate the final
    # destination file name from the info dict.

    # raise an error if there is no tmpsrc file
    if not os.path.exists(tmpsrc):
        os.remove(tmpsrc)
        module.fail_json(msg="Request failed");
    if not os.access(tmpsrc, os.R_OK):
        os.remove(tmpsrc)
        module.fail_json(msg=f"Source {tmpsrc} is not readable", **result)
    result['checksum_src'] = module.sha1(tmpsrc)

    # check if there is no dest file
    if os.path.exists(dest):
        # raise an error if copy has no permission on dest
        if not os.access(dest, os.W_OK):
            os.remove(tmpsrc)
            module.fail_json(msg=f"Destination {dest} is not writable", **result)
        if not os.access(dest, os.R_OK):
            os.remove(tmpsrc)
            module.fail_json(msg=f"Destination {dest} is not readable", **result)
        result['checksum_dest'] = module.sha1(dest)
    else:
        if not os.path.exists(os.path.dirname(dest)):
            os.remove(tmpsrc)
            module.fail_json(msg=f"Destination {os.path.dirname(dest)} does not exist", **result)
        if not os.access(os.path.dirname(dest), os.W_OK):
            os.remove(tmpsrc)
            module.fail_json(msg=f"Destination {os.path.dirname(dest)} is not writable", **result)

    if module.check_mode:
        if os.path.exists(tmpsrc):
            os.remove(tmpsrc)
        result['changed'] = ('checksum_dest' not in result or
                             result['checksum_src'] != result['checksum_dest'])
        module.exit_json(msg='OK', **result)

    # If a checksum was provided, ensure that the temporary file matches this checksum
    # before moving it to the destination.
    if checksum != '':
        tmpsrc_checksum = module.digest_from_file(tmpsrc, algorithm)

        if checksum != tmpsrc_checksum:
            os.remove(tmpsrc)
            module.fail_json(msg=f"The checksum for {tmpsrc} did not match {checksum}; it was {tmpsrc_checksum}.", **result)

    # Copy temporary file to destination if necessary
    backup_file = None
    if result['checksum_src'] != result['checksum_dest']:
        try:
            if backup:
                if os.path.exists(dest):
                    backup_file = module.backup_local(dest)
            module.atomic_move(tmpsrc, dest, unsafe_writes=module.params['unsafe_writes'])
        except Exception as e:
            if os.path.exists(tmpsrc):
                os.remove(tmpsrc)
            module.fail_json(msg=f"failed to copy {tmpsrc} to {dest}: {to_native(e)}", **result)
        result['changed'] = True
    else:
        result['changed'] = False
        if os.path.exists(tmpsrc):
            os.remove(tmpsrc)

    # allow file attribute changes
    file_args = module.load_file_common_arguments(module.params, path=dest)
    result['changed'] = module.set_fs_attributes_if_different(file_args, result['changed'])

    # Backwards compat only.  We'll return None on FIPS enabled systems
    try:
        result['md5sum'] = module.md5(dest)
    except ValueError:
        result['md5sum'] = None

    if backup_file:
        result['backup_file'] = backup_file

    # Mission complete
    module.exit_json(msg='OK', **result)


if __name__ == '__main__':
    main()

