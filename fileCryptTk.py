#!/usr/bin/python
# -*- coding: utf-8 -*-

# fileCrypt - main.py
# -------------------
# en/decrypts files, this loads the module and provides a simple form

from fileCrypt.fcForm import fcForm

if __name__ == '__main__':
    main = fcForm(None)
    main.mainloop()