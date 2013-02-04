#!/usr/bin/env python
import os
import sys


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vsq.settings_local")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

    if sys.argv[0] == 'runserver':
        from vsq.saver import handle_save_message
        handle_save_message()
