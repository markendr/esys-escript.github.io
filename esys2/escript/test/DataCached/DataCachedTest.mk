
DODEBUG := YES

DEFAULT_TARGET := DataCachedTest.exe

L_SRC_DIR := .

L_DEFS := DOASSERT

PACKAGES := escript CppUnitTest esysUtils pythonStatic boost

include $(ESYS_ROOT)/make/Makefile.default
