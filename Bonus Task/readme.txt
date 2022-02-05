
Module used: selenium, web driver, requests, amazoncaptcha
		io, pytesseract,pillow(PIL)

Approach :
 
Method 1: 
Step 1:
Step 1:
:- Using selenium, we create webdriver to get connection
:- with the "find_element_by_tag_name('img')" function
   in selenium, we get the captcha from site in the form 
   of image

Step 2:
:- After getting image link, we simply convert captcha
   image into text.




Method 2:
Step 1:
:- Using selenium, we create webdriver to get connection
:- with the "find_element_by_tag_name('img')" function
   in selenium, we get the captcha from site in the form 
   of image

Step 2:
:- we get the image in form link, so that we need to 
   encode image byte object

Step 3:
:- We convert image into text with help of pytesseract


Note: On wensite, captcha are present in 
      diiferent- different form
    
