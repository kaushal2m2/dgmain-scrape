# dgmain-scrape

Python Scripts to read various security forums, including Cisco's security forums, reddits r/cybersecurity, MalwareTips, and Wilders Security.
The CSV files of scraped data are also included.

All scripts depend on selenium, beautifulsoup4, chromedriver, and Google Chrome Beta. chromerdriver's version must match your chrome version. These scripts use version 104.0.5112.20

r/cybersecurity:

The questions asked in this subreddit seemed to be very career oriented-people wondering about the job market for cybersecurity. There were few questions about general cybersecurity.

cisco:

The questions are mostly about cisco's security products, such as Cisco's TALOS group's software.

MalwareTips:

The website is meant for general discussion about cybersecurity and malware, and the posts reflect that. They aren't about specific cybersecurity products, but rather are problems and questions normal people face on the internet.

Wilders Security:

The website is split up into sections, some of which discuss solely about security products, and some with peoples general questions about privacy and malware. The product questions seem to outnumber the general questions.  
  
Issues faced:
- Websites may want to send you notifications and will cause a pop up near the url of the page that can only be manually closed.
- Google Chrome version 103.0.5060.134 has a bug with selenium where elements are randomly unclickable, solved by using Google Chrome Beta version 104
- Cisco changed the way their website is laid out (changing html tags and the user end layout), rendering previously made code unusable. No fix other than to change tags/classes/selectors/xpaths in the code
- Cisco sometimes took a while to load, and the element was attempted to be clicked before it was fully loaded. The program was made to sleep for intervals to give the website time.
- Reddit had ads scattered through their page blending in with the posts. To deal with this, the link reference for each post was observed, and only posts that linked to reddit (user posts) were clicked, as the other ones were ads or news articles.
- Reddit had long, unreadable tags that made it unfriendly to use for scraping. To combat this oldreddit was used.
- When reddit opened a post, it laid the post on top of the previous page, so all the previous page's html was still present, along with the post, making it very difficult to read only the post. No fix was found. To combat this oldreddit was used.
- Reddit only stores a max of 1000 posts in its cache for each filter that is given to it. Nothing we could do about that.
- PaloAltoNetworks (no script in this repo) sent a pop up for a survey at a random time, making selenium clicks cause an exception. No fix found.
- TechRepublic had images under most questions that needed to be avoided when scraping through questions.
