precious
========

![](http://1.bp.blogspot.com/_g9aAldovQlE/TQbubvFcMtI/AAAAAAAAABA/dISjf3vbveI/s1600/6_gandalf_smokingpipe.jpg)

flat-file markdown wiki software written in Python.  Inspired heavily by gollum.

## Introduction

Just put .md files in the `notes/` directory and view a beautiful rendered wiki version in your browser.
The file `notes/foo-file.md` corresponds to `http://localhost:8080/notes/foo-file`.

Hypenated titles get treated as a space character (` `).

Codemirror is used as the editor for making edits to wiki pages.

**Warning**: Early beta software!

## Links

You can link to other pages by using the following format:

`[[link]]` will point to `notes/link.md`
`[[many word link]]` points to `notes/many-word-link.md`

**Warning**: Page hyperlinking is still in its infancy and likely has some edge cases.   Precious will attempt to conform to [gollum's linking format](https://github.com/gollum/gollum/wiki).

## Installation

**Note**: The below instructions assume `pip`, `virtualenv`, and `virtualenvwrapper` are installed.  Instructions on how to install the above 3 packages are forth-coming.

```bash
$ git clone git@github.com:mvanveen/precious.git
$ mkvirtualenv wiki
$ workon wiki
$ cd precious
$ pip install -r requirements.txt
$ python app/
```

go to [http://localhost:8080](http://localhost:8080).  You should see a wiki!
