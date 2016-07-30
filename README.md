# sina_fund_crawler
craw China fund information by Sina website

##Usage:
1. please ensure python2.7 environment on your computer.
2. execute `python funds_crawler.py` , we will get **funds.csv** at your working directory
3. choose a fund which you want to get it's net value list, and execute `python fund_net_value_crawler.py -p fund_number(like 519007)`, when process terminated, we will get **fund_number.csv (like 519007.csv)** at your working directory.
4. besides step 2 & 3 you can use `python funds_net_value_crawler.py all` to get all funds' net values.



I write this project for my roommate Ding Huan, who is a Data Mining Software Developer for State Street Corporation.
he is single now, and very kind to friend, if anyone want to make friend with him, I am glad to introduce.

##future
add simple gui to watch/download the data 