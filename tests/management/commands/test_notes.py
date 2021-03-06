# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django_extensions.management.commands.notes import Command


def test_without_args(capsys, settings):
    print_settings = Command()
    print_settings.run_from_argv(['manage.py', 'notes'])

    out, err = capsys.readouterr()
    assert 'tests/testapp/__init__.py:\n  * [  4] TODO  this is a test todo\n\n' in out


def test_with_utf8(capsys, settings):
    print_settings = Command()
    print_settings.run_from_argv(['manage.py', 'notes'])

    out, err = capsys.readouterr()
    assert 'tests/testapp/file_with_utf8_notes.py:\n  * [  3] TODO  Russian text followed: Это техт на кириллице\n\n' in out


def test_with_template_dirs(capsys, settings, tmpdir_factory):
    templates_dirs_path = tmpdir_factory.getbasetemp().strpath
    template_path = os.path.join(templates_dirs_path, 'fixme.html')
    settings.TEMPLATES[0]['DIRS'] = [templates_dirs_path]
    with open(template_path, 'w') as f:
        f.write('''{# FIXME This is a comment. #}
{# TODO Do not show this. #}''')

    print_settings = Command()
    print_settings.run_from_argv(['manage.py', 'notes', '--tag=FIXME'])
    out, err = capsys.readouterr()

    assert '{}:\n  * [  1] FIXME This is a comment.'.format(template_path) in out
    assert 'TODO Do not show this.' not in out
