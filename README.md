Archive Manager
===============

A simple archival system that helps you to back up your files based on their modification time.

## Contents

* [Download](#download)
* [Requirements](#requirements)
* [Contact](#contact)
* [Uninstall](#uninstall)
* [Purpose](#purpose)
* [Usage](#usage)
  * [Options](#options)
  * [Examples](#examples)
* [Update History](#update-history)

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

Archive Manager is a script that moves files from one location to another. The advantage of Archive Manager over simply scripting a `mv` or `cp` is that Archive Manager will automatically sort the files within the destination directory. In its regular mode of operation, subdirectories will be created within the destination based on the modification time of the files in the origin. The amount of subdirectories can be controlled, resulting in either a very fine or broad grouping of the files. This is useful when you have time-sensitive backups (e.g. you want to back up a year's worth of log files, but you want them grouped into subdirectories by day).

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
origin
|--File1     Aug 08, 2014 12:34:00
|--File2     Aug 12, 2014 00:00:00
|--File3     Sep 21, 2014 03:55:00
|--File4     Nov 19, 2014 17:33:00
```

If you were to run Archive Manager as `archiver.py origin destination`, then the destination would look like:

```
destination
|--2014
   |--08
   |  |--File1
   |  |--File2
   |--09
   |  |--File3
   |--11
      |--File4
```

However, if you were to run Archive Manager as `archiver.py --flat origin destination`, then the destination would look like:

```
destination
|--2014.08.08.File1
|--2014.08.12.File2
|--2014.09.21.File3
|--2014.11.19.File4
```

## Update History

This is a short, reverse-chronological summary of the updates to this project.

| Date       | Version | Update Description                                         |
|------------|:-------:|------------------------------------------------------------|
| 2015-06-19 | 1.1.1   | Fixed an issue where files weren't moved properly.         |
| 2015-06-01 | 1.1.0   | Resiliency improved (doesn't fail as easily).              |
| 2014-07-11 | 1.0     | Initial release. Mostly functional, with a package.        |
| 2014-07-01 | 0.5     | Can now update the modification timestamps on new files.   |
| 2014-07-01 | 0.4     | Added ability to change file name delimiter.               |
| 2014-07-01 | 0.3     | Rudimentary functionality implemented.                     |
| 2014-06-30 | 0.2     | Outline of all processes completed.                        |
| 2014-06-27 | 0.1     | Project started.                                           |
