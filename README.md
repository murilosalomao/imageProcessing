# Detecting Text in Still Images

Given a picture containing text in different scenarios, output one or more crops of the regions where the text is located.
As of now, the database we selected to be used is: [MSRA Text Detection 500 Database (MSRA-TD500)](http://www.iapr-tc11.org/mediawiki/index.php/MSRA_Text_Detection_500_Database_(MSRA-TD500)).

This database has its training examples labeled and classified as *difficult* or not. It also contains the rotation of the texts. In our approach, we intend to rotate the images so the texts are horizontal.
