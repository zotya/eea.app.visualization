#  EEA App Visualization

[![http://ci.eionet.europa.eu/job/eea.app.visualization-
www/badge/icon](https://camo.githubusercontent.com/9f96c1f4a61c5144c6325be829b37f6878d4c1cb/687474703a2f2f63692e65696f6e65742e6575726f70612e65752f6a6f622f6565612e6170702e76697375616c697a6174696f6e2d7777772f62616467652f69636f6e)](http://ci.eionet.europa.eu/job/eea.app
.visualization-www/lastBuild) [![http://ci.eionet.europa.eu/job/eea.app
.visualization-
plone4/badge/icon](https://camo.githubusercontent.com/26f003b2f9290b6928b53c4a11bef817f902666f/687474703a2f2f63692e65696f6e65742e6575726f70612e65752f6a6f622f6565612e6170702e76697375616c697a6174696f6e2d706c6f6e65342f62616467652f69636f6e)](http://ci.eionet.europa.eu/job/eea.app
.visualization-plone4/lastBuild) [![http://ci.eionet.europa.eu/job/eea.app
.visualization-
zope/badge/icon](https://camo.githubusercontent.com/4c1f7b34fa40249d468e2ddc057ad58e450c937a/687474703a2f2f63692e65696f6e65742e6575726f70612e65752f6a6f622f6565612e6170702e76697375616c697a6174696f6e2d7a6f70652f62616467652f69636f6e)](http://ci.eionet.europa.eu/job/eea.app
.visualization-zope/lastBuild)

[EEA App Visualization](http://eea.github.com/docs/eea.app.visualization) is
the Core API for [EEA Daviz](http://eea.github.com/docs/eea.daviz). This
package was added in order to be able to use [EEA Google
Charts](http://eea.github.com/docs/eea.googlecharts) without [EEA
Exhibit](http://eea.github.com/docs/eea.exhibit) and viceversa or any other
visualization library as a standalone visualization or as part of a bundle
package ([eea.daviz](http://eea.github.com/docs/eea.daviz))

[![](https://camo.githubusercontent.com/cddc9aeb767e719698477be1025c068fd141f91e/687474703a2f2f6565612e6769746875622e636f6d2f5f696d616765732f6565612e646176697a2e6c61796572732e737667)](https://camo.githubusercontent.com/cddc9aeb767e719698477be1025c068fd141f91e/687474703a2f2f6565612e6769746875622e636f6d2f5f696d616765732f6565612e646176697a2e6c61796572732e737667)

This package as standalone is just an API, you have to either install
[eea.daviz](http://eea.github.com/docs/eea.daviz) bundle, either install one
of the available visualization libraries
([eea.exhibit](http://eea.github.com/docs/eea.exhibit),
[eea.googlecharts](http://eea.github.com/docs/eea.googlecharts), etc) in order
to have a working Visualization Tool for your files.

Contents

  * Installation
  * Dependencies
  * Live demo
  * Source code
  * Copyright and license
  * Links
  * Funding

##  Installation

If you are using [zc.buildout](http://pypi.python.org/pypi/zc.buildout) and
the
[plone.recipe.zope2instance](http://pypi.python.org/pypi/plone.recipe.zope2instance)
recipe to manage your project, you can do this:

  * Update your buildout.cfg file:

    * Add [eea.app.visualization](http://eea.github.com/docs/eea.app.visualization) to the list of eggs to install
    * Tell the plone.recipe.zope2instance recipe to install a ZCML slug
    
        [instance]
    recipe = plone.recipe.zope2instance
    eggs = eea.app.visualization
    zcml = eea.app.visualization
    

  * Re-run buildout, e.g. with
    
        $ ./bin/buildout
    

You can skip the ZCML slug if you are going to explicitly include the package
from another package's configure.zcml file.

##  Dependencies

  * python-dateutil
  * Zope &gt;= 2.12
  * eea.jquery
  * collective.js.jqueryui &lt; 1.9 (Plone 4.0, 4.1, 4.2)
  * collective.js.jqueryui &gt; 1.9 (Plone 4.3+)

[![](https://camo.githubusercontent.com/1cc34aab15188eec03f811ea45d06bcbb137b948/687474703a2f2f6565612e6769746875622e636f6d2f5f696d616765732f6565612e646176697a2e646570656e64656e636965732e737667)](https://camo.githubusercontent.com/1cc34aab15188eec03f811ea45d06bcbb137b948/687474703a2f2f6565612e6769746875622e636f6d2f5f696d616765732f6565612e646176697a2e646570656e64656e636965732e737667)

##  Live demo

  1. <http://www.simile-widgets.org/exhibit>
  2. Exhibit only: <http://www.eea.europa.eu/data-and-maps/data/national-emissions-reported-to-the-unfccc-and-to-the-eu-greenhouse-gas-monitoring-mechanism-3/national-total-excluding-lulucf/ghg_v10_extract.csv>
  3. <http://code.google.com/apis/chart/>

##  Source code

Latest source code (Zope 2 compatible): \- [Plone Collective on
Github](https://github.com/collective/eea.app.visualization) \- [EEA on
Github](https://github.com/eea/eea.app.visualization)

##  Copyright and license

The Initial Owner of the Original Code is European Environment Agency (EEA).
All Rights Reserved.

The EEA App Visualization (the Original Code) is free software; you can
redistribute it and/or modify it under the terms of the GNU General Public
License as published by the Free Software Foundation; either version 2 of the
License, or (at your option) any later version.

More details under docs/License.txt

##  Links

  1. Simile Wiki - Exhibit 2.0: <http://simile.mit.edu/wiki/Exhibit>
  2. Simile widgets: <http://www.simile-widgets.org/exhibit>
  3. EEA Daviz howto: <http://taskman.eionet.europa.eu/projects/zope/wiki/HowToDaviz>
  4. EEA Daviz backlog wiki: <http://taskman.eionet.europa.eu/projects/zope/wiki/DaViz>
  5. Google charts: <http://code.google.com/apis/chart/>

##  Funding

[EEA](http://www.eea.europa.eu/) \- European Environment Agency (EU)

