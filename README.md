# HTMLSurfer - in testing

Exploring web pages using Requests and BeutifulSoup.

.pem file is CA Root Certificates file which some pages request (SSH).
# Requirements
- Python 3.7

Made using PyCharm

# Idea

Process starts exploring from one page, then following the links from it explores more content. Number of hops is determined by user. On each site text data is stored and later processed through counter. Counter shows how many words was repeated.
At the and of process two files are created.
 - out.txt - where all of links are stored
 - counter.txt - where counting result is stored

In midprocess main.tmp file is created where unfiltered links are stored. There is option for delete it in code, but it's commented out. 

Code surely isn't the best, but it kinda works :D
