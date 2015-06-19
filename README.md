Archive Manager
===============

A simple archival system that helps you to back up your files based on their modification time.

## Contents

* [Download](#download)
* [Requirements](#requirements)
* [Contact](#contact)
* [Uninstall](#uninstall)

## Download

[Download the latest installer here!](../../releases/)

## Requirements

* Python 2.7.x (which you can download [here](https://www.python.org/download/))
* [Management Tools](https://github.com/univ-of-utah-marriott-library-apple/management_tools)

## Contact

If you have any comments, questions, or other input, either [file an issue](../../issues) or [send us an email](mailto:mlib-its-mac-github@lists.utah.edu). Thanks!

## Uninstall

To remove Archive Manager from your system, download the .dmg and run the "Uninstall Archive Manager [x.x.x]" package to uninstall it. (Note that the version indicated does not actually matter, as any of the uninstall packages will remove any installed version of Archive Manager).

## Purpose

In our environment, we create disk images to be used to quickly restore computers to known states. We like to keep backups of these images, sorted by date, but often we would forget to upload new versions to our remote backup server. Eventually we decided to just automate the process, and so Archive Manager was born.

## Usage

```
$ archiver.py [-hvn] [-l log] [--flat] [--delimiter delimiter] [--granularity grain] [--no-replace] [--persist] [--update-time] origin destination
```

The archiver will move/copy files from `origin` to `destination`.

If you do not specify `--flat`, then a nested directory structure will be created to sort the files. By default, they will be sorted to [Granularity level](#granularity) 3 (day).

### Options

| Option                    | Purpose                                                                                                                                   |
|---------------------------|-------------------------------------------------------------------------------------------------------------------------------------------|
| `-h` `--help`             | Prints help message and quits.                                                                                                            |
| `-v` `--version`          | Prints only the version information and quits.                                                                                            |
| `-n` `--no-log`           | Redirects logging to the console (stdio).                                                                                                 |
| `-l log` `--log-dest log` | Outputs log files to `log` instead of the default. (This is overridden by `--no-log`.)                                                    |
| `--flat`                  | Instead of creating subdirectories to sort files, all files will be renamed with their modification date and placed in the destination.   |
| `--delimiter delimiter`   | Changes the delimiter used to change file names in `--flat` mode. Default is a period.                                                    |
| `--granularity grain`     | Determines how many aspects of the date should be used in sorting. See [Granularity](#granularity) below for more info.                   |
| `--no-replace`            | If there is a file in the destination folder that matches the current file, this prevents it from being overwritten.                      |
| `--persist`               | If used, leaves a copy of the original file in the origin directory.                                                                      |
| `--update-time`           | After moving the files to the destination, this will update their timestamps to the current time.                                         |

`origin` is where the files to be copied exist
`destination` is the top-level directory where you want your files to be migrated/copied to

#### Granularity

The granularity system allows you to specify how deeply-nested your destination files will be. There are six defined levels:

1. Year
2. Month
3. Day
4. Hour
5. Minute
6. Second

The granularity can be specified as either the integer value or the word (not case-sensitive).

### Examples

Imagine starting with an origin directory with these files:

```
(File)         (Last Modified)
Origin
|--File1     Aug 08, 2014 12:34:00
|--File2     Aug 12, 2014 00:00:00
|--File3     Sep 21, 2014 03:55:00
|--File4     Nov 19, 2014 17:33:00
```

If you were to run Archive Manager as `archiver.py origin destination`, then the destination would look like:

```
Destination
|--2014
   |--08
   |  |--File1
   |  |--File2
   |--09
   |  |--File3
   |--11
      |--File4
```
