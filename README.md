<!-- ---
title: "Package manual of highlightlatex"
author: Vincent Kuhlmann
date: 17 March 2021
geometry: margin=2cm
output: pdf_document
--- -->

# Highlight LaTeX: Pretty LaTeX code within LaTeX

Teaching other people LaTeX is great fun, and I've seen plenty of slides and
readers doing so. You show what you achieve, and how you achieve it. However,
while the LaTeX you achieve might look splendid, showing code is often done
using very rudimentary solutions (like plain old verbatim).

They're not to blame: using LaTeX alone, there aren't many alternatives.
Hence this package extends the generatic `listings` package to provide
for these needs; colored highlightign for LaTeX. The file `demo.tex` achieves this:

<img src="assets/demoshowoff.png" width="600"
alt="highlight demo" title="Highlight demo">

<!-- ![An example of syntax highlighting using highlightlatex. This was generated
by `demo.tex`.](assets/demoshowoff.png "Syntax highlighting
example") -->

The package is now available from CTAN. You can use `\usepackage{highlightlatex}` and
if your system requires manual installation, the package is called teh same. If you wish
to install the package version of the repository, refer to [the wiki](wiki/Manual-installation).

## Quickstart

After having added the package, you can add LaTeX in two ways:

* Inline style:

      Your file begins with a line of the form \hll|\documentclass[]{}|. The
      square brackets ...

  The first non-space character following `\hll` delimits the argument of this
  command.

* Block style:

      Your basic document now looks like
      \begin{highlightblock}[gobble=2]
          \documentclass[a4paper]{article}
          \begin{document}
              Hello world!
          \end{document}
      \end{highlightblock}
      
 **Refer to the manual for further documentation.**

## License & Credits

The package is available under MIT License. See LICENSE.txt.

Thanks for minor fixes:

gemmaro

---

For any small fix, bug, feature request, unclarity etc., you're welcome to
open an issue on

[https://github.com/vkuhlmann/highlight-latex/issues](https://github.com/vkuhlmann/highlight-latex/issues)

Thanks for thinking along!
