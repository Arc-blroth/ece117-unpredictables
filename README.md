### ECE M117 Final Project
# Team A12: Predicting the Unpredictable: Cracking Web Randomness
by @Arc-blroth, @AVDestroyer, @swang1111, @AnthonyFangqing, @alexedw01, @Seamarr

Code and test applications for our ECE M117 Final Project _Cracking Web Randomness_,
which combines taint analysis, cryptanalysis, and the HTTP/2 single packet attack
to predict future states of "randomness" in JS web apps!

This repository contains several proof-of-concept scripts that demonstrate successful attacks against a demo web application at [https://ece117.bulr.boo/](https://ece117.bulr.boo/).

Our report paper is [here](Predicting_the_Unpredictable_Cracking_Web_Randomness.pdf).

## Dependencies

To run our proof of concept exploits, you will need to install the following 2 Python packages:

`z3`: `pip install z3-solver`

`h2spacex`: `pip install h2spacex==0.1.3`

## POCs

### unified-exploit

By running `./attack.sh`, you can obtain the next number to guess in [https://ece117.bulr.boo/](https://ece117.bulr.boo/).

### exploit-with-spamming

By running `./attack.sh`, you can attempt to guess a random number in [https://ece117.bulr.boo/](https://ece117.bulr.boo/). This uses a "spamming environment", where another script continually requests the server. To get around the spamming, we predict a future number the server will pick, then send many requests to the server guessing this number.

## Semgrep/CodeQL rules

We also provide rules for Semgrep and CodeQL rules under `/rules` that detect if the application may be vulnerable against our exploit. Note that since the free version of Semgrep (Semgrep OSS) doesn't support cross-function or cross-file analysis, these rules are specialized for our example application and will not generalize. However, the CodeQL rules do support cross-function and cross-file analysis.
