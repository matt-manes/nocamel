# nocamel
Command line tool to convert python file(s) from camel case to PEP compliant snake case. <br>
Can optionally rename the file using snake case, as well as renaming instances in other non-.py files,
such as a readme or docs.<br>
Also has an option to lower the case of module names in your import statements. <br>
(Useful if you're converting multiple files in a directory that import each other.)<br>
Camel case names that start with a capital are ignored (class names).<br>

Usage:
<pre>
>nocamel -h
usage: nocamel [-h] [-s SOURCE_TO_CONVERT] [-ef [EXTRA_FILES ...]] [-lmn] [-cfn] [-r]

options:
  -h, --help            show this help message and exit
  -s SOURCE_TO_CONVERT, --source_to_convert SOURCE_TO_CONVERT
                        Source file or directory to convert. If None, all .py files in current working directory will
                        be converted.
  -ef [EXTRA_FILES ...], --extra_files [EXTRA_FILES ...]
                        Change the names in these non .py files as well.
  -lmn, --lower_module_names
                        Change module import names to lower case.
  -cfn, --convert_file_name
                        Convert the file name to snake case and delete the origninal.
  -r, --recursive       If -s/--source is None or a directory, convert all .py files including those in
                        subdirectories.
</pre>