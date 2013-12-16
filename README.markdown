# GenomeAssist

Mansi Arora and Roger Que,
[600.615](http://www.cs.jhu.edu/~yanif/teaching/bdslss/),
Fall 2013,
[Johns Hopkins University](http://www.jhu.edu/)

---

For an introduction to GenomeAssist, see [the project
writeup](writeup/writeup.pdf).

The primary Django application, with Celery tasks, is located in the
`genomeassist/` directory.
Python dependencies can be installed using `pip -r requirements.txt`.
[Bower](http://bower.io/) is required for the management of frontend
dependencies.

Additionally, installation-specific settings should be specified in
`genomeassist/local_settings.py`.
Consult the `settings.py` file in the same directory for more information on
which variables are used by GenomeAssist.
