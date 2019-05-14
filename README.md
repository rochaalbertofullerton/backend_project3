Project 3

How to run:
  MUST HAVE ->  [You must install feedgen for both python2 and python3,
                foreman,
                flask,
                tavern,
                siege,
                nginx]

                        * This py file will run foreman *
  To Start  Servers->       python3 startup.py 
                        *alt way to start forman
                            foreman start --formation all=3


  To Start  nginx->  *if it is not already running*
                        sudo nginx
                    * if it is already running*
                        sudo nginx -s quit
                        sudo nginx

                    !!MAKE SURE YOU CHANGE THE DEFAULT FILE TO THE ONE PROVIDED!!!

Report:
    Seige: Before caching
        We ran the siege for 1 min with 25 connections
        we 1521 hit 
        availability was 60.99% -> we saw our scylla burn up in flames 
        we included a snapshot of the siege reuslts named "Siege_Before_Cache.png"
        The longest transaction was about 3 sec
        The Shortest traction was about 0 sec



Dev1 ALBERTO ROCHA (berto323@csu.fullerton.edu)
    - Per the requirements of project 3
        -> Update code to use ScyllaDB : SUCCESS 
        -> Serachable Column indexed : SUCCESS
Dev2 JEN BERNARDINO (jerbernard96@csu.fullerton.edu)
    -Per the requirements of project 3
        -> Modify Code to Use HTTP Cache: IN PROGRESS
OPS Pooja Gajjar (pkgajjar@csu.fullerton.edu)
    - Per the requirements of project 3
        -> Tests : SUCCESS
        -> Ran Siege Test Before Cache : SUCCESS
        -> Ran Siege Test After Cache : WAITING : ON HTTP CACHING UPDATE 
