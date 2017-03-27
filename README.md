# sina_fund_crawler
craw China fund information by Sina website

## Usage:
1. please ensure python2.7 environment on your computer.
2. execute `python funds_crawler.py` , we will get **funds.csv** at your working directory
3. choose a fund which you want to get it's net value list, and execute `python fund_net_value_crawler.py -p fund_number(like 519007)`, when process terminated, we will get **fund_number.csv (like 519007.csv)** at your working directory.
4. besides step 2 & 3 you can use `python funds_net_value_crawler.py all` to get all funds' net values.



I write this project for my roommate Ding Huan, who is a Data Mining Software Developer for State Street Corporation.
he is single now, and very kind to friend, if anyone want to make friend with him, I am glad to introduce.

## Gui(for windows):
1. add Pyinstaller by `pip install pyinstaller` in python environment
2. use `pyinstaller -F -w gui.py` to make a **gui.exe** in *./dist* floder.
3. gui.exe is a single-file-software, you can copy it in any folder, and double click in to run.

## Gui(for all)
I use tkinter which is a python interface for TK, so it could run on Linux and Mac with python environment
you can use `python gui.py` to start(suitable for Windows too).


### Gui Usage:
1. when you open the **gui.exe**, it will show all funds' information, you can use scrollbar to look around.
2. if you want to see a specific fund's net value. you can click it's name(like *华夏成长混合*) or fund_code(like *000001*)
and a new window will open to show all net value of this fund. 
3. you can also click **Crawl All !** button in menu, 
after you choose whether update the data we has crawled or not,
then you will see a progress_bar about how many part we crawled. You can click **Stop Crawl** to kill this process.

