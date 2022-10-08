This is a repository of my Python solutions to the problems I encountered while doing the Google Foobar challenge.

I do provide brief explanations of the algorithms used in the the code files as comments. Maybe eventually I'll write a blog post with more in-depth explanations. I'd like to explore possibly more optimal solutions to the problems I did at a later date.

Environments
============

The challenge specification allows you to submit either Python 2.7.13 or Java 8 code for your solutions.

As it is the 23rd of April 2022 at time of writing, Python 2 is deprecated and I don't have (nor want) it on my system, I opted to use Docker to run my code in a Python 2 container to develop locally.

I created helpful Bash scripts to run your solutions in either a Python 2.7.13 or a Java 8 container:
- [`run-python2-docker.sh`](run-python2-docker.sh)
- [`run-java8-docker.sh`](run-java8-docker.sh)

Both scripts behave the same way, call the script from the root directory of this repository and provide the directory of the solution you wish to run.

Example usage:
```bash
google-foobar $ ./run-python2-docker.sh bomb-baby
```

Stage 1
=======
[The cake is not a lie!](the-cake-is-not-a-lie)

Stage 2
=======
1. [Numbers Station Coded Messages](numbers-station-coded-messages)
2. [En Route Salute](en-route-salute)

Stage 3
=======
1. [Prepare the Bunnies' Escape](prepare-the-bunnies-escape)
2. [The Grandest Staircase Of Them All](the-grandest-staircase-of-them-all)
3. [Bomb, Baby!](bomb-baby)

Stage 4
=======
1. [Escape Pods](escape-pods)
2. [Running with Bunnies](running-with-bunnies)

Stage 5
=======
[Disorderly Escape](disorderly-escape)
