# Makefile for source rpm: bash
# $Id$
NAME := bash
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
